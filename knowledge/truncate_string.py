#!/usr/bin/env python3
"""Digit-by-digit left-to-right string truncation. No float64."""

def truncate_string(src: str, n: int) -> str:
    """Truncate toward zero. N places after decimal. String only."""
    if not isinstance(src, str) or n < 0:
        return ""
    s = src.strip()
    if not s:
        return ""
    sign = ""
    if s[0] in "+-":
        sign = s[0]
        s = s[1:]
    if not s:
        return sign
    if "." not in s:
        return sign + s
    whole, rest = s.split(".", 1)
    frac = ""
    for c in rest:
        if c.isdigit():
            frac += c
        else:
            break
    if n == 0:
        return sign + whole
    frac = frac[:n]
    if frac:
        return sign + whole + "." + frac
    return sign + whole
