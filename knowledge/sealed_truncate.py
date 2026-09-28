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
    if not d.is_finite():
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
    frac = (frac + "0" * places)[:places]

    out = whole + ("." + frac if places else "")
    if set(whole + frac) == {"0"}:
        sign = ""
    return sign + out


def to_count(v, places=3):
    """Integer count at `places` (e.g. milli-counts), or None if UNKNOWN."""
    t = sealed_truncate(v, places)
    return None if t == UNKNOWN else int(t.replace(".", ""))
