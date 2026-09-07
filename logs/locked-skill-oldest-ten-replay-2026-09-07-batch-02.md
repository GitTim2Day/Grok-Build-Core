# Locked-Skill Oldest-Ten Replay — Batch 02 (2026-09-07)

**Skill:** locked-skill-batch-triage + audit-pattern-map-gosub-streamline + skill-shelf-second-pass-merge
**Batch size:** 10
**Selection rule:** oldest-by-commit in Grok-Build-Core/skills/
**Status:** REPLAY — membership identical to batch-01; classification unchanged

## Honest overlap
These ten are the same files already processed in batch-01 (commits 90a19207 + 5fdf943b). This pass does not invent a new shelf. It re-runs CLASSIFY / ASSIGN_PATH / QUEUE / STREAMLINE / SECOND_PASS against the *requested intake order* and checks for drift.

Blob SHAs unchanged from batch-01. Prior logs not rewritten.

## Intake order (commit time, oldest first)

| # | Skill | First commit |
|---|-------|--------------|
| 1 | hex-decode-pattern-map-audit | 90b40a3b 19:41Z |
| 2 | decision-matrix-audit | ce5fc2cf 19:45Z |
| 3 | tolerance-floor-audit | 2d7b199b 19:45Z |
| 4 | upgrade-trigger-map | da7594dd 19:45Z |
| 5 | mass-budget-band | 81d780ce 19:45Z |
| 6 | supplier-example-audit | ad85eff5 19:47Z |
| 7 | cost-class-band | ad85eff5 19:47Z |
| 8 | ratio-effective-audit | ad85eff5 19:47Z |
| 9 | skeletal-load-path-audit | ad85eff5 19:47Z |
| 10 | notes-why-better-audit | ad85eff5 19:47Z |

## GOSUB CLASSIFY (no drift vs batch-01)

| Skill | Family |
|-------|--------|
| hex-decode-pattern-map-audit | CONTROL |
| decision-matrix-audit | LISTING |
| tolerance-floor-audit | CONTROL |
| upgrade-trigger-map | ONE-JOB |
| mass-budget-band | ONE-JOB |
| supplier-example-audit | ONE-JOB |
| cost-class-band | STORE |
| ratio-effective-audit | ONE-JOB |
| skeletal-load-path-audit | NEW (SKELETAL OPEN) |
| notes-why-better-audit | ONE-JOB |

Counts: CONTROL 2 · LISTING 1 · ONE-JOB 5 · STORE 1 · NEW 1.

## GOSUB ASSIGN_PATH (unchanged)

- CONTROL → HEX_DECODE → STRUCTURE_MAP → DOMAIN_AUDIT → VALIDATE → APPEND
- LISTING → STRUCTURE_MAP → DOMAIN_AUDIT → VALIDATE → APPEND (skip HEX_DECODE)
- ONE-JOB → STRUCTURE_MAP → DOMAIN_AUDIT → member audit → VALIDATE → APPEND
- STORE → STRUCTURE_MAP → DOMAIN_AUDIT → COST_BAND → VALIDATE → APPEND
- NEW → STRUCTURE_MAP → DOMAIN_AUDIT → SKELETAL_AUDIT → VALIDATE → APPEND

## Two queues (do not collapse)

Intake order is history. Priority queue is process.

**Intake (this prompt):** hex-decode → decision-matrix → tolerance-floor → upgrade-trigger → mass-budget → supplier → cost-class → ratio → skeletal → notes

**Priority (batch-01, still standing):** hex-decode → decision-matrix → tolerance-floor → skeletal → ratio → supplier → cost-class → notes → upgrade-trigger → mass-budget

Difference: upgrade-trigger and mass-budget sit earlier in intake (they landed early) and later in priority (they are ONE-JOB, not anchors). Skeletal sits later in intake and earlier in priority (NEW load-path anchor).

## Streamline (replay)

All ten: VALIDATE pass. HEX_DECODE run only on CONTROL (hex-decode, tolerance-floor). Glyph set still ≤ ≥ × ° —. No new glyphs. No failed bounds.

## Second-pass (replay)

- DEDUPE merges: 0 (same as batch-01)
- In-batch contradictions: 0
- Watches carried (not resolved):
  1. tolerance-floor-audit vs key-tolerance-limits-normalize (out of batch)
  2. upgrade-trigger-map vs decision-trigger-sequence (out of batch)
  3. Family SKELETAL OPEN — human seal required
- Promoted: 10
- Demoted: 0
- Classification drift vs batch-01: none

## Classification table (final)

| Skill | Family | GOSUB path | Intake # | Priority # | Status |
|-------|--------|------------|----------|------------|--------|
| hex-decode-pattern-map-audit | CONTROL | HEX_DECODE → STRUCTURE_MAP → DOMAIN_AUDIT → VALIDATE → APPEND | 1 | 1 | PROMOTED |
| decision-matrix-audit | LISTING | STRUCTURE_MAP → DOMAIN_AUDIT → VALIDATE → APPEND | 2 | 2 | PROMOTED |
| tolerance-floor-audit | CONTROL | HEX_DECODE → STRUCTURE_MAP → DOMAIN_AUDIT → VALIDATE → APPEND | 3 | 3 | PROMOTED |
| upgrade-trigger-map | ONE-JOB | STRUCTURE_MAP → DOMAIN_AUDIT → TRIGGER_SEQ → VALIDATE → APPEND | 4 | 9 | PROMOTED |
| mass-budget-band | ONE-JOB | STRUCTURE_MAP → DOMAIN_AUDIT → VALIDATE → APPEND | 5 | 10 | PROMOTED |
| supplier-example-audit | ONE-JOB | STRUCTURE_MAP → DOMAIN_AUDIT → SUPPLIER_AUDIT → VALIDATE → APPEND | 6 | 6 | PROMOTED |
| cost-class-band | STORE | STRUCTURE_MAP → DOMAIN_AUDIT → COST_BAND → VALIDATE → APPEND | 7 | 7 | PROMOTED |
| ratio-effective-audit | ONE-JOB | STRUCTURE_MAP → DOMAIN_AUDIT → RATIO_AUDIT → VALIDATE → APPEND | 8 | 5 | PROMOTED |
| skeletal-load-path-audit | NEW | STRUCTURE_MAP → DOMAIN_AUDIT → SKELETAL_AUDIT → VALIDATE → APPEND | 9 | 4 | PROMOTED (family OPEN) |
| notes-why-better-audit | ONE-JOB | STRUCTURE_MAP → DOMAIN_AUDIT → NOTES_AUDIT → VALIDATE → APPEND | 10 | 8 | PROMOTED |

## What this replay earned
Not ten new skills. One check: oldest-first intake does not change family or VALIDATE. It only reorders the queue. Process queue stays the batch-01 priority list.

Next distinct batch is the nine skills still in /skills that were not in this ten (callers + remaining members), then the off-repo locked shelf after NDA.

Appended 2026-09-07. Append-only. No rewrite of batch-01 logs.
