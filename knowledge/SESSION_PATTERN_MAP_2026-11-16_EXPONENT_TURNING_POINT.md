# Exponent Turning Point and Baseline-1 Refinement
**Locked 2026-11-16T09:30 America/New_York**

## Statement
The 0 in an exponent is a turning point (inflection point) from numbers greater than 1, through 1, then to fractions (ratios of integers).  
It is not a path to negative values.

Our standard derives values > 0, never = 0.  
Baseline is 1.  
If a zero must be retained, it is 0^0 = 1.

(-1) × (1/4) yields the reciprocal of the magnitude, direction reapplied.  
It does not produce a negative value.

## Pattern match
- Bounded-Domain Numerics A2: representable magnitude domain [1e-8, 1e+8]. No true zero, no infinity. Floor and ceiling are reciprocal duals.
- A3: sign is direction, not value. Zero is the result of cancellation, not a magnitude.
- Tim’s Tables: no zero stored as value. Truncation of magnitude only. Reciprocal columns present. UNDEF / pole routing for exact-zero cases.
- Direction-only arithmetic (2026-11-16): a + (b × direction). Magnitudes positive.

## Map
Exponent 0 marks the transition:
- exponent > 0 → result > 1
- exponent = 0 → result = 1 (baseline)
- exponent < 0 → result = reciprocal of the corresponding positive-exponent magnitude (fraction)

Direction is carried separately and reapplied after the magnitude is formed.

## Audit
- Consistent with A2/A3 of Bounded-Domain Numerics.
- Consistent with Tim’s Tables “no zero stored as value” and reciprocal duals.
- Consistent with the string-deconcatenate truncation contract.
- 0^0 = 1 preserves the binomial theorem and empty-product identity.
- No contradiction with sealed truncation-toward-zero or direction-only arithmetic.

## Status
HIT: statement mapped to A2/A3 and Tim’s Tables.  
VAL: consistent with sealed reciprocal duals and direction-only rule.  
Miss: none on the refinement.  
Open: wire the exponent-turning-point case into the GOSUB catalog only if later named.
