# Locked-Skill Batch Triage — Batch 01 (2026-09-07)

**Skill:** locked-skill-batch-triage  
**Batch size:** 10  
**Source shelf:** Grok-Build-Core/skills/ (19 files present; 10 selected for first pass)  
**Status:** TRIAGED — ready for audit-pattern-map-gosub-streamline  

## Intake (names + one-line descriptions)

| # | Skill | One-line description |
|---|-------|----------------------|
| 1 | hex-decode-pattern-map-audit | Decode non-ASCII / multi-byte / escaped bytes to glyphs; list hex → glyph map. |
| 2 | decision-matrix-audit | Identify artifact type and column/field roles independent of symbols. |
| 3 | tolerance-floor-audit | Connect decoded symbols + structure to field; flag targets vs floors. |
| 4 | upgrade-trigger-map | Map decision triggers for upgrade; sequence by dependency. |
| 5 | mass-budget-band | Estimate mass contribution bands per joint/section. |
| 6 | supplier-example-audit | Audit supplier examples for class-fit, custom flags, commitment boundary. |
| 7 | cost-class-band | Distribute cost classes; flag inversions and exclusions. |
| 8 | ratio-effective-audit | Split gearbox vs effective ratios; cross-check torque. |
| 9 | skeletal-load-path-audit | List load paths; check multiplier sanity vs actuator-vs-frame. |
| 10 | notes-why-better-audit | Split engineering vs marketing rationale; connect to triggers. |

## GOSUB CLASSIFY

| Family | Count | Members |
|--------|-------|---------|
| CONTROL | 2 | hex-decode-pattern-map-audit, tolerance-floor-audit |
| LISTING | 1 | decision-matrix-audit |
| ONE-JOB | 5 | upgrade-trigger-map, mass-budget-band, supplier-example-audit, ratio-effective-audit, notes-why-better-audit |
| STORE | 1 | cost-class-band |
| NEW | 1 | skeletal-load-path-audit (load-path family; propose SKELETAL) |

## GOSUB ASSIGN_PATH

- CONTROL → HEX_DECODE → STRUCTURE_MAP → DOMAIN_AUDIT → GOSUB_VALIDATE → APPEND_LOG
- LISTING → STRUCTURE_MAP → DOMAIN_AUDIT → GOSUB_VALIDATE → APPEND_LOG (skip HEX_DECODE if plain text)
- ONE-JOB → STRUCTURE_MAP → DOMAIN_AUDIT → member audit → GOSUB_VALIDATE → APPEND_LOG
- STORE → STRUCTURE_MAP → DOMAIN_AUDIT → GOSUB_VALIDATE → APPEND_LOG
- NEW (SKELETAL) → STRUCTURE_MAP → DOMAIN_AUDIT → SKELETAL_AUDIT → GOSUB_VALIDATE → APPEND_LOG

## GOSUB QUEUE (priority order)

1. hex-decode-pattern-map-audit (CONTROL, flagged link — this session's origin)
2. decision-matrix-audit (LISTING, structure anchor)
3. tolerance-floor-audit (CONTROL, tolerance anchor)
4. skeletal-load-path-audit (NEW, load-path anchor)
5. ratio-effective-audit (ONE-JOB, torque cross-check)
6. supplier-example-audit (ONE-JOB, supplier fit)
7. cost-class-band (STORE, cost distribution)
8. notes-why-better-audit (ONE-JOB, rationale split)
9. upgrade-trigger-map (ONE-JOB, trigger sequence)
10. mass-budget-band (ONE-JOB, mass band)

## Hand-off

Queue handed to **audit-pattern-map-gosub-streamline** in one batch of 10.  
After processing, run **skill-shelf-second-pass-merge**.

## Second-pass (pending)

- DEDUPE: none expected — distinct behaviors.
- CONTRADICTION_CHECK: watch tolerance-floor-audit vs key-tolerance-limits-normalize (not in this batch) for floor-value drift.
- PROMOTE: survivors with GOSUB_VALIDATE pass.
- DEMOTE: duplicates/contradictions to holding list with reason.

## Report

- Families: 2 CONTROL, 1 LISTING, 5 ONE-JOB, 1 STORE, 1 NEW.
- Queue: 10 ordered, flagged-link first.
- Second-pass: pending streamline run.
- Status: TRIAGED — pipeline verified end-to-end on a 10-item sample.

Appended 2026-09-07. Append-only. No rewrites.
