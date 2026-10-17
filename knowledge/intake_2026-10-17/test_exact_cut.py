#!/usr/bin/env python3
"""Lock the sig-digit cut and the integer twin of exact_cut.bas."""
import random
from fractions import Fraction
from exact_text import frac_trunc_sig as T

MD = 10**14
MS = 40
MX = 70
ML = 254

def basic_cut(nu, dn, ns, ng):
    if dn > MD or dn < 1 or ns < 1 or ns > MS or nu == "" or len(nu) > ML:
        return "UNKNOWN"
    qu = ""
    rm = 0
    for ch in nu:
        dg = ord(ch) - 0x30
        if dg < 0 or dg > 9:
            return "UNKNOWN"
        rm = rm * 10 + dg
        qd = rm // dn
        rm = rm - qd * dn
        if not (qd == 0 and qu == ""):
            qu += chr(0x30 + qd)
    il = len(qu)
    if il == 0 and rm == 0:
        ot = "0"
    elif il >= ns:
        ot = qu[:ns] + ("0" * (il - ns))
    else:
        fd, fz, sc, nf = "", 0, il, (1 if il > 0 else 0)
        for _ in range(MX):
            if sc < ns:
                rm = rm * 10
                qd = rm // dn
                rm = rm - qd * dn
                if nf == 1:
                    fd += chr(0x30 + qd); sc += 1
                elif qd == 0:
                    fz += 1
                else:
                    nf = 1
                    fd += chr(0x30 + qd); sc += 1
        if sc < ns:
            return "UNKNOWN"
        ot = (qu + "." + fd) if il > 0 else ("0." + ("0" * fz) + fd)
    if ng == 1 and ot != "0":
        ot = "-" + ot
    return ot

def expect_pair(n, d, s, g):
    exp = T(Fraction(n, d), s)
    if g and exp != "0":
        exp = "-" + exp
    return exp

def main():
    fails = 0
    face = [
        (T(Fraction(1999999, 10**6), 3), "1.99"),
        (T(Fraction(-1999999, 10**6), 3), "-1.99"),
        (T(Fraction(0), 5), "0"),
        (T(Fraction(1, 10**20), 4), "0.00000000000000000001000"),
        (T(Fraction(1, 3), 12), "0.333333333333"),
        (T(Fraction(2, 3), 4), "0.6666"),
    ]
    for got, exp in face:
        if got != exp:
            fails += 1
            print("FAIL face", got, exp)
    if Fraction(1, 10) + Fraction(2, 10) != Fraction(3, 10):
        fails += 1
    # no exponent, no negative zero, on the five chain samples
    for i in range(5):
        s = T(Fraction(i, 10) - Fraction(3, 10), 6)
        if "e" in s.lower() or (s.startswith("-") and set(s[1:]) <= set("0.")):
            fails += 1
            print("FAIL sample", i, s)
    cases = [(1999999,10**6,3,0),(1999999,10**6,3,1),(1,3,12,0),(2,3,4,0),(0,5,5,0),(123456,1,2,0),(1,10**14,4,0),
             (156525121,1210320000,12,0),(1,7,10,0),(7,2,1,0),(99999,100,3,0),(1,1000,2,0),(5,1,1,0),(10,3,6,0),(1,10**14,1,1),
             (999999,1000000,2,0),(100,1,3,0),(12345678901234567,1,5,0),(3,10**14,15,0),(1,2,1,0)]
    for n, d, s, g in cases:
        exp = expect_pair(n, d, s, g)
        got = basic_cut(str(n), d, s, g)
        if got != exp:
            fails += 1
            print("FAIL case", n, d, s, g, got, exp)
    controls = [("0", 1, 5, 1, "0"), ("1", 10**14+1, 1, 0, "UNKNOWN"), ("12x", 1, 1, 0, "UNKNOWN"), ("1", 1, 41, 0, "UNKNOWN")]
    for nu, d, s, g, exp in controls:
        got = basic_cut(nu, d, s, g)
        if got != exp:
            fails += 1
            print("FAIL ctl", nu, got, exp)
    if basic_cut("1", 10**20, 4, 0) != "UNKNOWN":
        fails += 1
    rng = random.Random(20261017)
    for _ in range(200):
        digits = rng.randint(1, 40)
        nu = "".join(str(rng.randint(0, 9)) for _ in range(digits)).lstrip("0") or "0"
        dn = rng.randint(1, 10**14)
        ns = rng.randint(1, 40)
        g = rng.randint(0, 1)
        exp = expect_pair(int(nu), dn, ns, g)
        if basic_cut(nu, dn, ns, g) != exp:
            fails += 1
            print("FAIL wide", nu, dn, ns, g)
            break
    try:
        T(0.1, 3)
        fails += 1
        print("FAIL float accepted")
    except TypeError:
        pass
    print("FAILS", fails)
    return fails

if __name__ == "__main__":
    raise SystemExit(main())
