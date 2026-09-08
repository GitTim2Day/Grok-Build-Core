# dyneema-termination-methods

**Date:** 2026-09-08
**Tags:** architecture, validation, plan, dyneema, tendon
**Status:** Active explore — not a sealed pick. Denier / braid count / eyelet D/d remain OPEN.
**GOSUB ID:** TERM_DYN
**Siblings:** antagonistic-dyneema-muscle-tendon (catalog 2026-08-16), decision-trigger-sequence, mass-budget-band, key-tolerance-limits-normalize
**KB:** knowledge/dyneema-termination-explore-2026-09-08.md
**Notion:** https://app.notion.com/p/3d5c9bfe3aff810598cbedadae112bd3

## Purpose
Map a Dyneema/UHMWPE tendon to a **proximal** termination and a **distal** termination. They are not the same method. UHMWPE is strong and almost frictionless (µ ≈ 0.04). A clamp that holds steel will slip this. Antagonistic pairing goes slack; a bury without a lock can be pulled out.

## When to use
- Wrist / finger / hand tendon routing (proximal actuators + antagonistic Dyneema).
- S02 public face: SK78 core, overbraid, Ti/DLC eyelets, motors unchanged.
- Workbook stretch cap 0.8%; distal anchors 3× tension; very low distal mass.

## When not to use
- Do not pick a denier, strand count, sew length, or eyelet D/d if it is not on the sheet.
- Do not treat knots or a heat-fused blob as the load path.
- Do not fold this into Candidate A knee geometry.

## Required inputs
- Station: proximal (forearm actuator / screw-nut) or distal (phalanx / palm / named eyelet).
- Whether the pair is antagonistic (zero-load lock required).
- Line construction if known: coated vs uncoated; hollow 12-strand vs other. If unknown, leave OPEN.
- Named hardware already on the book (Ti/DLC eyelets, motors unchanged).

## GOSUB contract
- **Forward call:** TERM_DYN(tendon, station, antagonistic?) → station map, lock yes/no, OPEN list.
- **Reverse call:** TERM_DYN(method) → which station it is legal for; reject if slack-unlock and antagonistic.
- **Shared state:** reads joint matrix + S02 public face; writes only to the audit log. Does not write denier.
- **Direction tag:** forward | reverse.

## Steps
1. **Split the tendon into two stations.** Write proximal and distal on separate lines. Do not assign one method to both by default.
2. **Check slack.** If antagonistic, require a zero-load lock (Brummel, sew, or pot). Long bury alone fails this test.
3. **Apply mass budget.** Distal: reject marine 60d/100d bury and steel thimbles. Proximal: mass is allowed; capstan/drum wraps are first.
4. **Map, do not pick, unless the sheet already names the hardware.**
   - Distal candidates: sew-into-rigid-tab; small potted nubbin (Socketfast Blue A-20 is the UHMWPE-named resin); tiny locked eye over the named Ti/DLC eyelet.
   - Proximal candidates: extra wraps on drum or screw-nut so the end sees preload not peak; backup sewn tab or small nubbin. Matches motors unchanged.
5. **Cite published efficiencies as published, not as ours.** DSM bury 60d coated / 100d uncoated. D/d 8 best / 5 acceptable / 3 compact. 2 mm Dyneema: sew 25 mm ~85%; small clamp 28%; knots 8–58%.
6. **Report:** station map, lock yes/no, what stayed OPEN (denier, braid count, D/d, sew length, potting drawing).

## Rules
- Two stations. Always.
- No invented numbers. April 2025 originals, denier, termination drawing, pulley D/d stay OPEN until sourced.
- Stretch 0.8% is a working-stretch budget (Marlow D12 SK78-class ~0.51% at 10% BL, ~0.89% at 20% BL). A crushed knot or slipping clamp blows it.
- Coating fights a bury splice. If the line is coated, say so before splicing.
- Append only. Do not rewrite the 2026-09-03 Dyneema recovery notes.

## Anti-patterns
- One splice for both ends.
- Knot as primary load path.
- Heat-weld as load path.
- Claiming a pick is sealed when denier is still OPEN.
- Copying marine shroud practice (60d bury + closed SS thimble) into a phalanx.
- One-directional only.

## Example
Forward: wrist antagonistic SK78, Ti/DLC eyelet named, denier OPEN.
- Distal: locked eye over named eyelet or sew-into-palm tab. Lock = yes. D/d OPEN.
- Proximal: wraps on actuator/nut + sewn or potted backup. Motors unchanged.
- Report OPEN: denier, braid count, eyelet D/d, sew length.
Reverse: "long bury eye, no Brummel" → illegal on antagonistic distal (slack pull-out).
