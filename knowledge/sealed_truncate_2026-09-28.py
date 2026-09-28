#!/usr/bin/env python3
"""
sealed_truncate.py - sealed truncate face (text storage)

Rules
-----
1. Stored value is plain positional decimal TEXT. Never E-notation.
2. Truncation is a digit cut on the decimal text, toward zero. Nothing is
   added before the cut (no nudge) and nothing is rounded.
3. There is no negative zero. A result whose digits are all zero is stored
   unsigned: "0.00000000". A sign is a direction, not a value.
4. NaN, infinity, None, or unparseable input is stored as "UNKNOWN".
5. Precision is fixed. The places are never reduced to make a value fit.

Input handling
--------------
Uses str(v), not repr(v). Under NumPy 2, repr(np.float32(1.1)) is
"np.float32(1.1)", which is not a number; str() gives "1.1", the shortest
decimal for that width. Decimal accepts E-notation input ("1e-09") and
format(..., "f") writes it back out positionally.
"""

from decimal import Decimal, InvalidOperation

UNKNOWN = "UNKNOWN"


def to_decimal_text(v):
    """Exact positional decimal text of v, or UNKNOWN. No rounding, no E."""
    if v is None:
        return UNKNOWN
    try:
        d = v if isinstance(v, Decimal) else Decimal(str(v).strip())
    except (InvalidOperation, ValueError, TypeError):
        return UNKNOWN
    if not d.is_finite():                  # NaN, sNaN, +/-Infinity
        return UNKNOWN
    return format(d, "f")


def sealed_truncate(v, places=8):
    """Cut v to `places` decimals toward zero, stored as plain decimal text."""
    if not isinstance(places, int) or places < 0:
        raise ValueError("places must be a non-negative integer")

    s = to_decimal_text(v)
    if s == UNKNOWN:
        return UNKNOWN

    sign = ""
    if s.startswith("-"):
        sign, s = "-", s[1:]
    whole, _, frac = s.partition(".")
    whole = whole.lstrip("0") or "0"
    frac = (frac + "0" * places)[:places]          # pad, then chop: the cut

    out = whole + ("." + frac if places else "")
    if set(whole + frac) == {"0"}:                   # rule 3: no negative zero
        sign = ""
    return sign + out


def to_count(v, places=3):
    """Integer count at `places` (e.g. milli-counts), or None if UNKNOWN."""
    t = sealed_truncate(v, places)
    return None if t == UNKNOWN else int(t.replace(".", ""))


# ============================ TEST SWEEP ============================

def _run_tests():
    import math
    fails = []

    def check(name, got, want):
        if got != want:
            fails.append(f"{name}: got {got!r}, want {want!r}")

    # 1. Exact 3-decimal grid: 0.001 .. 99.999, both signs
    for i in range(1, 100000):
        x = i / 1000
        check(f"grid +{x}", to_count(x), i)
        check(f"grid -{x}", to_count(-x), -i)

    # 2. True truncation, no upward nudge
    check("sub-boundary", to_count(1.0009999999996), 1000)
    check("carry trap", sealed_truncate(1.0000000099, 8), "1.00000000")

    # 3. Never E-notation
    for v in (3.4e-9, 1e-20, 1.5e25, -7.2e-12):
        t = sealed_truncate(v, 8)
        check(f"no E {v}", "e" in t.lower(), False)
    check("tiny", sealed_truncate(3.4e-9, 9), "0.000000003")
    check("tiny cut", sealed_truncate(3.4e-9, 8), "0.00000000")
    check("big", sealed_truncate(1.5e25, 2), "15000000000000000000000000.00")

    # 4. No negative zero
    check("-0.0", sealed_truncate(-0.0, 8), "0.00000000")
    check("tiny neg", sealed_truncate(-0.0000000001, 8), "0.00000000")
    check("tiny neg count", to_count(-0.0004), 0)
    check("real neg", sealed_truncate(-2.5678, 3), "-2.567")

    # 5. UNKNOWN for non-values
    for v in (float("nan"), float("inf"), float("-inf"), None, "abc", ""):
        check(f"unknown {v!r}", sealed_truncate(v, 8), UNKNOWN)
    check("unknown count", to_count(float("nan")), None)

    # 6. Short text is padded, never loses a real digit
    check("pad", sealed_truncate(1.5, 8), "1.50000000")
    check("int", sealed_truncate(42, 3), "42.000")
    check("places 0", sealed_truncate(-9.99, 0), "-9")
    check("places 0 zero", sealed_truncate(-0.5, 0), "0")

    # 7. Text input stays exact
    check("text in", sealed_truncate("0.123456789123", 8), "0.12345678")
    check("text E in", sealed_truncate("2.5E-7", 8), "0.00000025")

    # 8. NumPy scalars (repr would break under NumPy 2)
    try:
        import numpy as np
        check("np32", sealed_truncate(np.float32(1.1), 3), "1.100")
        check("np32 tiny", sealed_truncate(np.float32(1e-9), 9), "0.000000001")
        check("np32 nan", sealed_truncate(np.float32("nan"), 3), UNKNOWN)
        check("np64", sealed_truncate(np.float64(-2.5678), 3), "-2.567")
    except ImportError:
        pass

    n = 199998 + 30
    if fails:
        print(f"FAIL: {len(fails)} checks")
        for f in fails[:20]:
            print("  ", f)
    else:
        print(f"PASS: all checks ({n} including the 199,998-value signed milli grid)")
    return not fails


if __name__ == "__main__":
    ok = _run_tests()
    raise SystemExit(0 if ok else 1)
