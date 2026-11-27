# SESSION_PATTERN_MAP_2026-11-27_CANONICAL_CYCLIC_PHASE_PRIMITIVE

Sitting 2026-11-27T11:43-05:00 · Canonical Cyclic Phase Primitive MAM

## Governing equation

$$P' = \left(P + \frac{d}{n}\right) \bmod 1$$

## Minimal sealed primitive

```python
from fractions import Fraction

def advance(phase, steps, n):
    # P' = (P + d/n) mod 1
    return (phase + Fraction(steps, n)) % 1
```

## Properties locked

- Magnitude: exact fractional displacement d/n
- Direction: sign of integer steps
- Closure: modulo one revolution; identity residual exactly 0
- Reversibility: advance(advance(P, d, n), -d, n) == P
- Precision: pure Fraction; no binary float, no base-10 rounding, no truncation

Scale-independent. Deterministic for phase ∈ [0, 1) as Fraction and n positive integer.
Suitable for SVCT spokes and WheelNetwork rings.

## Validation

VAL: assertions (positive, negative, full-cycle closure) held in sitting.
MISS: none material.
OPEN: float quadrature benchmark harness next when named.

Ledger hop 1a21de44726c994d to both addresses.
Notion 425c9bfe-3aff-81c4-b86a-e3b3300f49f8
Pointer skill: session-map-2026-11-27-canonical-cyclic-phase-primitive
Sibling of Tim’s Tables / SVCT exact spokes. Not a merge.
Six-pillar SVCT: content · context · data · time · semantics · validation
