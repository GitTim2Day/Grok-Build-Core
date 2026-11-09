# STREAMLINE NOTES — lock_loop_xfer (2026-11-09)

Input (read-only, untouched): `original/lock_loop_xfer.zip` sha256 d3fb85c9690157cc584b9401ed8b464a51a6eeedaa1d760ab741cdf40db7363d; `extracted/arrays.npz` db911354fd5ccf97…, `extracted/manifest.json` fb7aa5794c445574…. Schema lock-loop-bundle/v1, source synthetic, seed 7. All 48 per-array sha256 values in the manifest were re-checked against the npz bytes, and all 48 match.
Skills applied: first-principles-tim, ratios-are-values, exact-ratio-loops, minradius-lp-seal. Script: `streamline.py` (Python fractions.Fraction, integer math for renderings).

## Method
1. Each float64 → its exact binary ratio `Fraction(float)` (denominator a power of 2). **The ratio is the value**. Each `*_trunc15` string is a rendering only: the ratio cut toward zero to 15 significant digits (TRUNCATED, never rounded), produced with integer math.
2. **Negatives as direction**: resid, coef and scalars are stored as `mag` (>0, exact ratio) plus `dir` (+1 or −1). Value = mag × dir, so y = yhat + (|resid| × −1) when dir = −1.
3. **Offset frame for y and yhat**: the most negative original is y = −0.20067718312587335 (frame 13). The lowest yhat is −0.05855975495741188. I chose a single offset from the unit-ratio ladder: d = floor(1/0.20067…) = 4, so **offset = 1/4** (exact in base 2 and base 10). The offset is larger than the most negative magnitude. I applied it to y and yhat in **all 16 frames** so every frame uses one frame of reference. Stored y_shift = y + 1/4 and yhat_shift = yhat + 1/4. To recover: y = y_shift + (1/4 × −1). After the shift, the lowest value is 4.93228168741266e-2 (truncated), which is > 0 and far above L_p. Nothing was clamped.
4. **Zero rule**: if a value were an exact 0, it would be stored as the Planck-floor marker L_p = c·t_p = 299792458 × 539/10^46 (exact ratio) with a note. Exact zeros: **none found**. Non-finite (±∞/NaN): **none found**.
5. The sum-of-squares accumulator starts from the empty sum. That is a count position, not a stored value. No zero is written to any output.

## Counts (original data)
- Negative y: 97 (frames 8–15). Negative yhat: 16. Negative resid: 1608 of 3200. Negative coef: 21 of 64. All are stored as direction −1.

## Verification
- **Round-trip**: each y, yhat and resid was rebuilt from the stored outputs only (y_shift − offset, mag × dir) and converted back to float64, then compared bit for bit with the original. **pass 9600, fail 0** (3 arrays × 16 frames × 200 samples).
- **Lock recheck (exact)**: each frame tests mean(resid²) < thresh² on exact ratios, with no sqrt. I ran it twice, once with the float threshold's binary ratio 0.08 = 5764607523034235/72057594037927936 and once with the decimal intent 8/100. Both runs agree with the manifest in all 16 frames: frames 0–7 locked, frames 8–15 unlocked. Mismatches: **none found**.

## Findings (float64 drift — reported, not altered)
- F1: In 202 of 3200 samples, exact (y − yhat) ≠ the stored resid. This is float64 subtraction rounding. The worst gap is 1/36028797018963968 (2^−55). The stored resid is kept as delivered, and y and yhat are each kept exactly, so the exact residual can be recomputed from them.
- F2: The manifest rms², compared with the exact mean(resid²), differs by between about 5e-22 and 3e-20 per frame in frames 0–7, and between about 5e-19 and 1.2e-17 in frames 8–15. The difference goes both ways (truncated magnitudes), caused by float64 sqrt and sum drift. It has no effect on any lock decision.
- F3: The threshold knob 0.08 is stored as float64, and its binary ratio is slightly larger than 8/100. Using either gives the same verdicts.
- Rule conflicts: none found. Open: none.
