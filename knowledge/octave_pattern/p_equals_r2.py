# p_equals_r2.py - P = x^2+y^2+z^2 = R^2 on the 3-4-5 plane and the 3-4-12 lift.
# Exact Fraction only. No float, no square root taken.
from fractions import Fraction as F
import sys
def P(x, y, z): return x*x + y*y + z*z
res = []
for u in (F(1), F(2), F(7, 5)):
    rho = 5*u
    res.append(("plane z=0: P=25u^2=R^2, R=5u=rho", P(3*u, 4*u, 0) == 25*u*u == rho*rho))
    R = 13*u
    res.append(("lift: P=169u^2=R^2, R=13u", P(3*u, 4*u, 12*u) == 169*u*u == R*R))
    res.append(("lift = second right triangle rho^2+z^2=R^2 (5-12-13)", rho*rho + (12*u)**2 == R*R))
    res.append(("not plus: 3u+4u+12u=19u != 13u", 3*u + 4*u + 12*u != R))
# exact point on the unit sphere (divide by R)
x, y, z = F(3, 13), F(4, 13), F(12, 13)
res.append(("unit sphere point (3/13,4/13,12/13): P=1", P(x, y, z) == 1))
res.append(("latitude exact: cos=rho/R=5/13, sin=z/R=12/13", F(5, 13)**2 + F(12, 13)**2 == 1))
res.append(("negative control 3-4-11 is not R=13", P(3, 4, 11) != 169))
fails = sum(not ok for _, ok in res)
for n, ok in res: print(("PASS " if ok else "FAIL ") + n)
print(f"{len(res)-fails}/{len(res)}"); sys.exit(1 if fails else 0)
