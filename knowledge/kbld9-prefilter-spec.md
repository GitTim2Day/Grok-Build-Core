# KBLD-9 Pre-Filter Spec

**Status:** Earned component of Shepherd's Staff. Not the identity.
**Sealed:** 2026-09-08
**Owner:** Timothy H Norman (SVCT)

## What it is

`GOSUB_MAD_Sigma_Guard` inside `kbld/kbl_svct_stacks.py`.

- Computes median and MAD over a flat numeric sequence.
- Flags points beyond n×MAD (default n = 10).
- Returns `{guarded, data, flagged, dropped_nonfinite}` — never mutates input.
- Exit guard: kept + flagged + dropped == input count.
- Breakdown detector: collapsed MAD on a dispersed sample → `breakdown_suspected=True` (measured threshold 0.40, min-n 8).

## What it is not

- Not a probability claim. The 10 is a deterministic floor, equivalent or better, with or without probabilities.
- Not the whole Staff. The Staff is EV2 correction + harmonic resonance + shell snap + this guard as the earned pre-filter.

## Retests that closed Row 3C

1. **Numenta Anomaly Benchmark** (machine temp, 22,696 rows, labeled anomalies): IQR retained 99.49%, max robust z = 8.45 — below 9, 9.5, and 10. No probability invoked.
2. **UCI Wine Quality** (never-trained distribution): IQR retained 94.37%, max robust z = 2.79 — well under all three thresholds. Floor held without invoking probability.

## Standing

Earned. Re-testable. The floor is deterministic; sigma is a label, not a distributional assumption.
