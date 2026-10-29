# AUDIT - MAP_v1 checked against disk (fail closed)
Anchor 2026-10-29T00:54:33Z (ET display 20:54 EDT). Statuses: VERIFIED / DRIFT / CONFLICT / UNVERIFIED / NEW-OPEN.
A1 VERIFIED all 13 named source files re-hashed; each matches the LATEST line for it in SHA256SUMS.
A2 DRIFT (history, not corruption) sha256sum -c reports 6 FAILED: 4 superseded UNEXPLAINED_MATCHES.md append states + 2 root4_exact lines (failed sympy run; one is e3b0c442 empty hash). Append-only record; no file changed.
A3 DRIFT codata2022_allascii.txt was not in SHA256SUMS; hashed now 77fb90e66c40db3e6eb16630bc9c88e4c7c8beddbe5e71be406f2f26e3f67e67.
A4 CONFLICT RESULTS_v5.md FEL note says [FEL-OUT] cosmological values are "OUTSIDE the approved scope, Timothy needs to rule". Later Timothy scope note (UNEXPLAINED_MATCHES.md, R-a) rules cosmological Planck-based values legitimately exceed FEL. v5 left unedited; superseded by R-a.
A5 VERIFIED X = 0.26456697 (root4_exact.out 0.264566971036...); X^4 formula matches entry 5.
A6 VERIFIED H for X^2=7/100 = 67.3958425401870... truncated to 67.39584254.
A7 VERIFIED 5.4 sigma from SH0ES: (73.04-67.39584254)/1.04 = 5.42... ; 0.006% from 67.4.
A8 NEW-OPEN root4_exact.out lists X nearest p/q 168/635 rel err 1.583E-7, tighter than sqrt(7)/10 (X^2 7/100 rel err 6.168E-5). Not in MAP_v1. Per R-b logged OPEN, not dismissed, not chosen.
A9 VERIFIED R-d 2/3/6 in entry 3. R-e in entry 2 (G ~1.1e-5 relative).
A10 VERIFIED P3: electron 2.389222002668E+22 vs 2.389222127269E+22 -> agree to 7 significant digits; 6-7 claim holds.
A11 VERIFIED R-f against RESULTS_v3/v4/v5 + ERRATUM_v4 verdict lines.
A12 UNVERIFIED R-g: no reminder artifact or scheduled item exists on disk; only root4_exact.py holds the exact form. Pending.
A13 DRIFT RESULTS_v5.md header stores "~20:10 EDT" (display time), not Zulu. Not edited; Zulu equivalent ~2026-10-29T00:10Z is approximate (source says ~).
A14 UNVERIFIED O6: 1e-23/sqrtHz ASD and SNR=8 threshold unsourced (as v5 itself states); GW250114 distance not extracted.
A15 VERIFIED P4 1826/1685 and 1E-61 in root4_exact.out.
Count: 15 findings (8 VERIFIED: A1 A5 A6 A7 A9 A10 A11 A15; 3 DRIFT: A2 A3 A13; 1 CONFLICT: A4; 2 UNVERIFIED: A12 A14; 1 NEW-OPEN: A8).
