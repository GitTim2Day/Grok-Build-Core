# Failure-Pattern Ledger

Append-only. Named AI-assisted failure patterns, mitigations, and retests. No deletions. No rewrites of prior rows.

## Loop (every row)
1. **Identify** the failure mode.
2. **Characterize** it — where it shows up, what it costs.
3. **Mitigate** — the fix or guardrail.
4. **Retest** — run the same trigger again under the mitigation.
5. **Remediate** — if the retest still fails, fix again and retest.
6. Repeat until the retest passes **nearly flawless** — no residual recurrence under the same conditions.

A row is not closed until step 6 holds. "Mitigated" alone is not done.

## Rows

| # | Pattern | Layer | Mitigation | Retest status | Closed |
|---|---------|-------|------------|---------------|--------|
| 3B | *(seeded 2026-09-08 — first row pending)* | — | — | open | no |

## Seeded angles (not yet rows)
- Infra reliability: backup cooling/power gaps, uptime below target.
- Model behavior: CBRN, offensive cyber, loss of control, harmful manipulation.
- Safety-practice gap vs peers: image floods, spontaneous tirades → regression tests.
- Build/process: claiming done before verified, wrong parent nesting, skipped write-scope check.

Cross-cutting rule: if a system can harm life, it does not ship until mitigated and retested to near-flawless.
