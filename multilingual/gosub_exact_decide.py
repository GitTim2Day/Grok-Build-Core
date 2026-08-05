#!/usr/bin/env python3
"""
gosub_exact_decide.py — First shared subroutine
Exact margin → verdict / standing → five-pillar seal.

This is the single decision gate.
lid_exact and edge_adapter_control both call it.
No other translation or adapter work runs before it.

Version Clean. Finite. Musical. No infinity. No Zero's.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Dict, Optional
import hashlib
import time


class Standing(str, Enum):
    EXACT = "EXACT"
    INTERPOLATED = "INTERPOLATED"
    MEASURED = "MEASURED"
    UNDEF = "UNDEF"
    ABANDONED = "ABANDONED"
    IDLE = "IDLE"


class Verdict(str, Enum):
    PASSTHROUGH = "PASSTHROUGH"
    HELD = "HELD"
    TRANSLATED = "TRANSLATED"


@dataclass(frozen=True)
class ExactDecision:
    top_lang: Optional[str]
    margin: Fraction
    verdict: Verdict
    standing: Standing
    value_standing: Standing
    domain_repaired_from: Optional[str]
    exposure: int
    ts: float
    content_hash: str


def GOSUB_EXACT_MARGIN(scores: Dict[str, Fraction]):
    if not scores:
        return None, Fraction(0)
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    top_lang, top = ranked[0]
    second = ranked[1][1] if len(ranked) > 1 else Fraction(0)
    return top_lang, top - second


def GOSUB_EXACT_DECIDE(
    scores: Dict[str, Fraction],
    repaired: bool = False,
    repaired_from: Optional[str] = None,
    confident: Fraction = Fraction(5, 2),
    hold: Fraction = Fraction(1, 2),
) -> ExactDecision:
    top_lang, margin = GOSUB_EXACT_MARGIN(scores)
    exposure = len(scores)
    value_standing = Standing.INTERPOLATED if repaired else Standing.EXACT

    if top_lang is None:
        verdict, standing, value_standing = Verdict.HELD, Standing.UNDEF, Standing.UNDEF
    elif repaired:
        verdict = Verdict.HELD
        standing = Standing.MEASURED if margin >= hold else Standing.UNDEF
    else:
        if margin >= confident:
            verdict, standing = Verdict.PASSTHROUGH, Standing.EXACT
        elif margin >= hold:
            verdict, standing = Verdict.HELD, Standing.MEASURED
        else:
            verdict, standing = Verdict.HELD, Standing.UNDEF

    ts = time.time()
    payload = f"{top_lang}|{margin}|{verdict}|{standing}|{value_standing}|{repaired_from}|{exposure}|{ts}"
    content_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]

    return ExactDecision(
        top_lang=top_lang, margin=margin, verdict=verdict,
        standing=standing, value_standing=value_standing,
        domain_repaired_from=repaired_from, exposure=exposure,
        ts=ts, content_hash=content_hash,
    )


if __name__ == "__main__":
    scores = {"es": Fraction(1), "fr": Fraction(1, 5)}
    d1 = GOSUB_EXACT_DECIDE(scores)
    d2 = GOSUB_EXACT_DECIDE(scores, repaired=True, repaired_from="mojibake")
    assert d1.margin == d2.margin
    assert d2.value_standing == Standing.INTERPOLATED
    assert d2.standing != Standing.EXACT
    print("First subroutine OK.")
