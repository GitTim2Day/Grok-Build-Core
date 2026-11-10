# AUDIT pass 3 — on PATTERN_MAP_v3 (2026-11-09 20:45 EST / 2026-11-10T01:45Z, file mtime)

## Mechanical checks (same script as pass 2)
- Evidence ids: 120; cited in v3: 120; uncited: none.
- Cited in v2 but missing in v3: none. (v1 ⊆ v2 ⊆ v3.)
- File items re-hashed: 79; changed: 0.
- Hex references in v3: 7; one not in EVIDENCE text: Gmail id `1a1c0d631f365c6e` → traced by grep to E71 (2 hits). Untraceable: 0.

## Re-read of the 7 changed lines (v2 → v3)
- D18 fix: E70 and E63 both say "Gmail writes none"; E71 records the Code label on 1a1c0d631f365c6e. MATCH.
- D19 fix: E72 mtime 2026-11-09 17:06:47 EST. MATCH.
- D17 note: E75 line 7 and E1 §18 line 237 quoted as written. MATCH; left unresolved.

## Result
Pass 3: 0 new drops, 0 new discrepancies. Cycle closed at pass 3 (cap 3).

## Totals across passes
| pass | on | new drops | new discrepancies | fixed in |
|---|---|---:|---:|---|
| 1 | v1 | 41 (27 uncited + 14 window files) | 16 (D1-D16) | v2 (D1, D2, D10, D11 fixed in text; D3-D9, D12-D16 recorded) |
| 2 | v2 | 0 | 3 (D17-D19) | v3 (D18, D19 fixed; D17 recorded, needs Timothy) |
| 3 | v3 | 0 | 0 | — |

## Self-correction (before seal)
Header build times in v1, AUDIT, v2, AUDIT_pass2, v3 and this file were first written as estimates ahead of the clock (~20:42 to ~21:10). They were replaced, before sealing, with each file's first-write mtime (20:41-20:45 EST). No other content changed.
