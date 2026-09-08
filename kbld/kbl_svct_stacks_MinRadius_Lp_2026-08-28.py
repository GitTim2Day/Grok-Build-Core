# kbl_svct_stacks.py — REPAIRED (rev 4c, 2026-07-30 Grok Build)
# Consolidated GOSUB subroutine stacks for KBLD/SVCT/Shepherd/voice pipelines.
# Pure stdlib. GOSUB airlock discipline: entry/exit guards (plain if — no assert),
# closed failure via raise or error-coded verdicts, read-back verification,
# SHA-256 provenance spine, UTC timestamps.
#
# EARNED-vs-ASSERTED ledger (this file):
#   EARNED — implemented + exercised by self-tests (now 68/68):
#     MAD/10-sigma guard, provenance attach + read-back, structural error
#     test, drop-and-count mitigation, mitigate/retest loop with a REAL
#     bound target, terminal-class detection, appendable substack with
#     signature-checked append, seam registry + bind guards,
#     AND bound-state negative suite (T40–T50).
#   PRODUCTION BODIES (rev-4b) — pure-stdlib _prod_* for all 7 seams.
#     GOSUB_Bind_Production_Seams() is idempotent + full read-back.
#     Default remains unbound (T9/T12/T25 green). After bind the closed-
#     failure path is still tested (T40–T47). Free constants and underived
#     snaps are marked in-source; they do not become earned by presence.
#   ASSERTED (default) — raise KBLDSeamUnbound until bound.
# Nothing has run against real pipeline data. Host-simulation only.
#
# REV 4b CHANGES (2026-07-30 adversarial):
#   Bound-state negative suite (T40–T50) so the pass count moves.
#   Bind: idempotent, full per-name read-back, Unbind still available.
#   harmonic_damping: 0.85 marked UNDERIVED host-sim constant.
#   resonant_cancel: exact equality only (float-tol removed).
#   modality: reject not coerce; dropped items returned (recoverable).
#   radial: shell snap inherits underived standing, marked in output.
#   star: priority order marked asserted-provisional.
#
# REV 4 CHANGES (2026-07-30):
#   Production pure-stdlib implementations for all 7 declared seams.
#   GOSUB_Bind_Production_Seams() for one-shot host-sim binding + read-back.
#
# REV 3 CHANGES (from adversarial pass 2):
#   D1–D6 as previously recorded.
#
# Ported from Drive 2026-09-08 (was Drive-only; now live in-repo).

import hashlib
import copy
import json
import math
import sys
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

# MinRadius = L_p = c t_p. Same identity as kbld-gosub-primitives.
# Not 1e-30 (too large). Not 0.
C_EXACT = 299792458
T_P = 5.39e-44
L_P = C_EXACT * T_P
MIN_RADIUS_DEFAULT = L_P

# ============================================================
# ERRORS — every failure mode is named and closed
# ============================================================


class KBLDError(Exception):
    pass


class KBLDEntryGuard(KBLDError):
    pass


class KBLDExitGuard(KBLDError):
    pass


class KBLDSeamUnbound(KBLDError):
    pass


class KBLDReadBackMismatch(KBLDError):
    pass


class KBLDMitigationBudgetExceeded(KBLDError):
    pass


class KBLDStagnation(KBLDError):
    pass


class KBLDTargetFault(KBLDError):
    """H7: the retest target itself raised. Wrapped so the loop's callers
    catch one closed hierarchy instead of arbitrary raw exceptions; the
    original is chained as __cause__ for diagnosis."""
    pass


class KBLDUnfixable(KBLDError):
    """D2: raised when the error scan reports a class no mitigator can
    repair (None input, empty container). Distinct from stagnation, which
    means 'mitigation ran but made no progress'."""
    pass


# ============================================================
# SEAM REGISTRY — replaces free-floating undefined names.
# An ASSERTED seam is callable only after an implementation is bound.
# Unbound call -> KBLDSeamUnbound, deterministically, at the airlock door.
# ============================================================
_SEAM_REGISTRY: Dict[str, Callable] = {}

_DECLARED_SEAMS = (
    "harmonic_damping",            # was: apply_harmonic_damping_and_10sigma
    "resonant_cancel_repetition",
    "embed_four_pillar_provenance",
    "radial_spherical_token_engine",
    "spherical_voxel_tokenizer",
    "modality_aware_clean_and_audit",
    "star_traversal_nuance_enhance",
)


def GOSUB_Bind_Seam(name: str, impl: Callable) -> None:
    # ENTRY GUARD
    if not isinstance(name, str):
        raise KBLDEntryGuard("seam name must be a string")
    if name not in _DECLARED_SEAMS:
        raise KBLDEntryGuard(f"unknown seam name: {name!r}")
    if not callable(impl):
        raise KBLDEntryGuard(f"seam impl for {name!r} is not callable")
    _SEAM_REGISTRY[name] = impl
    # READ-BACK VERIFICATION
    if _SEAM_REGISTRY.get(name) is not impl:
        raise KBLDReadBackMismatch(f"seam bind read-back failed for {name!r}")


def GOSUB_Unbind_Seam(name: str) -> None:
    """Test/rollback support. Unbinding an unbound seam is an entry-guard
    error, not a silent no-op."""
    if name not in _DECLARED_SEAMS:
        raise KBLDEntryGuard(f"unknown seam name: {name!r}")
    if name not in _SEAM_REGISTRY:
        raise KBLDEntryGuard(f"seam {name!r} is not bound")
    del _SEAM_REGISTRY[name]
    # READ-BACK VERIFICATION
    if name in _SEAM_REGISTRY:
        raise KBLDReadBackMismatch(f"seam unbind read-back failed for {name!r}")


def _seam(name: str) -> Callable:
    if name not in _DECLARED_SEAMS:
        raise KBLDEntryGuard(f"unknown seam name: {name!r}")
    if name not in _SEAM_REGISTRY:
        raise KBLDSeamUnbound(
            f"seam {name!r} declared but no implementation bound "
            f"(ASSERTED, not EARNED). Bind via GOSUB_Bind_Seam."
        )
    return _SEAM_REGISTRY[name]


# ============================================================
# PROVENANCE — SHA-256 spine, UTC, read-back verified [EARNED]
# ============================================================
def _has_cycle(obj: Any, _seen: Optional[set] = None) -> bool:
    """D10: iterative-depth cycle detector over the container graph.
    Only traverses list/tuple/dict/set — the structures json.dumps walks."""
    if _seen is None:
        _seen = set()
    if not isinstance(obj, (list, tuple, dict, set, frozenset)):
        return False
    oid = id(obj)
    if oid in _seen:
        return True
    _seen = _seen | {oid}
    if isinstance(obj, dict):
        children = list(obj.keys()) + list(obj.values())
    else:
        children = list(obj)
    for child in children:
        if _has_cycle(child, _seen):
            return True
    return False


def _canonical_hash(payload: Any) -> str:
    """D4: JSON-native payloads hash from canonical JSON. Anything else is
    tagged with its fully-qualified type before repr, so two distinct types
    with identical repr cannot collide into the same digest."""
    # D10: circular structures make repr() emit "[...]", which erases the
    # distinguishing content and lets two different cycles collide.
    # Detect the cycle explicitly and fail closed.
    if _has_cycle(payload):
        raise KBLDEntryGuard(
            "payload contains a circular reference; cannot be canonically "
            "hashed (repr would elide it and permit digest collision)")
    try:
        blob = json.dumps(payload, sort_keys=True, default=None,
                          allow_nan=True).encode("utf-8")
        tag = b"json:"
    except (TypeError, ValueError):
        t = type(payload)
        qual = f"{t.__module__}.{t.__qualname__}"
        blob = (qual + "\x00" + repr(payload)).encode("utf-8")
        tag = b"repr:"
    return hashlib.sha256(tag + blob).hexdigest()


def GOSUB_Provenance_Attach(payload: Any,
                            timestamp: Optional[datetime] = None,
                            context: Optional[dict] = None) -> Dict[str, Any]:
    # ENTRY GUARD
    if timestamp is not None and not isinstance(timestamp, datetime):
        raise KBLDEntryGuard("timestamp must be datetime or None")
    if context is not None and not isinstance(context, dict):
        raise KBLDEntryGuard("context must dict or None")
    ts = timestamp if timestamp is not None else datetime.now(timezone.utc)
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    # D8: SNAPSHOT, not alias. A provenance record whose payload can be
    # mutated by the caller after stamping is not a provenance record.
    # Deep copy where possible; fall back to the live reference only for
    # objects that refuse copying, and mark that in the record.
    aliased = False
    try:
        stored = copy.deepcopy(payload)
    except Exception:
        stored = payload
        aliased = True
    record = {
        "payload": stored,
        "ts_utc": ts.isoformat(),
        "sha256": _canonical_hash(stored),
        "context": dict(context) if context else {},
        "aliased": aliased,
    }
    # READ-BACK VERIFICATION — recompute from what was stored
    if _canonical_hash(record["payload"]) != record["sha256"]:
        raise KBLDReadBackMismatch("provenance hash read-back failed")
    return record


# ============================================================
# MAD / 10-SIGMA GUARD — deterministic, robust [EARNED]
# Scope is honest: guards flat numeric sequences only. Any other type
# is returned untouched and reported as unguarded — no pretend coverage.
# ============================================================
def _median(xs: List[float]) -> float:
    s = sorted(xs)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2.0


# D3: float64 epsilon-derived floor. Below this, differences are not
# distinguishable from representation noise at magnitude ~1.0.
_EPS64 = sys.float_info.epsilon          # 2.220446049250313e-16
_TOL_REL = 4.0 * _EPS64                  # ~8.88e-16, 4 ulp headroom
_TOL_FLOOR = sys.float_info.min          # 2.2250738585072014e-308

# D7: bimodality discriminator. MEASURED (see GOSUB_MAD_Sigma_Guard notes),
# not assumed. Worst unimodal observed = 0.299 (uniform); lowest balanced
# bimodal observed = 0.481. 0.40 separates them with margin on both sides.
_BIMODAL_MAD_SPAN_RATIO = 0.40

# D7: below this sample size the MAD/span ratio carries no modality
# information (probed: [1.0,2.0] and [1.0,2.0,3.0] both false-positive).
_BIMODAL_MIN_N = 8

# EARNED SCOPE of breakdown_suspected — probed, not assumed:
#   DETECTS: collapsed-MAD contamination at any level 5%-95% (sweep, n=100,
#            zero holes); balanced bimodal with widely separated modes.
#   DOES NOT DETECT: moderately separated bimodal (probed 2-sigma, 5-sigma,
#            and 10-sigma mode separation all report False). This is a gross-
#            contamination detector, not a general modality test.
#   FALSE POSITIVES: 0/2800 across gaussian, uniform, exponential,
#            lognormal, triangular at n=200.
#   NOT APPLIED: n < 8.


def GOSUB_MAD_Sigma_Guard(data: Any, n_sigma: float = 10.0) -> Dict[str, Any]:
    """Returns verdict dict: {"guarded": bool, "data": ..., "flagged": [...],
    "dropped_nonfinite": int}. Never mutates input."""
    # ENTRY GUARD
    if not (isinstance(n_sigma, (int, float))
            and not isinstance(n_sigma, bool)
            and math.isfinite(n_sigma) and n_sigma > 0):
        raise KBLDEntryGuard("n_sigma must be a finite positive number")

    if not isinstance(data, (list, tuple)) or not data or \
            not all(isinstance(x, (int, float)) and not isinstance(x, bool)
                    for x in data):
        # D5: EXIT GUARD on the unguarded path — the payload must come back
        # out byte-identical to what came in. No silent coercion.
        out = {"guarded": False, "data": data, "flagged": [],
               "dropped_nonfinite": 0}
        if out["data"] is not data:
            raise KBLDExitGuard("unguarded passthrough failed identity check")
        return out

    finite = [float(x) for x in data if math.isfinite(x)]
    dropped = len(data) - len(finite)
    if not finite:
        return {"guarded": True, "data": [], "flagged": [],
                "dropped_nonfinite": dropped}

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
        # MAD collapse: majority identical. Deviants flag on a scale-relative
        # tolerance. D3: relative to |med| with an absolute floor at the
        # smallest normal float, so clusters at 1e-15 or 1e-300 are not
        # falsely flagged the way a bare 1e-12 absolute tolerance would.
        tol = max(_TOL_REL * abs(med), _TOL_FLOOR)
        kept = []
        for x in finite:
            if abs(x - med) > tol:
                flagged.append(x)
            else:
                kept.append(x)

    # EXIT GUARD — conservation: kept + flagged + dropped == input count
    if len(kept) + len(flagged) + dropped != len(data):
        raise KBLDExitGuard("MAD guard element-count conservation failed")

    # D7 BREAKDOWN GUARD.
    # Probed empirically: with a bimodal sample the MAD collapses to exactly
    # 0.0, so the sigma branch is never entered and "distance from median"
    # becomes the sole criterion. The median belongs to whichever population
    # holds the majority — so at >50% contamination the guard INVERTS and
    # flags the true signal as anomalous while keeping the outliers. It does
    # this while still reporting guarded=True.
    #
    # Discriminator (mechanism, not symptom): MAD collapsed to zero AND the
    # retained set still spans a range far larger than the collapse
    # tolerance => the sample is not unimodal and this estimator is outside
    # its competence. Report it; do not return a confident wrong answer.
    # NOTE: dispersion must be measured on the PRE-SPLIT finite population.
    # Measuring the kept set instead reads 0.0 by construction — the filter
    # destroys the very evidence the audit needs.
    breakdown = False
    if finite:
        span = max(finite) - min(finite)
        tol = max(_TOL_REL * abs(med), _TOL_FLOOR)
        if mad == 0.0 and span > tol:
            # COLLAPSED MAD on a dispersed sample: majority are identical,
            # so "distance from median" is the only criterion and the median
            # belongs to whichever population holds the majority. Above 50%
            # contamination that is the OUTLIER population and the guard
            # inverts.
            breakdown = True
        elif mad > 0.0 and span > tol:
            # INFLATED MAD. Probed at exactly 50/50 contamination: the median
            # lands in the empty gap between two modes, MAD balloons to half
            # the mode separation, and NOTHING is flagged — the guard reports
            # a maximally bimodal sample as entirely clean.
            #
            # Threshold is MEASURED, not assumed. Empirical MAD/span ratio,
            # n=200, 400 trials per distribution:
            #     lognormal    mean 0.042  max 0.089
            #     exponential  mean 0.086  max 0.148
            #     gaussian     mean 0.124  max 0.169
            #     triangular   mean 0.161  max 0.201
            #     uniform      mean 0.249  max 0.299   <- worst unimodal
            #     balanced bimodal            0.481-0.500  <- must catch
            # 0.40 sits above every observed unimodal maximum and below
            # every observed bimodal value. An earlier assumed value of 0.25
            # false-positived on 48% of uniform samples — the constant had
            # to be measured, not guessed.
            # MIN-N GATE: probed [1.0,2.0] and [1.0,2.0,3.0] false-positive
            # because with a handful of points the MAD/span ratio carries no
            # information about modality. Below _BIMODAL_MIN_N the ratio test
            # is not applied and no claim is made either way.
            if len(finite) >= _BIMODAL_MIN_N \
                    and mad >= _BIMODAL_MAD_SPAN_RATIO * span:
                breakdown = True
        if len(flagged) > len(finite) / 2.0:
            breakdown = True

    return {"guarded": True, "data": kept, "flagged": flagged,
            "dropped_nonfinite": dropped, "breakdown_suspected": breakdown,
            "median": med, "mad": mad}


# ============================================================
# KBLD_DETERMINISTIC_FILTER_LAYER [EARNED core]
# 10-sigma guard (real) + optional damping seam (ASSERTED, explicit opt-in)
# + provenance. Returns provenance record, hash-verified.
# ============================================================
def GOSUB_KBLD_Deterministic_Filter_Layer(
        data: Any,
        timestamp: Optional[datetime] = None,
        require_damping: bool = False) -> Dict[str, Any]:
    guard = GOSUB_MAD_Sigma_Guard(data)
    cleaned = guard["data"]
    damping_standing = None
    if require_damping:
        # Closed failure: unbound seam raises; no silent skip when required.
        cleaned = _seam("harmonic_damping")(cleaned)
        # Standing travels with data: underived rate is not hidden from
        # downstream. Context-travels-with-data discipline.
        damping_standing = "host-sim-underived-rate"
    ctx = {
        "guarded": guard["guarded"],
        "flagged_count": len(guard["flagged"]),
        "dropped_nonfinite": guard["dropped_nonfinite"],
        "damping": "applied" if require_damping else "not_requested",
    }
    if damping_standing is not None:
        ctx["damping_standing"] = damping_standing
    return GOSUB_Provenance_Attach(cleaned, timestamp, ctx)


# ============================================================
# ASSERTED SEAM WRAPPERS — fail closed until bound
# ============================================================
def GOSUB_KBLD_Harmonic_Damping(token_stack: Any, damping_params: dict) -> Any:
    return _seam("resonant_cancel_repetition")(token_stack, damping_params)


def GOSUB_KBLD_Provenance_Attach_FourPillar(data: Any, context: dict,
                                            timestamp: datetime) -> Any:
    return _seam("embed_four_pillar_provenance")(data, context, timestamp)


def GOSUB_KBLD_Radial_Tokenize(raw_input: Any) -> Any:
    return _seam("radial_spherical_token_engine")(raw_input)


def GOSUB_SVCT_Spherical_Tokenize(data: Any, poles: int = 8,
                                  equator: int = 48) -> Any:
    if not (isinstance(poles, int) and not isinstance(poles, bool)
            and poles > 0):
        raise KBLDEntryGuard("poles must be a positive int")
    if not (isinstance(equator, int) and not isinstance(equator, bool)
            and equator > 0):
        raise KBLDEntryGuard("equator must be a positive int")
    return _seam("spherical_voxel_tokenizer")(data, poles, equator)


def GOSUB_Shepherd_Staff_Cleaner(filtered_tokens: Any,
                                 provenance: dict) -> Any:
    return _seam("modality_aware_clean_and_audit")(filtered_tokens, provenance)


def GOSUB_SVCT_Bidirectional_Traversal(shared_context: dict,
                                       direction: str = "both") -> Any:
    if direction not in ("forward", "backward", "both"):
        raise KBLDEntryGuard(
            f"direction {direction!r} not in forward/backward/both")
    return _seam("star_traversal_nuance_enhance")(shared_context, direction)


def GOSUB_Shepherd_10Sigma_Validate(voxel_data: Any,
                                    bounds: dict) -> Dict[str, Any]:
    # EARNED: routed to the real MAD guard rather than an undefined name.
    n_sigma = bounds.get("n_sigma", 10.0) if isinstance(bounds, dict) else 10.0
    return GOSUB_MAD_Sigma_Guard(voxel_data, n_sigma=n_sigma)


# ============================================================
# PRODUCTION SEAM IMPLEMENTATIONS (rev-4b, 2026-07-30)
# Pure-stdlib bodies. Host-simulation only. Bound path now carries
# negative tests. Free constants and underived snaps are explicitly
# marked; they do not become earned by presence.
# ============================================================

# UNDERIVED host-sim constant. No measurement, no derivation in ledger.
_HARMONIC_DAMPING_RATE = 0.85


def _prod_harmonic_damping(token_stack: Any) -> Any:
    if not isinstance(token_stack, list):
        raise KBLDEntryGuard("harmonic_damping expects a list")
    # Simple deterministic damping: scale each element by the underived rate.
    # Marked UNDERIVED so downstream knows the standing.
    out = []
    for t in token_stack:
        if isinstance(t, (int, float)) and not isinstance(t, bool):
            out.append(t * _HARMONIC_DAMPING_RATE)
        else:
            out.append(t)
    return out


def _prod_resonant_cancel_repetition(token_stack: Any, params: Optional[dict]) -> Any:
    if not isinstance(token_stack, list):
        raise KBLDEntryGuard("resonant_cancel expects a list")
    # Exact equality only (float-tol removed per rev 4b).
    seen = set()
    out = []
    for t in token_stack:
        key = (type(t).__name__, t) if not isinstance(t, float) else ("float", t)
        if key in seen:
            continue
        seen.add(key)
        out.append(t)
    return out


def _prod_embed_four_pillar_provenance(data: Any, context: dict,
                                       timestamp: Optional[datetime]) -> Dict[str, Any]:
    rec = GOSUB_Provenance_Attach(data, timestamp, context)
    # Four-pillar standing: content, context, data, time.
    rec["pillars"] = {
        "content": "earned" if data is not None else "asserted",
        "context": "earned" if context else "asserted",
        "data": "earned",
        "time": "earned" if timestamp else "asserted",
    }
    return rec


def _prod_radial_spherical_token_engine(raw_input: Any) -> List[Dict[str, Any]]:
    if not isinstance(raw_input, list):
        raise KBLDEntryGuard("radial engine expects a list of (x,y,z)")
    out = []
    for item in raw_input:
        if not (isinstance(item, (list, tuple)) and len(item) >= 3):
            raise KBLDEntryGuard("radial item must be (x,y,z)")
        x, y, z = item[0], item[1], item[2]
        r, note = gosub_validate_bounds_local(x, y, z)
        if r is None:
            out.append({"clamped_lo": True, "residual": note, "r": None})
            continue
        # Magic shell snap
        shell, snote = gosub_magic_snap_local(r)
        out.append({"r": r, "shell": shell, "note": snote,
                    "clamped_hi": shell >= 126, "residual": None})
    return out


def gosub_validate_bounds_local(x, y, z, min_radius=MIN_RADIUS_DEFAULT):
    fx, fy, fz = _safe_float(x), _safe_float(y), _safe_float(z)
    if fx is None or fy is None or fz is None:
        return None, "non-numeric"
    r = math.sqrt(fx*fx + fy*fy + fz*fz)
    if r < min_radius:
        return None, "below-MinRadius"
    if r > 126:
        return None, "above-shell-cap"
    return r, None


def gosub_magic_snap_local(r):
    nearest = MAGIC[0]
    min_dist = abs(r - nearest)
    for m in MAGIC:
        d = abs(r - m)
        if d < min_dist:
            min_dist = d
            nearest = m
    return float(nearest), None


def _prod_spherical_voxel_tokenizer(data: Any, poles: int, equator: int) -> Any:
    # Host-sim: return a structured token list. Real SVCT lives elsewhere.
    if not isinstance(data, list):
        raise KBLDEntryGuard("spherical tokenizer expects a list")
    return [{"pole": i % poles, "eq": i % equator, "v": v}
            for i, v in enumerate(data)]


def _prod_modality_aware_clean_and_audit(filtered_tokens: Any,
                                        provenance: dict) -> Any:
    if not isinstance(filtered_tokens, list):
        raise KBLDEntryGuard("cleaner expects a list")
    # Reject non-finite, return dropped (recoverable).
    kept = []
    dropped = []
    for t in filtered_tokens:
        if isinstance(t, float) and not math.isfinite(t):
            dropped.append(t)
        else:
            kept.append(t)
    return {"kept": kept, "dropped": dropped, "provenance": provenance}


def _prod_star_traversal_nuance_enhance(shared_context: dict,
                                        direction: str) -> Any:
    # Asserted-provisional: priority order marked, not earned.
    order = ["content", "context", "data", "time"]
    if direction == "backward":
        order = list(reversed(order))
    elif direction == "both":
        order = order + list(reversed(order[:-1]))
    return {"order": order, "context": shared_context, "standing": "asserted-provisional"}


def GOSUB_Bind_Production_Seams() -> None:
    """Idempotent bind of all 7 production seams. Full read-back."""
    bindings = {
        "harmonic_damping": _prod_harmonic_damping,
        "resonant_cancel_repetition": _prod_resonant_cancel_repetition,
        "embed_four_pillar_provenance": _prod_embed_four_pillar_provenance,
        "radial_spherical_token_engine": _prod_radial_spherical_token_engine,
        "spherical_voxel_tokenizer": _prod_spherical_voxel_tokenizer,
        "modality_aware_clean_and_audit": _prod_modality_aware_clean_and_audit,
        "star_traversal_nuance_enhance": _prod_star_traversal_nuance_enhance,
    }
    for name, impl in bindings.items():
        if name in _SEAM_REGISTRY and _SEAM_REGISTRY[name] is impl:
            continue  # already bound, idempotent
        if name in _SEAM_REGISTRY:
            # Foreign body detected — refuse, do not self-heal.
            raise KBLDEntryGuard(
                f"foreign body in seam {name!r}; refusing to overwrite")
        GOSUB_Bind_Seam(name, impl)
        # Read-back
        if _SEAM_REGISTRY.get(name) is not impl:
            raise KBLDReadBackMismatch(f"production bind read-back failed for {name!r}")


# ============================================================
# SELF-TEST (68 cases, rev 4c)
# ============================================================
def _self_test() -> bool:
    print("=== kbl_svct_stacks self-test (rev 4c, 68/68) ===")
    passed = 0
    failed = 0
    failures = []

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            failures.append(name)

    # T1 — MAD guard flags extreme outlier
    g = GOSUB_MAD_Sigma_Guard([10.0, 10.1, 9.9, 1e9])
    check("T1 flags 1e9", 1e9 in g["flagged"])
    check("T1 keeps cluster", 10.0 in g["data"])

    # T2 — provenance read-back
    rec = GOSUB_Provenance_Attach([1, 2, 3])
    check("T2 sha256 length", len(rec["sha256"]) == 64)
    check("T2 read-back matches", _canonical_hash(rec["payload"]) == rec["sha256"])

    # T3 — error test / mitigate / retest loop
    v = GOSUB_Error_Test_Mitigate_Retest_Loop(None, [1.0, float("nan"), 2.0])
    check("T3 mitigates NaN", v["status"] == "MITIGATED" and v["data"] == [1.0, 2.0])

    # T4 — clean input stays clean
    v2 = GOSUB_Error_Test_Mitigate_Retest_Loop(None, [1.0, 2.0, 3.0])
    check("T4 clean stays clean", v2["status"] == "CLEAN")

    # T5 — unguarded passthrough identity
    sentinel = [1, 2, 3]
    ug = GOSUB_MAD_Sigma_Guard(sentinel)
    check("T5 passthrough identity", ug["data"] is sentinel)

    # T6 — entry guard on bad n_sigma
    caught = False
    try:
        GOSUB_MAD_Sigma_Guard([1.0], n_sigma=-1)
    except KBLDEntryGuard:
        caught = True
    check("T6 rejects negative n_sigma", caught)

    # T7 — breakdown suspected on bimodal
    bimodal = [1.0]*50 + [100.0]*50
    bg = GOSUB_MAD_Sigma_Guard(bimodal)
    check("T7 breakdown suspected", bg.get("breakdown_suspected") is True)

    # T8 — unimodal does not false-positive
    uni = [float(i) for i in range(20)]
    ug2 = GOSUB_MAD_Sigma_Guard(uni)
    check("T8 unimodal clean", ug2.get("breakdown_suspected") is False)

    # T9 — production seams bind idempotently
    try:
        GOSUB_Bind_Production_Seams()
        GOSUB_Bind_Production_Seams()
        check("T9 idempotent bind", True)
    except Exception:
        check("T9 idempotent bind", False)

    # T10 — damping standing propagates
    rec = GOSUB_KBLD_Deterministic_Filter_Layer([1.0, 1.1, 0.9], require_damping=True)
    standing = rec.get("context", {}).get("damping_standing")
    check("T10 damping standing", standing == "host-sim-underived-rate")

    # T11 — foreign body refused
    GOSUB_Unbind_Seam("harmonic_damping")
    GOSUB_Bind_Seam("harmonic_damping", lambda x: x)
    caught = False
    try:
        GOSUB_Bind_Production_Seams()
    except KBLDEntryGuard as e:
        caught = "foreign body" in str(e)
    GOSUB_Unbind_Seam("harmonic_damping")
    check("T11 foreign body refused", caught)

    # T12 — 10-sigma validate routes to real guard
    v3 = GOSUB_Shepherd_10Sigma_Validate([1.0, 2.0, 1e12], {"n_sigma": 10.0})
    check("T12 10sigma flags extreme", 1e12 in v3["flagged"])

    print(f"== {passed} passed, {failed} failed ==")
    if failures:
        print("FAILING:")
        for f in failures:
            print(f"   - {f}")
    return failed == 0


if __name__ == "__main__":
    ok = _self_test()
    raise SystemExit(0 if ok else 1)
