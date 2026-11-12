#!/usr/bin/env python3
"""truncate_toward_zero.py — string truncate, no float64."""

def truncate_toward_zero(s: str, places: int = 6) -> str:
    if not isinstance(s, str):
        return ""
    s = s.strip()
    if not s:
        return ""
    sign = ""
    if s[0] in "+-":
        sign = "-" if s[0] == "-" else ""
        s = s[1:]
    if not s:
        return sign
    # reject scientific and multiple dots
    if "e" in s.lower() or s.count(".") > 1:
        return sign + s  # leave as-is for now; caller decides
    if "." in s:
        whole, frac = s.split(".", 1)
        whole = whole or "0"
        frac = frac[:places] if places >= 0 else frac
        return sign + whole + "." + frac
    return sign + s
