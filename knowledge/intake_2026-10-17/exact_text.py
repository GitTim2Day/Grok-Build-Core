"""Significant-digit cut toward zero.

Plain positional text. No exponent. Zero is "0", never "-0".
Accepts Fraction or int only. A float is already rounded; it is refused.

Not cut8. cut8 rounds once at 10 places, then cuts to 8.
This cuts significant digits and does not round.
"""
from fractions import Fraction


def frac_trunc_sig(x, sig):
    if type(x) is int:
        x = Fraction(x)
    if type(x) is not Fraction:
        raise TypeError("Fraction or int")
    if type(sig) is not int or sig < 1:
        raise ValueError("sig")
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    ax = -x if x < 0 else x
    p = 0
    ten = Fraction(10)
    if ax >= 1:
        while ten ** (p + 1) <= ax:
            p += 1
    else:
        while ten ** p > ax:
            p -= 1
    scale_exp = p + 1 - sig
    if scale_exp >= 0:
        units = ax.numerator // (ax.denominator * (10 ** scale_exp))
    else:
        units = (ax.numerator * (10 ** (-scale_exp))) // ax.denominator
    digits = str(units)
    if len(digits) != sig:
        raise RuntimeError("digit width")
    if p >= 0:
        left = p + 1
        if left >= sig:
            body = digits + ("0" * (left - sig))
        else:
            body = digits[:left] + "." + digits[left:]
    else:
        body = "0." + ("0" * (-(p + 1))) + digits
    if set(body.replace(".", "")) <= {"0"}:
        return "0"
    return sign + body
