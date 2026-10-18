"""Numbers quoted in MAPPING.md (closed form, truncated never rounded)."""
import math, spiral_gear as sg
R = math.radians; T = sg.trunc
print("pitch-model ideal gear-2 travel over the missing-token slot [360-360/N, 360) deg,"
      " = re-sync jump of the hold rule:")
for N in (12, 24, 36, 72, 360):
    e = 360.0 - 360.0 / N
    trav = sg.TWO_PI - sg.theta2_closed(R(e))
    print(f"  N={N:4d} gap entry {T(e, 6)} deg: travel {T(trav, 9)} rad = {T(math.degrees(trav), 6)} deg"
          f" ({T(100 * trav / sg.TWO_PI, 6)} % of a gear-2 turn); ratio at entry {T(sg.ratio(R(e)), 9)}")
for d in (0.25, 2.25, 23.25, 356.5, 359.75):
    print(f"  shell (gear-1 contact radius r1/a) at {d} deg: {T(sg.r1(R(d)), 9)}; r2/a {T(sg.r2_from_line(R(d)), 9)}")
print(f"  step spans shells r/a from 1 to {T(sg.PHI**4, 12)} (length {T(sg.PHI**4 - 1, 12)} a)")
