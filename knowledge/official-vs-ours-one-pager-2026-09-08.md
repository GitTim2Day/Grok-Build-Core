# Official vs. Ours — One-Pager

**Date:** 2026-09-08  
**Status:** Draft for presentation. Not a claim of replacement.

## The official side (xAI / SpaceXAI)

Their June 30, 2026 Frontier AI Framework (FAIF) is model-behavior-first:

- **Identify** failure modes, **characterize** them, determine which present significant or unmitigated risk.
- Four domains: CBRN, Offensive Cyber, Loss of Control, Harmful Manipulation.
- Mitigations: safety training, system prompts, filters, tiered availability, red-teaming, post-market monitoring.
- Acceptance: qualitative "systemic risk acceptance determination" — risk tiers, safety margins, residual risk. No numeric deployment criteria remain (the December 2025 thresholds were removed in the rewrite).
- Loop ends at **mitigate + accept**. No mandatory retest-until-nearly-flawless step; re-evaluation happens at annual or trigger points.

Public safety page: https://x.ai/safety  
Framework PDF: media.x.ai (FAIF 30 June 2026)

## The ours side (SVCT / Shepherd's Staff)

Process-and-build-first, with the same vocabulary pointed at a different layer:

- **Identify → characterize → mitigate → retest → remediate**, repeat until nearly flawless. "Mitigated" alone does not close a row.
- **Do-no-harm root:** life first, everything else second. Non-negotiable floor above the logic.
- **Shepherd 10 Sigma equivalent or better** — deterministic floor, holds with or without probabilities. KBLD-9 pre-filter (IQR + golden-ratio damping + SHA-256), 10×MAD earned only. Proven on NAB + a never-trained distribution (Row 3C closed).
- **Bottleneck handler:** Socratic directing, second-mile carry, agree-quickly subroutine — surplus offered outward, not hoarded.
- **Five pillars**, validation as the fifth: unvalidated residents are refused.
- **Portable ledger:** every failure becomes a dated, retestable row — infra failures and model failures logged the same way.

## Where ours plugs in (the honest overlap)

| Layer | Official | Ours | Fit |
|-------|----------|------|-----|
| Model behavior (CBRN, cyber, loss of control) | Deep — refusal training, benchmarks, red-teaming | None claimed | They lead; we don't compete here |
| Process discipline | Identify → characterize → mitigate → accept | Identify → characterize → mitigate → **retest → remediate until nearly flawless** | Ours extends theirs — the missing close of the loop |
| Record-keeping | Documented assessments, annual cadence | Append-only dated ledger, every row retested | Ours is more granular and portable |
| Deterministic floors | Probability/severity estimation in acceptance | Shepherd 10σ equivalent, no probability invoked | Ours is the stronger claim on this specific point |
| Bottleneck behavior | Not addressed as a subroutine | Socratic + second-mile + agree-quickly | Ours adds a human-scale operating rule |

## The one sentence

**Their framework finds the failure; ours makes sure it doesn't come back — and records the proof.**

## What this is not

- Not a substitute for their model-side coverage.
- Not a claim that our process is complete — the ledger has two closed rows; theirs has years of evaluations.
- It is the portable, retestable layer that turns "mitigated" into "nearly flawless," with a floor that doesn't lean on probability.

## Provenance

Compiled from: xAI FAIF (30 June 2026), x.ai/safety, the do-no-harm root, the failure-pattern ledger (Rows 3B, 3C), the KBLD-9 spec, and the bottleneck-handler skill. All artifacts sealed in this repo under `knowledge/`.
