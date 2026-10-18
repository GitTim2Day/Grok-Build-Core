# kbld9-thvea-audit-2026-10-18

KBLD9 Probe suite 3 audited against Timothy H. Norman's Think-Harden-Verify-Earn-Answer-Validate (THVEA) rule. Sitting: Sun 2026-10-18, about 11:47-12:10 ET. Box only. No spend, no cloud agents, no service restarts. No existing or sealed file was edited. `/workspace/kbld9/protected/` was not opened. BOOT.bas and svct_v20* were not touched.

## Headline (measured)
- **Initial run (as found):** sealed T1-T4 (`ce0e09…`) vs r7: **4/4 PASS**. Same suite vs the skill-default r4: **0/4 ran** (AttributeError TIER_DAILY). Skill run command (truncated copy `e1484a83…`): **0/4 ran** (SyntaxError line 59).
- **Coverage audit:** 17 flags (4 MISSING, 9 THIN, 1 NOTE, 1 OPEN, 1 STALE, 1 CONFLICT). See COVERAGE_AUDIT.md.
- **Loop:** 5 rounds, 3 mitigations (harness thvea-v1 -> v2 -> v3). Mutants killed: 6/16 (sealed suite) -> 16/16 (v1) -> 18/22 (v2) -> **22/22 (v3)**.
- **Final:** v3 vs r7 **14/16 PASS** (FAIL H4a, H5; EARNED=False, gate blocked). v3 vs r4 15/16 (FAIL H4a). Missing module: all BLOCKED. Sealed suite vs r7 is still 4/4.
- **Open (needs Timothy):** G1 fused != reference at exact 3/6/9-sigma ULP boundaries (8/210, r4 and r7); G2 r7 returns ERROR on valid `[1e308,-1e308,0.0]` (r4 returns OK); plus G3-G10. See OPEN_GAPS.md.

## Files
| Path | What |
|---|---|
| COVERAGE_AUDIT.md | THVEA demand per step, 17 flags, mitigation map |
| ROUNDS.md | each round, each mitigation, what it fixed |
| FINAL_STATE.md | final pass/fail, mutant progression, untouched-file check |
| OPEN_GAPS.md | G1-G10 |
| harness/probe_suite_3_thvea_v3.py | current THVEA harness (new file) |
| harness/make_v3_from_v2.py | derivation script v2 -> v3 |
| harness/run_mutants_v3.py | case-level mutation runner |
| mutants/make_mutants_v1.py, make_mutants_v2.py, MUTANTS_MANIFEST_v*.json | mutant generators and manifests |
| mutants/kbld9_mut_m01..m22.py | mutants (copies of the protected core; LOCAL ONLY) |
| results/v3/, results/v3_stability/ | per-module results JSON (EARNED/BLOCKED) |
| archive/thvea-v1/, archive/thvea-v2/, archive/runners/ | superseded harnesses and runners, with their results |
| logs/ | every run log (R0a-R5) + env.txt |
| SHA256SUMS | sha256 of every file above (`sha256sum -c SHA256SUMS`) |

## Reproduce
```
cd /workspace/kbld9-thvea-audit-2026-10-18/mutants
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/workspace/kbld9 python3 ../harness/probe_suite_3_thvea_v3.py kbld9_core_r7 /tmp/out
python3 ../harness/run_mutants_v3.py $PWD/../harness/probe_suite_3_thvea_v3.py /tmp/out /tmp/mut.log
```

## Shelf policy
GitHub `GitTim2Day/Grok-Build-Core` is PUBLIC. Only the markdown, logs, results JSON, mutant manifests and SHA256SUMS go there. No `.py` files go there (the mutants are copies of the protected core; the harness oracle re-implements core contract logic). The Drive copy is one combined markdown file plus SHA256SUMS. Email: summary only, no attachments.
