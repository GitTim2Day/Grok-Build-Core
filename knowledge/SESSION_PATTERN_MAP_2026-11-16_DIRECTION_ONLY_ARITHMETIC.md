# Direction-Only Arithmetic Rule
**Standing rule locked 2026-11-16**

Sign is direction, not value.  
Standard subtraction is unnecessary.

## Core rule
- All magnitudes remain positive.
- The minus sign is a pure direction change (equivalent to multiplying by −1).
- Arithmetic is addition of positive units plus an explicit direction.
- Truncation (or any residual) is applied only to the positive magnitude before direction is reapplied.
- The truncation operator therefore sees exactly one sign and produces one fixed bias.

## Canonical form
```
a + (b × direction)
direction ∈ {+1, −1}
```

Example:
```
10 + (4 × −1) = 6
```

## Why
Under A3/A4 of Bounded-Domain Numerics (Tim’s Tablets, August 2026):
- Zero is the result of cancellation, not a value.
- Negative operands do not exist; only magnitudes with attached direction exist.
- Round-to-nearest on signed values produces a random-walk error.
- Truncating magnitude only and reapplying direction keeps the error sign fixed.

## Implementation notes
- String-deconcatenate path already implements this: keep magnitude as string, cut, reapply direction only if needed.
- Python and C++ adapters must produce identical results under this contract.
- BW BASIC output is captured as string, truncated toward zero on the magnitude, then direction reapplied.
- No float64 intermediate that sees a negative operand.

## Pattern-match sources
- Bounded-Domain Numerics for Tim’s Tablets (A3, A4)
- String truncation / deconcatenate contract (2026-11-12)
- SVCT string token format
- Practical device accuracy / truncation-toward-zero GOSUB

## Status
HIT: rule stated and mapped.  
VAL: consistent with sealed A3/A4 and string contract.  
Miss: none on the statement.  
Open: wire into active GOSUB catalog and brain node menu if later named.
