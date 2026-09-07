# Shepherd's Staff

**Family:** CONTROL  
**GOSUB ID:** SHEPHERD_FILTER  
**Status:** PROMOTED  
**Direction:** bidirectional  
**Cost class:** Low-Medium  
**Archived:** 2026-09-07

## Purpose
Separate clean animal-detection signal from contaminated training data before it reaches the model. The pet problem is a data-quality problem, not a model problem.

## Contract
- **Forward call:** SHEPHERD_FILTER(raw_rows) -> filtered_rows, contamination_report
- **Reverse call:** SHEPHERD_FILTER.reverse(filtered_rows) -> original_rows, dropped_rows
- **Shared state:** PetCanine sigma feature, 118-bin index, contamination threshold
- **Direction tag:** bidirectional — reverse must return the same rows the forward pass flagged

## Method
Feature-based filter using PetCanine sigma. Drops rows where the animal-detection signal is contaminated by non-animal sources (reflections, shadows, mislabeled frames).

## Proven run
- Input: 512 rows
- Output: 405 rows (81% retained)
- Bins: 118
- Dropped: 107 contaminated rows

## Why it matters
The contamination was visible in the raw signal before any model touched it. Shepherd's Staff patches the fence line before the wolf gets in the pen — the flock never knows the danger was there.

## Held for owner
- Threshold tuning per deployment environment
- Whether dropped rows are logged for retraining or discarded permanently

## Related
- KBLD-9 (noise-cleaning engine, broader scope)
- hex-decode-pattern-map-audit (intake decoding before any filter runs)