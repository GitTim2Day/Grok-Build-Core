# SESSION_PATTERN_MAP_2026-11-10_PHARMACY_LOOKUP_AND_GATE

America/New_York: 2026-11-10 19:54 EST

## Pattern Match and Map

Local lookup earned from the clarified table.

File: pharmacy_ingredients_lookup.py
SHA-256: 0f2ac8bb25d6053e711ec83520c0ae9dd1b59225d67a13332e79ba738176c0b7

Behavior:
- normalize name (case-insensitive, whitespace-collapsed)
- return Hazardous / Food-GRAS / Primary Use / Notes
- --validate checks 8 earned anchors and the H→API rule
- append_row writes candidates to pharmacy_ingredients_append.jsonl (does not rewrite the sealed TABLE)

Validation result: PASS (27 rows, 8 anchors).

## First part of gate decision (#3)

Current use: compounding hygiene lookup only.
The table answers “is this name on the facility Hazardous list and what is its ordinary role.”

Named columns that would feed a later claims/OCR gate (not wired):
- hazardous (H/NH)
- primary_use (API / Excipient / Both)
- notes (containment hint)

If a claims or OCR gate is later required, those three columns are the exact fields it would read. No other columns are required for that gate. The rest stays appendable.

## Audit

- Anchors match standard pharmacy knowledge (amphotericin B, bleomycin, cisplatin, cyclophosphamide = H; acacia, glycerin, lactose, ascorbic acid = NH).
- Every H row is API; no H row is an excipient.
- Append path does not mutate the sealed table.
- Lookup stays on the edge device; no external inventory.

## Pattern Match Again

The earned lookup is the local form of the clarified table. The first part of the gate decision is settled: hygiene lookup now; claims/OCR gate columns are named and left appendable. No rewrite of the sealed rows.

Open: none on the lookup. Gate wiring only if later named.
