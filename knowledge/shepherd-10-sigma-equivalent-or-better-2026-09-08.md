# Shepherd 10-Sigma Equivalent or Better

**Claim:** A deterministic accuracy floor that holds with or without probabilities.
**Rename sealed:** 2026-09-08.
**Owner:** Timothy H Norman (SVCT)

## The problem

Early Shepherd's Staff (v2.0, May 2026) defined the floor as median absolute error × 10 — a pure statistical threshold. By August the validator had moved off probability (EV2 correction, harmonic resonance, shell snap, data-driven anomaly mask) but still carried the "10-sigma" name, inviting a distributional reading the code no longer made.

## The fix

- **Name:** Shepherd 10-Sigma Equivalent or Better, with or without probabilities.
- **Identity:** deterministic floor, not a probability claim.
- **Earned component:** `GOSUB_MAD_Sigma_Guard` (KBLD-9) remains as a robust pre-filter — it computes median and MAD and flags beyond n×MAD, but sigma here is a label for the floor, not an assumption about the data's distribution.
- **Direction-lock sealed:** "Shepherd 10σ deterministic floor before earned."

## Proof (Row 3C, closed)

1. Numenta Anomaly Benchmark — 22,696 rows, labeled anomalies. IQR retained 99.49%, max robust z 8.45 (below 9, 9.5, 10). No probability invoked.
2. UCI Wine Quality — never-trained distribution. IQR retained 94.37%, max robust z 2.79. Floor held.

## Standing

The floor is deterministic. The name no longer promises a statistical guarantee it does not carry. Retestable on any distribution.
