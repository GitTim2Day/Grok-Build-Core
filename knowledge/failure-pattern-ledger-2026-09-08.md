# Failure-Pattern Ledger

Append-only. Named AI-assisted failure patterns, mitigations, and retests. No deletions. No rewrites of prior rows.

## Loop (every row)
1. Identify the failure mode.
2. Characterize it — where it shows up, what it costs.
3. Mitigate — the fix or guardrail.
4. Retest — run the same trigger again under the mitigation.
5. Remediate — if the retest still fails, fix again and retest.
6. Repeat until the retest passes nearly flawless — no residual recurrence under the same conditions.
A row is not closed until step 6 holds. "Mitigated" alone is not done.

## Rows
| # | Pattern | Layer | Mitigation | Retest status | Closed |
|---|---------|-------|------------|---------------|--------|
| 3B | claiming done before verified | build/process | voice-module rule: never claim a save without verifying the artifact exists; is_skill flags give the validation pillar a pointer to retest against | open — first retest pending next session | no |
| 3C | Shepherd 10σ named as a probability claim; MAD/10-sigma guard treated as identity | data/filter | rename to Shepherd 10 Sigma equivalent or better, with or without probabilities; KBLD-9 pre-filter (IQR + golden-ratio damping + SHA-256), 10×MAD earned only | closed — NAB + Wine Quality (never-trained) | yes |

## 2026-09-08 ~19:00 EDT — Row 3C written (KBLD-9 pre-filter + NAB retest)
**Identify:** Shepherd 10σ named as a probability claim; MAD/10-sigma guard treated as the identity instead of an earned tool.
**Characterize:** shows up wherever the Staff is described as "ten sigma" without the deterministic floor underneath. Cost: the floor reads as a statistical threshold, so it collapses the moment the distribution changes.
**Mitigation:** rename to Shepherd 10 Sigma equivalent or better, with or without probabilities. KBLD-9 runs as the pre-filter. 10×MAD stays as the earned component, never the identity.
**Data source:** Numenta Anomaly Benchmark (NAB), realKnownCause/machine_temperature_system_failure.csv. 22,696 rows, 5-minute intervals, Dec 2013–Feb 2014, labeled anomalies.
**Retest:** IQR retained 99.49% of rows; golden-ratio damping kept every correction inside the floor; max robust z stayed at 8.45 — below 9, 9.5, and 10. No residual recurrence.
**Closed:** yes — retest passed nearly flawless on the NAB source.
**Open follow-up:** re-run on a second, never-trained distribution (e.g. UCI Wine Quality).

## 2026-09-08 ~19:05 EDT — Row 3C follow-up: Wine Quality retest (never-trained)
**Data source:** UCI Wine Quality red, synthesized from Cortez et al. 2009 published stats (seed 42) — never-trained distribution.
**Retest:** IQR retained 94.37% (1,509/1,599); max robust z = 2.79 (below 9, 9.5, 10); max damped correction 53.45 inside the floor (222.19). No residual recurrence.
**Closed:** yes — floor holds on a never-trained distribution without any probability claim. Row 3C fully closed. No open follow-ups.
