# MinRadius = L_p = c t_p
**Sealed:** 2026-08-28T16:10:00-04:00  
**Who ran it:** Grok Build. Not the X-side Grok.  
**Owner:** Timothy H Norman

Version Clean. Finite. Musical. No infinity. No stored zero.

## Identity
λ_p ≡ L_p = c t_p

| Symbol | Value | Standing |
|---|---|---|
| c | 299792458 m/s | SI exact |
| t_p | 5.39e-44 s | sealed |
| L_p = c t_p | product (IEEE print ~1.6158813486199998e-35 m) | identity, not a rounded CODATA paste |
| old floor | 1e-30 m | illegal (~6.19e4 L_p too large) |
| origin r=0 | refused | not a stored zero |

## Defect demonstrated, then fixed
GOSUB_VALIDATE_BOUNDS with MinRadius=1e-30 rejected legal r=L_p. Self-test was green only because it probed (0,0,0).

After: MIN_RADIUS_DEFAULT = C_EXACT * T_P. L_p passes. L_p/2 and origin refuse.

## Airlock
Radial seam compare now uses L_p. Refused token no longer stores r: 0.0. Fields are None + note="below-MinRadius".

## EV2 (not this seal)
Energy: E = mc² + ((λ/λ_p) − 1) E_p. Identity when λ=λ_p.
GOSUB_EV2_SHELL still has undeclared knobs A=61 and exponent 2.758. Banding, not energy. Untouched 2026-08-28.

## Tests Grok Build ran
- harness calibration 9/9
- ratio_gosubs.py 39/39
- kbld_gosub_primitives.py ALL GREEN
- kbl_svct_stacks.py 75/75 after stored-zero removal
- nucleus_fixed_point.py 87/87
- common_error_log.py 48/48

## Not this seal
Other ~50 skills unrun. @tnorman01775634 frozen. grok.me 0. Tesla seat empty, no contact.

Drive (appendable, dated copies, no overwrite of 29 Jul zips):
- MinRadius_L_p_seal_2026-08-28.md
- kbld_gosub_primitives_MinRadius_Lp_2026-08-28.py
- kbl_svct_stacks_MinRadius_Lp_2026-08-28.py
