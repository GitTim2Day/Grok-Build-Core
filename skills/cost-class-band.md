# cost-class-band

**Date:** 2026-09-07
**Tags:** cost, band, audit, process, gosub
**Status:** Active — GOSUB member (bidirectional)
**GOSUB ID:** COST_BAND

## Purpose
Treat cost as a class band (High / Medium-High / Medium / Low-Medium), not a dollar figure, and sanity-check the class against the part type. Callable forward (band a sheet) or reverse (given a class, list the rows in it).

## When to use
- A spec assigns cost classes per row or subsystem.
- You need a quick cost sanity check before budgeting.
- Reverse: you want every High-cost row, or every Low-Medium row, across the matrix.

## Required inputs
- The cost class column.
- The part type (precision harmonic, roller-screw, tendon, small motor).

## GOSUB contract
- **Forward call:** COST_BAND(sheet) → class distribution, inversions, exclusions.
- **Reverse call:** COST_BAND(class) → rows carrying that class.
- **Shared state:** reads the cost column; writes only to the audit log.
- **Direction tag:** forward | reverse.

## Steps
1. **Read each cell as a class, not a number.** High / Medium-High / Medium / Low-Medium.
2. **Check class vs part type.** Precision strain-wave and roller-screws → High. Small BLDC (Maxon/FAULHABER) → Medium. Tendons/Dyneema → Medium. Compound pulley → Low-Medium. Flag inversions.
3. **Sum by class.** Count rows per class; report the distribution, not a total.
4. **Note exclusions.** Structure, wiring, assembly labor are outside the actuator cost class.
5. **Report:** class distribution, inversions, exclusions.

## Rules
- Classes, not dollars. Do not convert to a number unless the sheet gives one.
- An inversion (e.g. tendon marked High) is a flag, not a correction.
- Bidirectional: reverse must enumerate the same rows the forward pass counted.

## Anti-patterns
- Summing classes as if additive dollars.
- Treating Low-Medium as free.
- One-directional only.

## Example
Optimus matrix: Hip/Knee/Shoulder/Spine/Differential = High; Ankle/Elbow = Medium-High; Wrist/Fingers/Neck = Medium; Compound pulley = Low-Medium. Distribution: 5 High, 2 Medium-High, 3 Medium, 1 Low-Medium.
Reverse: "High" → Hip, Knee, Shoulder, Spine, Differential.
