# kbld9-r8-2026-10-18 — KBLD9 core r8 DRAFT (final draft: r8a), for Timothy H. Norman

Sitting: Sun 2026-10-18, about 12:15-12:55 ET. Box only. No spend, no cloud agents, no background restart. `/workspace/kbld9/protected/` was not opened. BOOT.bas and svct_v20* were not touched. No sealed or existing file was edited. r7 sha256 `465359bb…31d8` was checked before, during and after (unchanged). Production stays r7. r8a is a draft for Timothy to seal or reject.

## Headline (measured)
- **Fix logic applied (Timothy's rule):** 3/6/9-sigma membership is decided on EXACT values (Fraction == float.as_integer_ratio), in both the fused path and the reference. Truncation is ROUND_DOWN on exact digit strings. Wherever a float intermediate overflows, the exact/scaled path takes over. Everywhere else r8a is r7, operation for operation. Details: CHANGES_r8.md.
- **thvea-v3 harness:** r8a 14/16 (FAIL H4a, H4b). r7 14/16 (FAIL H4a, H5). **16/16 was not reached.** The v3 oracle decides membership by float division, and on 16 of the 210 boundary inputs the exact values disagree with it (OPEN_GAPS R8-G1).
- **Sealed T1-T4:** r8a 4/4 (every run).
- **Boundary vs the independent exact reference:** r8a **0/210** (fused and module reference) and 0/630 on the shifted-median set. r7: 12/210 and 16/210.
- **[1e308,-1e308,0.0]:** r8a OK, data unchanged, CLEAN x3 (r7 ERROR). Extreme X-cases: r8a 14/15 (X12 FAIL: the fence value is r7's float fence, R8-G1b).
- **Regression vs r7:** non-boundary 2/94 differ (both the [1e308,-1e308,0.0] input: ERROR -> OK). Boundary 12/210 differ (listed in TEST_RESULTS.txt).
- **Mutants:** 22/22 re-applied audit patterns killed, 12/12 r8-specific killed (34/34). Round 1 had 30/34 before the test gaps were closed.
- **T4 (box only):** r8a 174.7 ms vs r7 178.7 ms, median of 7 interleaved trials (ratio 0.978). No Pi 5 number.
- **Rounds:** 3 of 5 (ROUNDS.md). One core fix (r8 -> r8a: exact-path digit-string convention). Two test fixes (extra cases v2, v3).

## Files
| Path | What |
|---|---|
| core/kbld9_core_r8a.py | final r8 draft core (LOCAL ONLY: protected core code) |
| core/make_r8.py, core/make_r8a.py | builders: r7 -> r8 -> r8a by SHA-checked exact replacements |
| CHANGES_r8.md | diff summary vs r7. Full diff: results/diff_r7_r8a.patch (local only) |
| TEST_RESULTS.txt | every count and timing |
| OPEN_GAPS.md | R8-G1..G10 (contract decisions for Timothy) |
| ROUNDS.md | round-by-round findings and fixes |
| SKILL_UPDATE_PROPOSAL.md | proposed kbld9-probe-suite-3 run command (dry-run verified; skill not edited) |
| tests/ref_exact.py | independent exact reference (Decimal, Inexact trapped) |
| tests/suite_inputs.py | regenerates every sealed-suite and v3 input (same seeds) |
| tests/r8_extra_cases_v3.py | E1-E5 (exact boundary), X1-X15 (extreme) |
| tests/boundary_report_v2.py, tests/regression_v2.py, tests/timing_t4.py | boundary detail, r7-vs-r8a regression, T4 timing |
| mutants/make_mutants_r8.py, mutants/run_mutants_r8_v2.py, mutants/r8a/ | 34 mutants + manifest (LOCAL ONLY: copies of the core) |
| results/R2, results/R2_mutants, results/R3 | result JSON per run |
| logs/ | every run log, the r7 hash before and after |
| archive/r8/, archive/round1/, archive/scratch/, archive/stray_pycache_from_kbld9/ | superseded drafts, round-1 tests and results, probes, and the moved stray .pyc (R8-G10) |
| SHA256SUMS | sha256 of every file above (`sha256sum -c SHA256SUMS`) |

## Reproduce
```
cd /workspace/kbld9-r8-2026-10-18 && export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD/core:/workspace/kbld9
python3 /workspace/kbld9-thvea-audit-2026-10-18/harness/probe_suite_3_thvea_v3.py kbld9_core_r8a /tmp/r8a
(cd core && python3 /workspace/kbld9/probe_suite_3.py kbld9_core_r8a)
python3 tests/r8_extra_cases_v3.py kbld9_core_r8a /tmp/r8a/extra.json
python3 tests/boundary_report_v2.py kbld9_core_r8a /tmp/r8a/boundary.json
python3 tests/regression_v2.py kbld9_core_r8a /tmp/r8a/regression.json
python3 mutants/run_mutants_r8_v2.py kbld9_core_r8a $PWD/mutants/r8a $PWD/core /tmp/r8a/mut /tmp/r8a/mut.log   # about 11 min
python3 tests/timing_t4.py kbld9_core_r8a
```

## Shelf policy
GitHub `GitTim2Day/Grok-Build-Core` is PUBLIC. Only docs and hashes go there (README, CHANGES_r8, TEST_RESULTS, OPEN_GAPS, ROUNDS, SKILL_UPDATE_PROPOSAL, SHA256SUMS). No `.py`, no diff patch, no mutants, no results JSON. The Drive copy is one combined markdown file plus SHA256SUMS. Email: summary, hashes and paths, no attachments.
