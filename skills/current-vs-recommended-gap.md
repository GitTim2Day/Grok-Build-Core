# current-vs-recommended-gap

**Date:** 2026-09-07
**Tags:** gap, current, recommended, audit, process

## Purpose
Audit the gap between "Optimus Current" and "Recommended Primary" per row: state what changes, why, and whether the change is justified by the trigger.

## When to use
- A matrix has a current baseline and a recommended primary per row.
- You need to decide which gaps are worth closing and in what order.

## Required inputs
- The current and recommended columns.
- The upgrade trigger and notes columns.

## Steps
1. **List the gap per row.** Current → Recommended, one line.
2. **Classify the gap.** Architecture swap (harmonic→roller-screw), add-on (diff, damper), relocation (distal→proximal), ratio change.
3. **Check justification.** The gap should map to a trigger. A gap with no trigger is preference, not decision.
4. **Order by impact.** Always-on gaps (distal mass) first; threshold gaps (torque >200 Nm) later.
5. **Report:** gap list, classification, justification check, ordered impact.

## Rules
- A gap without a trigger is a preference, not a decision.
- Order by impact, not by row order.

## Anti-patterns
- Treating every gap as equal weight.
- Closing a gap that the trigger doesn't justify.

## Example
Knee: linear roller-screw+lever → planetary roller-screw+lever+damper (add damper, architecture refinement). Wrist: tendon-driven → proximal actuators+Dyneema (relocation, always-on). Hip: rotary harmonic → harmonic+optional diff (add-on, threshold). Differential: not emphasized → limited-slip (new, threshold >200 Nm).
