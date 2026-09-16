"""fraction_canon_face.py — CANON presentation face for Fraction.

Filed 2026-09-16 with FLOAT_DERIVED_FRACTION.
Not a sealed GOSUB. Format rule only.

Rule:
  If denom is 2^k, write n / 2^k = n / <decimal int> on one line.
  bit_length lives in its own fields. Never treat bit_length as exponent.
  bit_length(2^k) = k+1.
  Do not infer FLOAT_DERIVED_FRACTION from denom width. Construction-site only.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Optional


def _pow2_exp(n: int) -> Optional[int]:
    if n <= 0:
        return None
    if n & (n - 1) != 0:
        return None
    return n.bit_length() - 1  # bit_length(2^k) = k+1


def fraction_canon_face(value: Fraction) -> dict:
    if not isinstance(value, Fraction):
        value = Fraction(value)
    n, d = value.numerator, value.denominator
    k = _pow2_exp(d)
    if k is not None:
        value_line = f"{n} / 2^{k}  =  {n} / {d}"
    else:
        value_line = f"{n} / {d}"
    return {
        "value_line": value_line,
        "n": n,
        "d": d,
        "d_pow2_exp": k,
        "n_bit_length": n.bit_length(),
        "d_bit_length": d.bit_length(),
    }


if __name__ == "__main__":
    freeze = Fraction(0.23122)
    face = fraction_canon_face(freeze)
    assert face["d"] == 2**55
    assert face["d"] != 2**56
    assert face["d_pow2_exp"] == 55
    assert face["d_bit_length"] == 56
    assert face["n"] == 8330578446724849
    assert face["n_bit_length"] == 53
    assert "2^55" in face["value_line"]
    assert "36028797018963968" in face["value_line"]
    table = Fraction(3, 13)
    tface = fraction_canon_face(table)
    assert tface["d_pow2_exp"] is None
    assert tface["value_line"] == "3 / 13"
    assert "tag_hint" not in face
    assert "tag_hint" not in tface
    print("OUTPUT_OK")
    print(face["value_line"])
    print(tface["value_line"])
