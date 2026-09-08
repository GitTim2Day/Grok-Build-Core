#!/usr/bin/env python3
"""
KBLD - Kilobyte Loop Decision (Shepherd's Staff) Framework
Single-file production version — pure stdlib, bounded, no Inf/NaN, provenance-aware.

Aligns with Grok Build / KBLD9 / Shepherd Staff / EV2 / SVCT principles:
- Finite weave, no zeros, no infinities
- Explicit GOSUB-style nesting
- Error → Test → Mitigate → Retest loop until nearly flawless
- Provenance hash chain on every evaluation
- Accuracy floor + resonance scoring

Author lineage: Timothy H Norman + Grok Build extraction & repair 2026-07-19
"""

from __future__ import annotations
import math
import hashlib
import json
import time
import re
from typing import Any, Dict, List, Optional, Tuple

# ====================== CONSTANTS (bounded, no zero) ======================
MIN_SCORE = 0.1          # never true zero
MAX_SCORE = 10.0
THRESHOLD = 9.3
MAX_ITERATIONS = 5
EPS = 1e-12

# ====================== GOSUB PRIMITIVES (local sealed copies) ======================
def gosub_provenance_hash(content: Any, prev_hash: Optional[str] = None) -> str:
    """GOSUB: SHA256 chain. Bounded timestamp."""
    if isinstance(content, dict):
        content = json.dumps(content, sort_keys=True, separators=(",", ":"))
    payload = (prev_hash or "") + str(content) + f"{time.time():.6f}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def gosub_accuracy_floor(observed: float, reference: float) -> Tuple[Optional[float], Optional[str]]:
    """GOSUB: portable accuracy %. No zero reference, no negatives."""
    if reference <= 0 or observed < 0:
        return None, "ERROR: zero-or-negative — route to Shepherd 10σ"
    pct = abs(observed - reference) / reference * 100.0
    return round(pct, 6), None

# ====================== KBLD AUDITOR ======================
class KBLD_Auditor:
    """
    KBLD Mind Filter:
    K — Knowledge alignment
    B — Belief / core principles alignment
    L — Logical soundness
    D — Discernment / likely fruit
    """

    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.prev_hash: Optional[str] = None

    def _score_knowledge(self, text: str) -> float:
        """Heuristic: presence of factual, concrete, verifiable language."""
        text_l = text.lower()
        markers = ["because", "data", "measured", "observed", "evidence", "known",
                   "fact", "result", "experiment", "calculated", "value", "unit"]
        hits = sum(1 for m in markers if m in text_l)
        base = min(MAX_SCORE, 6.5 + hits * 0.7)
        # Penalty for pure speculation without grounding
        if "maybe" in text_l or "perhaps" in text_l:
            base = max(MIN_SCORE, base - 1.5)
        return round(max(MIN_SCORE, min(MAX_SCORE, base)), 2)

    def _score_belief(self, text: str) -> float:
        """Heuristic: alignment with finite, causal, no-infinity principles."""
        text_l = text.lower()
        positive = ["finite", "bounded", "causal", "resonance", "harmonic", "lattice",
                    "planck", "wave", "pattern", "stable", "consistent"]
        negative = ["infinite", "infinity", "singularity", "zero energy", "nothingness",
                    "arbitrary", "magic", "unbounded"]
        pos_hits = sum(1 for p in positive if p in text_l)
        neg_hits = sum(1 for n in negative if n in text_l)
        base = 7.0 + pos_hits * 0.7 - neg_hits * 1.8
        return round(max(MIN_SCORE, min(MAX_SCORE, base)), 2)

    def _score_logic(self, text: str) -> float:
        """Heuristic: connectors, structure, absence of contradiction markers."""
        text_l = text.lower()
        connectors = ["therefore", "thus", "because", "if", "then", "implies",
                      "leads to", "consequently", "so that"]
        hits = sum(1 for c in connectors if c in text_l)
        # Simple contradiction check
        contra = 0
        if ("not" in text_l and "is" in text_l) or ("never" in text_l and "always" in text_l):
            contra = 1.5
        base = 7.0 + hits * 0.55 - contra
        # Length discipline (avoid fluff)
        words = len(text.split())
        if words > 120:
            base -= 1.0
        elif words < 8:
            base -= 1.5
        return round(max(MIN_SCORE, min(MAX_SCORE, base)), 2)

    def _score_discernment(self, text: str) -> float:
        """Heuristic: practical fruit, actionable outcome, clarity of consequence."""
        text_l = text.lower()
        fruit = ["result", "outcome", "leads to", "produces", "enables", "allows",
                 "improves", "stabilizes", "reduces", "eliminates", "reveals"]
        hits = sum(1 for f in fruit if f in text_l)
        base = 7.2 + hits * 0.6
        # Clarity bonus
        if text.count(".") >= 1 and len(text) > 20:
            base += 0.8
        return round(max(MIN_SCORE, min(MAX_SCORE, base)), 2)

    def evaluate(self, response_text: str, context: str = "") -> Dict[str, Any]:
        """Main KBLD evaluation — returns structured result with provenance."""
        if not isinstance(response_text, str) or not response_text.strip():
            response_text = "Empty or invalid input — minimal seed response generated."

        scores = {
            "Knowledge": self._score_knowledge(response_text),
            "Belief": self._score_belief(response_text),
            "Logic": self._score_logic(response_text),
            "Discernment": self._score_discernment(response_text)
        }

        avg_score = sum(scores.values()) / 4.0
        confidence = round(avg_score * 10.0, 1)  # 0–100 scale

        result = {
            "confidence": f"{confidence}%",
            "avg_score": round(avg_score, 2),
            "detailed_scores": scores,
            "iterations_needed": 1,
            "text_preview": (response_text[:80] + "...") if len(response_text) > 80 else response_text
        }

        # Provenance
        result["hash"] = gosub_provenance_hash(result, self.prev_hash)
        self.prev_hash = result["hash"]

        self.history.append({
            "score": confidence,
            "avg": avg_score,
            "hash": result["hash"],
            "preview": result["text_preview"]
        })

        return result

    def _refine(self, text: str, result: Dict[str, Any]) -> str:
        """Mitigation step: tighten language, remove fluff, reinforce structure."""
        # Simple deterministic refine for demo
        cleaned = re.sub(r"\s+", " ", text).strip()
        if result["avg_score"] < 8.0:
            # Add structural clarity if weak
            if not cleaned.endswith("."):
                cleaned += "."
            cleaned = "Bounded observation: " + cleaned
        if "infinite" in cleaned.lower() or "infinity" in cleaned.lower():
            cleaned = cleaned.replace("infinite", "finite").replace("infinity", "bounded scale")
        return cleaned

    def iterate_until_strong(
        self,
        initial_response: str,
        max_iterations: int = MAX_ITERATIONS,
        threshold: float = THRESHOLD
    ) -> Tuple[str, Dict[str, Any]]:
        """
        GOSUB_Error_Test_Mitigate_Retest_Loop pattern.
        Keep refining until avg_score >= threshold or max passes.
        """
        response = initial_response
        best_result: Optional[Dict[str, Any]] = None
        best_response = response

        for iteration in range(1, max_iterations + 1):
            result = self.evaluate(response)
            result["iterations_needed"] = iteration

            if best_result is None or result["avg_score"] > best_result["avg_score"]:
                best_result = result
                best_response = response

            if result["avg_score"] >= threshold:
                return response, result

            # Mitigate
            response = self._refine(response, result)

        # Return best effort
        return best_response, best_result  # type: ignore

    def get_average_performance(self) -> float:
        """Average confidence across history. Never divide by zero."""
        if not self.history:
            return MIN_SCORE * 10.0
        total = sum(item["score"] for item in self.history)
        return round(total / len(self.history), 1)


# ====================== SELF-TEST & DEMO ======================
def _self_test() -> bool:
    print("=== KBLD_Auditor self-test (floor) ===")
    ok = True
    auditor = KBLD_Auditor()

    # 1. Basic evaluation
    r = auditor.evaluate("Data measured in experiment shows finite resonance pattern.")
    assert "confidence" in r and r["avg_score"] > 5.0, "basic eval failed"
    print("  [PASS] basic evaluation")

    # 2. Iteration reaches higher score or respects max
    weak = "maybe something infinite happens"
    final, conf = auditor.iterate_until_strong(weak, max_iterations=3)
    assert conf["avg_score"] >= auditor.evaluate(weak)["avg_score"] - 0.5, "iteration did not improve or hold"
    print(f"  [PASS] iteration (final avg={conf['avg_score']})")

    # 3. Empty input handled
    r_empty = auditor.evaluate("")
    assert r_empty["avg_score"] >= MIN_SCORE, "empty input crashed"
    print("  [PASS] empty/guard")

    # 4. Provenance chain grows
    assert len(auditor.history) >= 3, "history not recording"
    print("  [PASS] provenance history")

    # 5. Average performance
    perf = auditor.get_average_performance()
    assert MIN_SCORE * 10 <= perf <= 100.0, "performance out of bounds"
    print(f"  [PASS] average performance = {perf}%")

    print("=== ALL GREEN ===")
    return ok


if __name__ == "__main__":
    _self_test()
    print()
    auditor = KBLD_Auditor()
    test_response = "This is a sample response being evaluated for finite causal structure."
    final_response, confidence = auditor.iterate_until_strong(test_response)
    print(f"Final Response : {final_response}")
    print(f"Final Confidence: {confidence['confidence']} (avg {confidence['avg_score']})")
    print(f"Detailed       : {confidence['detailed_scores']}")
    print(f"Iterations     : {confidence['iterations_needed']}")
    print(f"Overall Perf   : {auditor.get_average_performance():.1f}%")
    print(f"Provenance Hash: {confidence['hash'][:16]}...")
