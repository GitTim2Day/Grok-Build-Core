# tolerance-floor-audit

**Date:** 2026-09-07
**Tags:** tolerance, backlash, stiffness, floor, audit, process

## Purpose
Audit the tolerance and stiffness floors in a spec: confirm units, direction (≤ or ≥), and whether the floor is physically meaningful for the joint class.

## When to use
- A spec lists backlash, stiffness, elongation, force resolution, accuracy.
- You need to check whether a floor is achievable or over-specified.

## Required inputs
- The tolerance column or list.
- The joint or subsystem class (rotary, linear, tendon).

## Steps
1. **Normalize units.** Arcmin, degrees, mm, percent, N, Nm/rad — convert to one consistent set per joint class.
2. **Check direction.** Backlash and elongation are upper bounds (≤); stiffness and impact are lower bounds (≥). Flag any reversed.
3. **Sanity-check magnitude.** Rotary backlash ≤1.5 arcmin is typical for harmonic; linear backlash ≤0.04 mm is tight but plausible for roller-screw; tendon elongation ≤0.8% is aggressive.
4. **Cross-check against skeletal load.** A floor that exceeds the frame's continuous capacity is a frame problem, not an actuator problem.
5. **Report:** normalized floors, direction check, magnitude sanity, frame cross-check.

## Rules
- Floors are acceptance criteria, not design targets.
- Never relax a floor without stating the risk.

## Anti-patterns
- Mixing arcmin and degrees without conversion.
- Treating a stiffness floor as a torque target.

## Example
Knee: linear backlash ≤0.04 mm, impact ≥6× BW; ankle: accuracy ≤0.1°, tunable compliance; wrist: elongation ≤0.8%, force res ≤1.5 N.
