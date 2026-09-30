# rt345_check.py - verify right-triangle-345-20260930T1323-0400 claims
# Exact Fraction arithmetic only. No float in the checked path.
# GOSUB style: each check is a subroutine returning (name, ok, detail).
from fractions import Fraction as F
import sys

RATIO = {"h": 3, "b": 4, "H": 5}          # height=3, base=4, hypotenuse=5

def gosub_unit(side, value):              # unit = known side / its ratio number
    return F(value) / RATIO[side]

def gosub_rebuild(unit):                  # unit times each ratio
    return {k: unit * r for k, r in RATIO.items()}

def gosub_root_check(t):                  # sqrt(a^2+b^2)=sqrt(c^2) <=> a^2+b^2=c^2 exactly
    return t["h"] ** 2 + t["b"] ** 2 == t["H"] ** 2

def check_unit_cases():
    cases = [("h", 3, 1), ("h", 15, 5), ("H", 25, 5), ("b", 8, 2),
             ("H", 5, 1), ("H", 10, 2), ("H", 7, F(7, 5)),
             ("h", F(21, 5), F(7, 5)), ("b", F(28, 5), F(7, 5))]
    bad = []
    for side, val, want in cases:
        u = gosub_unit(side, F(val))
        t = gosub_rebuild(u)
        if u != want or not gosub_root_check(t):
            bad.append((side, val, u))
    return "unit from any side (9 cases)", not bad, bad or "all roots matched"

def check_mismatch():                     # 3 and 5 as the two legs: units 1 and 5/4
    u1, u2 = gosub_unit("h", 3), gosub_unit("b", 5)
    ok = (u1 != u2) and (u2 == F(5, 4)) and (3**2 + 5**2 == 34)
    return "units disagree -> not 3-4-5, root needed (sqrt 34)", ok, (u1, u2)

def check_not_plus():                     # 3u+4u = 7u, never 5u
    bad = [u for u in (F(1), F(2), F(5), F(7, 5)) if 3*u + 4*u == 5*u]
    return "not plus: 3u+4u=7u != 5u (u=1,2,5,1.4)", not bad, "7,14,35,49/5"

def check_any_factor():                   # solve for any one factor
    tri = [(3, 4, 5), (15, 20, 25), (F(21, 5), F(28, 5), 7)]
    ok = all(a*a + b*b == c*c and c*c - b*b == a*a and c*c - a*a == b*b
             for a, b, c in tri)
    return "solve for any one factor", ok, "3-4-5, 15-20-25, 4.2-5.6-7"

def check_quadrants():                    # pair = (height, base); 5 keeps sign
    want = {1: (3, 4), 2: (3, -4), 3: (-3, -4), 4: (-3, 4)}
    sign = {1: (1, 1), 2: (1, -1), 3: (-1, -1), 4: (-1, 1)}  # (sin, cos)
    ok = all((3*sign[q][0], 4*sign[q][1]) == want[q] and
             (3*sign[q][0])**2 + (4*sign[q][1])**2 == 25 for q in want)
    return "four quadrants, all roots 5", ok, want

def check_fold_60():                      # 60 -> 60,120,240,300 all fold to 60
    def fold(d):                          # reference angle in the 0-90 store
        d %= 360
        return d if d <= 90 else 180 - d if d <= 180 else d - 180 if d <= 270 else 360 - d
    ok = [fold(d) for d in (60, 120, 240, 300)] == [60] * 4 and fold(360) == fold(0)
    return "stored 60 associates 60/120/240/300; 0 and 360 one wrap", ok, "fold ok"

def check_unit_circle():                  # PROPOSAL check: 3-4-5 is an exact rational point
    s, c = F(3, 5), F(4, 5)               # sin, cos of the 3-4-5 angle
    t = F(1, 3)                           # rational parameter: (1-t^2)/(1+t^2)=4/5, 2t/(1+t^2)=3/5
    ok = s*s + c*c == 1 and c == (1 - t*t)/(1 + t*t) and s == 2*t/(1 + t*t)
    return "3-4-5 = exact point (4/5, 3/5) on unit circle, t=1/3", ok, "no truncation"

CHECKS = [check_unit_cases, check_mismatch, check_not_plus, check_any_factor,
          check_quadrants, check_fold_60, check_unit_circle]

if __name__ == "__main__":
    fails = 0
    for fn in CHECKS:
        name, ok, detail = fn()
        print(("PASS " if ok else "FAIL ") + name + " | " + str(detail))
        fails += 0 if ok else 1
    # negative control: a wrong triangle must FAIL the root check
    neg = gosub_root_check({"h": F(3), "b": F(4), "H": F(6)})
    print(("PASS " if not neg else "FAIL ") + "negative control 3-4-6 rejected")
    fails += 1 if neg else 0
    print(f"{len(CHECKS)+1-fails}/{len(CHECKS)+1}")
    sys.exit(1 if fails else 0)
