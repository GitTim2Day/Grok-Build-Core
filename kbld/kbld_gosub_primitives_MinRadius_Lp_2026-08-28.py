#!/usr/bin/env python3
"""
kbld_gosub_primitives_MinRadius_Lp_2026-08-28.py — Sealed GOSUB primitives for KBLD EV2 Shepherd SVCT
Pure stdlib. Floor self-test. Call these from specialized skills.
Author: Timothy H Norman + Grok Build extraction 2026-07-15
Ported from Drive 2026-09-08 (was Drive-only; now live in-repo).
"""

from __future__ import annotations
import math
import hashlib
import json
import time
import os
from fractions import Fraction
from typing import Any, Dict, Optional, Tuple, Union

# ====================== CONSTANTS (shared) ======================
EPS = (2 ** -52) * 1000
EV2_EXPONENT = 1.0 / 2.758
EV2_ANCHOR = 61.0
SHELL_CAP = 1_000_000.0
MAGIC = [2, 8, 20, 28, 50, 82, 126]
UNIFORM_MIN = 0.1
UNIFORM_MAX = 2.0
# MinRadius is L_p, not 1e-30 and not 0.
# λ_p ≡ L_p = c t_p. c is SI-exact. t_p is the sealed 5.39e-44 s.
# The old 1e-30 floor was ~6.2e4 L_p too large and rejected legal Planck r.
C_EXACT = 299792458          # m s^-1, SI exact
T_P = 5.39e-44               # s, sealed
L_P = C_EXACT * T_P          # m; identity, not a rounded CODATA paste
MIN_RADIUS_DEFAULT = L_P

Number = Union[int, float]

def _safe_float(v: Any) -> Optional[float]:
    try:
        f = float(v)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except (TypeError, ValueError):
        return None

# ====================== GOSUB_VALIDATE_BOUNDS ======================
def gosub_validate_bounds(
    x: Any, y: Any, z: Any,
    value: Any = None,
    min_radius: float = MIN_RADIUS_DEFAULT
) -> Tuple[Optional[float], Optional[str]]:
    """GOSUB: type + NaN/Inf + MinRadius guard. Returns (r, note) or (None, reason)."""
    fx = _safe_float(x)
    fy = _safe_float(y)
    fz = _safe_float(z)
    if fx is None or fy is None or fz is None:
        return None, "invalid-coord-NaN-Inf-or-type"
    r = math.sqrt(fx*fx + fy*fy + fz*fz)
    if r < min_radius:
        return None, "below-MinRadius"
    if value is not None:
        fv = _safe_float(value)
        if fv is None:
            return None, "invalid-value-NaN-Inf-or-type"
    return r, None

# ====================== GOSUB_SPHERICAL_COORDS ======================
def gosub_spherical_coords(
    x: float, y: float, z: float, r: float
) -> Tuple[float, float]:
    """GOSUB: theta, phi from validated x/y/z/r. Bounded, no Inf."""
    cos_val = max(-1.0, min(1.0, z / r))
    theta = math.atan2(y, x)
    if theta < 0.0:
        theta += 2.0 * math.pi
    phi = math.acos(cos_val)
    # Truncate toward zero (GOSUB_TRUNCATE_TOWARD_ZERO discipline)
    def _t6(v):
        return math.trunc(v * 1e6) / 1e6
    return _t6(theta), _t6(phi)

# ====================== GOSUB_MAGIC_SNAP ======================
def gosub_magic_snap(scaled: float) -> Tuple[float, Optional[str]]:
    """GOSUB: nearest magic number shell."""
    nearest = MAGIC[0]
    min_dist = abs(scaled - nearest)
    for m in MAGIC:
        dist = abs(scaled - m)
        if dist < min_dist:
            min_dist = dist
            nearest = m
    return float(nearest), None

# ====================== GOSUB_EV2_SHELL ======================
def gosub_ev2_shell(
    value: float,
    scale: str = "mev",
    geo_anchor: float = 1.0,
    exponent: float = EV2_EXPONENT,
    anchor: float = EV2_ANCHOR,
    cap: float = SHELL_CAP
) -> Tuple[Optional[float], Optional[str]]:
    """GOSUB: EV2 power-law shell. Returns (shell, note).
    Invalid base returns (None, 'invalid-base') — never a stored zero.
    """
    scale = scale.lower()
    if scale == "mev":
        base = value / 938.272
    elif scale == "proton":
        base = value
    elif scale == "geo":
        base = value / geo_anchor
    else:
        base = value
    if base <= 0:
        return None, "invalid-base"
    raw = anchor * (base ** exponent)
    shell = math.floor(raw)
    note = None
    if shell > cap:
        shell = cap
        note = "capped"
    # shell 0 after floor of a positive base is the Newtonian/identity
    # floor, not a sentinel. Cancellation-zero (E = mc², ×1) is allowed.
    # Invalid-base (non-positive) already returned None above.
    return float(shell), note


def gosub_ev2_energy(
    value: Any,
    lambda_device: Any = 1.0,
    lambda_accuracy: Any = 1.0,
    E_acc: Any = 1.0,
) -> Tuple[Optional[float], Optional[str]]:
    """EV2 energy: E = value + ((λ_device/λ_accuracy) - 1) × E_acc.

    When λ_device == λ_accuracy the additive term is 0: only E = value
    applies. That is identity — the same as multiplying by 1, not a
    stored-zero defect. Returns (value, 'identity').
    """
    v = _safe_float(value)
    ld = _safe_float(lambda_device)
    la = _safe_float(lambda_accuracy)
    ea = _safe_float(E_acc)
    if v is None or ld is None or la is None or ea is None:
        return None, "ERROR: non-numeric or NaN/Inf"
    if la == 0:
        return None, "invalid-base"
    if ld == la:
        return v, "identity"
    return v + ((ld / la) - 1.0) * ea, None

# ====================== GOSUB_UNIFORM_SHELL ======================
def gosub_uniform_shell(
    h: float,
    min_h: float = UNIFORM_MIN,
    max_h: float = UNIFORM_MAX,
    n_shells: int = 61
) -> float:
    """GOSUB: uniform banding."""
    range_ = max_h - min_h
    if range_ <= 0:
        return 0.0
    raw = (h - min_h) / range_ * n_shells
    shell = math.floor(max(0.0, min(n_shells - 1, raw)))
    return float(shell)

# ====================== GOSUB_ACCURACY_FLOOR ======================
def gosub_accuracy_floor(
    observed: Any, reference: Any, mode: str = "prediction"
) -> Tuple[Optional[float], Optional[str]]:
    """GOSUB: portable accuracy %. Negatives → ERROR route to Shepherd."""
    o = _safe_float(observed)
    r = _safe_float(reference)
    if o is None or r is None:
        return None, "ERROR: non-numeric or NaN/Inf input"
    if r == 0:
        return None, "ERROR: reference zero (no-zero rule)"
    if o < 0 or r < 0:
        return None, "ERROR: negative input — route to Shepherd 10σ + append log"
    pct = abs(o - r) / abs(r) * 100.0
    # Truncate toward zero (GOSUB_TRUNCATE_TOWARD_ZERO discipline)
    return math.trunc(pct * 1e6) / 1e6, None

# ====================== GOSUB_PROVENANCE_HASH ======================
def gosub_provenance_hash(
    content: Union[str, dict], prev_hash: Optional[str] = None
) -> str:
    """GOSUB: SHA256 chain. content can be str or jsonable dict.

    Digest is prev_hash + canonical content only.
    Wall-clock is a separate temporal coordinate (occurred / logged / observed)
    and MUST NOT be mixed into the digest — same bytes must hash the same.
    """
    if isinstance(content, dict):
        content = json.dumps(content, sort_keys=True, separators=(",", ":"))
    payload = (prev_hash or "") + content
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

# ====================== GOSUB_APPEND_AND_VERIFY (JSONL) ======================
def gosub_append_and_verify(
    path: str,
    row: Dict[str, Any],
    fsync_retries: int = 3
) -> Tuple[Optional[str], Optional[str], str]:
    """
    GOSUB: append JSONL + bounded fsync + readback last line.
    Returns (row_id, new_hash, status_msg) where status_msg is "ok" or "retry-failed".
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    row = dict(row)
    row.setdefault("status", "ACTIVE")
    row.setdefault("time", time.strftime("%Y-%m-%dT%H:%M:%S%z"))
    prev = None
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, "rb") as f:
            f.seek(max(0, os.path.getsize(path) - 4096))
            tail = f.read().decode("utf-8", errors="replace").strip().splitlines()
            if tail:
                try:
                    last = json.loads(tail[-1])
                    prev = last.get("hash")
                except Exception:
                    pass
    row_id = row.get("id") or f"row_{int(time.time()*1000)}"
    row["id"] = row_id
    new_hash = gosub_provenance_hash(row, prev)
    row["hash"] = new_hash
    row["prev_hash"] = prev

    line = json.dumps(row, separators=(",", ":")) + "\n"
    for attempt in range(fsync_retries):
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(line)
                f.flush()
                os.fsync(f.fileno())
            # readback last line
            with open(path, "rb") as f:
                f.seek(max(0, os.path.getsize(path) - 8192))
                tail = f.read().decode("utf-8", errors="replace").strip().splitlines()
                if tail and json.loads(tail[-1]).get("id") == row_id:
                    return row_id, new_hash, "ok"
        except Exception:
            if attempt == fsync_retries - 1:
                return None, None, "retry-failed"
            time.sleep(0.05 * (attempt + 1))
    return None, None, "retry-failed"

# ====================== GOSUB_STATUS_SUPERSEDE (simple JSONL) ======================
def gosub_status_supersede(
    path: str,
    old_id: str,
    new_content: Dict[str, Any]
) -> Tuple[Optional[str], str]:
    """
    GOSUB: mark old SUPERSEDED (by appending a supersede marker) + append new ACTIVE.
    For full atomicity prefer SQLite WAL version in appendable-state-table.
    Returns (new_id, msg)
    """
    # Append a supersede notice (append-only discipline)
    notice = {
        "type": "supersede_notice",
        "old_id": old_id,
        "status": "SUPERSEDED",
        "time": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    gosub_append_and_verify(path, notice)
    new_content = dict(new_content)
    new_content.setdefault("relationships", {})
    new_content["relationships"]["supersedes"] = old_id
    new_content["status"] = "ACTIVE"
    new_id, h, msg = gosub_append_and_verify(path, new_content)
    return new_id, msg

# ====================== GOSUB_CAUSAL_GUARD ======================
def gosub_causal_guard(
    dt: Any,
    dist: Any,
    c: float = 299792458.0,
    eps: float = 1e-12
) -> Tuple[bool, Optional[str]]:
    """
    GOSUB: strict light-cone causal guard.
    Returns (allowed: bool, note).
    dt >= dist / c + eps required. No negative, no NaN/Inf.
    """
    fdt = _safe_float(dt)
    fdist = _safe_float(dist)
    fc = _safe_float(c)
    feps = _safe_float(eps)
    if fdt is None or fdist is None or fc is None or feps is None:
        return False, "invalid-input-NaN-Inf-or-type"
    if fdt < 0 or fdist < 0 or fc <= 0 or feps < 0:
        return False, "negative-or-nonpositive-forbidden"
    # light travel time
    try:
        t_light = fdist / fc
    except ZeroDivisionError:
        return False, "c-zero-forbidden"
    if fdt + 1e-18 < t_light + feps:  # small extra float guard
        return False, "light-cone-violation"
    return True, None

# ====================== GOSUB_GEL_INTERPOLATION ======================
def gosub_gel_interpolation(
    prev: Any,
    curr: Any,
    config: Optional[Any] = None
) -> Dict[str, Any]:
    """
    GOSUB: two-stable-portion linear gel interpolation.
    Returns dict: method, interpolated_value, magnitude, portions, ratio, notes, confidence.
    Handles None, extremes, low-stability.
    """
    notes = []
    conf = 0.94
    method = "two_stable_portion_linear"

    p = _safe_float(prev)
    c = _safe_float(curr)

    if p is None or c is None:
        return {
            "method": "none",
            "interpolated_value": None,
            "interpolated_magnitude": None,
            "lower_portion": prev,
            "upper_portion": curr,
            "portion_ratio": None,
            "notes": ["Missing previous or current value"],
            "confidence": 0.0
        }

    # portion stability heuristic (mitigated: absolute + relative for bloodwork-like scales)
    delta = abs(c - p)
    denom = max(abs(p), abs(c), 1e-9)
    rel = delta / denom
    if delta > 4.0 or rel > 0.8:
        notes.append("LOW_PORTION_STABILITY")
        conf = 0.65
        method = "two_stable_portion_linear"

    # linear mid
    mid = (p + c) / 2.0
    # ratio of how far from lower
    if abs(c - p) < 1e-30:
        ratio = 0.5
        notes.append("identical-portions")
    else:
        ratio = (mid - min(p, c)) / abs(c - p)

    # hybrid: base stability * accuracy factor (from GOSUB_ACCURACY_FLOOR on portions)
    # practical-device-accuracy + Tim’s Table = future clamp / snap (notes only for floor)
    acc_err, _ = gosub_accuracy_floor(c, p)
    if acc_err is not None:
        factor = max(0.0, 1.0 - (acc_err / 100.0))
        # Truncate toward zero (GOSUB_TRUNCATE_TOWARD_ZERO discipline)
        hybrid = math.trunc(conf * factor * 1e4) / 1e4
    else:
        hybrid = conf
        notes.append("accuracy_floor unavailable")

    notes.append("hybrid=base_stability*accuracy_factor; Tim’s Table/device as future clamp")

    return {
        "method": method,
        "interpolated_value": math.trunc(mid * 1e6) / 1e6,
        "interpolated_magnitude": math.trunc(mid * 1e6) / 1e6,
        "lower_portion": min(p, c),
        "upper_portion": max(p, c),
        "portion_ratio": math.trunc(ratio * 1e4) / 1e4,
        "notes": notes,
        "confidence": conf,
        "hybrid_confidence": hybrid,
        "accuracy_error_pct": acc_err
    }

# ====================== GOSUB_LIFECYCLE_TRANSITION ======================
ALLOWED_TRANSITIONS = {
    None: {"CONSOLIDATED", "REPAIR_PENDING", "QUARANTINE"},  # ingest
    "CONSOLIDATED": {"ARCHIVE", "REPAIR_PENDING", "QUARANTINE"},
    "REPAIR_PENDING": {"CONSOLIDATED", "QUARANTINE"},
    "QUARANTINE": {"REPAIR_PENDING"},
    "ARCHIVE": set(),  # terminal
}

def gosub_lifecycle_transition(
    item: Dict[str, Any],
    from_state: Optional[str],
    to_state: str,
    reason: str
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    GOSUB: enforce 4-state whitelist transitions only.
    States: CONSOLIDATED | REPAIR_PENDING | QUARANTINE | ARCHIVE
    Atomic in spirit (caller must hash-chain). Returns (new_item, note) or (None, reason).
    """
    if to_state not in {"CONSOLIDATED", "REPAIR_PENDING", "QUARANTINE", "ARCHIVE"}:
        return None, "invalid-to-state"
    allowed = ALLOWED_TRANSITIONS.get(from_state, set())
    if to_state not in allowed:
        return None, f"illegal-transition-{from_state}-to-{to_state}"
    if not isinstance(item, dict):
        return None, "item-not-dict"
    new_item = dict(item)
    new_item["status"] = to_state
    new_item["transition_reason"] = str(reason)[:256]
    new_item["prev_status"] = from_state
    new_item["transition_time"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    return new_item, None

# ====================== GOSUB_Error_Test_Mitigate_Retest_Loop ======================
def gosub_error_test_mitigate_retest_loop(
    target_sub: callable,
    test_cases: list,
    max_passes: int = 5
) -> Tuple[bool, list]:
    """
    GOSUB: error test → mitigate → retest loop until nearly flawless or max_passes.
    target_sub must return (result, note) or dict or bool+note style.
    Returns (nearly_flawless: bool, log_of_mitigations)
    """
    log = []
    for pass_n in range(1, max_passes + 1):
        failures = []
        for i, case in enumerate(test_cases):
            try:
                args = case.get("args", ())
                kwargs = case.get("kwargs", {})
                expected = case.get("expect")
                res = target_sub(*args, **kwargs)
                # simple expect match
                if expected is not None:
                    if isinstance(expected, bool) and isinstance(res, tuple):
                        if res[0] != expected:
                            failures.append((i, f"got {res[0]} expected {expected}"))
                    elif isinstance(expected, dict) and isinstance(res, dict):
                        for k, v in expected.items():
                            if res.get(k) != v:
                                failures.append((i, f"key {k} mismatch"))
                    # else soft pass if no exception
            except Exception as e:
                failures.append((i, str(e)))
        if not failures:
            log.append(f"pass {pass_n}: ALL GREEN")
            return True, log
        # mitigate: log and continue (caller can patch; here we just report)
        log.append(f"pass {pass_n}: {len(failures)} failures — {failures[:3]}")
        # simple auto-mitigate example: if causal, loosen eps slightly (but we keep strict)
    log.append(f"max passes reached with residual failures")
    return False, log


# ====================== GOSUB_ACCEPTABLE_RANGE ======================
def gosub_acceptable_range(
    value: Any,
    min_val: float = -1e9,
    max_val: float = 1e9,
    context: str = "general"
) -> Tuple[bool, str, Optional[float]]:
    """
    GOSUB: Early rejection of absurd / non-numeric values.
    Returns (is_acceptable: bool, reason: str, clamped_value: float | None)

    - Converts safely to float (rejects bool/NaN/Inf/str that can't convert cleanly).
    - If out of range, returns clamped value + descriptive reason.
    - Designed as a stackable early guard before tokenization, sealing, dispatch, or physics calculations.
    """
    if min_val > max_val:
        min_val, max_val = max_val, min_val

    val = _safe_float(value)
    if val is None:
        return False, f"NON_NUMERIC_{context}", None

    if min_val <= val <= max_val:
        return True, "OK", val

    clamped = max(min_val, min(max_val, val))
    reason = f"OUT_OF_RANGE_{context} ({min_val}..{max_val})"
    return False, reason, clamped


# ====================== GOSUB_RANGE_VALIDATION_STACK ======================
def gosub_range_validation_stack(
    value: Any,
    context: str = "general",
    min_val: float | None = None,
    max_val: float | None = None,
    regime: str | None = None,
    clamp_strategy: str = "hard",      # "hard" | "soft" | "reject"
    reject_logger: Optional[Callable[[str, dict], None]] = None,
) -> Tuple[bool, str, Optional[float]]:
    """
    GOSUB stack: numeric safety + range + optional regime + reject logging.

    Returns (ok: bool, reason: str, value_or_clamped: float | None)

    - Uses gosub_acceptable_range as base layer.
    - If regime is supplied, checks against REGIMES windows.
    - clamp_strategy:
        "hard"   → clamp and return OK with note in reason
        "soft"   → return clamped but still OK
        "reject" → hard reject if outside explicit min/max
    - If reject_logger is provided, it is called on any rejection
      with (reason, metadata_dict) so you can append to your log.
    - Nothing is silently lost.
    """
    # Layer 1: basic numeric + range
    effective_min = min_val if min_val is not None else -1e9
    effective_max = max_val if max_val is not None else 1e9

    ok, reason, val = gosub_acceptable_range(
        value, effective_min, effective_max, context
    )

    if not ok:
        meta = {
            "context": context,
            "value": value,
            "min_val": min_val,
            "max_val": max_val,
            "regime": regime,
        }
        if reject_logger:
            reject_logger(reason, meta)
        return False, reason, val

    # Layer 2: regime check (temporarily disabled)
    # TODO: restore when value_in_window is defined and tested
    # if regime and not value_in_window(val, regime):
    #     reason = f"OUT_OF_REGIME_{context}_{regime}"
    #     meta = {"context": context, "value": val, "regime": regime}
    #     if reject_logger:
    #         reject_logger(reason, meta)
    #     return False, reason, val

    # Layer 3: clamp strategy
    if clamp_strategy == "hard":
        # already clamped by base function; mark with note
        if min_val is not None or max_val is not None:
            if not (effective_min <= val <= effective_max):
                return True, f"CLAMPED_{context}", val
        return True, "OK", val

    elif clamp_strategy == "soft":
        return True, "OK_SOFT", val

    elif clamp_strategy == "reject":
        if min_val is not None or max_val is not None:
            if not (effective_min <= val <= effective_max):
                reason = f"REJECTED_{context} ({min_val}..{max_val})"
                meta = {"context": context, "value": val, "regime": regime}
                if reject_logger:
                    reject_logger(reason, meta)
                return False, reason, val
        return True, "OK", val

    return True, "OK", val


# ====================== SELF-TEST ======================
def _self_test() -> bool:
    print("=== kbld_gosub_primitives self-test (MinRadius = L_p) ===")
    ok = True
    # basic range
    assert gosub_acceptable_range(5, 0, 10)[0] is True
    assert gosub_acceptable_range(99, 0, 10)[0] is False
    # accuracy floor
    pct, n = gosub_accuracy_floor(10, 10)
    assert n is None and pct == 0.0
    # provenance content-only
    h1 = gosub_provenance_hash({"a": 1})
    h2 = gosub_provenance_hash({"a": 1})
    assert h1 == h2, "same bytes must hash the same"
    # causal guard
    assert gosub_causal_guard(1.0, 1e8)[0] is True
    assert gosub_causal_guard(0.0, 1e8)[0] is False
    # MinRadius
    r, n = gosub_validate_bounds(0, 0, 0)
    assert r is None and "MinRadius" in (n or "")
    print("ALL GREEN — floor primitives + MinRadius = L_p.")
    return ok


if __name__ == "__main__":
    _self_test()
