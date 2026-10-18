"""Golden-spiral non-circular gear pair: kinematics and a motor->joint mapping.

Source idea: X post 2111496987157917916 by @matharium (2026-10-17 12:38:06 EDT).
  r(theta) = a * phi**(2*theta/pi), one turn, closed by a straight step,
  axles D = a*(1 + phi**4) apart, r1 + r2 = D, w2/w1 = r1/r2.
The video attached to that post was NOT watched. Everything here is derived from
the quoted text only. All lengths are in units of a (a = 1 unless passed in).

Convention (chosen here, not taken from the post):
  gear 1 = motor side (input), angle t1 in [0, 2*pi) measured from the step,
  contact radius on gear 1 grows from a (t1 = 0) to a*phi**4 (t1 -> 2*pi).
  gear 2 = joint side (output), angle t2 starts at 0 with contact at r2 = a*phi**4.
Stdlib only.
"""
import math

PHI = (1.0 + math.sqrt(5.0)) / 2.0
K = 2.0 * math.log(PHI) / math.pi          # r = a*exp(K*theta)
TWO_PI = 2.0 * math.pi


def D_of(a=1.0):
    return a * (1.0 + PHI ** 4)


def r_spiral(theta, a=1.0):
    """Spiral radius at body angle theta in [0, 2*pi]."""
    return a * PHI ** (2.0 * theta / math.pi)


def r1(t1, a=1.0):
    return r_spiral(t1 % TWO_PI, a)


def r2_from_line(t1, a=1.0):
    """Gear-2 contact radius required by the line-of-centres condition."""
    return D_of(a) - r1(t1, a)


def ratio(t1, a=1.0):
    """w2/w1 = r1/r2 at motor angle t1 (single turn, t1 in [0, 2*pi))."""
    x = r1(t1, a)
    return x / (D_of(a) - x)


# ---------- numerical integration (the method asked for) ----------
def _integrand(t, a):
    x = r_spiral(t, a)
    return x / (D_of(a) - x)


def theta2_numeric(t1, a=1.0, n=2000):
    """theta2(t1) = integral_0^t1 r1/r2 dt by composite Simpson, n even panels.
    Single turn only: t1 in [0, 2*pi]."""
    if not (0.0 <= t1 <= TWO_PI):
        raise ValueError("t1 outside one turn [0, 2*pi]")
    if n % 2:
        n += 1
    if t1 == 0.0:
        return 0.0
    h = t1 / n
    s = _integrand(0.0, a) + _integrand(t1, a)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * _integrand(i * h, a)
    return s * h / 3.0


def theta2_closed(t1, a=1.0):
    """Closed form of the same integral (used only to check the numeric one):
    theta2 = (1/K) * ln((D - a) / (D - a*exp(K*t1)))."""
    D = D_of(a)
    return math.log((D - a) / (D - a * math.exp(K * t1))) / K


def theta1_closed(t2, a=1.0):
    """Inverse of theta2_closed on one turn."""
    D = D_of(a)
    return math.log((D - (D - a) * math.exp(-K * t2)) / a) / K


def r2_profile(t2, a=1.0):
    """Gear 2's OWN spiral radius at the body angle currently on the line of
    centres. Gear 2 is the same spiral; body angle at contact = 2*pi - t2."""
    return r_spiral(TWO_PI - t2, a)


# ---------- lookup-table transmission (motor -> joint) ----------
class SpiralGearTransmission:
    """Motor (gear 1) <-> joint (gear 2) mapping, multi-turn, built from a
    numerically integrated table with linear interpolation of theta2 and an
    exact ratio for velocity/effort. Ideal, lossless, rigid, zero backlash:
    those are ASSUMPTIONS, none is measured.

    extra_reduction: optional fixed reduction after gear 2 (joint = gear2/N).
    """

    def __init__(self, a=1.0, table_points=4097, simpson_n=64, extra_reduction=1.0):
        if table_points < 3:
            raise ValueError("table_points >= 3")
        if extra_reduction <= 0:
            raise ValueError("extra_reduction > 0")
        self.a = a
        self.N = float(extra_reduction)
        self.t1 = [TWO_PI * i / (table_points - 1) for i in range(table_points)]
        # cumulative Simpson panel-by-panel
        self.t2 = [0.0]
        acc = 0.0
        for i in range(1, table_points):
            lo, hi = self.t1[i - 1], self.t1[i]
            m = simpson_n
            h = (hi - lo) / m
            s = _integrand(lo, a) + _integrand(hi, a)
            for j in range(1, m):
                s += (4 if j % 2 else 2) * _integrand(lo + j * h, a)
            acc += s * h / 3.0
            self.t2.append(acc)
        self.turn_out = self.t2[-1]   # should be 2*pi

    @staticmethod
    def _split(x):
        turns = math.floor(x / TWO_PI)
        frac = x - turns * TWO_PI
        if frac >= TWO_PI:          # float guard
            turns += 1
            frac = 0.0
        return turns, frac

    @staticmethod
    def _interp(xs, ys, x):
        """Piecewise-linear y(x) on a strictly increasing table xs."""
        import bisect
        i = bisect.bisect_right(xs, x) - 1
        i = max(0, min(i, len(xs) - 2))
        x0, x1 = xs[i], xs[i + 1]
        y0, y1 = ys[i], ys[i + 1]
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

    # ros2_control-style names (actuator = motor = gear 1)
    def actuator_to_joint_position(self, motor_angle):
        turns, frac = self._split(motor_angle)
        g2 = turns * self.turn_out + self._interp(self.t1, self.t2, frac)
        return g2 / self.N

    def joint_to_actuator_position(self, joint_angle):
        g2 = joint_angle * self.N
        turns = math.floor(g2 / self.turn_out)
        frac = g2 - turns * self.turn_out
        return turns * TWO_PI + self._interp(self.t2, self.t1, frac)

    def ratio_at(self, motor_angle):
        _, frac = self._split(motor_angle)
        return ratio(frac, self.a) / self.N      # joint_vel / motor_vel

    def actuator_to_joint_velocity(self, motor_angle, motor_vel):
        return motor_vel * self.ratio_at(motor_angle)

    def joint_to_actuator_velocity(self, motor_angle, joint_vel):
        return joint_vel / self.ratio_at(motor_angle)

    def actuator_to_joint_effort(self, motor_angle, motor_effort):
        # ideal power balance: tau_j * w_j = tau_m * w_m
        return motor_effort / self.ratio_at(motor_angle)

    def joint_to_actuator_effort(self, motor_angle, joint_effort):
        return joint_effort * self.ratio_at(motor_angle)


def trunc(x, places):
    """Truncate (never round) a float's shortest repr to `places` decimals."""
    from decimal import Decimal, ROUND_DOWN
    q = Decimal(1).scaleb(-places)
    return str(Decimal(repr(float(x))).quantize(q, rounding=ROUND_DOWN))


def trunc_sci(x, digits=3):
    """Scientific notation with `digits` mantissa decimals, TRUNCATED (never rounded),
    from the float's shortest repr."""
    from decimal import Decimal, ROUND_DOWN
    d = Decimal(repr(float(x)))
    if d == 0:
        return "0." + "0" * digits + "e+00"
    sign = "-" if d < 0 else ""
    d = abs(d)
    e = d.adjusted()
    m = (d.scaleb(-e)).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_DOWN)
    return f"{sign}{m}e{e:+03d}"
