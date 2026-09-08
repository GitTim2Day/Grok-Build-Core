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
| 3B | claiming done before verified | build/process | voice-module rule: never claim a save without verifying the artifact exists; is_skill flags give the validation pillar a pointer to retest against | open — first retest pending next session | no |

## Seeded angles (not yet rows)
- Infra reliability: backup cooling/power gaps, uptime below target.
- Model behavior: CBRN, offensive cyber, loss of control, harmful manipulation.
- Safety-practice gap vs peers: image floods, spontaneous tirades → regression tests.
- Build/process: claiming done before verified, wrong parent nesting, skipped write-scope check.

Cross-cutting rule: if a system can harm life, it does not ship until mitigated and retested to near-flawless.

## 2026-09-08 ~18:33 EDT — mechanism note (not a closed row)
Batch A item (5) executed: five dated maps flagged is_skill = true. This is the portable pointer the validation pillar needs — a map marked is_skill is a claim, and the retest is whether a new person following it stalls. Row 3B (claiming done before verified) will cite this mechanism when written. Do not close 3B on this note alone.

## 2026-09-08 ~18:36 EDT — Row 3B written (first real row)
**Identify:** claiming a save, write, or flag succeeded before the artifact is verified to exist at the expected location.
**Characterize:** shows up in Stripe identity (passkey/camera treated as verified), Notion (page under wrong parent called done), GitHub (commit claimed without confirming on main), is_skill flags (flag set without checking the page carries a method). Cost: false confidence, wasted sessions, cracked shelf for new people.
**Mitigation:** voice-module-map-match-audit-pattern-map rule — never claim a save without verifying the artifact exists. is_skill flags only on dated maps with a real method, completion check, and GitHub sibling.
**Retest:** next session, run the same trigger (claim a save) under the mitigation and confirm the artifact check happens before the claim. Record result here. Do not close until the retest passes nearly flawless.
**Remediate:** if the retest fails, strengthen the guardrail and retest. Repeat until no residual recurrence under the same conditions.
**Closed:** no — first retest pending.
