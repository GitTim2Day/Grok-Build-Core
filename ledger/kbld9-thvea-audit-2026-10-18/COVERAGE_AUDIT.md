# COVERAGE_AUDIT — KBLD9 Probe suite 3 vs the THVEA rule (2026-10-18)

Rule source: `/home/box/agent-data/workflows/think-harden-verify-earn-answer-validate/SKILL.md`.
Suite audited (as found, read-only):

| File | Bytes | SHA-256 | Note |
|---|---:|---|---|
| `/workspace/kbld9/probe_suite_3.py` | 3257 | `ce0e09f329599dfa511cb036aa9f0c2bbb39d0d84deb46e43c34eb31f4d0096d` | = sealed `kbld9-handoff/probes/probe_suite_t1_t4.py` (CORE_LOCK 2026-09-18) |
| `/workspace/loaded/kbld9/probe_suite_3.py` | 3077 | `e1484a831846cff5015d7b0ede1e2f098afa75556591a154cf9b9d9321f805f5` | = `/workspace/kbld9/probe_suite_3_CORRUPT_backup.py`; PDF extraction, T2 line truncated |
| `/workspace/kbld9/kbld9_core_r7.py` | 26682 | `465359bb0339d3acdd1b94282a0d9191fb663b734cd2b552e36baf5e75da31d8` | production line `9.0.7-core` (sealed) |
| `/workspace/kbld9/kbld9_core_r4.py` | 15924 | `e111d03da65ad0bcc164a29d884ba6d8b0f9640ddaf9e39debebca2f37646239` | `9.0.4-core`, comparative baseline; see flag C15 |

`/workspace/kbld9/protected/` was NOT opened.

## Validation demand per THVEA step

| Step | Demand used for this audit |
|---|---|
| Think | explicit inputs and explicit expected outputs for every case |
| Harden | edge cases, negative tests, and one alternative (independent) check |
| Verify | the assertions actually run (counted, not vacuous) |
| Earn | a fail-closed gate that blocks output on failure |
| Answer | a defined output format |
| Validate | final output-vs-expected cross-check plus a hash |

## Flags (places the sealed suite is thinner than the rule requires)

| ID | Step | Severity | Finding (measured / read from file) |
|---|---|---|---|
| C1 | Think | THIN | No case declares an expected output. T1 and T4 are thresholds only (`<= 9.0 + 1e-9`, `< 300 ms`); T2's "expected" is the module's own `_snap`/`_classify`; inputs exist only as seeds inside code. |
| C2 | Think | THIN | The skill text describes T1 with 6 bin widths and T2 with 30 trials (= the PDF text). The sealed on-disk suite runs 9 bin widths x 3 tiers (T1) and 40 trials x 7 bin widths (T2). Record and code have drifted apart. |
| C3 | Harden | MISSING | No negative tests: NaN, inf, bool, str, None, non-list input, bad `bin_width` / `precision` are never exercised. Mutants M08, M09, M15 survived. |
| C4 | Harden | THIN | Edge cases only in T3 (mad==0). No empty stream, single point, exact 9-sigma boundary, extreme magnitude, denormals. Mutant M01 (fence widened to 9.5 in the fused path) survived. |
| C5 | Harden | THIN | The alternative check is not independent. T1 uses the module's own reported `median`/`mad_scaled`; T2's reference functions live inside the module under test. Shared-bug mutants survived: M05 (MAD constant), M06 (shared quantize), M11 (tier ignored), M16 (truncate replaced by round). |
| C6 | Harden | MISSING | No fault injection. The read-back gate, the `_guard` airlock, and stats transactionality are untested. M14 (read-back gate disabled) survived. |
| C7 | Harden | MISSING | Provenance is never checked (input/output SHA-256, chain, spine). M10 survived. |
| C8 | Verify | THIN | Assertions are not counted. T1's `if mad:` silently skips every zero-MAD configuration, so a vacuous T1 PASS is possible. |
| C9 | Verify | THIN | A crash aborts the whole suite with no per-case record. Measured: r4 -> `AttributeError: TIER_DAILY` before any check; skill command -> `SyntaxError` line 59. |
| C10 | Verify | NOTE | T4 is wall-clock on this box only. The handoff README says the Pi 5 timing is the measurement that matters; there is none here. |
| C11 | Earn | THIN | There is a gate (exit code = number of failures), but PASS lines print before the run ends and no blocked/earned artifact exists. A crash gives exit 1, not a per-case failure. |
| C12 | Earn | THIN | The skill's run command (`cd /workspace/loaded/kbld9 && python3 probe_suite_3.py kbld9_core_r4`) points at the truncated copy (cannot compile), and that directory has no core module. The gate is closed but tells you nothing. |
| C13 | Answer | THIN | Free-text output only, nothing machine-readable. T1 detail prints sigma with `:.4f` and T4 prints `:.1f`. Both ROUND, which breaks the truncate-never-round standing. |
| C14 | Validate | MISSING | No final cross-check of output against expected, and no hash of the results. |
| C15 | Provenance | OPEN | On-disk `kbld9_core_r4.py` (15924 B, `e111d03d…`) does not match the r4 seal recorded in COMPARATIVE_R4_vs_R7 (16314 B, `a608a393…`, 391 lines). LF->CRLF conversion gives 16315 B / `369c0b68…`, also no match. Not resolved. |
| C16 | Record | STALE | The skills say "kbld9_core_r4 is missing on this computer". It is present in `/workspace/kbld9/` and `/workspace/kbld9-handoff/`. |
| C17 | Record | CONFLICT | The skill's default import is r4, but the sealed suite `ce0e09…` needs r7 tier constants. Default skill run + sealed suite = crash. |

Totals: MISSING 4 (C3, C6, C7, C14) · THIN 9 (C1, C2, C4, C5, C8, C9, C11, C12, C13) · NOTE 1 (C10) · OPEN 1 (C15) · STALE 1 (C16) · CONFLICT 1 (C17) = 17 flags.

## Mitigation map (harness thvea-v3, new file `harness/probe_suite_3_thvea_v3.py`)

| Flag | Mitigation in v3 |
|---|---|
| C1 | every case carries `inputs` and `expected` in the results JSON |
| C3 | N1 (7 bad element types + 2 non-list inputs, error must name the element, stats and spine untouched), N2 (9 bad configurations -> ValueError) |
| C4 | H1 (8.999/9.001/9.2/9.49 sigma), H2 (empty, single, equal, -0.0, denormal), H3 (extreme magnitude), H4a/H4b (ULP boundary at 3/6/9 sigma, 210 inputs), H5 (valid near-max input) |
| C5 | independent oracle: its own median, MAD (1.4826), sigma, quantize, Decimal ROUND_DOWN truncate and SHA-256. It never calls module helpers. |
| C6 | F1 (read-back corruption), F2 (internal exception), F3 (tier places) |
| C7 | output/input SHA checked in every compare(); P1 checks chain, seed and spine |
| C8 | assertion counter with a declared minimum per case; below the minimum = FAIL "VACUOUS" |
| C9 | per-case isolation: a crash fails that case only; import failure = every case BLOCKED |
| C11 | `results_EARNED.json` only when every case passes, otherwise `results_BLOCKED.json` plus a nonzero exit |
| C13 | fixed line format + JSON; all printed numbers truncated (Decimal ROUND_DOWN) |
| C14 | results read back, re-hashed, and checked against the case manifest (ids unique and complete, counts consistent) |
| C2, C10, C12, C15, C16, C17 | not fixable in harness code; recorded in OPEN_GAPS.md |
