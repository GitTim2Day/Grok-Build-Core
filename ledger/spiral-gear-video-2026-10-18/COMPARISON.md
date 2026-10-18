# COMPARISON — video findings vs. spiral-gear-tendon-2026-10-18
2026-10-18 EDT. Prior work: /workspace/spiral-gear-tendon-2026-10-18/ (SESSION_MAP_v2.md, AUDIT.md, README.md read; files not modified).
Video facts below are MODEL OBSERVATION (see VIDEO_FINDINGS.md).

## Prior results (quoted from the prior folder, computed there)
- Motor-to-joint table (4097 pts): worst position error 4.223e-06 rad (Python sample set); round trip 2.131e-14 rad.
- Tests: Python 21/21, C++ 20/20 (parity 4.263e-14); mutants 8/8 killed.
- Ratio w2/w1: 0.145898033750 (φ⁻⁴) → 6.854101966249 (φ⁴); drop at the step 6.708203932499 (= 3√5), factor φ⁸; mean ratio over a turn 1.000000000000.
- Step-corner interference (ideal, zero clearance): 107 of 1440 sampled poses, max 0.038975766 a.

## Conclusions
| # | Conclusion | Effect on prior work |
|---|---|---|
| C1 | The video CONFIRMS the step is a real loss of drive, not a smooth transition. The animation hides it with a jump (≈0:08–0:09, 0:21–0:22). A physical drive would need an escapement, a re-indexing mechanism, or a restriction to partial-turn operation. | Strengthens AUDIT HIGH items D1 (step discontinuity) and D4 (phase must be known). Does not contradict the math. |
| C2 | Teeth exist, but their form is unspecified. Tooth form and backlash remain unmeasured. | D7 (backlash) and D9 (torque path / tooth form) stay open; D9 narrows: it is a toothed drive, not a friction drive (per model observation). |
| C3 | The table and the tests are unaffected: same equations (r = aφ^(2θ/π), r1+r2=D, ω2/ω1=r1/r2). | 4.223e-06 rad, 21/21, 20/20, 8/8 stand. |
| C4 | **REQUIRED PLUGIN CHANGE (future version; old code NOT edited):** the ROS2 plugin must treat the step as an undefined / no-drive zone and fail closed (joint limit, or position re-sync after the step), not as an instant ratio change. | spiral_gear_transmission.hpp / spiral_gear.py currently model the step as an instantaneous ratio drop; leave as is, change in the next version. Ties to D5/D6. |
| C5 | The video does not resolve corner overlap; an animation cannot show interference. | D2 (107/1440, max 0.038975766 a) stays open. |
| C6 | "Fibonacci" is a label; the profile is the golden spiral (r = aφ^(2θ/π), growth φ per quarter turn). | Naming only. |

## Still open
Tooth form, backlash, wear, torque/stress, physical size a, step-corner relief, ros2_control plugin (not built). Nothing here was measured on hardware.
