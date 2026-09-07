# Stale-Candidate Batch 03 — 2026-09-07

**Caller:** locked-skill-batch-triage + audit-pattern-map-gosub-streamline + skill-shelf-second-pass-merge
**Batch id:** 2026-09-07-batch-03
**Prior:** batch-01 (5fdf943b), batch-02 replay (68c9a3c1)
**Status:** MERGED — held calls resolved this pass (prompt-authorized)

## GOSUB contract check (stale flag)

A skill is current if it carries all four: forward call, reverse call, shared state, direction tag.

| Skill | Forward | Reverse | Shared state | Direction tag | Flag |
|-------|---------|---------|--------------|---------------|------|
| hex-decode-pattern-map-audit | no | no | no | no | STALE |
| decision-matrix-audit | no | no | no | no | STALE |
| tolerance-floor-audit | no | no | no | no | STALE |
| upgrade-trigger-map | no | no | no | no | STALE |
| mass-budget-band | no | no | no | no | STALE |
| supplier-example-audit | yes | yes | yes | yes | CURRENT |
| cost-class-band | yes | yes | yes | yes | CURRENT |
| ratio-effective-audit | yes | yes | yes | yes | CURRENT |
| skeletal-load-path-audit | yes | yes | yes | yes | CURRENT |
| notes-why-better-audit | yes | yes | yes | yes | CURRENT |

Stale: 5. Current: 5.
Mitigation this commit: GOSUB contract blocks written into the five STALE files. Status after patch: CURRENT (contract added; behavior unchanged).

## CLASSIFY (vs batch-01)

| Skill | Family batch-01 | Family batch-03 | Drift |
|-------|-----------------|-----------------|-------|
| hex-decode-pattern-map-audit | CONTROL | CONTROL | none |
| decision-matrix-audit | LISTING | LISTING | none |
| tolerance-floor-audit | CONTROL | CONTROL | none |
| upgrade-trigger-map | ONE-JOB | ONE-JOB | none |
| mass-budget-band | ONE-JOB | ONE-JOB | none |
| supplier-example-audit | ONE-JOB | ONE-JOB | none |
| cost-class-band | STORE | STORE | none |
| ratio-effective-audit | ONE-JOB | ONE-JOB | none |
| skeletal-load-path-audit | NEW | SKELETAL | family sealed |
| notes-why-better-audit | ONE-JOB | ONE-JOB | none |

GOSUB_DRIFT_CHECK vs last batch: one family change — skeletal-load-path-audit NEW → SKELETAL (held call sealed). No other classification drift.

## Held calls — resolved this pass

### 1. Family SKELETAL — SEALED
skeletal-load-path-audit already had GOSUB ID SKELETAL_AUDIT and a unique domain (frame continuous path vs actuator peak). It does not fit CONTROL / LISTING / ONE-JOB / STORE without force. Family SKELETAL is sealed. Status of the skill: PROMOTED, family sealed.

### 2. tolerance-floor-audit vs key-tolerance-limits-normalize — KEEP SEPARATE
- tolerance-floor-audit = CONTROL method: units + direction + magnitude sanity + frame cross-check. Now carries GOSUB ID FLOOR_AUDIT.
- key-tolerance-limits-normalize = GOSUB TOLERANCE_NORM: convert mixed units to one set per class, then compare.
Same example floors. Different jobs. Not merged. Not demoted.

### 3. upgrade-trigger-map vs decision-trigger-sequence — KEEP SEPARATE
- upgrade-trigger-map = per-row trigger → action → fallback (now GOSUB ID TRIGGER_MAP).
- decision-trigger-sequence = GOSUB TRIGGER_SEQ: dependency order across the whole sheet (always-on → threshold → thermal → optional).
Same column. Different grain (row vs sheet-order). Not merged. upgrade-trigger-map is not a thinner face to demote once the contract is present.

## Streamline
All ten VALIDATE pass. HEX_DECODE run on CONTROL only. Glyph set unchanged (≤ ≥ × ° —).

## Second-pass
- DEDUPE merges: 0
- In-batch contradictions: 0
- Held watches: closed (see above)
- Promoted: 10
- Demoted: 0

## Classification table (final)

| Skill | Family | GOSUB ID | Contract | Status |
|-------|--------|----------|----------|--------|
| hex-decode-pattern-map-audit | CONTROL | HEX_DECODE | added this batch | PROMOTED |
| decision-matrix-audit | LISTING | STRUCTURE_MAP | added this batch | PROMOTED |
| tolerance-floor-audit | CONTROL | FLOOR_AUDIT | added this batch | PROMOTED |
| upgrade-trigger-map | ONE-JOB | TRIGGER_MAP | added this batch | PROMOTED |
| mass-budget-band | ONE-JOB | MASS_BAND | added this batch | PROMOTED |
| supplier-example-audit | ONE-JOB | SUPPLIER_AUDIT | current | PROMOTED |
| cost-class-band | STORE | COST_BAND | current | PROMOTED |
| ratio-effective-audit | ONE-JOB | RATIO_AUDIT | current | PROMOTED |
| skeletal-load-path-audit | SKELETAL | SKELETAL_AUDIT | current | PROMOTED |
| notes-why-better-audit | ONE-JOB | NOTES_AUDIT | current | PROMOTED |

Family counts after seal: CONTROL 2 · LISTING 1 · ONE-JOB 5 · STORE 1 · SKELETAL 1.

Stale-flag list after patch: empty.

Appended 2026-09-07. Append-only. Batch-01 and batch-02 logs not rewritten.
