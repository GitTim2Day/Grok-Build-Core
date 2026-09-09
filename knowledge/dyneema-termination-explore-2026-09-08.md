# Dyneema termination methods — explore 2026-09-08

Append only. Not a sealed pick. No invented denier, strand count, or eyelet D/d.

Skill: skills/dyneema-termination-methods.md (GOSUB TERM_DYN)
Notion skill: https://app.notion.com/p/3d5c9bfe-3aff-8105-98cb-edadae112bd3
Sitting: THREAD PARENT MAP compare 2026-09-08. Cluster 17 open leaf.

Earned faces already on the book:
- S02 public: SK78 core, Dyneema overbraid, Ti/DLC eyelets, motors unchanged
- Gmail matrix 2026-08-13 (message_id 19ffde30b33198f0): wrist elongation ≤0.8%, force res ≤1.5 N; fingers ≤0.8 N; distal forearm anchors 3× tension; very low distal mass
- GitHub knowledge dyneema-optimus-tendon-recovery-append-2026-09-03: braid count / denier / termination / pulley diameters still OPEN

## Physics of the problem

UHMWPE is strong and almost frictionless. Published µ (UHPE sleeve on metal) ≈ 0.044 vs stainless wire ≈ 0.24 (Hasegawa 2022). A clamp that holds steel will slip Dyneema. Heat-weld is not a load path (orientation dies near melt). Knots crush the braid and throw away most of the break.

A tendon has two stations. They are not the same termination.

| Station | Job | Mass budget | Load when antagonist slacks |
|---|---|---|---|
| Proximal (forearm actuator / screw-nut) | take cyclic stroke | can be heavier | capstan wraps can unload the end |
| Distal (phalanx / palm / Ti-DLC eyelet) | hold 3× tension, stay light | kills bulk | must lock at zero load |

Antagonistic pairing makes the zero-load lock mandatory. A long bury without a lock can be pulled out when the line goes slack.

## Method families (published efficiencies — not ours)

| Family | How it holds | Strength face (published) | Distal? | Proximal? | Zero-load lock |
|---|---|---|---|---|---|
| Long bury eye | finger-trap, 60d coated / 100d uncoated (DSM) | manufacturer benchmark; OSU control | too long for a phalanx | possible if routing allows | no — eye can be pulled out slack |
| Locked Brummel + long bury | two passes through the braid, then bury | no stronger than the bury; lock is the slack insurance | still bulky | yes | yes |
| Eye + thimble / LFR | same splice, D/d of the ring | D/d 8 best, 5 acceptable (HMPE survey); 3× used as compact | steel thimble is mass; LFR lighter | yes | only if Brummel or stitch |
| Knots | crush + friction | OSU 8–58%; 2 mm Dyneema bowline ~47%, fig-8 ~51% (Hasegawa) | compact, weak | reject as primary | poor |
| Dry clamp / clip | friction on a slippery fiber | small clamp 28%, large 65% on 2 mm Dyneema | extra mass | backup only | no |
| Sew / stitch as load path | thread shear through the braid | 25 mm sew 85%; 40 mm 81% on 2 mm Dyneema | best distal candidate class | backup | yes if stitch remains |
| Calk / groove pin | custom groove + loop | calking up to ~90%; Hasegawa fig-8-in-groove 91.3% | compact if the pin is small | possible | yes |
| Pot / nubbin / epoxy wedge | splay fibers in a taper; Socketfast Blue A-20 is the UHMWPE-named resin | OSU adhesive series mixed; Sandia used tapered SS cylinder + epoxy | compact, not serviceable | yes | yes |
| Capstan / drum wraps | F_term = T/e^{mu psi} + T_pre | Sandia: extra wraps so the end only sees preload | n/a | best proximal candidate class | end still needs a backup |
| Chinese-finger sleeve | braid contracts on a cone | serviceable, no resin | medium bulk | possible | yes under tension |
| Crimp + CA (catheter class) | grit sleeve + Loctite 420 | medical/steerable, not 50–150 kg grip | wrong scale | wrong scale | — |

Marlow D12 (SK78-class 12-strand) datasheet: spliced-eye allowance 60d; soft-eye neck <=30 deg; D/d 5 for grommets. Working stretch ~0.51% at 10% BL, ~0.89% at 20% BL. The workbook 0.8% cap is a stretch budget, not a splice recipe.

S02 Ti/DLC eyelets, motors unchanged is already a distal hardware face. The OPEN is how that eye is made and the D/d of that eyelet vs. the line.

## Map to this architecture (not a pick)

- Distal, fingers/palm: sew-into-rigid-tab or small potted nubbin, or a tiny locked eye over the named Ti/DLC eyelet. Marine 60d bury does not fit a phalanx.
- Proximal, forearm: drum/nut wraps first so the termination sees preload, not peak; backup is a sewn tab or small nubbin. Matches motors unchanged.
- Do not use knots as the load path.
- Do not use a heat-fused blob as the load path.
- Coating (PU) fights a bury splice; if the line is coated, say so before splicing.

## Still OPEN (same list as 2026-09-03)

Braid count. Denier. Termination hardware drawing. Pulley / eyelet D/d. April 2025 originals. Sew length. Potting drawing.

No number invented this sitting.

---

## 2026-09-09 — orbital capture application (appended, not a pick)
This page is Optimus-tendon focused, but the same UHMWPE rules apply to the orbital bicycle-wheel depot capture tethers (see orbital-bicycle-wheel-depot).

- 12-strand per filament, 8 parallel bays, ~910 kg/bay, ~7.3 t total for Falcon 9 class load.
- Coating/embed layers are in progress separately; coating fights a bury splice — flag before splicing.
- Fatigue: 8-strand ~10 yr; 12-strand 10 yr to indefinite with cover swaps.
- Still OPEN: denier, coating chemistry, splice method, inspection cadence. No numbers sealed here.
