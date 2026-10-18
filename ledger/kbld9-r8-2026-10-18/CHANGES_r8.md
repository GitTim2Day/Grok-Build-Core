# CHANGES_r8 — kbld9_core_r8a.py vs kbld9_core_r7.py (DRAFT, not sealed)

- Base: `/workspace/kbld9/kbld9_core_r7.py` sha256 `465359bb0339d3acdd1b94282a0d9191fb663b734cd2b552e36baf5e75da31d8` (read-only, unchanged; hash checked before and after).
- Final draft: `core/kbld9_core_r8a.py` sha256 `16934bab2d88a3f7a63a9f16a7c986e296d13dd053c6d441eb05a028545347c6` (34542 B).
- Superseded draft: `archive/r8/kbld9_core_r8.py` sha256 `47b2921f1c9324a6c51f60033051aeb13833a6a60db6c46fc7b85a7aeb90d40f`.
- Built by script, not by hand: `core/make_r8.py` (r7 -> r8, 11 exact replacements, each must match once) and `core/make_r8a.py` (r8 -> r8a, 5 replacements). Full unified diff: `results/diff_r7_r8a.patch` (208 lines added, 48 removed).
- API: unchanged. Same public names (`KBLD9`, `process_stream`), same helpers with the same signatures (`_truncate`, `_places`, `_mad_scaled`, `_quantize`, `_snap`, `_classify`, `Welford`, `_sha256`, ...), same constants (`TIER_*`, `_MAD_K`), same envelope shape and field names. One import was added: `sys`, `fractions.Fraction` (stdlib).
- Version string: `9.0.7-core` -> `9.0.8a-core-draft` (so provenance never claims to be r7). This is the only intended envelope difference on inputs where r7 already returns OK and no point sits on a boundary.

## What changed (Timothy's rule: representation, not more math)
| # | Where | r7 | r8a |
|---|---|---|---|
| 1 | fused filter pass in `process` (G1) | tier and fence membership from the rounded float `s = (x-med)*(1/mad)` | membership decided on EXACT values: `abs(Fraction(x) - Fraction(med)) <= k*Fraction(mad)`, k = 3, 6, 9 (`Fraction(float)` is the exact binary value, the same as `float.as_integer_ratio`). A per-batch float pre-filter may decide a point only when its float deviation lies outside a +-2^-51 relative band around the exact threshold; one float subtraction errs by at most 2^-53, so the pre-filter cannot disagree with the exact test. Points in the band go to Fraction. |
| 2 | `_snap`, `_classify` reference (G1) | `(x-med)/mad` float division | the same exact comparison (the reference and the fused path now share the semantics; T2's differential still compares them) |
| 3 | fence snap values (G2) | `q_hi`, `q_lo` quantized eagerly. `9*mad` overflowed to inf, so `round(inf)` raised on `[1e308,-1e308,0.0]` | computed lazily, only for a side that actually has a point outside. Shared helper `_fence_snap`. While both float fences are finite it is r7's arithmetic, operation for operation (`hi = median + 9.0*mad`, `_quantize`, two-sided clamp). When a float fence overflows, the fence is computed on exact values and brought back toward the median, so the snap value stays inside the exact fence. |
| 4 | `_quantize` | `_truncate(round(v/bw)*bw, places)`. Raised when `v/bw` overflowed | the same float path when `v/bw` and the product are finite. Otherwise `_quantize_exact`: exact `round(V/B)*B` (half-even, the same rule as `round()`), cut toward zero at `places` digits by integer truncation (an exact decimal digit string), then represented as `_truncate` represents it, `float(cut digits)`. The ULP guard is kept. |
| 5 | median | `statistics.median` (an even-length midpoint can overflow to inf) | `_median_safe`: the same value, except when the midpoint overflows. Then the exact midpoint, truncated toward zero to float64. |
| 6 | scaled MAD | `median(devs)*1.4826` (can overflow to inf) | the same float. If it is inf, `_mad_exact` gives the exact value: the header carries it truncated toward zero if it fits float64, else inf, and classification uses the exact value. |
| 7 | Welford batch mean | `math.fsum(data)/n` (raises "intermediate overflow in fsum") | the same, with an exact-sum fallback only on OverflowError |
| 8 | `recurrence_bins` key for an outlier whose `x/bw` overflows | raised | `_quantize_exact` key; otherwise the same per-bin cache as r7 |

## Rounds
- r8 (round 1): items 1-8, but the exact path converted the cut digit string to float toward zero.
- r8a (round 2 fix): X13 showed key `'100000000.12345599'` where r7's `_truncate` convention gives `'100000000.123456'`, the float whose repr IS the cut digit string. `_quantize_exact` now uses that convention. No other change.

## Not changed (deliberately; see OPEN_GAPS.md)
- The snapped fence VALUE on the finite path is still r7's float `hi = median + 9.0*mad`. Measured: on 17 suite inputs this value lies above the exact `9*mad` fence, by at most 4.663E-15. Changing it would change 17 suite outputs and fail v3 T1/T2 against the v3 oracle (measured with a scratch variant, archived as `archive/scratch/make_r8a_try.py`).
- Airlock behaviour for `10**400` (G3): still ERROR, as in r7.
- No change to provenance, the read-back gate, transactional stats, the spine, tiers, or the configuration validator.
