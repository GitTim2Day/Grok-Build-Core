# skeletal-load-path-audit

**Date:** 2026-09-07
**Tags:** skeletal, load-path, audit, process, gosub
**Status:** Active — GOSUB member (bidirectional)
**GOSUB ID:** SKELETAL_AUDIT

## Purpose
Audit the minimum skeletal requirement column: confirm the continuous load path is stated, the multiplier (× body weight) is sane, and the actuator is not the weak link. Callable forward (audit paths) or reverse (given a load-path element, find the joints that depend on it).

## When to use
- A spec lists a skeletal or frame requirement per joint (e.g. pelvis ≥4× BW, femur-tibia column 4× BW).
- You need to check whether the frame can carry the actuator's peak.
- Reverse: a frame element changes and you need every joint it supports.

## Required inputs
- The skeletal requirement column.
- The peak torque and impact columns.

## GOSUB contract
- **Forward call:** SKELETAL_AUDIT(sheet) → load-path list, multiplier sanity, actuator-vs-frame check, gaps.
- **Reverse call:** SKELETAL_AUDIT(path_element) → joints whose continuous load path includes it.
- **Shared state:** reads the skeletal column; writes only to the audit log.
- **Direction tag:** forward | reverse.

## Steps
1. **List the load path per row.** Pelvis, femur-tibia, foot/tibia, scapula, arm tubes, forearm anchors, cervical, palm.
2. **Check the multiplier.** 3–4× body weight continuous is typical for legs; 3× shear/torsion for ankle; 3× tension for forearm anchors. Flag below 3× on a load-bearing joint.
3. **Cross-check against actuator peak.** If actuator peak exceeds the frame's continuous capacity, the frame is the problem, not the motor.
4. **Flag missing paths.** A joint with torque but no skeletal row is incomplete.
5. **Report:** load-path list, multiplier sanity, actuator-vs-frame check, gaps.

## Rules
- The frame carries continuous load; the actuator carries peak. Do not conflate.
- A missing skeletal row on a torque-bearing joint is a flag.
- Bidirectional: reverse returns the same joints the forward pass listed.

## Anti-patterns
- Treating the actuator as the load path.
- Skipping the actuator-vs-frame cross-check.
- One-directional only.

## Example
Hip: pelvis ≥4× BW. Knee: femur-tibia column 4× BW. Ankle: foot/tibia 3× BW shear & torsion. Wrist: forearm anchors 3× tension. Spine: pelvis-to-shoulder continuous. Compound pulley: rigid actuator output housing.
Reverse: "pelvis" → Hip, Spine.
