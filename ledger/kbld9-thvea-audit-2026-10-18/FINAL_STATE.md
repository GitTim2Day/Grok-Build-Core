# FINAL_STATE (2026-10-18, ET)

## Probe-suite state
| Suite | Module | Result |
|---|---|---|
| Sealed T1-T4 `ce0e09…` | kbld9_core_r7 | **4/4 PASS** (R0c and R5): T1 PASS, T2 PASS, T3 PASS, T4 PASS |
| Sealed T1-T4 `ce0e09…` | kbld9_core_r4 (skill default) | **0/4 ran**: AttributeError TIER_DAILY |
| Skill run command (truncated copy `e1484a83…`) | kbld9_core_r4 | **0/4 ran**: SyntaxError line 59 |
| THVEA harness v3 | kbld9_core_r7 | **14/16 PASS**. FAIL: H4a, H5. EARNED=False (gate blocked, as designed) |
| THVEA harness v3 | kbld9_core_r4 | **15/16 PASS**. FAIL: H4a |
| THVEA harness v3 | missing module | 16/16 BLOCKED, exit 1 (fail-closed) |
| THVEA harness v3 | 22 mutants of r7 | **22/22 killed**, 0 survived |
| Context: handoff ERRORTEST_ALL | kbld9_core_r7 | 51/51 |

Cases in v3 vs r7: T1 PASS (243 asserts), T2 PASS (440), T3 PASS (10), T4 PASS (2; median 182.1 ms in stability run 1), H1 PASS (44), H2 PASS (35), H3 PASS (3), **H4a FAIL** (8 of 210 boundary inputs: fused != oracle), H4b PASS (420), **H5 FAIL** (ERROR "cannot convert float infinity to integer"), N1 PASS (34), N2 PASS (9), P1 PASS (5), F1 PASS (2), F2 PASS (2), F3 PASS (3).

## Mutant progression
| Round | Suite | Killed / total |
|---|---|---|
| R1 | sealed T1-T4 | 6/16 |
| R2 | thvea-v1 | 16/16 |
| R3 | thvea-v2 (case-level, +6 mutants) | 18/22 |
| R4 | thvea-v3 | 22/22 |

## Untouched-file check (after all runs)
`/workspace/kbld9/probe_suite_3.py` `ce0e09f3…096d`, `/workspace/loaded/kbld9/probe_suite_3.py` `e1484a83…05f5`, `kbld9_core_r7.py` `465359bb…31d8`, `kbld9_core_r4.py` `e111d03d…6239`, `kbld9-handoff/probes/probe_suite_t1_t4.py` `ce0e09f3…096d`: all unchanged. No `__pycache__` was created (PYTHONDONTWRITEBYTECODE=1). No file under `/workspace/kbld9` or `/workspace/kbld9-handoff` is newer than the start of this audit. `/workspace/kbld9/protected/` was not opened. BOOT.bas and svct_v20* were not touched.

Environment: see `logs/env.txt`.
