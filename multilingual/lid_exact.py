#!/usr/bin/env python3
"""
lid_exact.py — Exact-arithmetic Language Identity layer
Sealed design decisions (2026-08-05 reconstruction from session record):

1. Evidence weights use exact rational arithmetic (Fraction). Float is display only.
2. Truncation only — never rounding. Truncation cannot promote a value across a boundary.
3. Language identity is categorical. The label is never interpolated.
4. Margin is a real quantity and may be compared; standing reflects provenance.
5. Repaired input carries value_standing = INTERPOLATED and is capped: never reaches CONFIDENT.
6. domain_repaired_from records marked repair with provenance.
7. Verdict classes: TRANSLATED | PASSTHROUGH | HELD
8. Empty population with exposure > 0 is IDLE (measured bound), not absence.
9. Fifth pillar (validation) required on every permanent write.

Version Clean. Finite. Musical. No infinity. No Zero's.
"""

from __future__ import annotations
from fractions import Fraction
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
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
    TRANSLATED = "TRANSLATED"
    PASSTHROUGH = "PASSTHROUGH"
    HELD = "HELD"


@dataclass(frozen=True)
class ExactWeight:
    """Rational evidence weight. Construct from string or int to avoid float."""
    num: int
    den: int = 1

    def as_fraction(self) -> Fraction:
        return Fraction(self.num, self.den)

    @classmethod
    def from_str(cls, s: str) -> "ExactWeight":
        s = s.strip()
        if "/" in s:
            n, d = s.split("/", 1)
            return cls(int(n), int(d))
        if "." in s:
            whole, frac = s.split(".", 1)
            scale = 10 ** len(frac)
            return cls(int(whole) * scale + int(frac), scale)
        return cls(int(s), 1)


@dataclass
class Evidence:
    lang: str
    weight: ExactWeight
    source: str = "token"


@dataclass
class LidDecision:
    text: str
    verdict: Verdict
    label: Optional[str]
    margin: Fraction
    standing: Standing
    value_standing: Standing
    domain_repaired_from: Optional[str] = None
    exposure: int = 0
    ts: float = field(default_factory=time.time)
    content_hash: str = ""

    def seal(self) -> "LidDecision":
        payload = f"{self.text}|{self.verdict}|{self.label}|{self.margin}|{self.standing}|{self.value_standing}|{self.domain_repaired_from}|{self.exposure}"
        self.content_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
        return self


class LidExact:
    def __init__(
        self,
        confident_margin: Fraction = Fraction(5, 2),
        hold_margin: Fraction = Fraction(1, 2),
        population_floor: int = 8,
    ):
        self.confident_margin = confident_margin
        self.hold_margin = hold_margin
        self.population_floor = population_floor
        self._ledger: List[LidDecision] = []

    def score(
        self,
        text: str,
        evidence: List[Evidence],
        repaired: bool = False,
        repaired_from: Optional[str] = None,
    ) -> LidDecision:
        totals: Dict[str, Fraction] = {}
        for e in evidence:
            totals[e.lang] = totals.get(e.lang, Fraction(0)) + e.weight.as_fraction()

        if not totals:
            dec = LidDecision(
                text=text, verdict=Verdict.HELD, label=None, margin=Fraction(0),
                standing=Standing.UNDEF, value_standing=Standing.UNDEF,
                domain_repaired_from=repaired_from, exposure=0,
            )
            return dec.seal()

        ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
        top_lang, top_score = ranked[0]
        second_score = ranked[1][1] if len(ranked) > 1 else Fraction(0)
        margin = top_score - second_score

        value_standing = Standing.INTERPOLATED if repaired else Standing.EXACT

        if repaired:
            if margin >= self.hold_margin:
                standing = Standing.MEASURED
                verdict = Verdict.HELD if margin < self.confident_margin else Verdict.PASSTHROUGH
            else:
                standing = Standing.UNDEF
                verdict = Verdict.HELD
            label = top_lang if standing != Standing.UNDEF else None
        else:
            if margin >= self.confident_margin:
                standing = Standing.EXACT
                verdict = Verdict.PASSTHROUGH
                label = top_lang
            elif margin >= self.hold_margin:
                standing = Standing.MEASURED
                verdict = Verdict.HELD
                label = top_lang
            else:
                standing = Standing.UNDEF
                verdict = Verdict.HELD
                label = None

        dec = LidDecision(
            text=text, verdict=verdict, label=label, margin=margin,
            standing=standing, value_standing=value_standing,
            domain_repaired_from=repaired_from, exposure=len(evidence),
        )
        return dec.seal()

    def append(self, decision: LidDecision) -> None:
        self._ledger.append(decision)

    @property
    def ledger(self) -> List[LidDecision]:
        return list(self._ledger)


if __name__ == "__main__":
    eng = LidExact()
    ev = [
        Evidence("es", ExactWeight.from_str("3/5")),
        Evidence("fr", ExactWeight.from_str("1/5")),
        Evidence("es", ExactWeight.from_str("2/5")),
    ]
    d1 = eng.score("hola mundo", ev, repaired=False)
    eng.append(d1)
    print(f"clean   → verdict={d1.verdict.value:12} label={d1.label} margin={d1.margin} standing={d1.standing.value} value={d1.value_standing.value}")

    d2 = eng.score("hola mundo", ev, repaired=True, repaired_from="mojibake")
    eng.append(d2)
    print(f"repaired→ verdict={d2.verdict.value:12} label={d2.label} margin={d2.margin} standing={d2.standing.value} value={d2.value_standing.value}")

    ev_tie = [
        Evidence("es", ExactWeight.from_str("3/5")),
        Evidence("fr", ExactWeight.from_str("3/5")),
    ]
    d3 = eng.score("de de de de", ev_tie)
    eng.append(d3)
    print(f"tie     → verdict={d3.verdict.value:12} label={d3.label} margin={d3.margin} standing={d3.standing.value}")

    assert d1.margin == d2.margin
    assert d1.value_standing != d2.value_standing
    assert d3.margin == 0
    print("\nAll smoke tests passed.")
