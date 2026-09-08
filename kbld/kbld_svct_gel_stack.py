#!/usr/bin/env python3
"""
kbld_svct_gel_stack.py
GOSUB stack: Acceptable-range guard → Gel interpolation → SVCT 56-cell closed-loop
Local-first, fixed-point, practical truncation.
If_then discipline. No what_if.
Author lineage: Timothy H Norman + Grok Build 2026-07-25
"""

from __future__ import annotations
import math
import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Tuple

try:
    import numpy as np
    from spherical_memory_pro import SphericalMemoryPro
    HAS_SVCT = True
except Exception:
    HAS_SVCT = False
    np = None
    SphericalMemoryPro = None

SCALE = 1_000_000
PRECISION_TIERS = {"day": 6, "standard": 8, "fine": 12, "ultra": 15}

def _safe_float(v: Any) -> Optional[float]:
    try:
        f = float(v)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except Exception:
        return None

def _to_fixed(f: float) -> Optional[int]:
    try:
        return math.trunc(f * SCALE)
    except Exception:
        return None

def _from_fixed(i: Optional[int]) -> Optional[float]:
    if i is None:
        return None
    return i / float(SCALE)

def practical_trunc(x: float, places: int = 8) -> float:
    if x is None:
        return 0.0
    try:
        factor = 10 ** places
        return math.trunc(x * factor) / float(factor)
    except Exception:
        return 0.0

def _truncate(f: float, n: int = 6) -> float:
    return practical_trunc(f, n)

def gosub_acceptable_range(
    value: Any,
    min_val: float = -1e9,
    max_val: float = 1e9,
    context: str = "general"
) -> Tuple[bool, str, Optional[float]]:
    if min_val > max_val:
        min_val, max_val = max_val, min_val
    val = _safe_float(value)
    if val is None:
        return False, "missing_or_non_numeric", None
    if min_val <= val <= max_val:
        return True, "OK", val
    clamped = max(min_val, min(max_val, val))
    reason = f"out_of_range_{context} ({min_val} to {max_val})"
    return False, reason, clamped

def eGFR_guard(v): return gosub_acceptable_range(v, 0.0, 150.0, "eGFR")
def HbA1c_guard(v): return gosub_acceptable_range(v, 3.0, 15.0, "HbA1c")
def Potassium_guard(v): return gosub_acceptable_range(v, 2.5, 7.0, "Potassium")

def gosub_accuracy_floor(observed: Any, reference: Any) -> Tuple[Optional[float], Optional[str]]:
    o = _safe_float(observed)
    r = _safe_float(reference)
    if o is None or r is None:
        return None, "ERROR: non-numeric"
    if r == 0.0:
        return None, "ERROR: reference zero"
    if o < 0.0 or r < 0.0:
        return None, "ERROR: negative - route Shepherd"
    pct = abs(o - r) / abs(r) * 100.0
    return _truncate(pct, 6), None

def gosub_gel_interpolation(
    prev: Any, curr: Any,
    config: Optional[Dict] = None,
    low_stability_delta: float = 4.0,
    precision: str = "standard",
    range_min: float = -1e9,
    range_max: float = 1e9,
    context: str = "gel"
) -> Dict[str, Any]:
    config = config or {}
    places = PRECISION_TIERS.get(precision, 8)
    notes = []
    ok_p, reason_p, clamped_p = gosub_acceptable_range(prev, range_min, range_max, context)
    ok_c, reason_c, clamped_c = gosub_acceptable_range(curr, range_min, range_max, context)
    if not ok_p:
        notes.append(f"prev_{reason_p}")
        prev = clamped_p
    if not ok_c:
        notes.append(f"curr_{reason_c}")
        curr = clamped_c
    p = _safe_float(prev)
    c = _safe_float(curr)
    if p is None or c is None:
        return {
            "method": "none", "value": None, "confidence_pre": 0.0,
            "confidence": 0.0, "hybrid_confidence": 0.0, "pillar_spread": 0.0,
            "agree_factor": 1.0, "contributing_anchors": [], "norm_weights": {},
            "accuracy_error_pct": None, "notes": notes + ["missing"],
            "precision": precision, "range_ok": False,
        }
    base_conf = 0.65 if abs(c - p) > low_stability_delta else 0.94
    mid = _from_fixed((_to_fixed(p) + _to_fixed(c)) // 2)
    valid = []
    spread = 0.0
    agree_factor = 1.0
    norm_weights = {}
    contributing = []
    weights = {"content": 0.40, "context": 0.30, "data": 0.20, "time": 0.10, "reason": 0.35, "creative": 0.25}
    for key, w in weights.items():
        anc = _safe_float(config.get(key + "_anchor"))
        if anc is not None and min(p, c) <= anc <= max(p, c):
            valid.append((anc, w, key))
    if valid:
        total_w = sum(w for _, w, _ in valid)
        mid = sum(a * w for a, w, _ in valid) / total_w
        mid = _from_fixed(_to_fixed(mid))
        notes.append("soft_blend")
        norm_weights = {lab: round(w / total_w, 4) for _, w, lab in valid}
        contributing = [lab for _, _, lab in valid]
        vals = [a for a, _, _ in valid]
        spread = max(vals) - min(vals)
        agree_factor = max(0.0, 1.0 - (spread / max(abs(p), abs(c), 1.0)))
        notes.append("agree_factor=%.3f" % agree_factor)
    err_pct, _ = gosub_accuracy_floor(c, p)
    if err_pct is None:
        err_pct = 0.0
    confidence = base_conf * agree_factor
    hybrid = confidence * max(0.0, 1.0 - err_pct / 100.0)
    return {
        "method": "fixedpoint_soft" if valid else "fixedpoint",
        "value": practical_trunc(mid, places),
        "confidence_pre": _truncate(base_conf, 4),
        "confidence": _truncate(confidence, 4),
        "hybrid_confidence": _truncate(hybrid, 4),
        "pillar_spread": spread, "agree_factor": agree_factor,
        "contributing_anchors": contributing, "norm_weights": norm_weights,
        "accuracy_error_pct": _truncate(err_pct, 4),
        "notes": notes, "precision": precision, "range_ok": ok_p and ok_c,
    }

def gosub_svct_align(gel_result: Dict[str, Any], anchors: Optional[Dict] = None, precision: str = "standard") -> Dict[str, Any]:
    places = PRECISION_TIERS.get(precision, 8)
    anchors = anchors or {}
    value = gel_result.get("value")
    if value is None or not HAS_SVCT:
        out = dict(gel_result)
        out.update({"svct_rt_error": None, "svct_hybrid": gel_result.get("hybrid_confidence"), "svct_available": False})
        return out
    meta = np.zeros(8, dtype=np.float64)
    meta[0] = value
    meta[1] = _safe_float(anchors.get("content_anchor")) or value
    meta[2] = _safe_float(anchors.get("context_anchor")) or value
    meta[3] = _safe_float(anchors.get("data_anchor")) or value
    meta[4] = _safe_float(anchors.get("time_anchor")) or value
    meta[5] = _safe_float(anchors.get("reason_anchor")) or value
    meta[6] = _safe_float(anchors.get("creative_anchor")) or value
    meta[7] = (meta[1] + meta[2] + meta[3] + meta[4]) / 4.0
    sv = SphericalMemoryPro(num_sectors=8, num_lat_bands=5, dtype=np.float64)
    sv.flow_in(meta, pole="north")
    rec = sv.flow_out()
    raw_err = float(np.max(np.abs(rec - meta)))
    rt_error = practical_trunc(raw_err, places)
    factor = max(0.0, 1.0 - (rt_error * (10 ** places)))
    svct_hybrid = _truncate(gel_result["hybrid_confidence"] * factor, 4)
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    prov = hashlib.sha256(json.dumps({"value": value, "hybrid": svct_hybrid, "ts": ts}, sort_keys=True).encode()).hexdigest()[:16]
    out = dict(gel_result)
    out.update({
        "svct_rt_error_raw": raw_err, "svct_rt_error": rt_error,
        "svct_hybrid": svct_hybrid, "svct_factor": factor,
        "svct_recovered_value": float(rec[0]), "svct_cells": 56,
        "provenance": prov, "timestamp": ts, "svct_available": True,
    })
    return out

def gosub_gel_svct_stack(prev, curr, config=None, precision="standard", range_min=0.0, range_max=150.0, context="eGFR"):
    gel = gosub_gel_interpolation(prev, curr, config=config, precision=precision, range_min=range_min, range_max=range_max, context=context)
    return gosub_svct_align(gel, anchors=config, precision=precision)

def gosub_error_test_mitigate_retest_loop(max_passes=5):
    log = []
    for pass_num in range(1, max_passes + 1):
        failures = []
        r = gosub_gel_interpolation(4.8, 5.6)
        if r["value"] is None or abs(r["value"] - 5.2) > 0.01:
            failures.append(("synthetic", r["value"]))
        r2 = gosub_gel_svct_stack(70.0, 61.0, {
            "content_anchor": 61.0, "context_anchor": 65.0, "data_anchor": 64.0,
            "time_anchor": 66.0, "reason_anchor": 63.0, "creative_anchor": 62.5
        })
        if r2["value"] is None:
            failures.append(("egfr", None))
        ok, _, _ = gosub_acceptable_range(999.0, 0, 150, "eGFR")
        if ok:
            failures.append(("range", "should_fail"))
        r3 = gosub_gel_interpolation(None, 5.0)
        if r3["confidence"] != 0.0:
            failures.append(("missing", r3["confidence"]))
        log.append({"pass": pass_num, "failures": len(failures), "details": failures})
        if not failures:
            return True, log
    return False, log

def _self_test():
    print("=== kbld_svct_gel_stack self-test ===")
    print("HAS_SVCT:", HAS_SVCT)
    ok, log = gosub_error_test_mitigate_retest_loop(3)
    for e in log:
        print(" pass", e["pass"], "failures:", e["details"])
    print("ALL GREEN - NEARLY FLAWLESS" if ok else "MITIGATE NEEDED")
    return ok

if __name__ == "__main__":
    _self_test()
