"""sweep.py -- Spectrum Sweep for the Canvas tab (Timothy, 2026-10-06 4:49 PM ET).

REPRESENTATION ONLY: the sweep is drawn as colour and (optionally) played as sound. It does not emit
or detect real radio waves or light.

Mapping (Timothy's text): f = 130.8 * 2**y Hz, y = octave number (y = 0 -> 130.8 Hz).
Vertical axis: log10(f / Hz), decades ascending bottom -> top, 10**7 .. 10**16 Hz.
Redshift: f_obs = f_emit / (1 + z)  ->  a uniform downward shift of log2(1 + z) octaves.
Curve modes:
  octave  : y runs linearly in x from y(f_start) to y(f_end)   (default 100 MHz -> 1 PHz, near-UV)
  decay   : y = A + B*exp(-k*x) + L   (the image's form; defaults A=-1.6, B=5; L = whole-octave lift)
  sampler : y(x) = m*x**n + c walked by the descending fixed-step sampler (exact Fractions, additions only)
Numbers: inputs, x, z, 1+z and every rational y / f are exact Fractions. Truncated decimal strings come from
Decimal at 50 significant digits, cross-checked at 70 (refused if they differ), cut (ROUND_DOWN) to 8 places;
log2 of an exact power of two is returned exactly. Plot values are IEEE-754 binary64 floats (about 15-16
significant digits), sent as computed (not rounded). Python 3 standard library only.
"""
from __future__ import annotations
import math, re
from decimal import Decimal, localcontext, ROUND_DOWN
from fractions import Fraction

from . import descend

F0 = Fraction(1308, 10)            # 130.8 Hz at y = 0 (Timothy's mapping)
C_LIGHT = 299792458                # m/s, exact by SI definition
AXIS_EXPS = tuple(range(7, 17))    # log10(Hz) decades, ascending: 10 MHz (bottom) .. 10 PHz (top)
AXIS_LABELS = {7: "10 MHz", 8: "100 MHz", 9: "1 GHz", 10: "10 GHz", 11: "100 GHz", 12: "1 THz", 13: "10 THz",
               14: "100 THz", 15: "1 PHz", 16: "10 PHz"}
VIS_LO_HZ = 400 * 10**12           # visible window 400-790 THz (about 749.4-379.4 nm)
VIS_HI_HZ = 790 * 10**12
# Latin labels, one language only. Boundaries are approximate conventional ones, for display.
BANDS = (
    ("Radio", 10**7, 10**9),
    ("Undae minimae", 10**9, 3 * 10**11),
    ("Infrarubrum", 3 * 10**11, VIS_LO_HZ),
    ("Visibile (lumen)", VIS_LO_HZ, VIS_HI_HZ),
    ("Ultravioletum", VIS_HI_HZ, 10**16),
)
OVERLAY_DEFAULT = "Lux orta est, et umbra recessit ... Frequens in aeternum"
NOTE = ("Visual and audio representation only: this sweep does not emit or detect real radio waves or light.")
PRECISION = ("exact: inputs, x, z, 1+z, rational y and f (Fractions); *_trunc8: Decimal 50 digits (checked at 70), "
             "truncated to 8 places, never rounded; floats: IEEE-754 binary64 (~15-16 significant digits), as computed")

FPS_ALLOWED = (32, 64)
MIN_SAMPLES, MAX_SAMPLES = 2, 1024
MAX_Z = 10000
F_MIN_HZ, F_MAX_HZ = 1, 10**20
MAX_AB, MAX_K, MAX_XMAX, MAX_LIFT = 64, 64, 100, 64
MAX_STEPS = MAX_SAMPLES - 1
MAX_ABS_Y = 200
MAX_OVERLAY = 200
AUDIO_LO_HZ, AUDIO_HI_HZ, AUDIO_TOP_HZ = 20, 20000, 16000
_NUM = re.compile(r"^[+-]?(?:\d{1,30}(?:\.\d{1,30})?(?:[eE][+-]?\d{1,3})?|\d{1,30}/\d{1,30})$")
_CTRL = re.compile(r"[\x00-\x1f\x7f\u2028\u2029]")
_LOG10_F0 = math.log10(130.8)
_LOG10_2 = math.log10(2)


class SweepError(ValueError):
    pass


# ------------------------------------------------------------------ parsing (fail closed)
def num(v, name: str) -> Fraction:
    """int, or an exact string: 7, -1.6, 1/4, 1e8, 5e14. Floats, bools, NaN/inf, junk refused."""
    if isinstance(v, bool):
        raise SweepError(f"{name}: bool refused")
    if isinstance(v, int):
        return Fraction(v)
    if not isinstance(v, str):
        raise SweepError(f"{name}: pass an integer or an exact string (floats refused)")
    s = v.strip()
    if len(s) > 64 or not _NUM.match(s):
        raise SweepError(f"{name}: not an exact number (use 7, -1.6, 1/4, 1e8)")
    try:
        return Fraction(s)
    except (ZeroDivisionError, ValueError):
        raise SweepError(f"{name}: zero denominator refused")


def _in(v: Fraction, name: str, lo, hi, lo_open=False):
    if v > hi or v < lo or (lo_open and v == lo):
        raise SweepError(f"{name}: must be {'>' if lo_open else '>='} {lo} and <= {hi}")
    return v


def _int(v, name, lo, hi) -> int:
    try:
        return descend._int_param(v, name, lo, hi)
    except descend.DescendError as e:
        raise SweepError(str(e))


def _samples(v) -> int:
    N = _int(v, "samples", 1, 10**8)
    if N > MAX_SAMPLES:
        raise SweepError(f"samples: at most {MAX_SAMPLES}")
    if N < MIN_SAMPLES:
        raise SweepError(f"samples: at least {MIN_SAMPLES}")
    return N


def fmt(q: Fraction) -> str:
    """Exact text: a finite decimal when the denominator is 2^a*5^b (e.g. -1.6), else num/den (e.g. -1/3)."""
    d, a = q.denominator, 0
    while d % 2 == 0:
        d //= 2
        a += 1
    b = 0
    while d % 5 == 0:
        d //= 5
        b += 1
    if d != 1 or q.denominator == 1:
        return descend.fmt(q)
    places = max(a, b)
    v = abs(q.numerator) * (10 ** places // q.denominator)
    sgn = "-" if q < 0 else ""
    return f"{sgn}{v // 10**places}.{str(v % 10**places).zfill(places)}"


# ------------------------------------------------------------------ exact / truncated helpers
def _pow2_exponent(q: Fraction):
    """k if q == 2**k exactly (k integer), else None."""
    n, d = q.numerator, q.denominator
    if n > 0 and n & (n - 1) == 0 and d & (d - 1) == 0:
        return (n.bit_length() - 1) - (d.bit_length() - 1)
    return None


def _cut(d: Decimal, places=8) -> str:
    with localcontext() as ctx:
        ctx.prec = 120
        t = format(d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_DOWN), "f")   # never scientific (no 0E-8)
        return t[1:] if t.startswith("-") and not t.strip("-0.") else t                # no "-0.00000000"


def _log2_dec(q: Fraction, prec: int) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = prec
        return (Decimal(q.numerator) / Decimal(q.denominator)).ln() / Decimal(2).ln()


def log2_trunc8(q: Fraction) -> str:
    """log2(q) truncated (never rounded) to 8 places; exact for powers of two; refused if unstable."""
    if q <= 0:
        raise SweepError("log2 of a non-positive number refused")
    k = _pow2_exponent(q)
    if k is not None:
        return f"{k}.00000000"
    a, b = _cut(_log2_dec(q, 50)), _cut(_log2_dec(q, 70))
    if a != b:
        raise SweepError("truncation not stable at 50 vs 70 digits (refused)")
    return a


def hz_from_y_trunc(y: Fraction, places=3) -> str:
    """130.8 * 2**y Hz for an exact y, truncated to `places` decimals (exact when y is an integer)."""
    if y.denominator == 1:
        return _cut(Decimal((F0 * Fraction(2) ** int(y)).numerator) / Decimal((F0 * Fraction(2) ** int(y)).denominator), places)
    outs = []
    for prec in (50, 70):
        with localcontext() as ctx:
            ctx.prec = prec
            yd = Decimal(y.numerator) / Decimal(y.denominator)
            outs.append(_cut((Decimal(1308) / Decimal(10)) * (Decimal(2) ** yd), places))
    if outs[0] != outs[1]:
        raise SweepError("truncation not stable (refused)")
    return outs[0]


def y_of_hz(f_hz: Fraction) -> float:
    return math.log2(float(f_hz / F0))


def log10_hz_of_y(y: float) -> float:
    return _LOG10_F0 + y * _LOG10_2


def observed(f_emit, one_plus_z):
    """Redshift: f_obs = f_emit / (1 + z). Works for Fractions (exact) and floats."""
    return f_emit / one_plus_z


# ------------------------------------------------------------------ colour
def wavelength_to_rgb(nm: float):
    """Visible wavelength (nm) -> (r, g, b) 0..255. Piecewise-linear spectrum (Bruton style), edge fall-off,
    gamma 0.8; channels TRUNCATED to integers (not rounded). Clamped to 380..780 nm."""
    lam = min(max(float(nm), 380.0), 780.0)
    if lam < 440:
        r, g, b = (440 - lam) / (440 - 380), 0.0, 1.0
    elif lam < 490:
        r, g, b = 0.0, (lam - 440) / (490 - 440), 1.0
    elif lam < 510:
        r, g, b = 0.0, 1.0, (510 - lam) / (510 - 490)
    elif lam < 580:
        r, g, b = (lam - 510) / (580 - 510), 1.0, 0.0
    elif lam < 645:
        r, g, b = 1.0, (645 - lam) / (645 - 580), 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    if lam < 420:
        fac = 0.3 + 0.7 * (lam - 380) / (420 - 380)
    elif lam <= 700:
        fac = 1.0
    else:
        fac = 0.3 + 0.7 * (780 - lam) / (780 - 700)
    return tuple(int(255 * (c * fac) ** 0.8) if c > 0 else 0 for c in (r, g, b))


LOG_VIS_LO, LOG_VIS_HI = math.log10(VIS_LO_HZ), math.log10(VIS_HI_HZ)
LOG_AXIS_LO, LOG_AXIS_HI = 7.0, 16.0


def rgb_for_log10_hz(L: float):
    """Frame colour for a frequency: visible -> wavelength colour (lambda = c/f); below visible -> deep red
    fading to dim; above visible -> violet fading to dim."""
    if L < LOG_VIS_LO:
        t = min(max((L - LOG_AXIS_LO) / (LOG_VIS_LO - LOG_AXIS_LO), 0.0), 1.0)
        return (40 + int(100 * t), 0, 0)
    if L > LOG_VIS_HI:
        t = min(max((L - LOG_VIS_HI) / (LOG_AXIS_HI - LOG_VIS_HI), 0.0), 1.0)
        s = 0.2 + 0.8 * (1.0 - t)
        return (int(120 * s), 0, int(200 * s))
    return wavelength_to_rgb(C_LIGHT / 10 ** L * 1e9)


def band_of(L: float) -> str:
    for name, lo, hi in BANDS:
        if math.log10(lo) <= L < math.log10(hi) or (name == BANDS[-1][0] and L == math.log10(hi)):
            return name
    return "below axis" if L < LOG_AXIS_LO else "above axis"


def axis():
    return [{"exp": e, "hz": f"1e{e}", "label": AXIS_LABELS[e]} for e in AXIS_EXPS]


def bands():
    return [{"name": n, "lo_hz": str(lo), "hi_hz": str(hi), "lo_log10": math.log10(lo), "hi_log10": math.log10(hi),
             "highlight": lo == VIS_LO_HZ and hi == VIS_HI_HZ} for n, lo, hi in BANDS]


# ------------------------------------------------------------------ key values
def key_values(z: Fraction = Fraction(0)) -> dict:
    opz = 1 + z
    return {"y_at_100MHz_trunc8": log2_trunc8(Fraction(10**8) / F0),
            "y_at_500THz_trunc8": log2_trunc8(Fraction(5 * 10**14) / F0),
            "z": fmt(z), "one_plus_z": fmt(opz), "z_shift_octaves_trunc8": log2_trunc8(opz),
            "z_shift_octaves_float": math.log2(float(opz)),
            "f0_hz": "654/5", "c_m_per_s": str(C_LIGHT)}


def overlay_ok(text) -> str:
    if not isinstance(text, str) or len(text) > MAX_OVERLAY:
        raise SweepError(f"overlay: one line of at most {MAX_OVERLAY} characters")
    if _CTRL.search(text):
        raise SweepError("overlay: must be a single unbroken line (no line breaks or control characters)")
    return text


# ------------------------------------------------------------------ main entry
def generate(mode="octave", samples=256, z="0", fps=32, f_start="100000000", f_end="1000000000000000",
             A="-1.6", B="5", k="1", xmax="5", lift=21, m="-1/4", n=1, c="42", x0="0", dx="1", steps=90,
             overlay=OVERLAY_DEFAULT) -> dict:
    if mode not in ("octave", "decay", "sampler"):
        raise SweepError("mode must be octave, decay or sampler")
    fps = _int(fps, "fps", 1, 1000)
    if fps not in FPS_ALLOWED:
        raise SweepError("fps must be 32 or 64")
    Z = num(z, "z")
    if Z < 0 or Z > MAX_Z:
        raise SweepError(f"z: must be >= 0 and <= {MAX_Z}")
    overlay = overlay_ok(overlay)
    opz = 1 + Z
    opz_f = float(opz)
    pts = []                       # (x Fraction, y_emit float, y_exact Fraction|None, f_emit_exact Fraction|None)
    final = None
    if mode == "octave":
        N = _samples(samples)
        fs = _in(num(f_start, "f_start"), "f_start", F_MIN_HZ, F_MAX_HZ)
        fe = _in(num(f_end, "f_end"), "f_end", F_MIN_HZ, F_MAX_HZ)
        ys, ye = y_of_hz(fs), y_of_hz(fe)
        for i in range(N):
            x = Fraction(i, N - 1)
            y = ys + float(x) * (ye - ys)
            fx = fs if i == 0 else fe if i == N - 1 else None
            yx = Fraction(_pow2_exponent(fx / F0)) if fx is not None and _pow2_exponent(fx / F0) is not None else None
            pts.append((x, y, yx, fx))
        formula = (f"y = y(f_start) + (y(f_end) - y(f_start))*x, x = 0..1; f = 130.8*2^y Hz; "
                   f"f_start = {fmt(fs)} Hz (y {log2_trunc8(fs / F0)}), f_end = {fmt(fe)} Hz (y {log2_trunc8(fe / F0)})")
        params = {"f_start": fmt(fs), "f_end": fmt(fe), "samples": N}
    elif mode == "decay":
        N = _samples(samples)
        Aq = _in(num(A, "A"), "A", -MAX_AB, MAX_AB)
        Bq = _in(num(B, "B"), "B", -MAX_AB, MAX_AB)
        kq = _in(num(k, "k"), "k", 0, MAX_K)
        Xq = _in(num(xmax, "xmax"), "xmax", 0, MAX_XMAX, lo_open=True)
        L = _int(lift, "lift", 0, MAX_LIFT)
        kf, Af, Bf = float(kq), float(Aq), float(Bq)
        for i in range(N):
            x = Xq * Fraction(i, N - 1)
            xf = float(x)
            e = math.exp(-kf * xf)
            y = Af + Bf * e + L
            yx = Aq + Bq + L if i == 0 else None
            fx = F0 * Fraction(2) ** int(yx) if yx is not None and yx.denominator == 1 else None
            pts.append((x, y, yx, fx))
        formula = f"y = {fmt(Aq)} + {fmt(Bq)}*exp(-{fmt(kq)}*x) + {L}   (image form y = A + B*exp(-k*x), lifted {L} whole octaves; shape kept), x = 0..{fmt(Xq)}"
        params = {"A": fmt(Aq), "B": fmt(Bq), "k": fmt(kq), "xmax": fmt(Xq), "lift": L, "samples": N}
    else:
        M, Cc, X0, DX = (descend.exact(m, "m"), descend.exact(c, "c"), descend.exact(x0, "x0"), descend.exact(dx, "dx"))
        Nn = _int(n, "n", 0, 8)
        S = _int(steps, "steps", 0, 10**8)
        if S > MAX_STEPS:
            raise SweepError(f"steps: at most {MAX_STEPS}")
        if S < 1:
            raise SweepError("steps: at least 1")
        d = descend.table(M, Nn, Cc, X0, DX)
        ys = [d[0]]
        for _ in range(S):                       # descending update, additions only
            for j in range(Nn):
                d[j] += d[j + 1]
            ys.append(d[0])
        closed = M * (X0 + S * DX) ** Nn + Cc
        if ys[-1] != closed:
            raise SweepError("sampler walk != closed form (refused)")
        for i, yq in enumerate(ys):
            if abs(yq) > MAX_ABS_Y:
                raise SweepError(f"sampler: |y| must stay <= {MAX_ABS_Y}")
            fx = F0 * Fraction(2) ** int(yq) if yq.denominator == 1 else None
            pts.append((X0 + i * DX, float(yq), yq, fx))
        N = len(pts)
        formula = f"y(x) = {fmt(M)}*x^{Nn} + {fmt(Cc)}, x = {fmt(X0)} + i*{fmt(DX)}, i = 0..{S} (descending sampler, exact; prints the final value only)"
        params = {"m": fmt(M), "n": Nn, "c": fmt(Cc), "x0": fmt(X0), "dx": fmt(DX), "steps": S}
        yfin = ys[-1]
        final = {"y": fmt(yfin), "y_trunc8": _cut(Decimal(yfin.numerator) / Decimal(yfin.denominator)),
                 "f_emit_hz_trunc3": hz_from_y_trunc(yfin), "y_obs_trunc8": None, "f_obs_hz_trunc3": None}
        if _pow2_exponent(opz) is not None:
            yo = yfin - _pow2_exponent(opz)
            final["y_obs_trunc8"] = _cut(Decimal(yo.numerator) / Decimal(yo.denominator))
            final["f_obs_hz_trunc3"] = hz_from_y_trunc(yo)
        else:
            final["y_obs_note"] = "observed y = y - log2(1+z) is irrational for this z; see key_values"
    out = []
    ymax = -1e300
    for i, (x, y, yx, fx) in enumerate(pts):
        if abs(y) > MAX_ABS_Y:
            raise SweepError(f"|y| must stay <= {MAX_ABS_Y}")
        y_obs = math.log2(observed(2.0 ** y, opz_f))
        Le, Lo = log10_hz_of_y(y), log10_hz_of_y(y_obs)
        ymax = max(ymax, y, y_obs)
        s = {"i": i, "x": fmt(x), "y_emit": y, "y_obs": y_obs, "log10_f_emit": Le, "log10_f_obs": Lo,
             "rgb_obs": list(rgb_for_log10_hz(Lo)), "band_obs": band_of(Lo)}
        if yx is not None:
            s["y_emit_exact"] = fmt(yx)
        if fx is not None:
            s["f_emit_exact_hz"] = fmt(fx)
            s["f_obs_exact_hz"] = fmt(observed(fx, opz))
        out.append(s)
    T = math.ceil(ymax - math.log2(AUDIO_TOP_HZ / 130.8))
    aud = sum(1 for s in out if AUDIO_LO_HZ <= 130.8 * 2.0 ** (s["y_obs"] - T) <= AUDIO_HI_HZ)
    return {"mode": mode, "fps": fps, "dt": f"1/{fps}", "params": params, "formula": formula,
            "mapping": "f = 130.8 * 2^y Hz (y = octave number)", "redshift": "f_obs = f_emit / (1 + z)",
            "key_values": key_values(Z), "axis": axis(), "bands": bands(),
            "visible_band_hz": [str(VIS_LO_HZ), str(VIS_HI_HZ)], "samples": out, "final": final,
            "audio": {"transpose_octaves": T, "rule": "y_audio = y - T (whole octaves; shape kept); left = observed, right = emitted",
                      "audible_fraction": fmt(Fraction(aud, len(out))), "default": "off",
                      "note": "audio is a representation only, transposed into hearing range"},
            "overlay": overlay, "overlay_default": OVERLAY_DEFAULT, "note": NOTE, "precision": PRECISION,
            "synthetic": True}


if __name__ == "__main__":
    kv = key_values(Fraction(1))
    print("Y100", kv["y_at_100MHz_trunc8"])
    print("Y500", kv["y_at_500THz_trunc8"])
    for zz in ("1", "3", "1/2"):
        print("SHIFT z=" + zz, log2_trunc8(1 + Fraction(zz)))
    r = generate(mode="sampler")
    print("SAMPLER_FINAL", r["final"]["y"])
