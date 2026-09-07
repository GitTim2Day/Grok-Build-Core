# hex-decode-pattern-map-audit

**Date:** 2026-09-07
**Tags:** hex, decoding, pattern-mapping, audit, optimus, process

## Purpose
Turn encoded or multi-byte text in a file into a clean, auditable pattern map before any interpretation. Team effort: the user sequences the reveals; the assistant decodes, maps, and audits.

## When to use
- A file arrives with text that is not plain ASCII (UTF-8 multi-byte, hex, or escaped symbols).
- The user says the text will require hexadecimal processing, or that it is not a waste of time.
- You are about to answer questions about a structured file (spreadsheet, matrix, spec) and the symbols carry meaning.

## Required inputs
- The file (xlsx, csv, json, or raw text).
- Any hint from the user about where the encoding points (e.g. robotics, Optimus, a specific domain).

## Steps
1. **Do not answer yet.** Acknowledge the file and the encoding hint.
2. **Extract the non-ASCII bytes.** Pull the shared strings or raw bytes; list every multi-byte UTF-8 sequence with its hex.
3. **Decode each sequence.** Map hex to the glyph (e.g. e2 89 a4 → ≤, e2 89 a5 → ≥, c3 97 → ×, c2 b0 → °, e2 80 94 → —). Note XML escapes too (&gt; → >, &amp; → &).
4. **Pattern-map the structure.** Identify what the sheet is (decision matrix, spec, archive) and what each column does, independent of the symbols.
5. **Audit against the domain hint.** Connect the decoded symbols to the likely field (torque targets, load paths, tolerances). State what the sheet is and is not.
6. **Report the three layers:** decoded bytes, structure map, domain audit. Then stop or offer the next concrete step.

## Rules
- Decode before interpret. Never guess the glyph from context alone when the bytes are available.
- The user's sequencing of reveals is part of the method — do not collapse it into one answer.
- Keep the artifact self-contained: another assistant can run this without the original chat.
- No stored negatives. Direction is a tag, not a payload.

## Anti-patterns
- Answering the content question before decoding the bytes.
- Treating the hex work as busywork because the final text looks ordinary.
- Saving the whole conversation instead of the method.

## Example (this session)
File: Book (1) copy.xlsx / 96f171...xlsx (10,574 bytes), Optimus joint-architecture decision matrix.
Non-ASCII: five UTF-8 sequences across twelve shared strings — ≤, ≥, ×, °, —.
Structure: 11 sections × 13 columns (current / recommended / alternative / ratio / torque / tolerances / skeletal / trigger / notes / mass / cost / suppliers).
Domain: humanoid joint architecture, 70 kg class; symbols are the tolerance and load-path floors.
