# Tim's Tables — Formulas

Entry date 2026-10-06T05:57-04:00. Rule: Timothy Norman. Append only.
Class: Tim's Tables formulas section. Sibling of the 3-4-5 unit entry (2026-09-30) and the equal-leg entry (2026-10-02).
No formulas section was found in the living tables (2/3 sheet, wrap-law sheet, 3-4-5, equal-leg, or `tims-tables/` CSVs). This file opens that section. It does not rewrite those entries.

Display is truncate-toward-zero. It is not the working value. CODATA digits below are faces, not working entries.

## Formulas

| ID | Formula | Domain | Fail |
|---|---|---|---|
| F_SPACE | f(x) = m x + b | x integer. m is MN/MD. b is BN/BD. | X_NOT_INT |
| F_GRAV | f(x) = m x + b − x²/λ | λ > 0. Positive flight: x > 0. Drag is off the line. A perfect empty is not stored. | X_NOT_INT, LAMBDA_NONPOSITIVE, OVERFLOW if x² does not fit signed 64-bit |
| RATIO | reduce N/D by gcd; sign on N; D > 0 | D = 0 never enters the Euclid loop | RATIO_DEN_ZERO |
| DISPLAY | trunc_toward_zero(ratio × 10^digits) | face only | — |
| LAMBDA_P | λ_p = c t_p | one length, not two limits. c = 299792458 exact. t_P is defined as ℓ_P/c | — |
| DOMAIN | λ_p < x ≤ c t, λ > 0, u > 0 | negative x and a negative denominator are runner checks, outside this domain | — |
| PACE | E = (1/2) m v², v < c, λ = 2 v_x² / g | m here is mass, not the slope in F_SPACE. More energy lengthens λ. It does not move λ_p and it does not license a speed past c. | — |
| DRAG | R = featured-surface drag / smooth-surface drag | earned on that surface. A golf dimple does not transfer onto the bow. In space there is no fluid wake to shrink. | — |

The square term drops, and f(x) = m x + b, only when the chamber is also free of a local mass. That is not a stored vacuum of zero.

## Not entered as formulas

Measured checks stay checks. They are not new constants.

- At x = 2, λ = 3, slope 1, intercept 0, the working value is 2/3. A truncating divide returns 1.
- The 2022 faces 5.391247(60)×10^−44 s and 1.616255(18)×10^−35 m differ by 189815126 counts of 10^−50 m. That gap sits inside both published uncertainties. The faces were not stored as a cutoff.
- A channel plate's drag ratio is not a hull formula. The nose share 1/(1+2L/D) was a geometry check, not a formula added here.
