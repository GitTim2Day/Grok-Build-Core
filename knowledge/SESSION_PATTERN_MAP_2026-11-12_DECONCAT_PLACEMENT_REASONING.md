# SESSION_PATTERN_MAP_2026-11-12_DECONCAT_PLACEMENT_REASONING.md

America/New_York: 2026-11-12T14:23:00-05:00 EST

SHA-256: 2a546f18566114cc832d15e017c1ddd0a4beb7400341f1c058c9dbaef06a574c
Ledger hop: 1a1d137b978c1f29

## Pattern match

Input: user asked for logical, truthful recommendation on placement of deconcatenate/truncate routine (Python adapter vs BASIC GOSUB vs SVCT token helper) and digit length (e-35).

Constraints already locked:
- String save → deconcatenate on use → no float64.
- Identical results in Python and C++ adapters.
- Provenance in SVCT.
- BASIC as menu/outline hierarchy (GOSUB/GOTO, IF-THEN-ELSE).
- Motor cortex = locomotion placeholder (ABSENT until drivetrain).
- Printer path as callable subroutine under motor node.

## Map

Reasoning steps that produced the recommendation:

1. Identify the operation: small deterministic string truncation (toward zero, fixed length). Not a decision, not a menu item, not a token store.
2. Locate ownership by function:
   - Routine (the code that truncates): belongs where adapters already match (Python on Pi 5, C++ on higher devices).
   - Result (string token + contract + hash): belongs in SVCT (provenance home).
   - Invocation: BASIC GOSUB can call or pass through; does not own the logic.
3. Reject alternatives that add complexity before first run:
   - Putting truncation inside BASIC: limited string handling, duplicates work the adapters must do anyway.
   - Putting the routine inside SVCT: SVCT is memory/provenance, not the execution layer for the light adapter path.
4. Digit length: user named e-35. Lock it as 35 decimal places toward zero. Deterministic, no fitting.
5. Outcome: routine in Python (and identical C++) adapter; SVCT holds token + contract + hash; BASIC invokes only.

## Audit

- Did the recommendation stay inside locked contracts? Yes.
- Did it introduce new free parameters? No.
- Did it preserve archive-not-delete and identical-results posture? Yes.
- Did it keep the BASIC menu as hierarchy rather than computation? Yes.
- Is the digit length explicit and user-named? Yes (e-35).

## Remap

Carry-forward rule for free discussion:
When the user asks for a logical placement or judgment among already-locked layers, identify the operation type (routine / result / invocation), assign each to the layer that already owns that type, reject moves that duplicate or invert ownership, and lock only the user-named constant. State the recommendation, mark the question closed, and ask the next open item. No unasked next step.

This is the second/third instance today of the same pattern (motor-cortex printer subroutine; GOSUB skeleton wiring; now deconcatenate placement). The pattern is stable.

## Status

HIT: reasoning mapped and audited.
VAL: consistent with prior locks (string path, identical adapters, SVCT provenance, BASIC menu).
miss: none on this map.
open: question 4 (skills/catalog dedupe) remains next.
