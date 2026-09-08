# Shepherd 10 Sigma equivalent or better

**Date:** 2026-09-08
**Status:** sealed rename — not a probability claim

## The rename
The Staff is no longer "10-Sigma Shepherd's Staff" as a statistical threshold. It is:

> **Shepherd 10 Sigma equivalent or better**, with or without probabilities.

The floor holds either way. Probabilities are optional, not required.

## Why
A pure sigma threshold (median absolute error × 10) is a probability claim — it assumes a distribution and reports how unlikely an outlier is. That assumption is the crack. The Staff's floor is deterministic: it holds by construction, not by the odds of a Gaussian tail.

## What stays, what goes
- **Stays:** the MAD/10-sigma guard in `kbl_svct_stacks.py` as an *earned component* — a real, tested filter for gross contamination. It is a tool, not the identity.
- **Goes as identity:** "10-Sigma" as the name of the Staff. Replaced by the equivalent-or-better formulation.
- **Added (sigma-free path):** EV2 correction, harmonic resonance, shell snap, data-driven anomaly mask. These do not lean on sigma at all.

## Provenance
- May 6, 2026 email: original v2.0 package named "10-SIGMA SHEPHERD'S STAFF."
- Aug 20, 2026 session close: "sigma_free" validator noted — no longer leans on sigma.
- svct-direction-lock (Aug 25): "Shepherd 10σ deterministic floor before earned" — sealed.
- true-action page (Sep 1): "Ten Delta or Ten Sigma remains OPEN" — now closed by this rename.
- This file: the explicit statement that Ten Sigma is not a probability claim.

## Retest
Run the Staff on a distribution it was never trained on. If the floor holds without invoking any probability, the rename is earned. If it silently falls back to a sigma assumption, remediate.
