#!/usr/bin/env python3
"""
edge_adapter_control.py — Streamlined control layer for offline translation adapters
Bergamot (neural) / Apertium (rule-based) sit behind this gate.
They are never the decision makers.

Five pillars on every permanent record:
  content · context · data · time · validation

All decisions use exact rational arithmetic where scores matter.
Truncation only. No float at the boundary.
GOSUB / IF-THEN-ELSE discipline throughout.

Version Clean. Finite. Musical. No infinity. No Zero's.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction
from typing import Optional, Dict, Any, List
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


class AdapterKind(str, Enum):
    NONE = "NONE"
    BERGAMOT = "BERGAMOT"
    APERTIUM = "APERTIUM"


@dataclass
class AdapterRecord:
    source_text: str
    result_text: Optional[str]
    source_lang: Optional[str]
    target_lang: Optional[str]
    adapter: AdapterKind
    verdict: Verdict
    margin: Fraction
    ts: float = field(default_factory=time.time)
    standing: Standing = Standing.UNDEF
    value_standing: Standing = Standing.UNDEF
    domain_repaired_from: Optional[str] = None
    exposure: int = 0
    content_hash: str = ""

    def seal(self) -> "AdapterRecord":
        payload = (
            f"{self.source_text}|{self.result_text}|{self.source_lang}|{self.target_lang}|"
            f"{self.adapter}|{self.verdict}|{self.margin}|{self.standing}|"
            f"{self.value_standing}|{self.domain_repaired_from}|{self.exposure}"
        )
        self.content_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
        return self


def GOSUB_VALIDATE_TEXT(text: str):
    if text is None:
        return False, "null_text"
    if not isinstance(text, str):
        return False, "not_string"
    stripped = text.strip()
    if len(stripped) == 0:
        return False, "empty_text"
    if len(stripped) > 100_000:
        return False, "text_too_long"
    return True, None


def GOSUB_EXACT_MARGIN(scores: Dict[str, Fraction]):
    if not scores:
        return None, Fraction(0)
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    top_lang, top = ranked[0]
    second = ranked[1][1] if len(ranked) > 1 else Fraction(0)
    return top_lang, top - second


def GOSUB_DECIDE_VERDICT(margin: Fraction, repaired: bool,
                         confident: Fraction = Fraction(5, 2),
                         hold: Fraction = Fraction(1, 2)):
    value_standing = Standing.INTERPOLATED if repaired else Standing.EXACT
    if repaired:
        if margin >= hold:
            return Verdict.HELD, Standing.MEASURED, value_standing
        return Verdict.HELD, Standing.UNDEF, value_standing
    if margin >= confident:
        return Verdict.PASSTHROUGH, Standing.EXACT, value_standing
    if margin >= hold:
        return Verdict.HELD, Standing.MEASURED, value_standing
    return Verdict.HELD, Standing.UNDEF, value_standing


def GOSUB_SELECT_ADAPTER(verdict: Verdict, source_lang, target_lang, prefer_neural: bool = True):
    if verdict != Verdict.TRANSLATED:
        return AdapterKind.NONE
    if not source_lang or not target_lang or source_lang == target_lang:
        return AdapterKind.NONE
    return AdapterKind.BERGAMOT if prefer_neural else AdapterKind.APERTIUM


def GOSUB_CALL_ADAPTER(adapter: AdapterKind, text: str, source_lang: str, target_lang: str):
    if adapter == AdapterKind.NONE:
        return None, "no_adapter"
    return None, f"adapter_{adapter.value}_not_bound_in_this_layer"


def GOSUB_SEAL_RESULT(source_text, result_text, source_lang, target_lang, adapter,
                      verdict, margin, standing, value_standing, repaired_from, exposure):
    rec = AdapterRecord(
        source_text=source_text, result_text=result_text,
        source_lang=source_lang, target_lang=target_lang,
        adapter=adapter, verdict=verdict, margin=margin,
        standing=standing, value_standing=value_standing,
        domain_repaired_from=repaired_from, exposure=exposure,
    )
    return rec.seal()


def PROCESS_EDGE_TRANSLATION(text, scores, target_lang, repaired=False,
                             repaired_from=None, prefer_neural=True):
    ok, reason = GOSUB_VALIDATE_TEXT(text)
    if not ok:
        return GOSUB_SEAL_RESULT(str(text), None, None, target_lang, AdapterKind.NONE,
                                Verdict.HELD, Fraction(0), Standing.UNDEF, Standing.UNDEF,
                                reason, 0)

    top_lang, margin = GOSUB_EXACT_MARGIN(scores)
    verdict, standing, value_standing = GOSUB_DECIDE_VERDICT(margin, repaired)

    if (verdict == Verdict.PASSTHROUGH and top_lang and target_lang
            and top_lang != target_lang and standing == Standing.EXACT and not repaired):
        verdict = Verdict.TRANSLATED

    adapter = GOSUB_SELECT_ADAPTER(verdict, top_lang, target_lang, prefer_neural)

    result_text = None
    if adapter != AdapterKind.NONE and top_lang:
        result_text, err = GOSUB_CALL_ADAPTER(adapter, text, top_lang, target_lang)
        if err:
            verdict = Verdict.HELD
            standing = Standing.MEASURED
            repaired_from = err

    return GOSUB_SEAL_RESULT(text, result_text, top_lang, target_lang, adapter,
                            verdict, margin, standing, value_standing,
                            repaired_from, len(scores))


if __name__ == "__main__":
    scores = {"es": Fraction(1), "fr": Fraction(1, 5)}
    rec = PROCESS_EDGE_TRANSLATION("hola mundo", scores, "en")
    print(f"verdict={rec.verdict.value} adapter={rec.adapter.value} standing={rec.standing.value}")
    rec2 = PROCESS_EDGE_TRANSLATION("hola mundo", scores, "en", repaired=True, repaired_from="mojibake")
    assert rec2.value_standing == Standing.INTERPOLATED
    print("Smoke tests passed.")
