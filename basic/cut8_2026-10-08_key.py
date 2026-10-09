"""Answer key v2 (Tim 2026-10-08): zero normalised (0 and -0 -> 0), sign as direction,
split integer part first (reduce), round fraction once at 10 places with carry, cut to 8, no negative zero.
Limit LM = 99999: 15 reliable significant digits = 5 integer + 8 places + 2 guard. Above it: REFUSED."""
from fractions import Fraction as F
import math
LM = 99999
def cut8(v: float) -> str:
    if v == 0: v = 0.0                      # Tim: -0 and 0 both become 0
    s = -1 if v < 0 else 1                  # sign is a direction
    m = F(v) * s                            # positive magnitude
    p = math.floor(m)                       # reduce: integer part
    if p > LM: return "REFUSED"
    w = math.floor((m - p) * 10**10 + F(1, 2))   # round fraction once at 10 places
    if w >= 10**10: p, w = p + 1, w - 10**10     # carry
    q = w // 100                            # cut to 8 places
    t = f"{p}.{q:08d}"
    return ("-" + t) if (s < 0 and (p > 0 or q > 0)) else t
cases = [("Y100", math.log(100000000/130.8)/math.log(2)), ("Y500", math.log(500000000000000/130.8)/math.log(2)),
         ("Z1", 1.0), ("Z3", 2.0), ("ZHALF", math.log(1.5)/math.log(2)), ("SAMPLER", 19.5),
         ("ZERO", 0.0), ("NEGZERO", -0.0), ("NEG", -0.58496250072), ("TINYNEG", -0.000000001),
         ("NINES", 0.999999999), ("NOISE", 0.1+0.2), ("BIG", 12345678.87654321), ("ONE_ULP_UNDER", 2.9999999999999996),
         ("CARRY", 0.99999999999), ("NEGCARRY", -4.99999999999), ("HUGE", 1e16), ("EDGE5", 99999.12345678), ("OVER5", 100000.5)]
for k, v in cases: print(f"{k} {cut8(v)}")
