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
| 3C | naming a deterministic floor as a probability claim | architecture/naming | rename to "Shepherd 10 Sigma equivalent or better, with or without probabilities"; sigma becomes an optional tool, not the identity | open — retest: run Staff on unseen distribution, confirm floor holds without invoking probability | no |

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

## 2026-09-08 ~19:00 EDT — Row 3C written
**Identify:** the Staff's floor was named "10-Sigma," which reads as a probability claim (assumes a distribution, reports tail odds). That assumption is the crack — the floor must hold by construction, not by the odds of a Gaussian tail.
**Characterize:** original May 6 v2.0 package shipped as "10-SIGMA SHEPHERD'S STAFF"; MAD/10-sigma guard in kbl_svct_stacks.py is a real earned component but was carrying the identity. Cost: anyone reading the name assumes a statistical guarantee the system never claimed to deliver; the floor looks probabilistic when it is deterministic.
**Mitigation:** rename to **Shepherd 10 Sigma equivalent or better, with or without probabilities.** Sigma stays as an optional tool (the MAD guard, the sigma-free path: EV2, harmonic resonance, shell snap, data-driven anomaly mask). The name no longer implies a distribution.
**Retest:** run the Staff on a distribution it was never trained on. If the floor holds without invoking any probability, the rename is earned. If it silently falls back to a sigma assumption, remediate.
**Remediate:** if the retest fails, strengthen the deterministic path and retest. Repeat until no residual recurrence under the same conditions.
**Closed:** no — first retest pending.
