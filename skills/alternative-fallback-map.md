# alternative-fallback-map

**Date:** 2026-09-07
**Tags:** alternative, fallback, audit, process, gosub
**Status:** Active — GOSUB member (bidirectional)
**GOSUB ID:** FALLBACK_MAP

## Purpose
Map every alternative path in a spec to its trigger and confirm no row is left without a fallback when the primary is blocked. Callable forward (map fallbacks) or reverse (given a trigger, find which alternatives activate).

## When to use
- A matrix lists an alternative per row.
- You need to know what to do when the primary is unavailable (cost, mass, packaging).
- Reverse: a trigger fires and you need the alternative it unlocks.

## Required inputs
- The alternative column.
- The upgrade trigger and notes columns.

## GOSUB contract
- **Forward call:** FALLBACK_MAP(sheet) → fallback list, trigger attachment, single-point flags.
- **Reverse call:** FALLBACK_MAP(trigger) → alternatives activated by that trigger.
- **Shared state:** reads the alternative + trigger columns; writes only to the audit log.
- **Direction tag:** forward | reverse.

## Steps
1. **List the alternative per row.** One line: primary blocked → alternative.
2. **Check it is a real fallback, not a duplicate.** Dual harmonic vs single harmonic is a fallback; same harmonic is not.
3. **Attach the trigger.** Every alternative needs the condition that activates it.
4. **Flag rows with no alternative.** A row with only a primary and no fallback is a single point of failure.
5. **Report:** fallback list, trigger attachment, single-point flags.

## Rules
- A fallback without a trigger is unused.
- A row with no fallback is a risk, not a choice.
- Bidirectional: reverse returns the same alternatives the forward pass mapped.

## Anti-patterns
- Treating the alternative as a second recommendation.
- Leaving a high-cost row with no fallback.
- One-directional only.

## Example
Hip: dual harmonic or planetary multi-stage (fallback if single harmonic insufficient). Knee: dual roller-screw (fallback if single fails). Ankle: harmonic 50:1–100:1 (fallback if linear packaging fails). Differential: none (flag — single point). Compound pulley: none (flag — optional, low risk).
Reverse: "rough terrain" → Hip diff, Ankle harmonic fallback.
