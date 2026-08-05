#!/usr/bin/env python3
"""tims_base_map.py — Map binary addressing onto Tim's Tables cyclic bases (6/8/10/12)."""
from __future__ import annotations
from fractions import Fraction
from dataclasses import dataclass
from typing import List, Tuple

TIMS_SPOKES = [Fraction(0), Fraction(1,10), Fraction(1,8), Fraction(1,6), Fraction(1,4), Fraction(1,3), Fraction(1,2), Fraction(2,3), Fraction(3,4), Fraction(1)]
CANDIDATE_BASES = (2, 6, 8, 10, 12)

@dataclass(frozen=True)
class BaseScore:
    base: int
    hit_count: int
    coverage: Fraction
    residual: Fraction
    note: str

def GOSUB_BASE_ALIGNMENT(base: int, spokes=None):
    spokes = spokes or TIMS_SPOKES
    step = Fraction(1, base)
    hits = 0
    residual_sum = Fraction(0)
    miss_count = 0
    for s in spokes:
        if (s / step).denominator == 1:
            hits += 1
        else:
            k = s / step
            below = Fraction(int(k), 1) * step
            above = below + step
            residual_sum += min(abs(s - below), abs(s - above))
            miss_count += 1
    coverage = Fraction(hits, len(spokes))
    residual = (residual_sum / miss_count) if miss_count else Fraction(0)
    notes = {8: "base-8 contact points invariant", 6: "sexagesimal / 36 bridge", 12: "doubles base-6; 36 residual", 10: "decimal; 1/10 primary spoke", 2: "native binary reference"}
    return BaseScore(base, hits, coverage, residual, notes.get(base, ""))

def GOSUB_RANK_BASES():
    scores = [GOSUB_BASE_ALIGNMENT(b) for b in CANDIDATE_BASES]
    scores.sort(key=lambda s: (-s.coverage, s.residual))
    return scores

def GOSUB_MAP_BINARY_INDEX(index: int, bit_width: int, target_base: int):
    if target_base < 2: raise ValueError("base must be >= 2")
    digits = []
    n = index
    max_val = (1 << bit_width) - 1
    places = 1
    span = target_base
    while span <= max_val:
        places += 1
        span *= target_base
    for _ in range(places):
        digits.append(n % target_base)
        n //= target_base
    return tuple(reversed(digits))

if __name__ == "__main__":
    for s in GOSUB_RANK_BASES():
        print(f"base {s.base}: coverage={s.coverage} residual={s.residual} {s.note}")
