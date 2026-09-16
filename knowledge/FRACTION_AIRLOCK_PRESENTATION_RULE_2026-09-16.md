# Fraction airlock — filed 2026-09-16T10:55 EDT

Standing: FILED now. Not held for a live CANON row.
Owner correction this sitting adopted as working memory.
HIT owner text · VAL measured 0.23122 freeze · OUTPUT_OK this file + formatter self-test.

## Adopted defect name

`FLOAT_DERIVED_FRACTION`

- ingest_gate check: `_check_no_float_derived_fraction`
- Reason code: `Reason.FLOAT_DERIVED_FRACTION`
- Meaning: value wears `Tag.FRACTION` but was built from an already-rounded outside float (`Fraction(0.23122)`). Type/float checks pass. Rounded last digit is inside the numerator. Same family as research-digit / EV2 midplane: display digit smuggled into work.
- Tag says *how* contamination entered. This file does not invent the check body (live file not on this chair).

## Adopted presentation rule (CANON face)

For any power-of-two denominator, one line carries both coordinates of the *value*:

    n / 2^k  =  n / <decimal int>

`bit_length` is its own column. It never doubles as an implied exponent.

Why: `bit_length(2^k) = k+1`. Storage width 56 and value `2^55` are both true of the same int. Reporting them without a shared key reads as two competing denoms — a false defect on a correct freeze.

Composes with `FLOAT_DERIVED_FRACTION`: the tag is contamination-of-origin; this rule is anti-misread of a *correct* value during review.

## Worked example (VAL, not a CANON physics row)

Freeze of `float` 0.23122, measured this sitting:

    8330578446724849 / 2^55  =  8330578446724849 / 36028797018963968

| field | value |
|---|---|
| n | 8330578446724849 |
| n.bit_length | 53 |
| d | 36028797018963968 |
| d as 2^k | 2^55 |
| d.bit_length | 56 |
| d == 2^55 | True |
| d == 2^56 | False |
| hex | 0x1.d989df1172ef1p-3 |

`d.bit_length == 56` is storage width. Exponent remains 55.

## Defect filed and mitigated this sitting

`tag_hint` inferred `FLOAT_DERIVED_FRACTION` from `k is not None and k >= 52`.

That is an enough-bits test. Origin is construction, not denom width.

- False positive: exact working Fraction from repeated halving (binary lattice / SVCT) with pow2 denom at exp ≥52, never touched a float.
- False negative: `Fraction(float)` after reduction is not pinned at exp 52–55; small or large magnitude floats miss `k >= 52`.

Mitigation 2026-09-16T11:00 EDT: `tag_hint` removed. Face reports `d_pow2_exp` and bit lengths only. Provenance tag stays on `ingest_gate.py` at the construction site. Edge: one less branch, no shape-as-origin.

## Not sealed here

- Live `ingest_gate.py` body (N=10) still not on this chair / not on GitTim2Day as of prior search.
- Fifth `__main__` demo still not in the file.
- This is exact-arithmetic *memory + format rule*, not a new GOSUB seal. Proposed name if later sealed: `GOSUB_FRACTION_CANON_FACE`.

## Files this sitting

- artifacts/INGEST_GATE_N10_CORRECTION_2026-09-16.md
- artifacts/FRACTION_AIRLOCK_PRESENTATION_RULE_2026-09-16.md
- artifacts/fraction_canon_face.py
