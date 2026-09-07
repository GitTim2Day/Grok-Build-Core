# decision-matrix-gosub-bidirectional-stack

**Date:** 2026-09-07
**Tags:** gosub, bidirectional, stack, audit, process, locked-skills
**Status:** Active — caller for the 10 aligned audit members

## Purpose
Caller that runs the ten decision-matrix audit skills as a bidirectional GOSUB stack. Every member can be invoked forward (sheet → report) or reverse (query → rows), so the stack operates in any direction — the same way the core reasoning loop does. One entry point, one exit, append-only log.

## When to use
- A decision matrix or spec needs a full audit pass, not a single column check.
- You want to query the matrix from any angle (by supplier, by torque, by trigger stage) without re-reading the sheet.
- Batching the 200–300 locked skills: this stack is the reusable unit they plug into.

## GOSUB wiring (bidirectional members)
This skill is the caller. It dispatches these sealed GOSUBs; each accepts a direction tag (forward | reverse):

1. **GOSUB HEX_DECODE** — extract non-ASCII / multi-byte / escaped bytes, decode to glyphs. (hex-decode-pattern-map-audit)
2. **GOSUB STRUCTURE_MAP** — identify artifact type and column/field roles. (decision-matrix-audit)
3. **GOSUB DOMAIN_AUDIT** — connect symbols + structure to the field; is/is-not + target-vs-floor. (decision-matrix-audit + tolerance-floor-audit)
4. **GOSUB SUPPLIER_AUDIT** — class-fit, custom flags, commitment boundary. (supplier-example-audit) — bidirectional
5. **GOSUB COST_BAND** — class distribution, inversions, exclusions. (cost-class-band) — bidirectional
6. **GOSUB RATIO_AUDIT** — gearbox vs effective split, class fit, torque cross-check. (ratio-effective-audit) — bidirectional
7. **GOSUB SKELETAL_AUDIT** — load-path list, multiplier sanity, actuator-vs-frame. (skeletal-load-path-audit) — bidirectional
8. **GOSUB NOTES_AUDIT** — engineering-vs-marketing split, trigger connection. (notes-why-better-audit) — bidirectional
9. **GOSUB GAP_AUDIT** — gap list, classification, justification, ordered impact. (current-vs-recommended-gap) — bidirectional
10. **GOSUB FALLBACK_MAP** — fallback list, trigger attachment, single-point flags. (alternative-fallback-map) — bidirectional
11. **GOSUB TORQUE_CHECK** — scaled targets, ratio cross-check, class sanity. (torque-target-cross-check) — bidirectional
12. **GOSUB TOLERANCE_NORM** — normalized set, direction check, unit mismatches. (key-tolerance-limits-normalize) — bidirectional
13. **GOSUB TRIGGER_SEQ** — ordered sequence, dependency rationale, fallbacks. (decision-trigger-sequence) — bidirectional
14. **GOSUB GOSUB_VALIDATE** — bounds check, provenance hash, append-and-verify, accuracy floor.
15. **GOSUB APPEND_LOG** — one append-only entry: timestamp, artifact, direction tags, audit verdict, hash.

## Steps (caller)
1. Receive artifact + direction hint (forward default; reverse if a query is given).
2. GOSUB HEX_DECODE → glyph map.
3. GOSUB STRUCTURE_MAP → column/field roles.
4. GOSUB DOMAIN_AUDIT → is/is-not + target-vs-floor.
5. Dispatch members 4–13 in dependency order; each runs in the tagged direction.
6. GOSUB GOSUB_VALIDATE → pass/fail + hash.
7. GOSUB APPEND_LOG → one line, append-only.
8. Report the layers + validation hash. Stop or offer next batch.

## Bidirectional rule
- Every member 4–13 carries a direction tag: forward (sheet → report) or reverse (query → rows).
- Reverse calls must return the same rows the forward pass would have flagged — no drift between directions.
- Direction is a tag on the log entry, never a stored payload.

## Batch mode (for 200–300 locked skills)
- Run steps 1–7 per skill, logging each.
- Group by tag family so related skills share a structure map.
- After each batch of 10–20, run skill-shelf-second-pass-merge across the batch.
- DO UNTIL backlog empty or a stop condition.

## Rules
- Decode before interpret. Never guess glyphs from context when bytes are available.
- The user's sequencing of reveals is part of the method — do not collapse it.
- GOSUB_VALIDATE must pass before anything is promoted to the living index.
- Append-only. No stored negatives. Direction is a tag, not a payload.
- Keep each skill self-contained: another assistant can run this without the original chat.
- Bidirectional members must be testable in both directions before promotion.

## Anti-patterns
- Answering content before decoding bytes.
- One-directional GOSUB members — a stack member that only runs forward is not aligned.
- Skipping GOSUB_VALIDATE to save time.
- Rewriting prior log entries instead of appending.
- Running batch mode without the second-pass merge.

## Example (this session)
Artifact: Book (1) copy.xlsx / 96f171…xlsx (10,574 bytes), Optimus joint-architecture decision matrix.
Direction: forward.
HEX_DECODE → five UTF-8 sequences: ≤, ≥, ×, °, —.
STRUCTURE_MAP → 11 sections × 13 columns.
DOMAIN_AUDIT → humanoid joint architecture, 70 kg class; decision table, not a BOM.
SUPPLIER_AUDIT → 3 real + 1 placeholder at hip; all roller-screw at knee.
COST_BAND → 5 High, 2 Medium-High, 3 Medium, 1 Low-Medium.
RATIO_AUDIT → gearbox vs effective split clean; torque cross-check passes.
SKELETAL_AUDIT → all load-bearing joints ≥3× BW; no missing paths.
NOTES_AUDIT → all engineering, none marketing; trigger connections hold.
GAP_AUDIT → 4 gap classes; always-on gaps (wrist, fingers) ordered first.
FALLBACK_MAP → Differential + Compound pulley flagged single-point (low risk).
TORQUE_CHECK → per-kg scaling sane; legs > arms > distal — correct.
TOLERANCE_NORM → 3 unit sets (rotary/linear/tendon); no reversals.
TRIGGER_SEQ → always-on → threshold → thermal → optional.
GOSUB_VALIDATE → pass. APPEND_LOG → one entry, hash recorded.
