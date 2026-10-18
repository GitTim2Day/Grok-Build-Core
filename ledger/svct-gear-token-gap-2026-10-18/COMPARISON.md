# COMPARISON — token-gap mapping vs. video findings and earlier conclusions
2026-10-18 EDT. Earlier: /workspace/spiral-gear-tendon-2026-10-18/ (AUDIT D1–D21) and /workspace/spiral-gear-video-2026-10-18/ (C1–C6). Video facts = MODEL OBSERVATION. Nothing new is taken from the video: no new numbers.

## Consistent
| Item | Earlier | Token-gap mapping |
|---|---|---|
| Step = loss of drive | Video C1: toothless step, drive lost, animation fast-forwards (≈0:08, ≈0:21) with a zip sound | Gap = missing token: no drive, hold (fail closed). The fast-forward is consistent with the re-sync jump (MODEL vs MODEL OBSERVATION; jump size not measurable from the video). |
| Plugin must fail closed | Video C4: future plugin must treat the step as a no-drive zone, joint limit or re-sync | Implemented as a Python reference (not ROS): `fail_closed` in the gap, `resync` on token arrival. The old code is not edited. |
| Contact on the axle line | Prior math r1+r2=D (5.168e-08a); video: contact point on the axle line | The voxel is centred on that contact; shells r1 and r2 = D−r1. |
| Teeth along the spiral | Video C2 | Teeth = circular tokens. |
| Table accuracy | 4.223e-06 rad worst (8001 samples) | Reproduced exactly (trunc 4.223e-06) on the same set. The new module equals the table bit-for-bit outside the gap (max diff 0.000e+00). |
| Phase must be known | AUDIT D4 | The lattice needs absolute ring position; `turns` + slot come from it. |
| Corner overlap | D2: 107/1440, 0.25°–23.25°, 356.5°–359.75°, max 0.038975766a at 2.25° | Same zones as the `overlap` (shell competition) flag. The test counts 107/1440 and matches all 140 listed pose depths. |

## What changes
1. **Step semantics.** The prior code models the step as an instantaneous ratio drop (D1, 3√5, φ⁸). Timothy's model reads it as a missing token, not a broken ratio: the ratio is defined where a token is present and undefined in the gap. D1's unbounded-acceleration issue is replaced by a hold followed by a re-index jump.
2. **Gap gets an angular width (MODEL).** Ideal pitch curves have a zero-width step. The token model gives the gap one pitch (30° at N = 12). Inside it the module's output differs from the ideal table by up to the slot's gear-2 travel (2.288261048 rad at N = 12; 0.117178792 rad at N = 360, MEASURED closed form). The real width is unmeasured.
3. **Where the table error sits (MEASURED).** With N = 12, the worst table error over the samples outside the gap is 9.514e-07 rad. The 4.223e-06 rad peak lies inside the gap slot, near the step, where the output is now held rather than used.
4. **D12 "one ratio" row.** It is consistent with "one ratio per present token-angle". The gap carries no ratio. The source row is not edited.
5. **Overlap is split by the gap.** At N = 12 the 356.5°–359.75° side (14 poses) is already held. Only the token-0 side (93 poses) is driven while competing.

## Open gaps (unchanged or newly exposed)
- **Tooth form** (profile, module) and **tooth count**: unknown, so N is a model choice, not data.
- **Backlash** (D7) and wear (D8): unmeasured; the hold assumes zero backlash.
- **Physical re-engagement mechanism**: what moves gear 2 through the re-sync jump (escapement, spring, indexing pawl, partial-turn use) is unknown. Neither the video nor the math shows it.
- Real gap width / drive-loss angle; step-corner relief (D2); reversal through the gap (D13): only the bookkeeping is tested, not the physics.
- The ros2_control plugin is still not built (D5/D6). This is a stdlib Python reference only.
