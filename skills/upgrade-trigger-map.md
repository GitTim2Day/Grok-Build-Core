# upgrade-trigger-map

**Date:** 2026-09-07
**Tags:** upgrade-trigger, decision, roadmap, process

## Purpose
Map every upgrade trigger in a spec to a concrete condition and a fallback path, so the decision table becomes a roadmap instead of a wish list.

## When to use
- A matrix has a "Decision Trigger for Upgrade" column.
- You need to sequence upgrades by priority or dependency.

## Required inputs
- The trigger column.
- The alternative column for each row.

## Steps
1. **List triggers per row.** One line each: condition → action.
2. **Classify by type.** Payload, terrain, mass, torque threshold, thermal, always-on.
3. **Order by dependency.** Always-on (distal mass) first; threshold-based (torque >200 Nm) later.
4. **Attach the fallback.** Every trigger needs its alternative path from the matrix.
5. **Report:** ordered trigger list with fallbacks, plus any row with no trigger (flag it).

## Rules
- A trigger without a fallback is incomplete.
- Always-on triggers are not optional.

## Anti-patterns
- Treating every trigger as equal priority.
- Leaving a row with "always" but no alternative.

## Example
Hip: torque >200 Nm or rough terrain → add limited-slip diff. Wrist: always (distal mass) → proximal actuators + Dyneema. Compound pulley: motor thermal limit → optional 2:1–3:1 stage.
