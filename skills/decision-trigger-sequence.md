# decision-trigger-sequence

**Date:** 2026-09-07
**Tags:** trigger, sequence, roadmap, process

## Purpose
Sequence the upgrade triggers across a spec into a build order: always-on first, then threshold-based, so the roadmap is dependency-ordered not row-ordered.

## When to use
- A matrix has multiple upgrade triggers across rows.
- You need to know which to build first and which can wait.

## Required inputs
- The upgrade trigger column across all rows.
- The alternative and notes columns.

## Steps
1. **List every trigger.** One line: condition → action → row.
2. **Classify.** Always-on (distal mass, precision), threshold (torque >200 Nm, mass >70 kg, rough terrain), thermal (motor limit), optional (compound pulley).
3. **Order by dependency.** Always-on → threshold → thermal → optional. Within threshold, order by impact on the platform.
4. **Attach fallback.** Every sequenced trigger gets its alternative.
5. **Report:** ordered sequence, dependency rationale, fallbacks, any unsequenced row.

## Rules
- Always-on triggers are not optional and come first.
- A trigger without a fallback breaks the sequence.

## Anti-patterns
- Sequencing by row number instead of dependency.
- Treating optional triggers as required.

## Example
1. Always-on: wrist (distal mass) → proximal+Dyneema; fingers (distal mass) → under-actuated; neck (precision) → small harmonic.
2. Threshold: hip (torque >200 Nm / rough terrain) → add diff; knee (high impact / mass >70 kg) → dual roller-screw; ankle (rough terrain) → harmonic fallback.
3. Thermal: compound pulley (motor thermal limit) → optional 2:1–3:1.
4. Optional: differential (Class M/L) → limited-slip.
