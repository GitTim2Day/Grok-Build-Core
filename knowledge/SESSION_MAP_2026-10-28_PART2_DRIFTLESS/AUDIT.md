# AUDIT - PART2 MAP_v1 checked against disk (fail closed)
Anchor 2026-10-29T01:46Z (ET display 21:46 EDT). Statuses: VERIFIED / DRIFT / CONFLICT / UNVERIFIED / NEW-OPEN.
B1 VERIFIED all 11 scoped files re-hashed; each matches the LATEST line for it in source SHA256SUMS (source SHA256SUMS sha 9ec69369...0a4391).
B2 DRIFT (history) sha256sum -c on source SHA256SUMS: 11 FAILED = superseded append states (UNEXPLAINED_MATCHES x8, SOURCES x1, root4_exact x2 from parent A2). No corruption.
B3 VERIFIED ASD: recomputed min over 20-2000 Hz = 3.218410259045847313e-24 at 350.375 Hz; 1e-23 / floor = 3.107 (SOURCES "about 3.1x").
B4 VERIFIED R-i: A-C H0 6.194e-8 -> 9.1907e-8 %; B-C 2.1078e-14 -> 3.1275e-14 % (truncated 3.12e-14).
B5 VERIFIED R-j: C H0(7/100) 67.39584247824... truncated 67.39584247; (67.4-H)/0.5 = 0.008315; (73.04-H)/1.04 = 5.427; 168/635 H 67.40002128792 -> 67.40002129 in sources is ROUNDED (truncation gives 67.40002128).
B6 DRIFT UNEXPLAINED entry 9 states 7/100 H0 "67.39584248" (rounded); truncated value is 67.39584247 (PREDICTION). Parent R-c/A6 67.39584254 used truncated hbar; superseded by R-i. Not edited.
B7 CONFLICT separation threshold: entry 9 says H0 to "about 0.0001%"; PREDICTION says sigma(H0) ~0.0014 (= 0.00207 %, "about 0.002%"). PREDICTION figure recomputes; entry 9 left as-is.
B8 VERIFIED sqrt635 = 25.199206336708... truncated 25.19920633; entry 7 "25.19920634" is ROUNDED -> DRIFT note. Factors 635=5*127, 168=2^3*3*7 correct.
B9 UNVERIFIED entry 7 Higgs 125.20+-0.11 GeV "taken from memory, not fetched" (source says so).
B10 VERIFIED R-k table and findings 1-6 present in RESULTS_EARLY_UNIVERSE.md; zeta3=1.202 and Mpc 3.0857e22 named as A-only constants in early_universe_exact.py; pi computed by Machin in .out.
B11 VERIFIED z_eq 3417.94 vs 3402+-26 and column caveat (+BAO column 0.14240, 3387+-21) stated in source; Planck table not re-fetched this run (values UNVERIFIED externally).
B12 UNVERIFIED LISA "mid-2030s possible test": SOURCES has ESA launch planned 2035; PREDICTION_7_100.md does not itself mention LISA. Owner rule, not a file claim.
B13 NEW-OPEN fourth-root reminder (parent O7/A12): entry 9 and PREDICTION give the exact no-root form X^4 and inverse H0 form with sqrt last -> PARTLY ADDRESSED. Boot item 24 not located on disk this run; no reminder artifact exists.
B14 VERIFIED all scoped anchors are Zulu and after 2026-10-29T00:54:33Z (01:06Z..01:37Z); PREDICTION carries ET display alongside.
Count: 14 findings (8 VERIFIED: B1 B3 B4 B5 B8 B10 B11 B14; 2 DRIFT: B2 B6; 1 CONFLICT: B7; 2 UNVERIFIED: B9 B12; 1 NEW-OPEN: B13). B5 and B8 carry rounding notes.
