# skeletal-load-path-audit

**Date:** 2026-09-07
**Tags:** skeletal, load-path, audit, process

## Purpose
Audit the minimum skeletal requirement column: confirm the continuous load path is stated, the multiplier (× body weight) is sane, and the actuator is not the weak link.

## When to use
- A spec lists a skeletal or frame requirement per joint (e.g. pelvis ≥4× BW, femur-tibia column 4× BW).
- You need to check whether the frame can carry the actuator's peak.

## Required inputs
- The skeletal requirement column.
- The peak torque and impact columns.

## Steps
1. **List the load path per row.** Pelvis, femur-tibia, foot/tibia, scapula, arm tubes, forearm anchors, cervical, palm.
2. **Check the multiplier.** 3–4× body weight continuous is typical for legs; 3× shear/torsion for ankle; 3× tension for forearm anchors. Flag below 3× on a load-bearing joint.
3. **Cross-check against actuator peak.** If actuator peak exceeds the frame's continuous capacity, the frame is the problem, not the motor.
4. **Flag missing paths.** A joint with torque but no skeletal row is incomplete.
5. **Report:** load-path list, multiplier sanity, actuator-vs-frame check, gaps.

## Rules
- The frame carries continuous load; the actuator carries peak. Do not conflate.
- A missing skeletal row on a torque-bearing joint is a flag.

## Anti-patterns
- Treating the actuator as the load path.
- Skipping the actuator-vs-frame cross-check.

## Example
Hip: pelvis ≥4× BW. Knee: femur-tibia column 4× BW. Ankle: foot/tibia 3× BW shear & torsion. Wrist: forearm anchors 3× tension. Spine: pelvis-to-shoulder continuous. Compound pulley: rigid actuator output housing.
