# audit-pattern-map-gosub-streamline

**Date:** 2026-09-07
**Tags:** audit, pattern-map, gosub, streamline, process, locked-skills
**Status:** Active — streamlined for batch runs

## Purpose
Run the full audit + pattern-map pass as a GOSUB-driven subroutine so the remaining 200–300 locked skills can be processed in batches instead of one-by-one. One entry point, one exit, append-only log.

## When to use
- A new file or skill shelf lands and needs decode → map → audit before interpretation.
- The locked-skill backlog needs a pass (200–300 items).
- You want the same method every time, not a fresh improvisation.

## GOSUB wiring (subroutines)
This skill is the caller. It dispatches these sealed GOSUBs in order:

1. **GOSUB HEX_DECODE** — extract non-ASCII / multi-byte / escaped bytes, decode to glyphs, list hex → glyph map. (Source: hex-decode-pattern-map-audit)
2. **GOSUB STRUCTURE_MAP** — identify what the artifact is (matrix, spec, archive, skill) and what each column/field does, independent of symbols. (Source: decision-matrix-audit)
3. **GOSUB DOMAIN_AUDIT** — connect decoded symbols + structure to the likely field; state what it is and is not; flag targets vs floors. (Source: decision-matrix-audit + tolerance-floor-audit)
4. **GOSUB GOSUB_VALIDATE** — run the result through kbld-gosub-primitives: bounds check, provenance hash, append-and-verify, accuracy floor. No zero stored; direction is a tag.
5. **GOSUB APPEND_LOG** — write one append-only entry: timestamp, artifact, decoded bytes, structure map, audit verdict, GOSUB validation hash. Never overwrite.

## Steps (caller)
1. Receive artifact + any domain hint.
2. GOSUB HEX_DECODE → return glyph map.
3. GOSUB STRUCTURE_MAP → return column/field roles.
4. GOSUB DOMAIN_AUDIT → return is/is-not + target-vs-floor split.
5. GOSUB GOSUB_VALIDATE → return pass/fail + hash.
6. GOSUB APPEND_LOG → one line, append-only.
7. Report the three layers (decoded, mapped, audited) + validation hash. Stop or offer next batch.

## Batch mode (for 200–300 locked skills)
- Run steps 1–6 per skill, one at a time, logging each.
- Group by tag family (CONTROL, LISTING, ONE-JOB, STORE, etc.) so related skills share a structure map.
- After each batch of 10–20, run a second-pass pattern-match across the batch: merge duplicate maps, flag contradictions, promote survivors to the living index.
- DO UNTIL backlog empty or a stop condition (e.g. 50 processed, or a flagged link arrives).

## Rules
- Decode before interpret. Never guess glyphs from context when bytes are available.
- The user's sequencing of reveals is part of the method — do not collapse it.
- GOSUB_VALIDATE must pass before anything is promoted to the living index.
- Append-only. No stored negatives. Direction is a tag, not a payload.
- Keep each skill self-contained: another assistant can run this without the original chat.

## Anti-patterns
- Answering content before decoding bytes.
- Treating hex work as busywork.
- Skipping GOSUB_VALIDATE to save time — that is exactly when drift enters.
- Rewriting prior log entries instead of appending.
- Running batch mode without the second-pass merge — duplicates and contradictions accumulate.

## Example (this session)
Artifact: Book (1) copy.xlsx / 96f171…xlsx (10,574 bytes), Optimus joint-architecture decision matrix.
HEX_DECODE → five UTF-8 sequences: ≤, ≥, ×, °, —.
STRUCTURE_MAP → 11 sections × 13 columns (current / recommended / alternative / ratio / torque / tolerances / skeletal / trigger / notes / mass / cost / suppliers).
DOMAIN_AUDIT → humanoid joint architecture, 70 kg class; symbols are tolerance and load-path floors; sheet is a decision table, not a BOM.
GOSUB_VALIDATE → pass (bounds, provenance, append-and-verify).
APPEND_LOG → one entry, hash recorded.
