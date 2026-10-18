# ROUNDS — error-test / mitigate loop (5 of max 6 rounds used)

All times ET (America/New_York). Every mitigation is a NEW file. No existing or sealed file was edited (re-hashed after the run, unchanged; see FINAL_STATE.md). Superseded harness versions are archived with their results in `archive/`.

## Round 0 — the suite as it was found (step 2)
| Run | Command | Result | Log |
|---|---|---|---|
| R0a | skill command: `cd /workspace/loaded/kbld9 && python3 probe_suite_3.py kbld9_core_r4` | `SyntaxError` line 59 (truncated T2 f-string). 0 of 4 probes ran: T1 FAIL, T2 FAIL, T3 FAIL, T4 FAIL (not executed) | logs/R0a_loaded_skillcmd_r4.log |
| R0b | sealed suite `ce0e09…` vs `kbld9_core_r4` (skill default) | `AttributeError: module 'kbld9_core_r4' has no attribute 'TIER_DAILY'`. 0 of 4 ran: T1-T4 FAIL (not executed) | logs/R0b_kbld9_suite_r4.log |
| R0c | sealed suite `ce0e09…` vs `kbld9_core_r7` (production line) | T1 PASS, T2 PASS, T3 PASS, T4 PASS = 4/4. T4 runs 182.5, 185.7, 190.4, 197.8, 206.0 ms (median 190.4) | logs/R0c_kbld9_suite_r7.log |
| R0e | PDF-text copy `probe_suite_3_CORRUPT_backup.py` vs r4 | `SyntaxError` line 59, 0 of 4 ran | logs/R0e_pdfversion_r4.log |
| R0d | context: `kbld9-handoff/ERRORTEST_ALL.py` (r7, 5 sealed suites) | 15/15 + 10/10 + 4/4 + 8/8 + 14/14 = 51/51, total failures 0 | logs/R0d_handoff_errortest_all_r7.log |

## Round 1 — error-test the sealed suite
- Built 16 mutants of r7 (`mutants/make_mutants_v1.py`). The source is SHA-checked and every pattern must match exactly once, or that mutant is not written.
- Sealed suite vs mutants: **6 killed** (M02 hi fence 9.5, M03 no clamp, M04 CLEAN band 3.5, M07 mad0 no snap, M12 tier on cleaned, M13 +0.4 s sleep). **10 survived:** M01, M05, M06, M08, M09, M10, M11, M14, M15, M16. Log: `logs/R1_error_test_existing_suite_vs_mutants.log`.
- Fault and edge findings: the suite crashes outright on r4 and on the truncated copy (C9, C12).
- **Mitigation 1:** new harness `thvea-v1` (now `archive/thvea-v1/probe_suite_3_thvea_v1.py`, sha256 `4de3c03f…2ebfd`). It adds an explicit inputs/expected manifest, an independent oracle, negative tests N1/N2, faults F1-F3, boundary H1, edges H2/H3, provenance SHA checks, an assertion counter, an EARNED/BLOCKED gate, and read-back validation. Its first draft hit a `SyntaxError` at its own first run. That draft was fixed before any result was recorded (it had never run successfully).

## Round 2 — rerun + re-error-test v1
- v1 vs r7: 12/12 PASS, EARNED (logs/R1_thvea_v1_r7.log). v1 vs 16 mutants: 16/16 killed (logs/R2_thvea_v1_vs_mutants.log). Missing module: all 12 BLOCKED, exit 1 (fail-closed OK).
- v1 vs r4: 6/12. Defects found in the **harness**: T1 "VACUOUS" (the declared minimum assumed 3 tiers), `IndexError PRECS[1]` in 4 cases, and the oracle crashing with `OverflowError` on the r4 OK envelope for `[1e308,-1e308,0]`.
- New edge probe (ULP scan): fused path != module reference in 8 of 210 boundary inputs, on both r4 and r7. Also, r7 returns ERROR on `[1e308,-1e308,0.0]` where r4 returns OK.
- **Mitigation 2:** `thvea-v2`, derived by script `make_v2_from_v1.py` (v1 left byte-identical). Changes: minimum counts scale with tiers, no hard tier index, lazy overflow-safe oracle fence, new H4 (ULP boundary) and H5 (valid near-max input). The first two derivation attempts stopped fail-closed on a pattern-count assertion and wrote no file (logs/R2_thvea_v2_*.log show "can't open file").

## Round 3 — rerun + re-error-test v2
- v2 vs r7: 12/14 (FAIL H4, H5). v2 vs r4: 13/14 (FAIL H4). Logs: `logs/R3_thvea_v2_kbld9_core_r7.log` and `logs/R3_thvea_v2_kbld9_core_r4.log`.
- Re-error-test: 6 new mutants M17-M22 (`mutants/make_mutants_v2.py`) and a case-level runner `harness/run_mutants_v3.py`. That runner counts a mutant as killed only when a case that passes on the baseline fails on the mutant, so a known baseline failure cannot hide a mutant.
- Result: **18/22 killed. Survived: M17** (reference `_classify` DRIFT 6.5), **M18** (reference `_snap` fence 9.5), **M21** (spine not advanced), **M22** (chain dropped). Cause: the H4 baseline failure masked reference checks, v1 had dropped the T2 tier differential that the sealed suite has, and there was no spine test. Log: `logs/R3_thvea_v2_vs_22_mutants.log`.
- **Mitigation 3:** `thvea-v3` (`harness/probe_suite_3_thvea_v3.py`, sha256 `a656148d2022c9b02698049fee98c63c5e734af06cefb0563acbe196e14c5f38`), derived by `harness/make_v3_from_v2.py`. Changes: T2 tier differential vs module `_classify` restored; H4 split into H4a (fused vs oracle) and H4b (module reference vs oracle); H1 also checks the module reference; new P1 (chain, seed, spine).

## Round 4 — rerun + re-error-test v3
- v3 vs 22 mutants: **22/22 killed**, 0 survived (logs/R4_thvea_v3_vs_22_mutants.log). Missing module: 16/16 BLOCKED, exit 1.
- v3 vs r7: 14/16 (FAIL H4a, H5). v3 vs r4: 15/16 (FAIL H4a).

## Round 5 — stability + stop
- v3 vs r7 run 3 times: identical verdicts each time (14/16; H4a and H5 FAIL). The result-file hashes differ between runs because T4 timings are recorded (T4 medians 182.1 / 182.1 / 185.2 ms). Log: `logs/R5_stability_v3_r7_x3.log`. Results: `results/v3_stability/`.
- Sealed suite rerun vs r7: 4/4 (T4 median 173.4 ms). Log: `logs/R5_sealed_suite_r7_rerun.log`.
- **Stop reason:** every mutant is killed. The two remaining failures (H4a, H5) are behaviour of the sealed production core. Fixing them needs a new core revision, and R7 is the line Timothy chose on 2026-09-18, so this needs Timothy. Round 6 was not used.
