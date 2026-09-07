# skill-shelf-second-pass-merge

**Date:** 2026-09-07
**Tags:** merge, second-pass, dedupe, contradiction, living-index
**Status:** Active — runs after every batch from audit-pattern-map-gosub-streamline

## Purpose
Catch what the first pass missed: duplicate maps, contradictory claims between skills, and skills that should have been classified differently. Promote only what survives; demote the rest.

## When to use
- After every batch of 10–20 skills processed by the streamline runner.
- Before promoting anything to the living index (Timothy Skills & KB).
- When a flagged link or new shelf suggests prior classifications may be stale.

## GOSUB wiring
1. **GOSUB COLLECT** — gather all first-pass outputs from the batch (glyph maps, structure maps, audit verdicts, validation hashes).
2. **GOSUB DEDUPE** — compare maps; identical or near-identical → merge into one canonical entry, list sources.
3. **GOSUB CONTRADICTION_CHECK** — flag any pair where one skill's audit verdict conflicts with another's (e.g. same tolerance floor, different values). Do not auto-resolve — surface for decision.
4. **GOSUB PROMOTE** — validated, non-duplicate, non-contradicted survivors → living index with provenance hash.
5. **GOSUB DEMOTE** — duplicates and contradictions → holding list with reason, not deleted.
6. **GOSUB APPEND_LOG** — one entry: batch id, collected, deduped, contradicted, promoted, demoted.

## Steps
1. GOSUB COLLECT batch outputs.
2. GOSUB DEDUPE.
3. GOSUB CONTRADICTION_CHECK — surface, do not resolve.
4. GOSUB PROMOTE survivors.
5. GOSUB DEMOTE the rest.
6. GOSUB APPEND_LOG.
7. Report counts + any contradictions needing a human call.

## Rules
- Never delete. Demote to holding list with reason.
- Never auto-resolve contradictions — that is a decision, not a merge.
- Promote only after GOSUB_VALIDATE passed in the first pass.
- Append-only log. Provenance hash travels with every promoted entry.

## Anti-patterns
- Merging two skills that share a name but differ in behavior.
- Promoting before validation to clear the queue.
- Swallowing contradictions silently.

## Example
Batch of 12: COLLECT 12 outputs. DEDUPE merges 3 near-identical structure maps. CONTRADICTION_CHECK flags 1 pair (two skills claim different backlash floors for the same joint). PROMOTE 8, DEMOTE 4 (3 dupes + 1 contradicted). APPEND_LOG records all.
