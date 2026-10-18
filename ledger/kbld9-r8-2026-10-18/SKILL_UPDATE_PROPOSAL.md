# SKILL_UPDATE_PROPOSAL — kbld9-probe-suite-3 (PROPOSAL ONLY; the skill was NOT edited. Timothy edits it.)

## Replace this (broken)
```
cd /workspace/loaded/kbld9 && python3 probe_suite_3.py kbld9_core_r4
```
Why it is broken (measured in the 2026-10-18 audit): `/workspace/loaded/kbld9/probe_suite_3.py` (`e1484a83…05f5`) is the PDF-text copy. Its T2 line is truncated, so it raises SyntaxError at line 59 and 0 of 4 probes run. That directory has no core module. The r4 default also crashes the sealed suite (AttributeError TIER_DAILY).

## With this (primary: core r8a draft; fallback: r7 production)
```
# 0) provenance gate: stop if any hash differs
sha256sum -c <<'SUMS' || { echo "PROVENANCE MISMATCH - stop"; exit 2; }
a656148d2022c9b02698049fee98c63c5e734af06cefb0563acbe196e14c5f38  /workspace/kbld9-thvea-audit-2026-10-18/harness/probe_suite_3_thvea_v3.py
ce0e09f329599dfa511cb036aa9f0c2bbb39d0d84deb46e43c34eb31f4d0096d  /workspace/kbld9/probe_suite_3.py
16934bab2d88a3f7a63a9f16a7c986e296d13dd053c6d441eb05a028545347c6  /workspace/kbld9-r8-2026-10-18/core/kbld9_core_r8a.py
465359bb0339d3acdd1b94282a0d9191fb663b734cd2b552e36baf5e75da31d8  /workspace/kbld9/kbld9_core_r7.py
SUMS

# 1) core r8a (draft): THVEA v3 harness + sealed T1-T4 + r8 extra cases
cd /workspace/kbld9-r8-2026-10-18/core && \
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/workspace/kbld9-r8-2026-10-18/core:/workspace/kbld9 && \
python3 /workspace/kbld9-thvea-audit-2026-10-18/harness/probe_suite_3_thvea_v3.py kbld9_core_r8a /tmp/kbld9_probe3/r8a ; \
python3 /workspace/kbld9/probe_suite_3.py kbld9_core_r8a ; \
python3 /workspace/kbld9-r8-2026-10-18/tests/r8_extra_cases_v3.py kbld9_core_r8a /tmp/kbld9_probe3/r8a/extra_v3.json

# 2) fallback, core r7 (production line), same harness and sealed suite
cd /workspace/kbld9 && \
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/workspace/kbld9 && \
python3 /workspace/kbld9-thvea-audit-2026-10-18/harness/probe_suite_3_thvea_v3.py kbld9_core_r7 /tmp/kbld9_probe3/r7 ; \
python3 /workspace/kbld9/probe_suite_3.py kbld9_core_r7
```

## Expected today (measured 2026-10-18 ET, box only)
| Run | r8a | r7 |
|---|---|---|
| thvea-v3 harness | 14/16, FAIL H4a + H4b (16/210 inputs: the v3 float-division oracle vs exact membership, OPEN_GAPS R8-G1); exit 1 (gate BLOCKED by design) | 14/16, FAIL H4a (8/210) + H5 (ERROR on [1e308,-1e308,0.0]) |
| sealed T1-T4 `ce0e09…` | 4/4 | 4/4 |
| r8 extra cases v3 | 19/20, FAIL X12 (R8-G1b) | 2/20 |

Notes for the skill text (flags only, not edits):
- Use `PYTHONDONTWRITEBYTECODE=1`. Without it, Python writes `__pycache__` into `/workspace/kbld9` (this happened once today; see R8-G10).
- The sealed suite's default module is `kbld9_core_r4`. Always pass the module name explicitly.
- If Timothy adopts exact membership as the contract, the v3 oracle needs an exact-comparison revision. Until then, an H4a/H4b FAIL on r8a is the known contract conflict, not a regression.
- If r8a is rejected or the r8 folder is moved, run only step 2 (r7). The r8 lines and the r8a hash then come out of the gate.
