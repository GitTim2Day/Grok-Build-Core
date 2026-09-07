# torque-target-cross-check

**Date:** 2026-09-07
**Tags:** torque, target, cross-check, audit, process, gosub
**Status:** Active — GOSUB member (bidirectional)
**GOSUB ID:** TORQUE_CHECK

## Purpose
Cross-check peak torque targets against ratio × motor torque and against body-weight scaling, to catch targets that are physically unreachable or over-specified. Callable forward (check targets) or reverse (given a torque value, find joints near it).

## When to use
- A spec lists peak torque targets per joint for a platform class (e.g. 70 kg).
- You need to sanity-check the numbers before designing around them.
- Reverse: you have a torque budget and need the joints that consume it.

## Required inputs
- The peak torque column.
- The ratio column and any motor torque hint.
- The platform mass class.

## GOSUB contract
- **Forward call:** TORQUE_CHECK(sheet) → scaled targets, ratio cross-check, class sanity, gaps.
- **Reverse call:** TORQUE_CHECK(torque_value) → joints whose target is at or above that value.
- **Shared state:** reads the torque column; writes only to the audit log.
- **Direction tag:** forward | reverse.

## Steps
1. **List torque targets per row.** One line: joint → Nm.
2. **Scale by body weight.** 70 kg class: hip 250–300 Nm ≈ 3.5–4.3 Nm/kg; knee 180–250 ≈ 2.6–3.6; ankle 100–140 ≈ 1.4–2.0. Flag outliers.
3. **Cross-check ratio × motor.** If ratio × plausible motor torque (e.g. 1–3 Nm small BLDC, 5–10 Nm larger) lands near target, OK. Large gap = flag.
4. **Check joint class.** Legs carry more than arms; distal joints carry less. Inversions are flags.
5. **Report:** scaled targets, ratio cross-check, class sanity, gaps.

## Rules
- Torque is joint peak, not motor peak. Never conflate.
- Scaling is per-kg, not absolute.
- Bidirectional: reverse returns the same joints the forward pass scaled.

## Anti-patterns
- Treating peak torque as motor torque.
- Skipping the per-kg scaling check.
- One-directional only.

## Example
70 kg class: hip 250–300 Nm (3.5–4.3/kg), knee 180–250 (2.6–3.6/kg), ankle 100–140 (1.4–2.0/kg), shoulder 120–160 (1.7–2.3/kg), wrist 15–30 (0.2–0.4/kg). Legs scale higher than arms — correct. Wrist low — correct for distal mass.
Reverse: ">200 Nm" → Hip, Knee.
