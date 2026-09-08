#!/usr/bin/env python3
"""
kbl_svct_stacks.py — REPAIRED (rev 2, adversarial pass 1)
Consolidated GOSUB subroutine stacks for KBLD/SVCT/Shepherd/voice pipelines.
Pure stdlib. GOSUB airlock discipline. Earned vs Asserted.
Source sealed from email 2026-07-18 into Grok Build 2026-07-25.
"""
from __future__ import annotations
import hashlib, json, math
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

class KBLDError(Exception): pass
class KBLDEntryGuard(KBLDError): pass
class KBLDExitGuard(KBLDError): pass
class KBLDSeamUnbound(KBLDError): pass
class KBLDReadBackMismatch(KBLDError): pass
class KBLDMitigationBudgetExceeded(KBLDError): pass
class KBLDStagnation(KBLDError): pass

_SEAM_REGISTRY: Dict[str, Callable] = {}
_DECLARED_SEAMS = (
    "harmonic_damping", "resonant_cancel_repetition",
    "embed_four_pillar_provenance", "radial_spherical_token_engine",
    "spherical_voxel_tokenizer", "modality_aware_clean_and_audit",
    "star_traversal_nuance_enhance",
)

def GOSUB_Bind_Seam(name: str, impl: Callable) -> None:
    if name not in _DECLARED_SEAMS:
        raise KBLDEntryGuard(f"unknown seam name: {name!r}")
    if not callable(impl):
        raise KBLDEntryGuard(f"seam impl for {name!r} is not callable")
    _SEAM_REGISTRY[name] = impl
    if _SEAM_REGISTRY.get(name) is not impl:
        raise KBLDReadBackMismatch(f"seam bind read-back failed for {name!r}")

def _seam(name: str) -> Callable:
    if name not in _DECLARED_SEAMS:
        raise KBLDEntryGuard(f"unknown seam name: {name!r}")
    if name not in _SEAM_REGISTRY:
        raise KBLDSeamUnbound(
            f"seam {name!r} declared but no implementation bound "
            f"(ASSERTED, not EARNED). Bind via GOSUB_Bind_Seam.")
    return _SEAM_REGISTRY[name]

def _canonical_hash(payload: Any) -> str:
    try:
        blob = json.dumps(payload, sort_keys=True, default=repr, allow_nan=True).encode("utf-8")
    except (TypeError, ValueError):
        blob = repr(payload).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()

def GOSUB_Provenance_Attach(payload: Any, timestamp: Optional[datetime] = None,
                            context: Optional[dict] = None) -> Dict[str, Any]:
    if timestamp is not None and not isinstance(timestamp, datetime):
        raise KBLDEntryGuard("timestamp must be datetime or None")
    ts = timestamp if timestamp is not None else datetime.now(timezone.utc)
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    record = {
        "payload": payload,
        "ts_utc": ts.isoformat(),
        "sha256": _canonical_hash(payload),
        "context": dict(context) if context else {},
    }
    if _canonical_hash(record["payload"]) != record["sha256"]:
        raise KBLDReadBackMismatch("provenance hash read-back failed")
    return record

def _median(xs: List[float]) -> float:
    s = sorted(xs)
    n = len(s)
    mid = n // 2
    return s[mid] if n % 2 == 1 else (s[mid-1] + s[mid]) / 2.0

def GOSUB_MAD_Sigma_Guard(data: Any, n_sigma: float = 10.0) -> Dict[str, Any]:
    if not (isinstance(n_sigma, (int, float)) and math.isfinite(n_sigma) and n_sigma > 0):
        raise KBLDEntryGuard("n_sigma must be a finite positive number")
    if not isinstance(data, (list, tuple)) or not data or \
       not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in data):
        return {"guarded": False, "data": data, "flagged": [], "dropped_nonfinite": 0}
    finite = [float(x) for x in data if math.isfinite(x)]
    dropped = len(data) - len(finite)
    if not finite:
        return {"guarded": True, "data": [], "flagged": [], "dropped_nonfinite": dropped}
    med = _median(finite)
    mad = _median([abs(x - med) for x in finite])
    flagged: List[float] = []
    if mad > 0.0:
        sigma = 1.4826 * mad
        kept = []
        for x in finite:
            if abs(x - med) > n_sigma * sigma:
                flagged.append(x)
            else:
                kept.append(x)
    else:
        tol = 1e-12 * max(1.0, abs(med))
        kept = []
        for x in finite:
            if abs(x - med) > tol:
                flagged.append(x)
            else:
                kept.append(x)
    if len(kept) + len(flagged) + dropped != len(data):
        raise KBLDExitGuard("MAD guard element-count conservation failed")
    return {"guarded": True, "data": kept, "flagged": flagged, "dropped_nonfinite": dropped}

def GOSUB_KBLD_Deterministic_Filter_Layer(data: Any,
                                          timestamp: Optional[datetime] = None,
                                          require_damping: bool = False) -> Dict[str, Any]:
    guard = GOSUB_MAD_Sigma_Guard(data)
    cleaned = guard["data"]
    if require_damping:
        cleaned = _seam("harmonic_damping")(cleaned)
    ctx = {
        "guarded": guard["guarded"],
        "flagged_count": len(guard["flagged"]),
        "dropped_nonfinite": guard["dropped_nonfinite"],
        "damping": "applied" if require_damping else "not_requested",
    }
    return GOSUB_Provenance_Attach(cleaned, timestamp, ctx)

def GOSUB_Shepherd_10Sigma_Validate(voxel_data: Any, bounds: dict) -> Dict[str, Any]:
    n_sigma = bounds.get("n_sigma", 10.0) if isinstance(bounds, dict) else 10.0
    return GOSUB_MAD_Sigma_Guard(voxel_data, n_sigma=n_sigma)

def GOSUB_Error_Test(current: Any, target: Optional[Callable] = None) -> List[str]:
    errors: List[str] = []
    if current is None:
        return ["data_is_none"]
    if isinstance(current, (list, tuple)):
        if len(current) == 0:
            errors.append("empty_sequence")
        for i, x in enumerate(current):
            if isinstance(x, float) and not math.isfinite(x):
                errors.append(f"nonfinite_at_index_{i}")
    elif isinstance(current, dict):
        if len(current) == 0:
            errors.append("empty_mapping")
        for k, v in current.items():
            if isinstance(v, float) and not math.isfinite(v):
                errors.append(f"nonfinite_at_key_{k}")
    return errors

def GOSUB_Mitigate(current: Any, errors: List[str], target: Optional[Callable] = None) -> Any:
    if isinstance(current, (list, tuple)):
        return [x for x in current if not (isinstance(x, float) and not math.isfinite(x))]
    if isinstance(current, dict):
        return {k: v for k, v in current.items() if not (isinstance(v, float) and not math.isfinite(v))}
    return current

def GOSUB_Retest(current: Any, target: Optional[Callable] = None) -> Any:
    if callable(target):
        result = target(current)
        if isinstance(result, dict) and "payload" in result and "sha256" in result:
            return result["payload"]
        return result
    return current

def GOSUB_Error_Test_Mitigate_Retest_Loop(target: Optional[Callable],
                                          input_data: Any,
                                          max_passes: int = 5,
                                          strict: bool = True) -> Dict[str, Any]:
    if not (isinstance(max_passes, int) and max_passes >= 1):
        raise KBLDEntryGuard("max_passes must be int >= 1")
    if target is not None and not callable(target):
        raise KBLDEntryGuard("target must be callable or None")
    current = input_data
    chain: List[Dict[str, Any]] = []
    errors = GOSUB_Error_Test(current, target)
    if not errors:
        return {"status": "CLEAN", "data": current, "passes": 0,
                "residual_errors": [], "provenance_chain": [GOSUB_Provenance_Attach(current)]}
    for p in range(1, max_passes + 1):
        before = list(errors)
        current = GOSUB_Mitigate(current, errors, target)
        current = GOSUB_Retest(current, target)
        errors = GOSUB_Error_Test(current, target)
        chain.append({"pass": p, "errors_before": before, "errors_after": list(errors),
                      "record": GOSUB_Provenance_Attach(current, context={"pass": p})})
        if not errors:
            return {"status": "MITIGATED", "data": current, "passes": p,
                    "residual_errors": [], "provenance_chain": chain}
        if len(errors) >= len(before):
            if strict:
                raise KBLDStagnation(f"pass {p}: error count did not shrink")
            return {"status": "FAILED_BUDGET", "data": current, "passes": p,
                    "residual_errors": errors, "provenance_chain": chain}
    if strict:
        raise KBLDMitigationBudgetExceeded(f"{max_passes} passes exhausted; residual: {errors}")
    return {"status": "FAILED_BUDGET", "data": current, "passes": max_passes,
            "residual_errors": errors, "provenance_chain": chain}

# Minimal self-test
if __name__ == "__main__":
    print("=== kbl_svct_stacks self-test ===")
    v = GOSUB_Error_Test_Mitigate_Retest_Loop(None, [1.0, 2.0, 3.0])
    assert v["status"] == "CLEAN"
    v = GOSUB_Error_Test_Mitigate_Retest_Loop(None, [1.0, float("nan"), 2.0])
    assert v["status"] == "MITIGATED" and v["data"] == [1.0, 2.0]
    g = GOSUB_MAD_Sigma_Guard([10.0, 10.1, 9.9, 1e9])
    assert 1e9 in g["flagged"]
    r = GOSUB_Provenance_Attach([1, 2, 3])
    assert len(r["sha256"]) == 64
    print("ALL GREEN")
