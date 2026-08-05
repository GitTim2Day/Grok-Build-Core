# /multilingual — Exact Language Identity Layer

**Status:** ACTIVE (reconstructed 2026-08-05 from sealed session decisions)  
**Author:** Timothy H Norman  
**Handles:** @Timothy01775634 · @Tnorman01775634

## What was recovered

The detailed source files from the recent multilingual work were never written into the sealed 2026-07-29 archives. The **design decisions** were sealed. This module reconstructs the core from those decisions so the work is active again.

## Sealed design rules (now executable)

1. Evidence weights use exact rational arithmetic (`Fraction`). Float is display only.
2. Truncation only — never rounding.
3. Language identity is categorical. The **label is never interpolated**.
4. Margin is a real quantity; standing reflects provenance of the evidence.
5. Repaired input carries `value_standing = INTERPOLATED` and is capped: it can never reach CONFIDENT / EXACT decision standing.
6. `domain_repaired_from` records marked repair with provenance.
7. Verdict classes: `TRANSLATED | PASSTHROUGH | HELD`
8. Empty population with exposure > 0 is IDLE (measured bound), not absence.
9. Fifth pillar (validation) required on every permanent write.

## Files

- `lid_exact.py` — exact-arithmetic LID engine + five-pillar decision record
- `README.md` — this seal

## Relation to the rest of the lattice

- Uses the same five pillars as permanent SVCT structures.
- Compatible with Tim’s Tables ratio anchors and the base-8 → base-6 / 36 bridge.
- Does not alter the 8×64 circular-token / spherical-voxel geometry.
- Intended as the language-identity gate before any translation or passthrough path.

## Next leaves (not yet present)

- Neutral-span library
- Code-switching subroutine
- Segment-source adapter
- Full ut_pipeline with HELD/TRANSLATED routing
- Bergamot / Apertium edge adapters

These remain open work. The core exact gate is now active.

Version Clean. Finite. Musical. No infinity. No Zero’s.
