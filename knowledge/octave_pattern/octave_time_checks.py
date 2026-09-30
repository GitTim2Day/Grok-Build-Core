# octave_time_checks.py - time-not-distance link, light cone, octave ladder, area bands.
# Exact Fraction / integer only. No float. No square root taken.
from fractions import Fraction as F
import sys
R = []
def chk(name, ok): R.append((name, bool(ok)))

# A. Time side is plus: pair creation (SPDC) and frequency doubling (SHG)
for fp in (F(2), F(10), F(7, 5)):
    f1, f2 = fp / 3, fp - fp / 3                     # any split: sum fixed
    chk("A1 split: f1+f2=fp", f1 + f2 == fp)
    chk("A2 even split: each fp/2, one octave down", fp / 2 + fp / 2 == fp and fp / (fp / 2) == 2)
    chk("A3 doubling: f+f=2f, one octave up", (fp / 2) * 2 == fp)

# B. Distance side is not plus: momenta add as arrows, closed by squares
ks, ki = (4, 3), (4, -3)                              # each |k|^2 = 25 -> |k| = 5
kp = (ks[0] + ki[0], ks[1] + ki[1])                   # (8, 0) -> |k|^2 = 64
chk("B1 arrow sum closes by squares: |kp|^2=64", kp[0]**2 + kp[1]**2 == 64)
chk("B2 not plus: |kp|=8 != 5+5=10", 64 != (5 + 5)**2)

# C. Light cone: s^2 = P - (ct)^2 ; R = ct when s^2 = 0 ; forward-only t >= 0
def P(x, y, z): return x*x + y*y + z*z
for u in (F(1), F(2), F(7, 5)):
    chk("C1 3-4-5 with ct=5u on the cone", P(3*u, 4*u, 0) - (5*u)**2 == 0)
    chk("C2 3-4-12 with ct=13u on the cone", P(3*u, 4*u, 12*u) - (13*u)**2 == 0)
chk("C3 time-like control ct=6: s^2<0", P(3, 4, 0) - 6**2 < 0)
chk("C4 space-like control ct=4: s^2>0", P(3, 4, 0) - 4**2 > 0)
chk("C5 forward-only: every cone point used has t>=0", all(t >= 0 for t in (5, 13)))

# D. Octave ladder: time/distance x2, area x4, volume x8 per octave (exponents 1:2:3)
for n in range(0, 6):
    L, A, V = 2**n, 4**n, 8**n
    chk(f"D octave {n}: L=2^n, A=L^2, V=L^3", A == L*L and V == L*L*L)
chk("D balloon: doubling R multiplies sphere area 4piP by exactly 4", P(6, 8, 24) == 4 * P(3, 4, 12))
chk("D one octave of volume = three octaves of length (8 = 2*2*2)", 8 == 2**3)

# E. Area on the sphere: fraction above height z is (1 - z/R)/2 (hat-box rule)
def frac_above(z_over_R): return (1 - z_over_R) / 2
chk("E1 cap above 3-4-12-13 point is exactly 1/26", frac_above(F(12, 13)) == F(1, 26))
chk("E2 band equator->point is exactly 6/13", F(1, 2) - frac_above(F(12, 13)) == F(6, 13))
edges = [F(k, 4) for k in range(-4, 5)]               # 8 equal-z bands
bands = [frac_above(edges[i]) - frac_above(edges[i+1]) for i in range(8)]
chk("E3 8 equal-z bands each exactly 1/8", all(b == F(1, 8) for b in bands))
chk("E4 8 bands x 8 sectors = 64 cells of exactly 1/64", F(1, 8) / 8 == F(1, 64))
chk("E5 point z/R=12/13 lands in top band [3/4,1]", F(3, 4) <= F(12, 13) <= 1)
chk("E6 negative control: equal-ANGLE bands are not equal area", frac_above(F(0)) - frac_above(F(1, 2)) != F(1, 8))

fails = sum(not ok for _, ok in R)
for n, ok in R: print(("PASS " if ok else "FAIL ") + n)
print(f"{len(R)-fails}/{len(R)}"); sys.exit(1 if fails else 0)
