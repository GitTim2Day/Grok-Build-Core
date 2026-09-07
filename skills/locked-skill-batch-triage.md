# locked-skill-batch-triage

**Date:** 2026-09-07
**Tags:** triage, locked-skills, batch, gosub, process
**Status:** Active — feeds audit-pattern-map-gosub-streamline

## Purpose
Sort the remaining 200–300 locked skills into families so the streamline runner can process them in batches instead of individually. Classify, assign a GOSUB path, queue, then second-pass merge.

## When to use
- Starting a pass over the locked-skill backlog.
- A new shelf of skills arrives (Drive zip, Gmail, Notion import).
- After a batch run, to re-triage anything the second pass flagged.

## GOSUB wiring
1. **GOSUB CLASSIFY** — read each skill's name, description, tags; assign one family:
   - CONTROL — gates, locks, direction, validation
   - LISTING — catalogs, inventories, indexes
   - ONE-JOB — single-purpose tools (measure, clock, call, navigate)
   - STORE — rummage, compact, archive, retrieve
   - NEW — does not fit; propose a family, do not force it
2. **GOSUB ASSIGN_PATH** — map family → GOSUB sequence from audit-pattern-map-gosub-streamline (some families skip HEX_DECODE if plain text).
3. **GOSUB QUEUE** — append to the batch queue with priority (flagged links first, then by family size).
4. **GOSUB SECOND_PASS** — after 10–20 processed, merge: dedupe maps, flag contradictions, promote survivors, demote duplicates to a holding list.

## Steps
1. Intake the shelf (list names + one-line descriptions).
2. GOSUB CLASSIFY per item.
3. GOSUB ASSIGN_PATH per family.
4. GOSUB QUEUE — ordered list.
5. Hand queue to audit-pattern-map-gosub-streamline in batches of 10–20.
6. GOSUB SECOND_PASS after each batch.
7. Report: families, counts, queue order, second-pass findings.

## Rules
- Classify by behavior, not by name alone.
- Do not invent a family to force a fit — NEW is a valid answer.
- Second-pass is mandatory; skipping it is how duplicates and contradictions accumulate.
- Append-only queue. No reordering of sealed entries.

## Anti-patterns
- Triage by filename pattern instead of actual behavior.
- Skipping second-pass to move faster.
- Promoting a skill to the living index before GOSUB_VALIDATE passes.

## Example
Shelf: 15 locked skills from a Drive zip. CLASSIFY → 4 CONTROL, 3 LISTING, 5 ONE-JOB, 2 STORE, 1 NEW. ASSIGN_PATH → CONTROL skips HEX_DECODE. QUEUE ordered by flagged-link priority. Hand to streamline runner in two batches; SECOND_PASS merges 2 near-duplicates.
