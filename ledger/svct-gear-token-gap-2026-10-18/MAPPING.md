# MAPPING — golden-spiral gear step as a TOKEN GAP in the SVCT ring
2026-10-18 EDT. Project: Timothy H. Norman. New files only; prior folders read, not modified.
Labels: **MODEL** = Timothy's stated model or an encoding chosen here (not measured). **MEASURED** = computed on the box (logs in this folder or the prior folder). **MODEL OBSERVATION** = reported by a video-analysis model (prior video job). Numbers are truncated, never rounded. Lengths in units of a.

## 0. Sources
- Prior math: /workspace/spiral-gear-tendon-2026-10-18/ (SESSION_MAP_v2.md, AUDIT.md, spiral_gear.py, interference_exact.json). spiral_gear.py and interference_exact.json are copied here byte-identical (sha256 1ab41e52…4250b, ac1371e1…eb40, both match the prior SHA256SUMS).
- Video job: /workspace/spiral-gear-video-2026-10-18/ (VIDEO_FINDINGS.md, COMPARISON.md).
- SVCT vocabulary (rg of reference map and /workspace; kbld9/protected/ not opened): SVCT = **Spherical Voxel Circular Token**; "SVCT lattice"; spherical voxel with layers that bloom outward in rings; circular_tokens promoted to spherical_voxels; concentric shells ("ONE shell … 64 cells", "61-shell"); fail-closed; append-only. The earned sphere geometry (8 contacts, 64 cells) is **not** used for the gear: nothing in the sources maps teeth to the 8 contacts, so that mapping is not made.

## 1. Ring position (MODEL: Timothy's 12-hour clock)
- Motor (gear 1) angle θ1 → `(turns, ring position p)`, p = θ1 mod 360° in [0°, 360°). At 360° the angle becomes 0°: `turns` advances by one. This is a new starting point, not a break.
- Gear model unchanged (MEASURED in prior work): r(θ)=aφ^(2θ/π), D=a(1+φ⁴)=7.854101966249a, r1+r2=D, ω2/ω1=r1/r2, ratio 0.145898033750 → 6.854101966249 within a turn, mean ratio 1, step drop 3√5 = 6.708203932499.

## 2. Spherical voxel, shell, circular token, gap (definitions)
| SVCT term | Gear meaning | Label |
|---|---|---|
| **Spherical voxel** | The meshing cell of the pair: centred on the contact point, which always sits on the axle line (prior math; video MODEL OBSERVATION agrees). | MODEL |
| **Shell** | A concentric radius level of the voxel. The contact on gear 1 sits on shell r1 ∈ [a, aφ⁴]; gear 2 is on the complementary shell r2 = D − r1. Over one turn the contact climbs outward shell by shell (r1 = a → aφ⁴), the bloom outward. | MODEL (radii MEASURED) |
| **Ring** | The voxel's equator = the ring position p, wrapped mod 360°. | MODEL |
| **Circular token** | One tooth = one token sitting in a slot of the ring lattice. N slots of pitch 360°/N. The default N = 12 is the 12-hour clock. The physical tooth count is **UNKNOWN** (the video gives none). | MODEL |
| **Lattice** | (turns ∈ ℤ) × (slot ∈ ℤ_N) × (phase within slot). Slot = ⌊p / pitch⌋ mod N (truncation). | MODEL |
| **Gap** | The toothless straight step = the **missing token**: slot N−1, the slot that ends where the ring closes (360°→0°). It is a missing token, not a broken ratio. Gap width = one pitch (30° for N = 12). The physical drive-loss width is **UNMEASURED**. In the ideal pitch-curve model the step has zero angular width. | MODEL |
| **Edge competition** | The corner overlap: the step is a straight radial segment that crosses **every** shell from a to aφ⁴ (length 5.854101966249a). Near the closure the step corner of one gear and the spiral flank of the other occupy the same shell, so two tokens compete for one shell. | MODEL; zones MEASURED |

Shell competition zones (MEASURED, ideal zero-clearance profiles, 0.25° poses, prior interference_exact.json): **107 of 1,440** poses, p ∈ **[0.25°, 23.25°]** (93 poses) and **[356.5°, 359.75°]** (14 poses). The deepest overlap is 0.038975766a at 2.25°. Shells there (MEASURED, mapping_numbers_run): r1/a = 1.001337593 at 0.25°, 1.012102950 at 2.25°, 1.132370309 at 23.25°, 6.727028441 at 356.5°, 6.844946212 at 359.75°. With N = 12 the 356.5°–359.75° side lies inside the gap (already held). The 0.25°–23.25° side is token 0: driven while competing. With N = 360 (gap [359°, 360°)), 356.5°–358.75° would be driven while competing.

## 3. Fail-closed and re-sync come from the lattice (MODEL)
1. **Absent token → no drive → hold.** The output is driven only through a present token. Slot N−1 holds no token, so it has no drive term. The reader returns no table value there (`classify` gives `joint=None`) and fails closed: it holds the last driven joint angle (`fail_closed=True`) and never extrapolates. A cold start inside the gap holds the gap's entry edge.
2. **Next token → re-index.** The slot index is ⌊p/pitch⌋ mod N. Moving forward out of slot N−1, the floor carries into `turns`, and the slot becomes 0 with phase 0. That carry *is* the re-sync: the joint is re-indexed to the table value at the arriving token's lattice position (turns·2π at phase 0). No extra rule is bolted on. The same happens when a sample jump skips the gap across the closure, and when backing out of the gap into slot N−2 (re-index to that token's phase).
3. **Consequence (MEASURED, closed form):** the hold-then-re-sync jump equals the ideal gear-2 travel over the missing-token slot:

| N | gap entry | jump (rad) | jump (deg) | % of a gear-2 turn | ratio at entry |
|---|---|---|---|---|---|
| 12 | 330° | 2.288261048 | 131.107700 | 36.418805 | 2.896308399 |
| 24 | 345° | 1.384436818 | 79.322386 | 22.033996 | 4.139291120 |
| 36 | 350° | 0.996137877 | 57.074496 | 15.854026 | 4.788482303 |
| 72 | 355° | 0.542520231 | 31.084119 | 8.634477 | 5.651453675 |
| 360 | 359° | 0.117178792 | 6.713850 | 1.864958 | 6.577159074 |

Test run (N = 12, table): held 3.994925162 rad, re-sync jump 2.288260144 rad (the table vs closed form differ by under 1e-5).

## 4. Code
`svct_gear_token_gap.py`: `ring_position`, `token_index`, `in_overlap`, `SVCTGearTokenRing.classify` (stateless) and `.step` (stateful hold / re-sync), returning `TokenState(token_index, in_gap, fail_closed, joint_angle, overlap, resync, turns, ring_deg)`. Outside the gap the joint angle is the existing `SpiralGearTransmission` table (4097 pts, Simpson 64), unchanged.
