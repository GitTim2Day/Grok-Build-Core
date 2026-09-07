# key-tolerance-limits-normalize

**Date:** 2026-09-07
**Tags:** tolerance, normalize, units, audit, process

## Purpose
Normalize mixed tolerance units (arcmin, degrees, mm, percent, N, Nm/rad) into one consistent set per joint class before comparing or auditing.

## When to use
- A spec mixes units across the tolerance column (backlash in arcmin and mm, stiffness in Nm/rad, elongation in percent).
- You need to compare tolerances across joints or suppliers.

## Required inputs
- The tolerance column with mixed units.
- The joint class per row.

## Steps
1. **List each tolerance with its unit.** Backlash, stiffness, elongation, force resolution, accuracy.
2. **Convert to one set per class.** Rotary: arcmin + Nm/rad. Linear: mm + N/mm. Tendon: percent + N. Flag any unit that doesn't fit the class.
3. **Check direction consistency.** ≤ for backlash/elongation/accuracy; ≥ for stiffness/impact. Flag reversals.
4. **Compare within class.** Two rotary joints: compare arcmin directly. Two linear: compare mm directly. Never compare arcmin to mm.
5. **Report:** normalized set, direction check, within-class comparison, unit mismatches.

## Rules
- Never compare different units directly. Convert first.
- Direction must match the physics (backlash is upper bound).

## Anti-patterns
- Comparing arcmin to degrees without conversion.
- Mixing ≤ and ≥ without noticing.

## Example
Knee: linear backlash ≤0.04 mm, impact ≥6× BW → linear set (mm, ×BW). Ankle: accuracy ≤0.1°, tunable compliance → rotary set (deg). Wrist: elongation ≤0.8%, force res ≤1.5 N → tendon set (%, N). Hip: backlash ≤1.5 arcmin, stiffness ≥12000 Nm/rad → rotary set (arcmin, Nm/rad).
