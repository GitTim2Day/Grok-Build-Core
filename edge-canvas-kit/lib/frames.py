"""frames.py -- RGB frame data for the Canvas player, generated from the descending sampler.

SYNTHETIC: pixels are computed, not captured. 32 or 64 fps is the rate Timothy named
(MAP_PASS_1: "named, not measured"); dt = 1/32 s or 1/64 s exactly.
Pixel walk: the forward-difference table of f = m x^n + B advances one step per pixel,
row-major, continuing across frames.  R = floor(f) mod 256, G = floor(d1) mod 256,
B = floor(d2) mod 256 (0 when n < 2).  All arithmetic exact (integers over one common
denominator), so a rational dx stays exact.
"""
from __future__ import annotations
import base64
from fractions import Fraction
from math import lcm

from . import descend

FPS_ALLOWED = (32, 64)
MAX_W = MAX_H = 64
MAX_FRAMES = 64
MAX_PIXEL_STEPS = 64 * 64 * 32


class FramesError(ValueError):
    pass


def generate(fps=32, frames=8, w=32, h=32, m=5, n=3, B=7, x0=0, dx=3) -> dict:
    fps = descend._int_param(fps, "fps", 1, 1000)
    if fps not in FPS_ALLOWED:
        raise FramesError("fps must be 32 or 64")
    frames = descend._int_param(frames, "frames", 1, MAX_FRAMES)
    w = descend._int_param(w, "w", 1, MAX_W)
    h = descend._int_param(h, "h", 1, MAX_H)
    if frames * w * h > MAX_PIXEL_STEPS:
        raise FramesError(f"frames*w*h must be <= {MAX_PIXEL_STEPS}")
    M, Bb, X0, DX = (descend.exact(m, "m"), descend.exact(B, "B"), descend.exact(x0, "x0"), descend.exact(dx, "dx"))
    N = descend._int_param(n, "n", 0, 8)
    d = descend.table(M, N, Bb, X0, DX)
    D = 1
    for v in d:
        D = lcm(D, v.denominator)
    di = [int(v * D) for v in d]           # exact: every entry is an integer multiple of 1/D
    nn = len(di) - 1
    out = []
    for _ in range(frames):
        buf = bytearray(w * h * 3)        # the frame exists only while it is built (client shows or drops)
        j = 0
        for _p in range(w * h):
            buf[j] = (di[0] // D) % 256
            buf[j + 1] = (di[1] // D) % 256 if nn >= 1 else 0
            buf[j + 2] = (di[2] // D) % 256 if nn >= 2 else 0
            j += 3
            for k in range(nn):
                di[k] += di[k + 1]
        out.append(base64.b64encode(bytes(buf)).decode("ascii"))
    return {"fps": fps, "dt": f"1/{fps}", "shape": [frames, h, w, 3], "encoding": "base64 raw RGB, row-major",
            "frames": out, "synthetic": True,
            "source": "descending sampler f=m*x^n+B (computed, not a measured capture)",
            "params": {"m": descend.fmt(M), "n": N, "B": descend.fmt(Bb), "x0": descend.fmt(X0), "dx": descend.fmt(DX)},
            "end_value": descend.fmt(Fraction(di[0], D))}
