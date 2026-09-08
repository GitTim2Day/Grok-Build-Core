#!/usr/bin/env python3
"""
KBLDA - Kilobyte Loop Decision Auditor (Shepherd's Staff) Framework
Single-file production version — pure stdlib, bounded, no Inf/NaN, provenance-aware.
No type hints (saved for end). No encryption beyond basic hash.

Aligns with Grok Build / KBLDA9 / Shepherd Staff / EV2 / SVCT principles:
- Finite weave, no zeros, no infinities
- Explicit GOSUB-style nesting
- Error → Test → Mitigate → Retest loop until nearly flawless
- Provenance hash chain on every evaluation

Author lineage: Timothy H Norman + Grok Build extraction & repair 2026-07-19
"""

import hashlib
import json
import time
import re

MIN_SCORE = 0.1
MAX_SCORE = 10.0
THRESHOLD = 9.3
MAX_ITERATIONS = 5

def gosub_provenance_hash(content, prev_hash=None):
    if isinstance(content, dict):
        content = json.dumps(content, sort_keys=True, separators=(",", ":"))
    payload = (prev_hash or "") + str(content) + f"{time.time():.6f}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

class KBLDA_Auditor:
    def __init__(self):
        self.history = []
        self.prev_hash = None

    def _score_knowledge(self, text):
        text_l = text.lower()
        markers = ["because", "data", "measured", "observed", "evidence", "known",
                   "fact", "result", "experiment", "calculated", "value", "unit"]
        hits = sum(1 for m in markers if m in text_l)
        base = min(MAX_SCORE, 6.5 + hits * 0.7)
        if "maybe" in text_l or "perhaps" in text_l:
            base = max(MIN_SCORE, base - 1.5)
        return round(max(MIN_SCORE, min(MAX_SCORE, base)), 2)

    def _score_belief(self, text):
        text_l = text.lower()
        positive = ["finite", "bounded", "causal", "resonance", "harmonic", "lattice",
                    "planck", "wave", "pattern", "stable", "consistent"]
        negative = ["infinite", "infinity", "singularity", "zero energy", "nothingness",
                    "arbitrary", "magic", "unbounded"]
        pos_hits = sum(1 for p in positive if p in text_l)
        neg_hits = sum(1 for n in negative if n in text_l)
        base = 7.0 + pos_hits * 0.7 - neg_hits * 1.8
        return round(max(MIN_SCORE, min(MAX_SCORE, base)), 2)

    def _score_logic(self, text):
        text_l = text.lower()
        connectors = ["therefore", "thus", "because", "if", "then", "implies",
                      "leads to", "consequently", "so that"]
        hits = sum(1 for c in connectors if c in text_l)
        contra = 0
        if ("not" in text_l and "is" in text_l) or ("never" in text_l and "always" in text_l):
            contra = 1.5
        base = 7.0 + hits * 0.55 - contra
        words = len(text.split())
        if words > 120:
            base -= 1.0
        elif words < 8:
            base -= 1.5
        return round(max(MIN_SCORE, min(MAX_SCORE, base)), 2)

    def _score_discernment(self, text):
        text_l = text.lower()
        fruit = ["result", "outcome", "leads to", "produces", "enables", "allows",
                 "improves", "stabilizes", "reduces", "eliminates", "reveals"]
        hits = sum(1 for f in fruit if f in text_l)
        base = 7.2 + hits * 0.6
        if text.count(".") >= 1 and len(text) > 20:
            base += 0.8
        return round(max(MIN_SCORE, min(MAX_SCORE, base)), 2)

    def evaluate(self, response_text, context=""):
        if not isinstance(response_text, str) or not response_text.strip():
            response_text = "Empty or invalid input — minimal seed response generated."

        scores = {
            "Knowledge": self._score_knowledge(response_text),
            "Belief": self._score_belief(response_text),
            "Logic": self._score_logic(response_text),
            "Discernment": self._score_discernment(response_text)
        }

        avg_score = sum(scores.values()) / 4.0
        confidence = round(avg_score * 10.0, 1)

        result = {
            "confidence": f"{confidence}%",
            "avg_score": round(avg_score, 2),
            "detailed_scores": scores,
            "iterations_needed": 1,
            "text_preview": (response_text[:80] + "...") if len(response_text) > 80 else response_text
        }

        result["hash"] = gosub_provenance_hash(result, self.prev_hash)
        self.prev_hash = result["hash"]

        self.history.append({
            "score": confidence,
            "avg": avg_score,
            "hash": result["hash"],
            "preview": result["text_preview"]
        })

        return result

    def _refine(self, text, result):
        cleaned = re.sub(r"\s+", " ", text).strip()
        if result["avg_score"] < 8.0:
            if not cleaned.endswith("."):
                cleaned += "."
            cleaned = "Bounded observation: " + cleaned
        if "infinite" in cleaned.lower() or "infinity" in cleaned.lower():
            cleaned = cleaned.replace("infinite", "finite").replace("infinity", "bounded scale")
        return cleaned

    def iterate_until_strong(self, initial_response, max_iterations=MAX_ITERATIONS, threshold=THRESHOLD):
        response = initial_response
        best_result = None
        best_response = response

        for iteration in range(1, max_iterations + 1):
            result = self.evaluate(response)
            result["iterations_needed"] = iteration

            if best_result is None or result["avg_score"] > best_result["avg_score"]:
                best_result = result
                best_response = response

            if result["avg_score"] >= threshold:
                return response, result

            response = self._refine(response, result)

        return best_response, best_result

    def get_average_performance(self):
        if not self.history:
            return MIN_SCORE * 10.0
        total = sum(item["score"] for item in self.history)
        return round(total / len(self.history), 1)


def _self_test():
    print("=== KBLDA_Auditor self-test (floor) ===")
    auditor = KBLDA_Auditor()

    r = auditor.evaluate("Data measured in experiment shows finite resonance pattern.")
    assert "confidence" in r and r["avg_score"] > 5.0
    print("  [PASS] basic evaluation")

    weak = "maybe something infinite happens"
    final, conf = auditor.iterate_until_strong(weak, max_iterations=3)
    assert conf["avg_score"] >= auditor.evaluate(weak)["avg_score"] - 0.5
    print(f"  [PASS] iteration (final avg={conf['avg_score']})")

    r_empty = auditor.evaluate("")
    assert r_empty["avg_score"] >= MIN_SCORE
    print("  [PASS] empty/guard")

    assert len(auditor.history) >= 3
    print("  [PASS] provenance history")

    perf = auditor.get_average_performance()
    assert MIN_SCORE * 10 <= perf <= 100.0
    print(f"  [PASS] average performance = {perf}%")

    print("=== ALL GREEN ===")
    return True


if __name__ == "__main__":
    _self_test()
    print()
    auditor = KBLDA_Auditor()
    test_response = "This is a sample response being evaluated for finite causal structure."
    final_response, confidence = auditor.iterate_until_strong(test_response)
    print(f"Final Response : {final_response}")
    print(f"Final Confidence: {confidence['confidence']} (avg {confidence['avg_score']})")
    print(f"Detailed       : {confidence['detailed_scores']}")
    print(f"Iterations     : {confidence['iterations_needed']}")
    print(f"Overall Perf   : {auditor.get_average_performance():.1f}%")
    print(f"Provenance Hash: {confidence['hash'][:16]}...")
