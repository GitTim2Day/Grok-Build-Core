# rt345_check — 3-4-5 / circular slide rule checks

Owner: Tim. Built and run by Claude (Opus 5.5), 2026-09-30.
Source body: Drive RIGHT_TRIANGLE_345_20260930T1323-0400.md (1qYMn4NcrGQ4oc3_vO_moEKTKGxjXG9Zg).
Name: circular-slide-rule-20260930T1335-0400. Lesson: math-before-agent (BOOT_SET item 10).

| File | Bytes | Lines | SHA-256 | Status |
|---|---|---|---|---|
| rt345_check.py | 3930 | 79 | 0fec931a2fc5adcfa9079db017d3f47b8d90964207b367bfac552d20a05715a0 | EARNED: 8/8, exit 0 |
| rt345_check.cpp | 2758 | 47 | e8c0f58d7ad47a0eb4348aa97935d6744f79874594859ddeba46f4511170b3b0 | EARNED: 8/8, exit 0 (g++ -std=c++17) |
| rt345_check.bas | 914 | 18 | f608d94ce35972a0839f713cd8d20395feecdabd55300ef27d12f03bccb0063a | ASSERTED: not run, no BASIC interpreter on host |

Exact rational arithmetic only. No float in the checked path.
Checks: unit from any side (9 cases), mismatch needs the root (sqrt 34), not plus (3u+4u=7u),
solve for any one factor, four quadrants all roots 5, 60 folds to 60/120/240/300, 0 and 360 one wrap,
3-4-5 is the exact unit-circle point (4/5, 3/5) at t=1/3 (PROPOSAL), negative control 3-4-6 rejected.

Supersession: first build used t=1/2. Both builds failed that check. t=1/2 gives (3/5, 4/5), the other acute angle. Fixed to t=1/3.

Homes: Drive folder 1Q-MCJwaATYmV5rGDa1Ci_ALG589Tm5P4 (py 1cRc_BFYnEABqnT6MBZnY02KweS6k9HsI, cpp 1i8eWd46gyMv0_u-Ci27H16fYDRoXPRVY, bas 1k9RgWnBgcGDGuewqcREDBZtqowR8CQek).
Status sheet 1iA7l1X57cg4kzBBlRfYkW93jWCGNb-yu2wI_XEGfIpI (row 0 names 13kBkE0OgZVm7Yjow1c4MX5Cv1oqYzq-rLXTr22N2Vok).

Run: `python3 rt345_check.py` ; `g++ -std=c++17 -o rt345 rt345_check.cpp && ./rt345`
