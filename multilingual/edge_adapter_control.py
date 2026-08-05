#!/usr/bin/env python3
"""
edge_adapter_control.py — Adapter selection and call, AFTER the shared decision gate.
Depends on: gosub_exact_decide.GOSUB_EXACT_DECIDE (runs first)
Bergamot / Apertium are never decision makers.
Version Clean. Finite. Musical. No infinity. No Zero's.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Dict, Optional
import hashlib

from gosub_exact_decide import (
    GOSUB_EXACT_DECIDE, ExactDecision, Standing, Verdict,
)


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
    decision: ExactDecision
    content_hash: str = ""

    def seal(self) -> "AdapterRecord":
        payload = f"{self.source_text}|{self.result_text}|{self.source_lang}|{self.target_lang}|{self.adapter}|{self.decision.content_hash}"
        self.content_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
        return self


def GOSUB_VALIDATE_TEXT(text: str):
    if text is None: return False, "null_text"
    if not isinstance(text, str): return False, "not_string"
    stripped = text.strip()
    if len(stripped) == 0: return False, "empty_text"
    if len(stripped) > 100_000: return False, "text_too_long"
    return True, None


def GOSUB_SELECT_ADAPTER(decision, target_lang, prefer_neural=True):
    if decision.verdict != Verdict.PASSTHROUGH: return AdapterKind.NONE
    if decision.standing != Standing.EXACT: return AdapterKind.NONE
    if decision.value_standing != Standing.EXACT: return AdapterKind.NONE
    if not decision.top_lang or not target_lang: return AdapterKind.NONE
    if decision.top_lang == target_lang: return AdapterKind.NONE
    return AdapterKind.BERGAMOT if prefer_neural else AdapterKind.APERTIUM


def GOSUB_CALL_ADAPTER(adapter, text, source_lang, target_lang):
    if adapter == AdapterKind.NONE: return None, "no_adapter"
    return None, f"adapter_{adapter.value}_not_bound_in_this_layer"


def PROCESS_EDGE_TRANSLATION(text, scores, target_lang, repaired=False, repaired_from=None, prefer_neural=True):
    ok, reason = GOSUB_VALIDATE_TEXT(text)
    if not ok:
        decision = GOSUB_EXACT_DECIDE({}, repaired=True, repaired_from=reason)
        return AdapterRecord(str(text), None, None, target_lang, AdapterKind.NONE, decision).seal()

    decision = GOSUB_EXACT_DECIDE(scores, repaired=repaired, repaired_from=repaired_from)
    adapter = GOSUB_SELECT_ADAPTER(decision, target_lang, prefer_neural)
    result_text = None
    if adapter != AdapterKind.NONE and decision.top_lang:
        result_text, err = GOSUB_CALL_ADAPTER(adapter, text, decision.top_lang, target_lang)
        if err:
            decision = GOSUB_EXACT_DECIDE(scores, repaired=True, repaired_from=err)
            adapter = AdapterKind.NONE
    return AdapterRecord(text, result_text, decision.top_lang, target_lang, adapter, decision).seal()


if __name__ == "__main__":
    scores = {"es": Fraction(1), "fr": Fraction(1, 5)}
    rec = PROCESS_EDGE_TRANSLATION("hola mundo", scores, "en")
    print(f"verdict={rec.decision.verdict.value} adapter={rec.adapter.value}")
    rec2 = PROCESS_EDGE_TRANSLATION("hola mundo", scores, "en", repaired=True, repaired_from="mojibake")
    assert rec2.decision.value_standing == Standing.INTERPOLATED
    print("Deduped. Shared gate runs first.")
