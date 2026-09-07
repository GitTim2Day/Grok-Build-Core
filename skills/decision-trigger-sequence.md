# decision-trigger-sequence

**Date:** 2026-09-07
**Tags:** trigger, sequence, roadmap, process, gosub
**Status:** Active — GOSUB member (bidirectional)
**GOSUB ID:** TRIGGER_SEQ

## Purpose
Sequence the upgrade triggers across a spec into a build order: always-on first, then threshold-based, so the roadmap is dependency-ordered not row-ordered. Callable forward (sequence triggers) or reverse (given a build stage, find the triggers that belong there).

## When to use
- A matrix has multiple upgrade triggers across rows.
- You need to know which to build first and which can wait.
- Reverse: you are at a build stage and need the triggers that fire there.

## Required inputs
- The upgrade trigger column across all rows.
- The alternative and notes columns.

## GOSUB contract
- **Forward call:** TRIGGER_SEQ(sheet) → ordered sequence, dependency rationale, fallbacks, unsequenced rows.
- **Reverse call:** TRIGGER_SEQ(stage) → triggers assigned to that stage.
- **Shared state:** reads the trigger column; writes only to the audit log.
- **Direction tag:** forward | reverse.

## Steps
1. **List every trigger.** One line: condition → action → row.
2. **Classify.** Always-on (distal mass, precision), threshold (torque >200 Nm, mass >70 kg, rough terrain), thermal (motor limit), optional (compound pulley).
3. **Order by dependency.** Always-on → threshold → thermal → optional. Within threshold, order by impact on the platform.
4. **Attach fallback.** Every sequenced trigger gets its alternative.
5. **Report:** ordered sequence, dependency rationale, fallbacks, any unsequenced row.

## Rules
- Always-on triggers are not optional and come first.
- A trigger without a fallback breaks the sequence.
- Bidirectional: reverse returns the same triggers the forward pass sequenced.

## Anti-patterns
- Sequencing by row number instead of dependency.
- Treating optional triggers as required.
- One-directional only.

## Example
1. Always-on: wrist (distal mass) → proximal+Dyneema; fingers (distal mass) → under-actuated; neck (precision) → small harmonic.
2. Threshold: hip (torque >200 Nm / rough terrain) → add diff; knee (high impact / mass >70 kg) → dual roller-screw; ankle (rough terrain) → harmonic fallback.
3. Thermal: compound pulley (motor thermal limit) → optional 2:1–3:1.
4. Optional: differential (Class M/L) → limited-slip.
Reverse: "always-on" → Wrist, Fingers/Hand, Neck.
