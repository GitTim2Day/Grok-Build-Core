"""descend.py -- descending forward-difference power update, exact Fractions (Timothy's sampler).

f(x) = m * x^n + B.  Build the forward-difference table at x0 with step dx, then walk it
`steps` times by additions only.  Returns the FINAL value only (no intermediate print).
Locked case (2026-10-05, MAP_PASS_1): m=5, n=3, B=7, x0=0, dx=3, steps=4 -> 8647.
Fail-closed: inputs must be exact integers / fractions / finite decimal strings (no floats,
no exponents); the walk is cross-checked against the closed form and refuses on mismatch.
"""
from __future__ import annotations
import re
from fractions import Fraction

MAX_N = 32
MAX_STEPS = 1_000_000
MAX_TOKEN = 64
_NUM = re.compile(r"^[+-]?(?:\d+(?:\.\d+)?|\d+/\d+)$")


class DescendError(ValueError):
    pass


def exact(v, name: str) -> Fraction:
    """Accept int or a string '7', '-3', '0.01', '1/100'. Floats, bools, exponents refused."""
    if isinstance(v, bool):
        raise DescendError(f"{name}: bool refused")
    if isinstance(v, int):
        return Fraction(v)
    if not isinstance(v, str):
        raise DescendError(f"{name}: pass an integer or an exact string (floats refused)")
    s = v.strip()
    if len(s) > MAX_TOKEN or not _NUM.match(s):
        raise DescendError(f"{name}: not an exact number string (use 7, -3, 0.01 or 1/100)")
    try:
        return Fraction(s)
    except ZeroDivisionError:
        raise DescendError(f"{name}: zero denominator refused")


def _int_param(v, name: str, lo: int, hi: int) -> int:
    if isinstance(v, bool):
        raise DescendError(f"{name}: bool refused")
    if isinstance(v, str) and re.fullmatch(r"\d{1,8}", v.strip()):
        v = int(v.strip())
    if not isinstance(v, int) or not (lo <= v <= hi):
        raise DescendError(f"{name}: integer {lo}..{hi} required")
    return v


def table(m: Fraction, n: int, B: Fraction, x0: Fraction, dx: Fraction) -> list:
    """Forward-difference table [f, d1, ..., dn] at x0 (exact)."""
    vals = [m * (x0 + k * dx) ** n + B for k in range(n + 1)]
    d = []
    row = vals
    for _ in range(n + 1):
        d.append(row[0])
        row = [row[i + 1] - row[i] for i in range(len(row) - 1)]
    return d


def walk(d: list, steps: int) -> list:
    """Descending update: d[k] += d[k+1] for k = 0..n-1 (additions only), `steps` times."""
    d = list(d)
    n = len(d) - 1
    for _ in range(steps):
        for k in range(n):
            d[k] += d[k + 1]
    return d


def final_value(m, n, B, x0, dx, steps) -> Fraction:
    M, Bb, X0, DX = exact(m, "m"), exact(B, "B"), exact(x0, "x0"), exact(dx, "dx")
    N = _int_param(n, "n", 0, MAX_N)
    S = _int_param(steps, "steps", 0, MAX_STEPS)
    if N * S > 4_000_000:
        raise DescendError("work cap: n*steps must be <= 4,000,000")
    d = walk(table(M, N, Bb, X0, DX), S)
    closed = M * (X0 + S * DX) ** N + Bb
    if d[0] != closed:   # fail closed: never return an unchecked value
        raise DescendError("walk != closed form (refused)")
    return d[0]


def fmt(f: Fraction) -> str:
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


if __name__ == "__main__":
    print(fmt(final_value(5, 3, 7, 0, 3, 4)))
