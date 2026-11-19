"""
GOSUB_TRUNCATE_STRING — digit-by-digit left-to-right string truncate toward zero.

Contract (locked 2026-11-19):
- Input is a string (raw BW BASIC PRINT or any decimal representation).
- No float64 conversion. Finished string is never converted to a number.
- Keep sign first. Append digits after the decimal until the named place count is reached, then stop.
- Places is the parameter (current test contract is six).
- Identical results required in Python and C++ adapters.
- Example: "0.70710678" @ places=6 → "0.707106"

Provenance: session-map-2026-11-19-digit-by-digit-string-build
SHA sealed after write.
"""

from __future__ import annotations

def truncate_string(s: str, places: int = 6) -> str:
    """Truncate a decimal string toward zero to exactly `places` digits after the decimal.
    
    Digit-by-digit left-to-right. No float conversion.
    """
    if not s or places < 0:
        return s
    s = s.strip()
    if not s:
        return s

    # Preserve sign
    sign = ""
    if s[0] in "+-":
        sign = s[0]
        s = s[1:]

    if "." not in s:
        return sign + s

    whole, frac = s.split(".", 1)
    # Truncate fractional part (toward zero = cut, do not round)
    frac = frac[:places]
    if not frac:
        return sign + whole
    return sign + whole + "." + frac


def truncate_from_bwbasic_raw(raw: str, places: int = 6) -> str:
    """Extract first decimal-looking token from BW BASIC raw output and truncate it.
    
    Returns the truncated string, or empty string if no match.
    """
    import re
    m = re.search(r"[-+]?\d*\.?\d+", raw or "")
    if not m:
        return ""
    return truncate_string(m.group(0), places)


if __name__ == "__main__":
    # Locked test case
    cases = [
        ("0.70710678", 6, "0.707106"),
        ("0.70710678", 4, "0.7071"),
        ("-0.70710678", 6, "-0.707106"),
        (".707107", 6, ".707107"),
        ("42", 6, "42"),
        ("", 6, ""),
    ]
    for inp, p, expected in cases:
        got = truncate_string(inp, p)
        status = "PASS" if got == expected else f"FAIL got={got!r}"
        print(f"{inp!r} @ {p} → {got!r}  {status}")
