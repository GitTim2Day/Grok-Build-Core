# skill-shelf-second-pass-merge

**Date:** 2026-09-07
**Tags:** merge, second-pass, dedupe, contradiction, living-index, drift
**Status:** Active — runs after every batch from audit-pattern-map-gosub-streamline
**Rev:** batch-03 — GOSUB_DRIFT_CHECK added

## Purpose
Catch what the first pass missed: duplicate maps, contradictory claims between skills, classification drift vs the last batch, and skills that should have been classified differently. Promote only what survives; demote the rest.

## When to use
- After every batch of 10–20 skills processed by the streamline runner.
- Before promoting anything to the living index (Timothy Skills & KB).
- When a flagged link or new shelf suggests prior classifications may be stale.

## GOSUB wiring
1. **GOSUB COLLECT** — gather all first-pass outputs from the batch (glyph maps, structure maps, audit verdicts, validation hashes).
2. **GOSUB DEDUPE** — compare maps; identical or near-identical → merge into one canonical entry, list sources.
3. **GOSUB CONTRADICTION_CHECK** — flag any pair where one skill's audit verdict conflicts with another's. Do not auto-resolve — surface for decision unless the current prompt names the pair and authorizes a resolve.
4. **GOSUB DRIFT_CHECK** — one line per skill: Family_this vs Family_last. Flag any change. No change → `none`.
5. **GOSUB PROMOTE** — validated, non-duplicate, non-contradicted survivors → living index with provenance hash.
6. **GOSUB DEMOTE** — duplicates and contradictions → holding list with reason, not deleted.
7. **GOSUB APPEND_LOG** — one entry: batch id, collected, deduped, contradicted, drifted, promoted, demoted.

## Steps
1. GOSUB COLLECT batch outputs.
2. GOSUB DEDUPE.
3. GOSUB CONTRADICTION_CHECK — surface, do not resolve unless authorized.
4. GOSUB DRIFT_CHECK — compare classification table to last batch.
5. GOSUB PROMOTE survivors.
6. GOSUB DEMOTE the rest.
7. GOSUB APPEND_LOG.
8. Report counts + drift line + any contradictions needing a human call.

## Rules
- Never delete. Demote to holding list with reason.
- Never auto-resolve contradictions — that is a decision, not a merge.
- Drift is a flag, not a rewrite. Record it.
- Promote only after GOSUB_VALIDATE passed in the first pass.
- Append-only log. Provenance hash travels with every promoted entry.

## Anti-patterns
- Merging two skills that share a name but differ in behavior.
- Promoting before validation to clear the queue.
- Swallowing contradictions or drift silently.

## Example
Batch of 12: COLLECT 12. DEDUPE merges 3. CONTRADICTION_CHECK flags 1 pair. DRIFT_CHECK: 1 family change (NEW → SKELETAL), 11 none. PROMOTE 8, DEMOTE 4. APPEND_LOG records all.
