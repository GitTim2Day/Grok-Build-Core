# AUDIT of MAP_v1 (append-only; MAP_v1 not edited)
Anchor 2026-11-01T01:50Z (ET display 2026-10-31 21:50 EDT). Method: grep scans of MAP_v1.md plus hand check against sources. Nothing in any source was edited.
## (i) Rounding: 1 finding
- A1: R-p figures "~3.2e-7", "6.17e-5", "~0.008 sigma", "7.43e-3" are copied as recorded in RESULTS_SQFIX.md / UNEXPLAINED_MATCHES.md:72 (source writes them as approximate); not recomputed here. Label "as recorded".
## (ii) Floats: none found (all numbers are display text; no computation in this map).
## (iii) Subtraction form: none found (no value subtraction written; residuals are cited, not computed).
## (iv) zero/UNDEFINED misuse: none found (UNDEFINED appears only inside rule statements; M4 (iii) correctly written "none found").
## (v) Unsourced values: 4 findings
- A2: M5 cause "unpaid invoice on the paying account" has no on-disk source; boot file drift note S12 marks it UNVERIFIED. Label UNVERIFIED (per brief: platform failure notices).
- A3: M7 ticket T-H76312, $100.11, $0.61: from brief; only on-disk hits are in /workspace/ifthen-merge-2026-10-20/tests/ (2026-10-18 mail copies), not re-read this run. Label UNVERIFIED.
- A4: R-l PENDING rule: no on-disk ruling file (boot Number rules S12 cite Research memory). Label "per memory".
- A5: map anchor is box clock, not HTTPS-synced this run; precision UNVERIFIED.
## Counts: i 1, ii none found, iii none found, iv none found, v 4. Total 5.
## Verified: parent MAP_v2 3712fa5a...415e; SESSION_AUDIT_FULL 50 rows (counts line 81-86); NIGHTLY 17 (boot line 94); H0 45-digit string RESULTS_SQFIX.md:92 matches brief prefix; UNEXPLAINED_MATCHES sha 538beecd...3de.
