# PATTERN MAP — voice dist earn 2026-09-11
Pickup: 2026-09-11T18:33:00-04:00
Chair: this disk. Owner: Timothy H. Norman.

AUTH Style A SHA-256 3d78fbbe0bf7cc383e7a410d6922baf0224b014395fa4838d05d8e97926cbc12
Map SHA-256 5d233b2df902c3f1da5d13f4d7edf4fbf2e6dda6fd4759dcf24a2cb17668de5f
CSV SHA-256 900ab194c871d6b6ee8e94b787903f19a0fe7822ca47777066ccf199b1d681a4
gosub_brain.py SHA-256 71d576edb3296c62b0eab714a6efa6d21069f7141eb02f35821de48f6424573d
Recipe: tract_v1_frame30_hop10_f0_60_350
Primary: D=(1-cos)^2 on THIS vector. Sibling 3e-5 is THEIR vector. Do not copy.

## MATCH
GOSUB_BRAIN ingest|takech|raw|extract|extract_tract|highband|dist
u_hi own column; sr<44100 E_SR_LOW
Smoke 7-D SUPERSEDED. F0 two-key leaked DL+WT.
L1 ~2x. First-integral volume = F0 restated. sum_sq 3.8-5.2x.
Fail-first A28-46 vs A46-75 D=0.000024 FR at 2e-5; floor 3e-5.
After: same 3/3 MATCH; impostor 57/57 NO-MATCH; CLOSE+veto 22; n=60 errors=0.
Style B / Fort MISSING this hop.
Sibling cosine fixture 0.96922 / A vs B 0.9837 — their recipe.

## GOSUB_DIST
D=(1-cos)^2
IF D<=3e-5 THEN MATCH
ELSE IF D<=3e-4 THEN CLOSE; IF sum_sq>0.04 THEN NO-MATCH
ELSE NO-MATCH
Backups CLOSE only: sum_sq, F1/F2, rel_f0, dcov.

## OPEN
B/Fort this disk; LPC; new mic/room; 300-count; probability fold; 99.9%.
REFUSE: copy sibling threshold; pad u_hi; average recipes.
