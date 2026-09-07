# ratio-effective-audit

**Date:** 2026-09-07
**Tags:** ratio, transmission, audit, process, gosub
**Status:** Active — GOSUB member (bidirectional)
**GOSUB ID:** RATIO_AUDIT

## Purpose
Audit transmission ratios in a spec: distinguish gearbox ratio from effective ratio (after lever or pulley), and check the number against the joint class. Callable forward (audit ratios) or reverse (given a ratio band, find matching joints).

## When to use
- A matrix lists ratio ranges per joint (e.g. 80:1–120:1, effective 50:1–80:1).
- You need to check whether a ratio is plausible for the actuator type.
- Reverse: you have a target ratio and need the joints that use it.

## Required inputs
- The ratio column.
- The joint class (rotary harmonic, linear roller-screw, tendon).

## GOSUB contract
- **Forward call:** RATIO_AUDIT(sheet) → gearbox/effective split, class fit, torque cross-check.
- **Reverse call:** RATIO_AUDIT(ratio_band) → joints whose ratio falls in that band.
- **Shared state:** reads the ratio column; writes only to the audit log.
- **Direction tag:** forward | reverse.

## Steps
1. **Tag each ratio as gearbox or effective.** Gearbox = the transmission alone; effective = after lever, pulley, or tendon stage.
2. **Check class fit.** Harmonic rotary 80:1–120:1 is typical; roller-screw effective 50:1–80:1 is plausible with lever; tendon 20:1–40:1 is low-distal-mass correct; fingertip 8:1–30:1 is under-actuated range.
3. **Flag missing "effective" tags.** A linear joint without an effective tag is ambiguous — the lever multiplies.
4. **Cross-check against torque target.** Ratio × motor torque should land near the peak torque target; flag large gaps.
5. **Report:** gearbox vs effective split, class fit, torque cross-check.

## Rules
- Effective ratios are not gearbox ratios. Never compare them directly.
- A ratio without a torque cross-check is incomplete.
- Bidirectional: reverse lookup returns the same joints the forward pass tagged.

## Anti-patterns
- Treating every ratio as a gearbox ratio.
- Comparing effective and gearbox numbers as if same units.
- One-directional only.

## Example
Hip: 80:1–120:1 gearbox (+1:1–3:1 diff) → 250–300 Nm. Knee: effective 50:1–80:1 (roller-screw + lever) → 180–250 Nm. Wrist: actuator 20:1–40:1 → 15–30 Nm joint. Fingers: proximal 8:1–30:1 → 10–20 N fingertip.
Reverse: "80:1–120:1" → Hip, Shoulder, Spine.
