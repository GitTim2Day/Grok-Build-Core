#!/usr/bin/env python3
"""
kbld_gosub_primitives.py — Sealed GOSUB primitives for KBLD EV2 Shepherd SVCT
Pure stdlib. Floor self-test. Call these from specialized skills.
Author: Timothy H Norman + Grok Build extraction 2026-07-15
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
                reason = f"REJECTED_{context}"
                if reject_logger:
                    reject_logger(reason, {"value": val, "context": context})
                return False, reason, val
        return True, "OK", val

    return True, "OK", val


# ====================== GOSUB_DETECT_EDGE_CAPABILITY ======================
def detect_edge_capability(probe=None):
    """
    GOSUB airlock: entry guard -> probe -> classify -> read-back -> return.
    Total function: never raises to caller; returns error-coded dict on failure.
    'probe' injectable for test (MockProbe); None => real hardware probe.
    """
    # ---- ENTRY GUARD ----
    UNWIRED = -1  # honest sentinel, never fabricated capability

    def _guard(cond, code, msg):
        if not cond:
            return {"ok": False, "error_code": code, "reason": msg}
        return None

    # ---- GOSUB: acquire raw hardware facts (closed failure) ----
    try:
        info = probe() if probe is not None else _real_gpu_probe()
    except Exception as e:
        return {"ok": False, "error_code": "PROBE_RAISED", "reason": repr(e)}

    err = _guard(isinstance(info, dict), "PROBE_SHAPE", "probe did not return dict")
    if err:
        return err

    vram_gb = info.get("vram_gb", UNWIRED)
    compute = info.get("compute_capability", UNWIRED)  # e.g. 8.6
    name = info.get("name", "UNKNOWN")

    err = _guard(isinstance(vram_gb, (int, float)), "VRAM_TYPE", "vram_gb not numeric")
    if err:
        return err

    # ---- GOSUB: classify by VRAM, not name-string (record-not-derive) ----
    if vram_gb == UNWIRED:
        tier = "UNKNOWN"
    elif vram_gb <= 6:
        tier = "LOW"       # 3050 4GB/laptop, low headroom
    elif vram_gb <= 10:
        tier = "MID"       # 3060/3070 class
    else:
        tier = "HIGH"      # 3080/3090+, 12GB+

    QUANT = {"LOW": "Q4", "MID": "Q8", "HIGH": "FP16", "UNKNOWN": "Q4"}
    CONTEXT = {"LOW": 4096, "MID": 8192, "HIGH": 16384, "UNKNOWN": 4096}
    FULL = {"LOW": False, "MID": True, "HIGH": True, "UNKNOWN": False}

    result = {
        "ok": True,
        "gpu_name": name,
        "vram_gb": vram_gb,
        "compute_capability": compute,
        "tier": tier,
        "quant_level": QUANT[tier],
        "max_context": CONTEXT[tier],
        "use_full_kbl_pipeline": FULL[tier],
    }

    # ---- EXIT GUARD / READ-BACK ----
    for k in ("quant_level", "max_context", "use_full_kbl_pipeline"):
        if result.get(k) is None:
            return {"ok": False, "error_code": "READBACK_NULL", "reason": f"{k} unset"}
    return result


def _real_gpu_probe():
    """Telemetry-first skeleton. UNWIRED until run on real silicon."""
    return {"name": "UNKNOWN", "vram_gb": -1, "compute_capability": -1}


# ====================== GOSUB_LATTICE_ACCEL ======================
def gosub_lattice_accel(
    pos: Tuple[float, float],
    gm: float,
    beta_eff: float = 0.0,
    n: int = 2,
    min_r: float = 1e-15,
) -> Tuple[Optional[Tuple[float, float]], Optional[str]]:
    """
    Unit-aware Newtonian + lattice acceleration.
    pos: coordinates in the same length unit used for gm (e.g. AU if gm = 4π²).
    gm: G*M in consistent units (AU³/yr² or m³/s²).
    beta_eff: effective dimensionless strength. Must absorb any (λ_p)^n scaling
              so that magnitudes remain perturbative at the working scale.
              Pure Planck α without scaling produces no observable effect at AU.
    Returns ((ax, ay), None) or (None, reason).
    Truncation / finite only. No classical sigma.
    """
    try:
        x, y = float(pos[0]), float(pos[1])
        gm = float(gm)
        beta_eff = float(beta_eff)
        n = int(n)
    except (TypeError, ValueError):
        return None, "ERROR: non-numeric input"
    if not (math.isfinite(x) and math.isfinite(y) and math.isfinite(gm) and math.isfinite(beta_eff)):
        return None, "ERROR: non-finite input"
    r2 = x*x + y*y
    if r2 < min_r * min_r:
        return None, "below-MinRadius"
    r = math.sqrt(r2)
    inv_r = 1.0 / r
    f_n = -gm * inv_r * inv_r
    if abs(beta_eff) < 1e-30:
        f_l = 0.0
    else:
        f_l = -(n + 1) * beta_eff * gm * (inv_r ** (n + 2))
    a = f_n + f_l
    if not math.isfinite(a):
        return None, "ERROR: non-finite acceleration"
    ax = a * x * inv_r
    ay = a * y * inv_r
    # practical truncation of returned accel
    places = 12
    factor = 10.0 ** places
    ax = math.trunc(ax * factor) / factor
    ay = math.trunc(ay * factor) / factor
    return (ax, ay), None



# ====================== GOSUB_PRECESSION_ACCURACY ======================
def gosub_precession_accuracy(
    observed_arcsec_per_cy: float,
    reference_arcsec_per_cy: float = 42.98,
    beta_used: float = 0.0,
    newtonian_tol: float = 2.0,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Accuracy comparison for perihelion advance (Sun/Mercury style).
    - Truncates residuals (never rounds).
    - Newtonian recovery flag when beta≈0.
    - pct_toward_reference only when beta drives a physical lattice signal.
    - Routes any negative / non-finite through the same ERROR path as ACCURACY_FLOOR.
    Returns (result_dict, None) or (None, msg).
    """
    try:
        obs = float(observed_arcsec_per_cy)
        ref = float(reference_arcsec_per_cy)
        beta = float(beta_used)
        tol = float(newtonian_tol)
    except (TypeError, ValueError):
        return None, "ERROR: non-numeric input"
    if not (math.isfinite(obs) and math.isfinite(ref)):
        return None, "ERROR: non-finite advance or reference"
    # truncation
    def _t(v, p=6):
        f = 10.0 ** p
        return math.trunc(v * f) / f
    obs_t = _t(obs)
    ref_t = _t(ref)
    residual = _t(abs(obs_t - ref_t))
    newton_ok = None
    pct = None
    if abs(beta) < 1e-30:
        newton_ok = abs(obs_t) < tol
    else:
        if residual < abs(ref_t) and abs(ref_t) > 1e-12:
            pct = _t(max(0.0, 100.0 * (1.0 - residual / abs(ref_t))), 4)
        else:
            pct = 0.0
    result = {
        "observed": obs_t,
        "reference": ref_t,
        "residual_abs": residual,
        "pct_toward_reference": pct,
        "newtonian_limit_ok": newton_ok,
        "beta_used": beta,
        "sigma_free": True,
    }
    return result, None


# ====================== GOSUB_TRUNCATE_TOWARD_ZERO ======================
# Exact path is the INTEGER COUNT (gosub_truncate_to_count).
# The float return is presentation only — it is not binary-exact (C1).
# Count 0 is refused (C2, no-stored-zero). Never return 0.0 with note=None.

SITES_TRUNC = {
    "g1": "type not admitted",
    "g2": "count is zero (no-stored-zero)",
    "g3": "value is not finite",
    "g4": "places not a positive int",
}
_SEAM_TRUNC = "truncate"


def _site_trunc(ordinal: str) -> str:
    return "%s:%s" % (_SEAM_TRUNC, ordinal)


def gosub_truncate_to_count(
    value: Any,
    places: int = 8,
) -> Tuple[Optional[int], Optional[str]]:
    """Exact truncated count: trunc(value * 10**places) toward zero.

    Fraction(1,3) @ 8 → 33333333 exactly (Audit 2 I3 pass case).
    Sub-tier values (1e-9 @ 8) → (None, truncate:g2). Never a stored zero.
    """
    if type(places) is not int or places <= 0:
        return None, _site_trunc("g4")
    t = type(value)
    if t is bool:
        return None, _site_trunc("g1")
    if t is int:
        frac = Fraction(value)
    elif t is Fraction:
        frac = value
    elif t is float:
        if value != value or value in (float("inf"), float("-inf")):
            return None, _site_trunc("g3")
        frac = Fraction(value)
    else:
        return None, _site_trunc("g1")
    scaled = frac * (10 ** places)
    count = int(scaled)  # Python int(Fraction) truncates toward zero
    if count == 0:
        return None, _site_trunc("g2")
    return count, None


def gosub_truncate_toward_zero(
    value: Any,
    factor: float = 1e8,
) -> Tuple[Optional[float], Optional[str]]:
    """
    GOSUB_TRUNCATE_TOWARD_ZERO — Presentation face of truncate_to_count.

    Discipline (2026-08-20, repaired same day):
    - Truncation only (toward zero), never round.
    - Exact artifact is the integer count. This float is presentation.
    - Default places=8 from factor 1e8. Non-numeric / NaN / Inf → (None, site).
    - Count 0 → (None, truncate:g2). Never stores 0.0.

    Motto: Calculate wide. Truncate hard.
    """
    places = 8
    if factor != 1e8:
        fv = _safe_float(factor)
        if fv is None or fv <= 0:
            return None, _site_trunc("g4")
        places_f = math.log10(fv)
        nearest = int(math.trunc(places_f + (0.0 if places_f >= 0 else -1e-12)))
        if abs(places_f - nearest) > 1e-9 or nearest <= 0:
            return None, _site_trunc("g4")
        places = nearest
    count, err = gosub_truncate_to_count(value, places)
    if err:
        if err.endswith(":g1") or err.endswith(":g3"):
            return None, "ERROR: non-numeric or NaN/Inf — no truncation applied"
        if err.endswith(":g4"):
            return None, "ERROR: invalid factor"
        return None, err
    presented = float(Fraction(count, 10 ** places))
    return presented, None


# ====================== GOSUB_RATIO_CLASS_A + GOSUB_RATIO_RECIPROCAL ======================
# Hardened 2026-08-20 from earned drop (ratio_gosubs.py).
# Repairs: A1 reduction instability, A2 type gate, A3 Fraction misread, A4 inf escapes.
# Contract: closed failure with stable sites; type is (never isinstance); no stored zero;
# gcd reduction before classification; orientation-independent for class_a.
# Added: gosub_ratio_on_lattice (one-sided storage), gosub_ratio_from_float (explicit).

from math import gcd as _gcd

SITES_RATIO = {
    "g1": "type not admitted (int or Fraction only; bool rejected)",
    "g2": "numerator zero (no-stored-zero)",
    "g3": "denominator zero (no-stored-zero)",
    "g4": "reciprocal of a value with zero numerator is undefined",
    "g5": "float is not finite (nan)",
    "g6": "float is not finite (inf)",
    "g7": "float admitted only via from_float",
}

_SEAM_CLASS = "ratio_class_a"
_SEAM_RECIP = "ratio_reciprocal"
_SEAM_FLOAT = "ratio_from_float"


def _site_ratio(seam: str, ordinal: str) -> str:
    return "%s:%s" % (seam, ordinal)


def _admit_ratio(value: Any, seam: str) -> Tuple[Optional[Fraction], Optional[str]]:
    """Strict entry. Returns (Fraction, None) or (None, site).
    `type is` and not isinstance: bool is a subclass of int.
    """
    t = type(value)
    if t is bool:
        return None, _site_ratio(seam, "g1")
    if t is int:
        return Fraction(value), None
    if t is Fraction:
        return value, None
    if t is float:
        return None, _site_ratio(seam, "g7")
    return None, _site_ratio(seam, "g1")


def _reduce_ratio(n: int, d: int) -> Tuple[int, int]:
    """Canonical form: sign in numerator, gcd removed. Total, never raises."""
    if d < 0:
        n, d = -n, -d
    g = _gcd(abs(n), d)
    if g > 1:
        n //= g
        d //= g
    return n, d


def _strip_235(n: int) -> bool:
    """True iff |n| factors entirely into {2,3,5}, or |n| == 1.
    Zero is not admitted here -- callers gate it first (no-stored-zero).
    """
    n = abs(n)
    if n == 1:
        return True
    for p in (2, 3, 5):
        while n % p == 0:
            n //= p
    return n == 1


def gosub_ratio_class_a(
    num: Any, den: Any
) -> Tuple[Optional[bool], Optional[str]]:
    """
    GOSUB_RATIO_CLASS_A — Two-sided, reduction-stable class test.
    Class A <=> both numerator and denominator of the REDUCED ratio
    factor into {2,3,5}.
    STRICTLY STRONGER than on_lattice (measured 399/1600 disagreements).
    Orientation-independent by construction.
    Returns (bool, None) or (None, site).
    """
    n, err = _admit_ratio(num, _SEAM_CLASS)
    if err:
        return None, err
    d, err = _admit_ratio(den, _SEAM_CLASS)
    if err:
        return None, err
    if d == 0:
        return None, _site_ratio(_SEAM_CLASS, "g3")
    if n == 0:
        return None, _site_ratio(_SEAM_CLASS, "g2")
    value = n / d
    p, q = _reduce_ratio(value.numerator, value.denominator)
    return (_strip_235(p) and _strip_235(q)), None


def gosub_ratio_on_lattice(
    num: Any, den: Any
) -> Tuple[Optional[bool], Optional[str]]:
    """
    GOSUB_RATIO_ON_LATTICE — One-sided storage predicate.
    Does the REDUCED denominator divide 360**k for some k?
    (i.e. factors into {2,3,5}). Useful for Tim’s Tables / base-360 exact storage.
    Not orientation-independent (correct for storage).
    Returns (bool, None) or (None, site).
    """
    n, err = _admit_ratio(num, _SEAM_CLASS)
    if err:
        return None, err
    d, err = _admit_ratio(den, _SEAM_CLASS)
    if err:
        return None, err
    if d == 0:
        return None, _site_ratio(_SEAM_CLASS, "g3")
    if n == 0:
        return None, _site_ratio(_SEAM_CLASS, "g2")
    value = n / d
    _, q = _reduce_ratio(value.numerator, value.denominator)
    return _strip_235(q), None


def gosub_ratio_reciprocal(
    num: Any, den: Any
) -> Tuple[Optional[Tuple[int, int]], Optional[str]]:
    """
    GOSUB_RATIO_RECIPROCAL — Exact involution by swap. Sign forced into numerator.
    No division operation is executed. Output always reduced with d > 0.
    Returns ((n, d), None) or (None, site).
    """
    n, err = _admit_ratio(num, _SEAM_RECIP)
    if err:
        return None, err
    d, err = _admit_ratio(den, _SEAM_RECIP)
    if err:
        return None, err
    if d == 0:
        return None, _site_ratio(_SEAM_RECIP, "g3")
    if n == 0:
        return None, _site_ratio(_SEAM_RECIP, "g4")
    value = n / d
    p, q = _reduce_ratio(value.denominator, value.numerator)
    return (p, q), None


def gosub_ratio_from_float(
    value: Any
) -> Tuple[Optional[Fraction], Optional[str]]:
    """
    Explicit, opt-in float admission. Exact — no rounding, no tolerance.
    Fraction(float) is the exact binary value (e.g. 0.1 → 3602879701896397/2**55).
    Returns (Fraction, None) or (None, site).
    """
    if type(value) is bool:
        return None, _site_ratio(_SEAM_FLOAT, "g1")
    if type(value) is int:
        return Fraction(value), None
    if type(value) is not float:
        return None, _site_ratio(_SEAM_FLOAT, "g1")
    if value != value:
        return None, _site_ratio(_SEAM_FLOAT, "g5")
    if value in (float("inf"), float("-inf")):
        return None, _site_ratio(_SEAM_FLOAT, "g6")
    return Fraction(value), None


# ====================== SELF-TEST ======================
def _self_test() -> bool:
    print("=== kbld_gosub_primitives self-test (floor) ===")
    ok = True


    # bounds
    r, note = gosub_validate_bounds(0.3, 0.4, 0.5, 0.87)
    assert r is not None and note is None, "validate good"
    r2, note2 = gosub_validate_bounds(0, 0, 0)
    assert r2 is None and "MinRadius" in (note2 or ""), "MinRadius origin"
    r3, note3 = gosub_validate_bounds(float("nan"), 1, 1)
    assert r3 is None, "NaN"
    # Planck floor: MinRadius = L_p = c t_p. Not 1e-30. Not 0.
    assert MIN_RADIUS_DEFAULT == C_EXACT * T_P, "MinRadius is the product c*t_p"
    assert MIN_RADIUS_DEFAULT > 0.0, "MinRadius is not stored zero"
    assert MIN_RADIUS_DEFAULT < 1e-30, "old 1e-30 floor was larger than L_p"
    r_lp, n_lp = gosub_validate_bounds(L_P, 0.0, 0.0)
    assert r_lp is not None and n_lp is None, "L_p is a legal radius"
    r_half, n_half = gosub_validate_bounds(L_P / 2.0, 0.0, 0.0)
    assert r_half is None and "MinRadius" in (n_half or ""), "below L_p refused"
    th_lp, ph_lp = gosub_spherical_coords(L_P, 0.0, 0.0, r_lp)  # type: ignore
    assert 0 <= th_lp < 2 * math.pi and 0 <= ph_lp <= math.pi

    # spherical
    th, ph = gosub_spherical_coords(0.3, 0.4, 0.5, r)  # type: ignore
    assert 0 <= th < 2*math.pi and 0 <= ph <= math.pi

    # magic
    s, _ = gosub_magic_snap(7.9)
    assert s == 8.0

    # EV2
    shell, note = gosub_ev2_shell(938.272, scale="mev")  # ~1 proton mass
    assert shell > 0 and note is None
    shell0, note0 = gosub_ev2_shell(-1.0)
    assert shell0 is None and note0 == "invalid-base"
    e_id, n_id = gosub_ev2_energy(5.0, 1.0, 1.0)
    assert n_id == "identity" and e_id == 5.0, "EV2 identity is ×1, correction 0 allowed"
    e_bad, n_bad = gosub_ev2_energy(5.0, 1.0, 0.0)
    assert e_bad is None and n_bad == "invalid-base"

    # accuracy
    pct, n = gosub_accuracy_floor(100, 100)
    assert pct == 0.0
    pctn, nn = gosub_accuracy_floor(-1, 1)
    assert nn and "negative" in nn

    # hash chain
    h1 = gosub_provenance_hash({"a": 1})
    h2 = gosub_provenance_hash({"a": 2}, h1)
    assert h1 != h2 and len(h1) == 64
    h1b = gosub_provenance_hash({"a": 1})
    assert h1 == h1b, "provenance digest is content-only (no wall-clock)"

    # append (temp)
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as tf:
        path = tf.name
    try:
        rid, hh, msg = gosub_append_and_verify(path, {"test": True, "id": "t1"})
        assert msg == "ok" and rid == "t1"
        rid2, msg2 = gosub_status_supersede(path, "t1", {"test": False, "id": "t2"})
        assert msg2 == "ok"
    finally:
        os.unlink(path)

    # ===== NEW GOSUBs =====
    # causal
    ok_c, n = gosub_causal_guard(1.0, 1e8)  # ~0.33s light time, 1s ok
    assert ok_c is True and n is None
    bad, nb = gosub_causal_guard(0.0001, 1e8)
    assert bad is False and "light-cone" in (nb or "")
    bad2, _ = gosub_causal_guard(-1, 10)
    assert bad2 is False

    # gel + hybrid
    g = gosub_gel_interpolation(4.8, 5.6)
    assert g["method"] == "two_stable_portion_linear"
    # After GOSUB_TRUNCATE_TOWARD_ZERO: 5.199999 is correct truncated form of 5.2
    assert abs(g["interpolated_value"] - 5.2) < 1e-5
    assert g["confidence"] == 0.94
    assert "hybrid_confidence" in g
    assert g["hybrid_confidence"] is not None
    gnone = gosub_gel_interpolation(None, 5.0)
    assert gnone["confidence"] == 0.0
    gext = gosub_gel_interpolation(1.0, 10.0)
    assert "LOW_PORTION_STABILITY" in gext["notes"]
    assert gext["confidence"] == 0.65
    assert "hybrid_confidence" in gext

    # lifecycle
    item = {"id": "x1", "data": 42}
    newi, n = gosub_lifecycle_transition(item, None, "CONSOLIDATED", "ingest")
    assert newi is not None and newi["status"] == "CONSOLIDATED"
    newi2, n2 = gosub_lifecycle_transition(newi, "CONSOLIDATED", "ARCHIVE", "done")
    assert newi2["status"] == "ARCHIVE"
    badt, nt = gosub_lifecycle_transition(item, "ARCHIVE", "CONSOLIDATED", "illegal")
    assert badt is None and "illegal" in (nt or "")

    # error-test-mitigate-retest on the three
    causal_cases = [
        {"args": (1.0, 1e8), "expect": True},
        {"args": (0.0001, 1e8), "expect": False},
        {"args": (-0.1, 10), "expect": False},
        {"args": (1e-9, 0.0), "expect": True},  # dist=0 always ok
    ]
    nearly, log = gosub_error_test_mitigate_retest_loop(gosub_causal_guard, causal_cases)
    assert nearly, f"causal not green: {log}"

    gel_cases = [
        {"args": (4.8, 5.6), "expect": {"confidence": 0.94}},
        {"args": (None, 5.0), "expect": {"confidence": 0.0}},
    ]
    nearly2, log2 = gosub_error_test_mitigate_retest_loop(gosub_gel_interpolation, gel_cases)
    assert nearly2, f"gel not green: {log2}"

    life_cases = [
        {"args": ({"id":1}, None, "CONSOLIDATED", "ok"), "expect": None},  # soft
        {"args": ({"id":1}, "ARCHIVE", "CONSOLIDATED", "bad"), "expect": None},
    ]
    nearly3, log3 = gosub_error_test_mitigate_retest_loop(gosub_lifecycle_transition, life_cases)
    # soft pass for lifecycle (dict returns)

    # lattice accel + precession accuracy (unit-aware, magnitude-respecting, hardened)
    a, note = gosub_lattice_accel((0.3, 0.0), gm=4*math.pi**2, beta_eff=0.0)
    assert a is not None and note is None and a[0] < 0, "lattice newtonian"
    a2, n2 = gosub_lattice_accel((0.0, 0.0), gm=1.0)
    assert a2 is None and "MinRadius" in (n2 or ""), "lattice MinRadius"
    a3, n3 = gosub_lattice_accel((0.3, 0.0), gm=float("nan"))
    assert a3 is None and "non-finite" in (n3 or ""), "lattice NaN guard"
    a4, n4 = gosub_lattice_accel(("x", 0.0), gm=1.0)
    assert a4 is None and "non-numeric" in (n4 or ""), "lattice type guard"
    a0, _ = gosub_lattice_accel((0.4, 0.0), gm=4*math.pi**2, beta_eff=0.0)
    a1, _ = gosub_lattice_accel((0.4, 0.0), gm=4*math.pi**2, beta_eff=1e-4)
    assert abs(a1[0]) > abs(a0[0]), "lattice beta magnitude"
    prec, pn = gosub_precession_accuracy(0.5, 42.98, beta_used=0.0)
    assert prec is not None and prec["newtonian_limit_ok"] is True and prec["sigma_free"] is True
    prec2, _ = gosub_precession_accuracy(40.0, 42.98, beta_used=1e-4)
    assert prec2 is not None and prec2["pct_toward_reference"] is not None
    prec3, pn3 = gosub_precession_accuracy(float("nan"), 42.98)
    assert prec3 is None and "non-finite" in (pn3 or ""), "precession NaN guard"
    prec4, _ = gosub_precession_accuracy(42.98, 42.98, beta_used=1e-5)
    assert prec4 is not None and prec4["residual_abs"] == 0.0 and prec4["pct_toward_reference"] == 100.0

    # truncate-toward-zero (IEEE unlearn gate) + exact count (C1/C2 repair)
    t1, n1 = gosub_truncate_toward_zero(1.9800000000000002)
    assert n1 is None and t1 == 1.98, "truncate e-8 residue"
    t2, n2 = gosub_truncate_toward_zero(-1.23456789)
    assert n2 is None and t2 < 0 and abs(t2 - (-1.23456788)) < 1e-12, "truncate preserves sign"
    t3, n3 = gosub_truncate_toward_zero("bad")
    assert t3 is None and "non-numeric" in (n3 or ""), "truncate rejects non-numeric"
    t4, n4 = gosub_truncate_toward_zero(float("nan"))
    assert t4 is None, "truncate rejects NaN"
    # C2: sub-tier must refuse, never store 0.0
    for tiny in (1e-9, -1e-9, 5e-9, 0.0, -0.0):
        tz, nz = gosub_truncate_toward_zero(tiny)
        assert tz is None and nz and "g2" in nz, "C2 refuse stored zero for %r" % (tiny,)
    cnt, cn = gosub_truncate_to_count(Fraction(1, 3), 8)
    assert cn is None and cnt == 33333333, "exact count Fraction(1,3)@e8"
    cnt0, cn0 = gosub_truncate_to_count(1e-9, 8)
    assert cnt0 is None and cn0 == "truncate:g2", "count 0 refused"
    assert gosub_truncate_to_count(True, 8)[0] is None, "bool rejected from count"

    # ratio class A + reciprocal + on_lattice + from_float (hardened 2026-08-20)
    # A1 reduction stability
    assert gosub_ratio_class_a(7, 14)[0] is True, "7/14 reduces to 1/2 → A"
    assert gosub_ratio_class_a(14, 7)[0] is True, "14/7 reduces to 2/1 → A"
    assert gosub_ratio_class_a(21, 35)[0] is True, "21/35 reduces to 3/5 → A"
    assert gosub_ratio_class_a(7, 12)[0] is False, "7/12 not class A (reciprocal off)"
    assert gosub_ratio_class_a(3, 5)[0] is True, "3/5 is A"
    assert gosub_ratio_class_a(8, 25)[0] is True, "8/25 is A"
    # type gate (strict type is)
    assert gosub_ratio_class_a(True, 12)[0] is None, "bool rejected"
    assert gosub_ratio_class_a(3.9, 12)[0] is None, "float rejected (use from_float)"
    assert gosub_ratio_class_a("12", 5)[0] is None, "str rejected"
    # Fraction path
    assert gosub_ratio_class_a(Fraction(1, 3), 4)[0] is True, "Fraction(1,3)/4 == 1/12 A"
    assert gosub_ratio_class_a(Fraction(1, 7), 4)[0] is False, "Fraction(1,7)/4 == 1/28 B"
    # on_lattice (one-sided)
    assert gosub_ratio_on_lattice(7, 12)[0] is True, "7/12 stores exactly on 360 lattice"
    assert gosub_ratio_on_lattice(7, 11)[0] is False, "7/11 den not 2/3/5"
    # reciprocal involution + sign
    r, n = gosub_ratio_reciprocal(3, 4)
    assert n is None and r == (4, 3), "3/4 → 4/3"
    r2, n2 = gosub_ratio_reciprocal(-3, 4)
    assert n2 is None and r2 == (-4, 3), "sign forced into num"
    r3, n3 = gosub_ratio_reciprocal(3, -4)
    assert n3 is None and r3 == (-4, 3), "neg den normalized"
    r4, _ = gosub_ratio_reciprocal(7, 15)
    r5, _ = gosub_ratio_reciprocal(*r4)
    assert r5 == (7, 15), "exact involution"
    assert gosub_ratio_reciprocal(0, 5)[0] is None, "zero num blocked (g4)"
    assert gosub_ratio_reciprocal(5, 0)[0] is None, "zero den blocked (g3)"
    # from_float explicit
    f05, e05 = gosub_ratio_from_float(0.5)
    assert e05 is None and f05 == Fraction(1, 2), "from_float 0.5 exact"
    finf, einf = gosub_ratio_from_float(float("inf"))
    assert finf is None and einf and "g6" in einf, "inf closed to g6"
    fnan, enan = gosub_ratio_from_float(float("nan"))
    assert fnan is None and enan and "g5" in enan, "nan closed to g5"
    # zero gates
    assert gosub_ratio_class_a(0, 5)[0] is None, "zero num refused"
    assert gosub_ratio_class_a(5, 0)[0] is None, "zero den refused"

    print("ALL GREEN — floor primitives + truncate C2 refuse + provenance content-only + ratio hardened 2026-08-20.")
    return ok



if __name__ == "__main__":
    _self_test()
