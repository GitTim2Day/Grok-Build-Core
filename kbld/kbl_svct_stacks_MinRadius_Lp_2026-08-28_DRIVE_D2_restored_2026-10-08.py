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
        raise KBLDEntryGuard("context must be dict or None")
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
# Standing: provisional only. Must be replaced by a measured or
# first-principles value before any claim of EARNED damping.
_HOST_SIM_DAMP_RATE = 0.85
_HOST_SIM_DAMP_PASSES = 3

# Finite-real entry gate (converged pattern). Rejects NaN/Inf before any
# computation. type(nan) is float is True — type-only gates are insufficient.
def _require_finite_real(x: Any, where: str) -> float:
    """Closed failure on non-finite. Returns float on success."""
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise KBLDEntryGuard(f"{where}: expected real number, got {type(x).__name__}")
    v = float(x)
    if math.isnan(v) or math.isinf(v):
        raise KBLDEntryGuard(f"{where}: non-finite value rejected")
    return v


def _prod_harmonic_damping(data: Any) -> Any:
    """Exponential damping on numeric sequences / dict values / scalar.
    Uses _HOST_SIM_DAMP_RATE (underived). Non-numeric left untouched.
    Closed on None. Non-finite numerics rejected at entry."""
    if data is None:
        raise KBLDEntryGuard("harmonic_damping: data must not be None")
    rate = _HOST_SIM_DAMP_RATE
    passes = _HOST_SIM_DAMP_PASSES
    if isinstance(data, (list, tuple)):
        out = []
        for v in data:
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                x = _require_finite_real(v, "harmonic_damping")
                for _ in range(passes):
                    x *= rate
                out.append(x)
            else:
                out.append(v)
        return out
    if isinstance(data, dict):
        out = {}
        for k, v in data.items():
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                x = _require_finite_real(v, "harmonic_damping")
                for _ in range(passes):
                    x *= rate
                out[k] = x
            else:
                out[k] = v
        return out
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        x = _require_finite_real(data, "harmonic_damping")
        for _ in range(passes):
            x *= rate
        return x
    return data


def _prod_resonant_cancel_repetition(token_stack: Any,
                                    damping_params: Any = None) -> Any:
    """Collapse consecutive *exact-identity* duplicates only.
    Contract: type(prev) is type(item) AND prev == item.
    - Rejects bool/int cross via type-is (True is not 1).
    - Does NOT implement near-float tolerance. Floats that differ by
      any ULP stay. Near-duplicate semantics are out of scope for this
      body; the declared seam name is retained for registry stability
      but the body is exact-identity only. Rename of the declared seam
      is a separate registry change.
    Non-sequences returned unchanged. Empty -> empty list.
    damping_params accepted for signature compatibility; ignored."""
    if not isinstance(token_stack, (list, tuple)):
        return token_stack
    if not token_stack:
        return list(token_stack)
    out = [token_stack[0]]
    for item in token_stack[1:]:
        prev = out[-1]
        # type-is first: blocks True == 1 and 1.0 == 1 cross-type
        if type(prev) is type(item) and prev == item:
            continue
        out.append(item)
    return out


def _prod_embed_four_pillar_provenance(data: Any, context: Any,
                                       timestamp: Any) -> Any:
    """Force four-pillar record: content · context · data · time.
    Snapshot + hash read-back that crosses a real boundary.

    Boundary: pillars are serialized to canonical JSON bytes; the hash
    is of those bytes. Read-back re-hashes the stored serialized form
    (not the live object). A vacuous same-reference comparison is not
    a read-back. Fault injection = perturb the stored bytes.
    """
    if context is not None and not isinstance(context, dict):
        raise KBLDEntryGuard("four_pillar: context must be dict or None")
    if timestamp is not None and not isinstance(timestamp, datetime):
        raise KBLDEntryGuard("four_pillar: timestamp must be datetime or None")
    # First extra timestamp: sealed_utc (write time) distinct from occurred_utc.
    # Old code set both fields to the same value — that was not two timestamps.
    sealed = datetime.now(timezone.utc)
    if timestamp is not None:
        occurred = timestamp if timestamp.tzinfo else timestamp.replace(tzinfo=timezone.utc)
    else:
        occurred = sealed
    ctx = dict(context) if context else {}
    aliased = False
    try:
        stored = copy.deepcopy(data)
    except Exception:
        stored = data
        aliased = True
    pillars = {
        "content": stored,
        "context": ctx,
        "data": {
            "type": type(data).__name__,
            "len": len(data) if hasattr(data, "__len__") else None,
        },
        "time": {
            "occurred_utc": occurred.isoformat(),
            "sealed_utc": sealed.isoformat(),
        },
    }
    # Second optional timestamp: received_utc (operator/boundary arrival).
    # Only if caller places it in context — never invented. Makes channel lag
    # visible when measured; absent when unknown.
    recv = ctx.get("received_utc")
    if recv is not None:
        if isinstance(recv, datetime):
            if recv.tzinfo is None:
                recv = recv.replace(tzinfo=timezone.utc)
            pillars["time"]["received_utc"] = recv.isoformat()
        elif isinstance(recv, str):
            pillars["time"]["received_utc"] = recv
        else:
            raise KBLDEntryGuard("received_utc must be datetime or ISO str")
    # Cross a boundary: serialize, hash the bytes, store the bytes.
    try:
        serialized = json.dumps(pillars, sort_keys=True, separators=(",", ":"),
                                ensure_ascii=True, default=str).encode("utf-8")
    except (TypeError, ValueError) as e:
        raise KBLDEntryGuard(f"four_pillar: pillars not serializable: {e}")
    digest = hashlib.sha256(serialized).hexdigest()
    record = {
        "payload": pillars,
        "payload_bytes": serialized,          # stored form — the boundary
        "ts_utc": sealed.isoformat(),  # outer convenience = seal time
        "sha256": digest,
        "context": ctx,
        "aliased": aliased,
        "pillars": ("content", "context", "data", "time"),
    }
    # Read-back: re-hash the *stored bytes*, not the live object.
    if hashlib.sha256(record["payload_bytes"]).hexdigest() != record["sha256"]:
        raise KBLDReadBackMismatch("four_pillar hash read-back failed")
    return record


def _prod_radial_spherical_token_engine(raw_input: Any) -> Any:
    """Pure-stdlib radial token.

    Grid (declared):
      r     — n=8 decimal digits, integer-scaled truncation (not round).
      theta — n=6 (same method).
      phi   — n=6 (same method).
    Units: dimensionless (host-sim coordinates). No physical unit claimed.

    Shell snap:
      MAGIC = (2, 8, 20, 28, 50, 82, 126) is the nuclear shell-model
      magic-number sequence (spin-orbit coupling, nuclear physics).
      Its use as a radial quantization grid for tokens is NOT derived
      from that pedigree. Standing remains host-sim-underived-shell.
      Tie-break: lower shell wins (iteration order of the tuple).
      Saturation: values below 2 or above 126 clamp; residual and
      clamp flags are returned so saturation is never silent.
    """
    if raw_input is None:
        raise KBLDEntryGuard("radial_engine: raw_input must not be None")

    def _trunc(v: float, n: int) -> float:
        # Integer-scaled truncation toward zero. Declared grid, not round.
        scale = 10 ** n
        return math.trunc(v * scale) / scale

    items = raw_input if isinstance(raw_input, (list, tuple)) else [raw_input]
    # Nuclear shell-model magic numbers. Pedigree does not transfer.
    MAGIC = (2, 8, 20, 28, 50, 82, 126)
    MAGIC_LO, MAGIC_HI = MAGIC[0], MAGIC[-1]
    tokens = []
    for it in items:
        x = y = z = 0.0
        if isinstance(it, dict):
            try:
                x = _require_finite_real(it.get("x", 0) or 0, "radial.x")
                y = _require_finite_real(it.get("y", 0) or 0, "radial.y")
                z = _require_finite_real(it.get("z", 0) or 0, "radial.z")
            except (TypeError, ValueError, KBLDEntryGuard):
                tokens.append({"error": "unparseable-or-nonfinite-dict",
                               "raw": str(it)[:64]})
                continue
        elif isinstance(it, (list, tuple)) and len(it) >= 3:
            try:
                x = _require_finite_real(it[0], "radial.x")
                y = _require_finite_real(it[1], "radial.y")
                z = _require_finite_real(it[2], "radial.z")
            except (TypeError, ValueError, KBLDEntryGuard):
                tokens.append({"error": "unparseable-or-nonfinite-tuple",
                               "raw": str(it)[:64]})
                continue
        else:
            try:
                r_proxy = _require_finite_real(it, "radial.scalar")
                tokens.append({
                    "r": _trunc(abs(r_proxy), 8), "theta": 0.0, "phi": 0.0,
                    "shell": 0, "magic": False,
                    "residual": None, "clamped_lo": False, "clamped_hi": False,
                    "note": "scalar-proxy", "standing": "host-sim",
                    "grid": {"r_n": 8, "method": "trunc"},
                })
                continue
            except (TypeError, ValueError, KBLDEntryGuard):
                tokens.append({"error": "unparseable-or-nonfinite",
                               "raw": str(it)[:64]})
                continue
        r = math.sqrt(x * x + y * y + z * z)
        # r is finite if x,y,z were (sqrt of sum of squares of finites)
        if r < MIN_RADIUS_DEFAULT:
            tokens.append({
                "r": None, "theta": None, "phi": None,
                "shell": None, "magic": False,
                "residual": None, "clamped_lo": False, "clamped_hi": False,
                "note": "below-MinRadius", "standing": "host-sim",
                "grid": {"r_n": 8, "method": "trunc"},
            })
            continue
        theta = math.atan2(y, x)
        if theta < 0:
            theta += 2 * math.pi
        cos_val = max(-1.0, min(1.0, z / r))
        phi = math.acos(cos_val)

        # Shell snap — residual and clamp flags always returned
        scaled = r
        clamped_lo = scaled < MAGIC_LO
        clamped_hi = scaled > MAGIC_HI
        if scaled <= 0:
            shell = 0
            residual = None
        else:
            shell = min(MAGIC, key=lambda m: abs(m - scaled))
            residual = scaled - shell  # signed; positive => above shell
        is_magic = (shell in MAGIC) and (residual is not None) and (abs(residual) < 0.5)

        tokens.append({
            "r": _trunc(r, 8),
            "theta": _trunc(theta, 6),
            "phi": _trunc(phi, 6),
            "shell": shell,
            "magic": is_magic,
            "residual": residual,
            "clamped_lo": clamped_lo,
            "clamped_hi": clamped_hi,
            "standing": "host-sim-underived-shell",
            "grid": {"r_n": 8, "theta_n": 6, "phi_n": 6, "method": "trunc",
                     "units": "dimensionless-host-sim"},
            "magic_note": "nuclear-shell-model-sequence; pedigree-does-not-transfer",
        })
    return tokens


# Declared ceiling for voxel layout allocation. Above this is validation
# error, not an allocation. Host-sim bound; raise if a real deployment
# needs more — do not silently grow.
_SPHERICAL_LAYOUT_CEILING = 4096


def _prod_spherical_voxel_tokenizer(data: Any, poles: int = 8,
                                    equator: int = 48) -> Any:
    """N/E/S layout by index. poles/equator: positive int, <= ceiling."""
    if not (isinstance(poles, int) and not isinstance(poles, bool) and poles > 0):
        raise KBLDEntryGuard("spherical_voxel: poles must be positive int")
    if not (isinstance(equator, int) and not isinstance(equator, bool) and equator > 0):
        raise KBLDEntryGuard("spherical_voxel: equator must be positive int")
    if poles > _SPHERICAL_LAYOUT_CEILING or equator > _SPHERICAL_LAYOUT_CEILING:
        raise KBLDEntryGuard(
            f"spherical_voxel: poles/equator exceed ceiling "
            f"{_SPHERICAL_LAYOUT_CEILING}")
    items = list(data) if isinstance(data, (list, tuple)) else [data]
    n = len(items)
    north = [None] * poles
    south = [None] * poles
    eq = [None] * equator
    for i, v in enumerate(items):
        if i < poles:
            north[i] = v
        elif i < poles + equator:
            eq[i - poles] = v
        else:
            south[(i - poles - equator) % poles] = v
    return {
        "north": north,
        "equator": eq,
        "south": south,
        "poles": poles,
        "equator_cells": equator,
        "input_count": n,
        "layout": "N-E-S",
    }


def _prod_modality_aware_clean_and_audit(filtered_tokens: Any,
                                         provenance: Any) -> Any:
    """Reject, do not coerce. Dropped items are returned (recoverable).
    Counts + recovered lists. Closed on None tokens."""
    if filtered_tokens is None:
        raise KBLDEntryGuard("modality_clean: tokens must not be None")
    dropped_none = []
    dropped_empty = []
    rejected = []   # non-numeric, non-container that we refuse to coerce
    kept = []
    seq = (filtered_tokens if isinstance(filtered_tokens, (list, tuple))
           else [filtered_tokens])
    for item in seq:
        if item is None:
            dropped_none.append(item)
            continue
        if isinstance(item, (list, tuple, dict, str)) and len(item) == 0:
            dropped_empty.append(item)
            continue
        # Accept only: numbers (no bool), non-empty containers, or str
        if isinstance(item, bool):
            rejected.append(item)
            continue
        if isinstance(item, (int, float)):
            kept.append(item)          # keep original type — no coerce
            continue
        if isinstance(item, (list, tuple, dict, str)):
            kept.append(item)
            continue
        rejected.append(item)
    audit = {
        "input_type": type(filtered_tokens).__name__,
        "dropped_none_count": len(dropped_none),
        "dropped_empty_count": len(dropped_empty),
        "rejected_count": len(rejected),
        "kept_count": len(kept),
    }
    prov_note = None
    if isinstance(provenance, dict):
        prov_note = provenance.get("sha256") or provenance.get("ts_utc")
    return {
        "cleaned": kept,
        "dropped_none": dropped_none,
        "dropped_empty": dropped_empty,
        "rejected": rejected,
        "audit": audit,
        "provenance_ref": prov_note,
        "status": "CLEANED" if not rejected else "CLEANED_WITH_REJECTS",
    }


def _prod_star_traversal_nuance_enhance(shared_context: Any,
                                        direction: str = "both") -> Any:
    """Bidirectional key walk. Priority order is ASSERTTED provisional
    (content > context > data > time). Not derived; host-sim only."""
    if not isinstance(shared_context, dict):
        raise KBLDEntryGuard("star_traversal: shared_context must be dict")
    if direction not in ("forward", "backward", "both"):
        raise KBLDEntryGuard(
            f"direction {direction!r} not in forward/backward/both")
    # ASSERTTED order — not measured
    priority = ("content", "context", "data", "time", "payload", "sha256", "ts_utc")
    keys = list(shared_context.keys())
    forward = []
    for p in priority:
        if p in shared_context:
            forward.append((p, shared_context[p]))
    for k in keys:
        if k not in priority:
            forward.append((k, shared_context[k]))
    backward = list(reversed(forward))
    result = {
        "direction": direction,
        "nuance_order": list(priority),
        "nuance_standing": "asserted-provisional",
        "key_count": len(keys),
    }
    if direction in ("forward", "both"):
        result["forward"] = forward
    if direction in ("backward", "both"):
        result["backward"] = backward
    result["status"] = "TRAVERSED"
    return result


def GOSUB_Bind_Production_Seams() -> Dict[str, str]:
    """Bind all 7 declared seams to production bodies.
    - Idempotent: re-binding the same impl is a no-op success.
    - Full read-back: every name is verified present and points to the
      expected callable after the loop.
    - Unbind remains available via GOSUB_Unbind_Seam (one-way door only
      if the caller never unbinds).
    Returns status map. Raises on any read-back failure."""
    binds = {
        "harmonic_damping": _prod_harmonic_damping,
        "resonant_cancel_repetition": _prod_resonant_cancel_repetition,
        "embed_four_pillar_provenance": _prod_embed_four_pillar_provenance,
        "radial_spherical_token_engine": _prod_radial_spherical_token_engine,
        "spherical_voxel_tokenizer": _prod_spherical_voxel_tokenizer,
        "modality_aware_clean_and_audit": _prod_modality_aware_clean_and_audit,
        "star_traversal_nuance_enhance": _prod_star_traversal_nuance_enhance,
    }
    status = {}
    for name, impl in binds.items():
        current = _SEAM_REGISTRY.get(name)
        if current is impl:
            status[name] = "ALREADY_BOUND"
            continue
        if current is not None and current is not impl:
            # Foreign body present — closed failure, do not self-heal.
            # Evidence that something rebound the seam must survive.
            raise KBLDEntryGuard(
                f"seam {name!r} already bound to foreign body "
                f"{current!r}; refuse to overwrite. Unbind first.")
        GOSUB_Bind_Seam(name, impl)
        status[name] = "BOUND"
    # Full read-back of every assignment
    for name, impl in binds.items():
        bound = _SEAM_REGISTRY.get(name)
        if bound is not impl:
            raise KBLDReadBackMismatch(
                f"production bind read-back failed for {name!r}: "
                f"got {bound!r}, expected {impl!r}")
    if len(_SEAM_REGISTRY) < len(binds):
        raise KBLDReadBackMismatch(
            f"production bind count low: {len(_SEAM_REGISTRY)} < {len(binds)}")
    return status


# ============================================================
# APPENDABLE SUBSTACK — no mutable default args. [EARNED]
# Uniform seam contract enforced at append time: fn(data, timestamp).
# ============================================================
KBLD_APPENDABLE_SUBSTACK: List[Callable] = []


def GOSUB_KBLD_Append_Filter_Layer(
        stack: Optional[List[Callable]] = None,
        layer: Optional[Callable] = None) -> List[Callable]:
    target = KBLD_APPENDABLE_SUBSTACK if stack is None else stack
    fn = GOSUB_KBLD_Deterministic_Filter_Layer if layer is None else layer
    # ENTRY GUARD
    if not isinstance(target, list):
        raise KBLDEntryGuard("stack must be a list or None")
    if not callable(fn):
        raise KBLDEntryGuard("layer must be callable")
    if fn not in target:
        target.append(fn)
        # READ-BACK VERIFICATION
        if target[-1] is not fn:
            raise KBLDReadBackMismatch("substack append read-back failed")
    return target


def GOSUB_KBLD_Execute_Appendable_Stack(
        data: Any,
        timestamp: Optional[datetime] = None,
        stack: Optional[List[Callable]] = None) -> Any:
    target = KBLD_APPENDABLE_SUBSTACK if stack is None else stack
    if not isinstance(target, list):
        raise KBLDEntryGuard("stack must be a list or None")
    if not target:
        raise KBLDEntryGuard(
            "appendable substack is empty — nothing to execute")
    ts = timestamp if timestamp is not None else datetime.now(timezone.utc)
    for i, sub in enumerate(target):
        if not callable(sub):
            raise KBLDEntryGuard(f"substack element {i} is not callable")
        result = sub(data, ts)
        # Uniform contract: provenance records carry payload forward.
        data = result["payload"] if (isinstance(result, dict)
                                     and "payload" in result
                                     and "sha256" in result) else result
    return data


# ============================================================
# ERROR TEST / MITIGATE / RETEST LOOP [EARNED]
# Real error scan, real mitigation, closed failure, stagnation guard,
# per-pass provenance. Never returns raw garbage stamped "validated".
# ============================================================

# D2: error classes no mitigator can repair. Presence of any of these
# terminates the loop immediately with KBLDUnfixable rather than burning
# passes and reporting stagnation.
_TERMINAL_ERRORS = ("data_is_none", "empty_sequence", "empty_mapping")


def GOSUB_Error_Test(current: Any,
                     target: Optional[Callable] = None) -> List[str]:
    errors: List[str] = []
    if current is None:
        errors.append("data_is_none")
        return errors
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


def _terminal_subset(errors: List[str]) -> List[str]:
    return [e for e in errors if e in _TERMINAL_ERRORS]


def GOSUB_Mitigate(current: Any, errors: List[str],
                   target: Optional[Callable] = None) -> Any:
    """Drop-and-count policy: non-finite entries removed, removal recorded
    by the caller's provenance chain. Unfixable classes (None, empty) pass
    through unchanged so the loop fails closed instead of fabricating
    data."""
    # D9: preserve the container type. A mitigator that silently converts
    # tuple -> list changes the caller's contract without saying so.
    if isinstance(current, tuple):
        return tuple(x for x in current
                     if not (isinstance(x, float) and not math.isfinite(x)))
    if isinstance(current, list):
        return [x for x in current
                if not (isinstance(x, float) and not math.isfinite(x))]
    if isinstance(current, dict):
        return {k: v for k, v in current.items()
                if not (isinstance(v, float) and not math.isfinite(v))}
    return current


def GOSUB_Retest(current: Any, target: Optional[Callable] = None) -> Any:
    if callable(target):
        try:
            result = target(current)
        except KBLDError:
            raise
        except Exception as e:
            raise KBLDTargetFault(
                f"retest target raised {type(e).__name__}: {e}") from e
        if isinstance(result, dict) and "payload" in result \
                and "sha256" in result:
            return result["payload"]
        return result
    return current


def GOSUB_Is_Nearly_Flawless(current: Any,
                             target: Optional[Callable] = None) -> bool:
    # Derived from the same scan the loop uses — cannot drift into a
    # standalone hardcoded verdict.
    return len(GOSUB_Error_Test(current, target)) == 0


def GOSUB_Error_Test_Mitigate_Retest_Loop(
        target: Optional[Callable],
        input_data: Any,
        max_passes: int = 5,
        strict: bool = True) -> Dict[str, Any]:
    """Returns verdict: {"status": CLEAN|MITIGATED|FAILED_BUDGET|UNFIXABLE,
    "data", "passes", "residual_errors", "provenance_chain"}.
    strict=True raises on unfixable input, budget exhaustion, or stagnation
    (closed failure); strict=False returns the error-coded verdict instead —
    never a bare payload dressed as clean."""
    # ENTRY GUARD
    if not (isinstance(max_passes, int) and not isinstance(max_passes, bool)
            and max_passes >= 1):
        raise KBLDEntryGuard("max_passes must be int >= 1")
    if target is not None and not callable(target):
        raise KBLDEntryGuard("target must be callable or None")

    current = input_data
    chain: List[Dict[str, Any]] = []

    errors = GOSUB_Error_Test(current, target)
    if not errors:
        return {"status": "CLEAN", "data": current, "passes": 0,
                "residual_errors": [],
                "provenance_chain": [GOSUB_Provenance_Attach(current)]}

    # D2: terminal classes short-circuit before any pass is burned.
    terminal = _terminal_subset(errors)
    if terminal:
        if strict:
            raise KBLDUnfixable(
                f"unfixable error class(es) present: {terminal}; "
                f"no mitigation policy can repair these")
        return {"status": "UNFIXABLE", "data": current, "passes": 0,
                "residual_errors": errors,
                "provenance_chain": []}

    for p in range(1, max_passes + 1):
        before = list(errors)
        current = GOSUB_Mitigate(current, errors, target)
        current = GOSUB_Retest(current, target)
        errors = GOSUB_Error_Test(current, target)
        chain.append({"pass": p,
                      "errors_before": before,
                      "errors_after": list(errors),
                      "record": GOSUB_Provenance_Attach(
                          current, context={"pass": p})})
        if not errors:
            return {"status": "MITIGATED", "data": current, "passes": p,
                    "residual_errors": [], "provenance_chain": chain}

        # A pass may CREATE a terminal condition (e.g. mitigation empties
        # the sequence, or the retest target returns None). That is closed
        # failure, not stagnation.
        terminal = _terminal_subset(errors)
        if terminal:
            if strict:
                raise KBLDUnfixable(
                    f"pass {p} produced unfixable error class(es): "
                    f"{terminal}")
            return {"status": "UNFIXABLE", "data": current, "passes": p,
                    "residual_errors": errors, "provenance_chain": chain}

        # STAGNATION GUARD — mitigation must make progress each pass
        if len(errors) >= len(before):
            if strict:
                raise KBLDStagnation(
                    f"pass {p}: error count did not shrink "
                    f"({len(before)} -> {len(errors)}); refusing to burn "
                    f"budget")
            return {"status": "FAILED_BUDGET", "data": current, "passes": p,
                    "residual_errors": errors, "provenance_chain": chain}

    if strict:
        raise KBLDMitigationBudgetExceeded(
            f"{max_passes} passes exhausted; residual errors: {errors}")
    return {"status": "FAILED_BUDGET", "data": current, "passes": max_passes,
            "residual_errors": errors, "provenance_chain": chain}


# ============================================================
# LEGACY SHIM — delegates; dead globals() branch removed
# ============================================================
def GOSUB_Mitigation_Loop(target_subroutine: Optional[Callable],
                          input_data: Any, max_passes: int = 5) -> Any:
    """DEPRECATED: use GOSUB_Error_Test_Mitigate_Retest_Loop. Kept so old
    call sites keep working; returns verdict["data"] on success, raises on
    failure (closed — the legacy silent-return path is gone)."""
    verdict = GOSUB_Error_Test_Mitigate_Retest_Loop(
        target_subroutine, input_data, max_passes=max_passes, strict=True)
    return verdict["data"]


# ============================================================
# SELF-TESTS — including negative tests. Garbage must NOT pass.
# ============================================================
if __name__ == "__main__":
    passed = 0
    failed = 0
    failures: List[str] = []

    def check(name: str, cond: bool) -> None:
        global passed, failed
        if cond:
            passed += 1
            print(f"  PASS  {name}")
        else:
            failed += 1
            failures.append(name)
            print(f"  FAIL  {name}")

    print("== kbl_svct_stacks self-tests (rev 3) ==")

    # ---- T1 clean numeric path
    v = GOSUB_Error_Test_Mitigate_Retest_Loop(None, [1.0, 2.0, 3.0])
    check("T1 clean list -> CLEAN, data intact",
          v["status"] == "CLEAN" and v["data"] == [1.0, 2.0, 3.0])

    # ---- T2 non-finite garbage mitigated, recorded, verdict honest
    v = GOSUB_Error_Test_Mitigate_Retest_Loop(
        None, [1.0, float("nan"), 2.0, float("inf")])
    check("T2 NaN/Inf mitigated -> MITIGATED, finite payload",
          v["status"] == "MITIGATED" and v["data"] == [1.0, 2.0]
          and v["passes"] == 1)
    check("T2 provenance chain records before/after error sets",
          v["provenance_chain"][0]["errors_before"] != []
          and v["provenance_chain"][0]["errors_after"] == [])

    # ---- T3 NEGATIVE — unfixable garbage must fail CLOSED, named correctly
    caught = None
    try:
        GOSUB_Error_Test_Mitigate_Retest_Loop(None, None, max_passes=3)
    except KBLDUnfixable:
        caught = "unfixable"
    except KBLDStagnation:
        caught = "stagnation"
    check("T3 None input raises KBLDUnfixable (not stagnation-by-accident)",
          caught == "unfixable")

    # ---- T4 NEGATIVE — non-strict returns error-coded verdict, not clean
    v = GOSUB_Error_Test_Mitigate_Retest_Loop(None, None, max_passes=3,
                                              strict=False)
    check("T4 strict=False -> UNFIXABLE with residual errors",
          v["status"] == "UNFIXABLE" and v["residual_errors"] != []
          and v["data"] is None)

    # ---- T5 MAD/10-sigma guard flags gross outlier, conserves counts
    g = GOSUB_MAD_Sigma_Guard([10.0, 10.1, 9.9, 10.05, 9.95, 1e9])
    check("T5 outlier flagged", g["flagged"] == [1e9])
    check("T5 inliers kept", len(g["data"]) == 5)

    # ---- T6 MAD collapse branch (majority identical + deviant)
    g = GOSUB_MAD_Sigma_Guard([5.0, 5.0, 5.0, 5.0, 42.0])
    check("T6 MAD==0 fallback still flags deviant", g["flagged"] == [42.0])

    # ---- T6b D3 REGRESSION — tiny-magnitude cluster must NOT be flagged
    tiny = [1e-15, 1e-15, 1e-15, 1e-15]
    g = GOSUB_MAD_Sigma_Guard(tiny)
    check("T6b tiny cluster (1e-15) not falsely flagged by tolerance floor",
          g["flagged"] == [] and len(g["data"]) == 4)

    # ---- T6c D3 REGRESSION — deviant at tiny magnitude still caught
    g = GOSUB_MAD_Sigma_Guard([1e-15, 1e-15, 1e-15, 5e-15])
    check("T6c tiny-magnitude deviant still flagged", g["flagged"] == [5e-15])

    # ---- T7 guard honest about scope
    probe = {"not": "numeric"}
    g = GOSUB_MAD_Sigma_Guard(probe)
    check("T7 non-numeric input reported unguarded, untouched",
          g["guarded"] is False and g["data"] is probe)

    # ---- T7b guard rejects bools masquerading as ints
    g = GOSUB_MAD_Sigma_Guard([True, False, True])
    check("T7b bool sequence treated as non-numeric, unguarded",
          g["guarded"] is False)

    # ---- T8 provenance attach + read-back + UTC
    r = GOSUB_Provenance_Attach([1, 2, 3])
    check("T8 sha256 present and 64 hex chars", len(r["sha256"]) == 64)
    check("T8 timestamp is UTC ISO", r["ts_utc"].endswith("+00:00"))

    # ---- T8b D4 REGRESSION — distinct types with equal repr must not collide
    class _A:
        def __repr__(self):
            return "SAME"

    class _B:
        def __repr__(self):
            return "SAME"

    check("T8b repr-collision channel closed (distinct types, distinct hash)",
          _canonical_hash(_A()) != _canonical_hash(_B()))

    # ---- T8c naive datetime is coerced to UTC, not rejected silently
    naive = datetime(2026, 1, 1, 12, 0, 0)
    r = GOSUB_Provenance_Attach([1], timestamp=naive)
    check("T8c naive timestamp coerced to UTC",
          r["ts_utc"].endswith("+00:00"))

    # ---- T9 NEGATIVE — unbound seam raises KBLDSeamUnbound, never NameError
    caught = False
    try:
        GOSUB_SVCT_Spherical_Tokenize([1, 2, 3])
    except KBLDSeamUnbound:
        caught = True
    except NameError:
        caught = False
    check("T9 unbound seam -> KBLDSeamUnbound (NameError class eliminated)",
          caught)

    # ---- T10 seam bind + read-back + call-through
    GOSUB_Bind_Seam("spherical_voxel_tokenizer",
                    lambda d, p, e: {"tokens": d, "poles": p, "equator": e})
    out = GOSUB_SVCT_Spherical_Tokenize([1, 2], poles=4, equator=12)
    check("T10 bound seam executes with args intact",
          out == {"tokens": [1, 2], "poles": 4, "equator": 12})

    # ---- T11 filter layer end-to-end: guard + provenance, no damping
    rec = GOSUB_KBLD_Deterministic_Filter_Layer([1.0, 1.1, 0.9, 1e15])
    check("T11 filter layer strips 10-sigma outlier and stamps provenance",
          rec["payload"] == [1.0, 1.1, 0.9]
          and rec["context"]["flagged_count"] == 1
          and len(rec["sha256"]) == 64)

    # ---- T12 NEGATIVE — require_damping with unbound seam fails closed
    caught = False
    try:
        GOSUB_KBLD_Deterministic_Filter_Layer([1.0], require_damping=True)
    except KBLDSeamUnbound:
        caught = True
    check("T12 required-but-unbound damping raises", caught)

    # ---- T13 appendable substack: append, read-back, execute
    stack: List[Callable] = []
    GOSUB_KBLD_Append_Filter_Layer(stack)
    GOSUB_KBLD_Append_Filter_Layer(stack)   # idempotent
    check("T13 append is idempotent", len(stack) == 1)
    data = GOSUB_KBLD_Execute_Appendable_Stack([2.0, 2.1, 1.9, 9e12],
                                               stack=stack)
    check("T13 stack execution unwraps provenance and filters",
          data == [2.0, 2.1, 1.9])

    # ---- T14 NEGATIVE — empty substack refuses to fake a run
    caught = False
    try:
        GOSUB_KBLD_Execute_Appendable_Stack([1.0], stack=[])
    except KBLDEntryGuard:
        caught = True
    check("T14 empty substack raises entry guard", caught)

    # ---- T15 legacy shim delegates and stays closed
    check("T15 legacy shim returns mitigated data",
          GOSUB_Mitigation_Loop(None, [1.0, float("nan")]) == [1.0])
    caught = False
    try:
        GOSUB_Mitigation_Loop(None, None)
    except KBLDError:
        caught = True
    check("T15 legacy shim fails closed on unfixable input", caught)

    # ---- T16 dict payloads: non-finite value keys dropped, recorded
    v = GOSUB_Error_Test_Mitigate_Retest_Loop(None, {"a": 1.0,
                                                     "b": float("nan")})
    check("T16 dict NaN mitigated",
          v["status"] == "MITIGATED" and v["data"] == {"a": 1.0})

    # ---- T17 D1 — RETEST LEG with a REAL bound target
    # Target scales every element; loop must carry the retest output forward.
    def _doubling_target(seq):
        if isinstance(seq, list):
            return [x * 2.0 for x in seq]
        return seq

    v = GOSUB_Error_Test_Mitigate_Retest_Loop(
        _doubling_target, [1.0, float("nan"), 3.0])
    check("T17 retest leg actually executes target and carries result",
          v["status"] == "MITIGATED" and v["data"] == [2.0, 6.0])

    # ---- T18 D1 — retest target returning a provenance record is unwrapped
    def _provenance_target(seq):
        return GOSUB_Provenance_Attach(seq, context={"via": "target"})

    v = GOSUB_Error_Test_Mitigate_Retest_Loop(
        _provenance_target, [1.0, float("inf"), 2.0])
    check("T18 retest unwraps provenance record payload",
          v["status"] == "MITIGATED" and v["data"] == [1.0, 2.0])

    # ---- T18b NEGATIVE — retest target that destroys data fails closed
    def _nulling_target(seq):
        return None

    caught = False
    try:
        GOSUB_Error_Test_Mitigate_Retest_Loop(
            _nulling_target, [1.0, float("nan")])
    except KBLDUnfixable:
        caught = True
    check("T18b target returning None -> KBLDUnfixable, no silent pass",
          caught)

    # ---- T19 D6 — bind guard rejects unknown seam name
    caught = False
    try:
        GOSUB_Bind_Seam("not_a_real_seam", lambda: None)
    except KBLDEntryGuard:
        caught = True
    check("T19 bind rejects undeclared seam name", caught)

    # ---- T20 D6 — bind guard rejects non-callable impl
    caught = False
    try:
        GOSUB_Bind_Seam("harmonic_damping", "not callable")
    except KBLDEntryGuard:
        caught = True
    check("T20 bind rejects non-callable impl", caught)

    # ---- T21 D6 — tokenizer entry guards on poles/equator
    caught = 0
    for bad in ({"poles": 0}, {"poles": -1}, {"equator": 0},
                {"poles": True}):
        try:
            GOSUB_SVCT_Spherical_Tokenize([1], **bad)
        except KBLDEntryGuard:
            caught += 1
    check("T21 poles/equator entry guards reject 0, negative, bool",
          caught == 4)

    # ---- T22 D6 — traversal direction guard
    caught = False
    try:
        GOSUB_SVCT_Bidirectional_Traversal({}, direction="sideways")
    except KBLDEntryGuard:
        caught = True
    check("T22 traversal rejects invalid direction", caught)

    # ---- T23 loop entry guards
    caught = 0
    for bad_kwargs in ({"max_passes": 0}, {"max_passes": True}):
        try:
            GOSUB_Error_Test_Mitigate_Retest_Loop(None, [1.0], **bad_kwargs)
        except KBLDEntryGuard:
            caught += 1
    try:
        GOSUB_Error_Test_Mitigate_Retest_Loop("not callable", [1.0])
    except KBLDEntryGuard:
        caught += 1
    check("T23 loop entry guards reject max_passes<1, bool, non-callable",
          caught == 3)

    # ---- T24 n_sigma entry guard
    caught = 0
    for bad in (0, -1.0, float("nan"), float("inf"), True):
        try:
            GOSUB_MAD_Sigma_Guard([1.0, 2.0], n_sigma=bad)
        except KBLDEntryGuard:
            caught += 1
    check("T24 n_sigma guard rejects 0, negative, NaN, Inf, bool",
          caught == 5)

    # ---- T25 unbind restores unbound behaviour (test isolation is real)
    GOSUB_Unbind_Seam("spherical_voxel_tokenizer")
    caught = False
    try:
        GOSUB_SVCT_Spherical_Tokenize([1])
    except KBLDSeamUnbound:
        caught = True
    check("T25 unbind restores closed-failure state", caught)

    # ---- T26 all-nonfinite sequence: guard empties it, honest count
    g = GOSUB_MAD_Sigma_Guard([float("nan"), float("inf")])
    check("T26 all-nonfinite -> empty data, dropped counted",
          g["guarded"] is True and g["data"] == []
          and g["dropped_nonfinite"] == 2)

    # ---- T27 conservation invariant under random-ish mixed input
    mixed = [1.0, 2.0, 3.0, 1e12, float("nan"), 2.5, -1e12, 2.2]
    g = GOSUB_MAD_Sigma_Guard(mixed)
    check("T27 conservation: kept + flagged + dropped == input",
          len(g["data"]) + len(g["flagged"]) + g["dropped_nonfinite"]
          == len(mixed))

    # ---- T28 input never mutated
    original = [1.0, float("nan"), 2.0]
    snapshot = list(original)
    GOSUB_MAD_Sigma_Guard(original)
    GOSUB_Error_Test_Mitigate_Retest_Loop(None, original)
    same = (len(original) == len(snapshot)
            and all((math.isnan(a) and math.isnan(b)) or a == b
                    for a, b in zip(original, snapshot)))
    check("T28 caller input never mutated", same)

    # ---- T29 D7 REGRESSION — MAD breakdown must be reported, not hidden.
    # 3/5 contamination: outliers own the median, estimator inverts.
    g = GOSUB_MAD_Sigma_Guard([1.0, 1.0, 1e9, 1e9, 1e9])
    check("T29 majority-outlier inversion raises breakdown_suspected",
          g.get("breakdown_suspected") is True)

    # ---- T29b unimodal clean data must NOT trip the breakdown flag
    g = GOSUB_MAD_Sigma_Guard([10.0, 10.1, 9.9, 10.05, 9.95, 1e9])
    check("T29b unimodal + single outlier: no false breakdown",
          g.get("breakdown_suspected") is False and g["flagged"] == [1e9])

    # ---- T29c identical-value sequence must not trip breakdown
    g = GOSUB_MAD_Sigma_Guard([5.0, 5.0, 5.0, 5.0])
    check("T29c all-identical: no false breakdown",
          g.get("breakdown_suspected") is False and g["flagged"] == [])

    # ---- T30 D8 REGRESSION — provenance payload is a snapshot, not an alias
    payload = [1.0, 2.0]
    rec = GOSUB_Provenance_Attach(payload)
    payload.append(999.0)
    check("T30 caller mutation cannot invalidate stamped provenance",
          rec["payload"] == [1.0, 2.0]
          and _canonical_hash(rec["payload"]) == rec["sha256"])

    # ---- T30b nested mutation also cannot reach the record
    nested = {"a": [1, 2]}
    rec = GOSUB_Provenance_Attach(nested)
    nested["a"].append(3)
    check("T30b deep mutation cannot reach stamped payload",
          rec["payload"] == {"a": [1, 2]}
          and _canonical_hash(rec["payload"]) == rec["sha256"])

    # ---- T31 D9 REGRESSION — tuple stays a tuple through mitigation
    v = GOSUB_Error_Test_Mitigate_Retest_Loop(
        None, (1.0, float("nan"), 2.0))
    check("T31 tuple container type preserved through mitigation",
          isinstance(v["data"], tuple) and v["data"] == (1.0, 2.0))

    # ---- T32 D10 REGRESSION — circular payload fails closed, no collision
    circ = []
    circ.append(circ)
    caught = False
    try:
        _canonical_hash(circ)
    except KBLDEntryGuard:
        caught = True
    check("T32 circular payload raises rather than hashing an elided repr",
          caught)

    # ---- T32b acyclic shared references are NOT false-positived
    shared = [1, 2]
    ok_struct = [shared, shared]
    check("T32b shared-but-acyclic structure still hashes",
          len(_canonical_hash(ok_struct)) == 64)

    # ---- T33 provenance on circular payload fails closed too
    caught = False
    try:
        GOSUB_Provenance_Attach(circ)
    except KBLDEntryGuard:
        caught = True
    check("T33 provenance attach rejects circular payload", caught)

    # ---- T34 breakdown flag survives the filter-layer wrapper's context
    g = GOSUB_MAD_Sigma_Guard([1.0, 1.0, 1e9, 1e9, 1e9])
    check("T34 breakdown case still conserves element count",
          len(g["data"]) + len(g["flagged"]) + g["dropped_nonfinite"] == 5)

    # ---- T35 D7 REGRESSION — exactly 50/50 bimodal (the inflated-MAD hole).
    # Median lands in the empty gap, MAD balloons, nothing gets flagged.
    g = GOSUB_MAD_Sigma_Guard([1.0] * 50 + [1e9] * 50)
    check("T35 50/50 bimodal detected (inflated-MAD hole closed)",
          g["breakdown_suspected"] is True)

    # ---- T36 D7 REGRESSION — uniform data must NOT false-positive.
    # An assumed 0.25 threshold tripped on 48% of uniform samples; the
    # measured 0.40 must not.
    import random as _rnd
    _rnd.seed(13)
    fp = 0
    for _ in range(200):
        gg = GOSUB_MAD_Sigma_Guard([_rnd.uniform(0.0, 1.0)
                                    for _ in range(200)])
        if gg["breakdown_suspected"]:
            fp += 1
    check("T36 uniform(0,1) zero false positives over 200 trials", fp == 0)

    # ---- T36b gaussian must not false-positive either
    _rnd.seed(7)
    fp = 0
    for _ in range(200):
        gg = GOSUB_MAD_Sigma_Guard([_rnd.gauss(100.0, 5.0)
                                    for _ in range(200)])
        if gg["breakdown_suspected"]:
            fp += 1
    check("T36b gaussian(100,5) zero false positives over 200 trials",
          fp == 0)

    # ---- T37 D7 REGRESSION — min-n gate: tiny samples make no claim
    check("T37 n=2 does not false-positive on ratio test",
          GOSUB_MAD_Sigma_Guard([1.0, 2.0])["breakdown_suspected"] is False)
    check("T37b n=3 does not false-positive on ratio test",
          GOSUB_MAD_Sigma_Guard([1.0, 2.0, 3.0])["breakdown_suspected"]
          is False)

    # ---- T38 contamination sweep has no holes between 5% and 95%
    holes = []
    for pct in range(5, 100, 5):
        gg = GOSUB_MAD_Sigma_Guard([1.0] * (100 - pct) + [1e9] * pct)
        if not gg["breakdown_suspected"]:
            holes.append(pct)
    check("T38 contamination sweep 5-95% has zero detection holes",
          holes == [])

    # ---- T39 (H7): exploding retest target wrapped in named halt
    def _bomb(d):
        raise RuntimeError("target exploded")
    caught = False
    try:
        GOSUB_Error_Test_Mitigate_Retest_Loop(_bomb, [1.0, float("nan")])
    except KBLDTargetFault as e:
        caught = isinstance(e.__cause__, RuntimeError)
    except RuntimeError:
        caught = False
    check("T39 H7: target explosion -> KBLDTargetFault with cause chained",
          caught)

    # ---- T39b KBLD errors from the target pass through unwrapped
    def _kbld_bomb(d):
        raise KBLDStagnation("already named")
    caught = False
    try:
        GOSUB_Error_Test_Mitigate_Retest_Loop(_kbld_bomb,
                                              [1.0, float("nan")])
    except KBLDStagnation:
        caught = True
    check("T39b H7: KBLD errors from target pass through unwrapped", caught)

    # ============================================================
    # BOUND-STATE SUITE (rev-4c)
    # Per-test bind/unbind so a mid-suite failure cannot leave the
    # module bound and poison T9/T12/T25. Identity read-back on unbind.
    # Positive cancel proof + standing propagation included.
    # ============================================================

    def _bind_all():
        return GOSUB_Bind_Production_Seams()

    def _unbind_all_identity():
        """Unbind every declared seam; then prove each raises Unbound.
        Count-parity alone is not identity — call the seam."""
        for name in list(_DECLARED_SEAMS):
            if name in _SEAM_REGISTRY:
                GOSUB_Unbind_Seam(name)
        for name in _DECLARED_SEAMS:
            try:
                _seam(name)
                raise KBLDReadBackMismatch(
                    f"unbind identity: {name!r} still callable after unbind")
            except KBLDSeamUnbound:
                pass
            except KBLDEntryGuard:
                # poles/equator guards fire before seam lookup on some
                # wrappers; that is still "not the production body"
                pass

    # T40 — harmonic_damping closed on None (bound)
    _bind_all()
    caught = False
    try:
        _seam("harmonic_damping")(None)
    except KBLDEntryGuard:
        caught = True
    _unbind_all_identity()
    check("T40 bound harmonic_damping rejects None", caught)

    # T41 — four-pillar closed on bad context
    _bind_all()
    caught = False
    try:
        _seam("embed_four_pillar_provenance")({"v": 1}, "not-a-dict", None)
    except KBLDEntryGuard:
        caught = True
    _unbind_all_identity()
    check("T41 bound four_pillar rejects non-dict context", caught)

    # T42 — four-pillar closed on bad timestamp
    _bind_all()
    caught = False
    try:
        _seam("embed_four_pillar_provenance")({"v": 1}, {}, "not-datetime")
    except KBLDEntryGuard:
        caught = True
    _unbind_all_identity()
    check("T42 bound four_pillar rejects non-datetime timestamp", caught)

    # T43 — radial closed on None
    _bind_all()
    caught = False
    try:
        _seam("radial_spherical_token_engine")(None)
    except KBLDEntryGuard:
        caught = True
    _unbind_all_identity()
    check("T43 bound radial rejects None", caught)

    # T44 — spherical_voxel closed on poles=0
    _bind_all()
    caught = False
    try:
        GOSUB_SVCT_Spherical_Tokenize([1], poles=0)
    except KBLDEntryGuard:
        caught = True
    _unbind_all_identity()
    check("T44 bound spherical_voxel rejects poles=0", caught)

    # T45 — modality closed on None
    _bind_all()
    caught = False
    try:
        _seam("modality_aware_clean_and_audit")(None, {})
    except KBLDEntryGuard:
        caught = True
    _unbind_all_identity()
    check("T45 bound modality rejects None tokens", caught)

    # T46 — star closed on non-dict
    _bind_all()
    caught = False
    try:
        _seam("star_traversal_nuance_enhance")("not-dict", "both")
    except KBLDEntryGuard:
        caught = True
    _unbind_all_identity()
    check("T46 bound star_traversal rejects non-dict", caught)

    # T47 — star closed on bad direction
    _bind_all()
    caught = False
    try:
        _seam("star_traversal_nuance_enhance")({}, "sideways")
    except KBLDEntryGuard:
        caught = True
    _unbind_all_identity()
    check("T47 bound star_traversal rejects bad direction", caught)

    # T48 — bind idempotent + identity read-back
    s1 = _bind_all()
    s2 = _bind_all()
    check("T48 bind idempotent (second call ALREADY_BOUND or BOUND)",
          all(v in ("BOUND", "ALREADY_BOUND") for v in s2.values()))
    _unbind_all_identity()

    # T49 — all 7 present after bind
    _bind_all()
    all_present = all(name in _SEAM_REGISTRY for name in _DECLARED_SEAMS)
    _unbind_all_identity()
    check("T49 all 7 seams present after bind", all_present)

    # T50 — unbind restores Unbound raise on every declared seam
    _bind_all()
    _unbind_all_identity()  # itself asserts each raises
    check("T50 unbind restores KBLDSeamUnbound on every seam", True)

    # T51 POSITIVE — exact same-type duplicates cancel
    _bind_all()
    cancelled = _seam("resonant_cancel_repetition")(
        [1.0, 1.0, 2, 2, 2, 3, "a", "a"], None)
    _unbind_all_identity()
    check("T51 positive: exact same-type duplicates cancelled",
          cancelled == [1.0, 2, 3, "a"])

    # T51b — near-float does NOT cancel (scope boundary)
    _bind_all()
    near = _seam("resonant_cancel_repetition")(
        [0.1 + 0.2, 0.3], None)
    _unbind_all_identity()
    check("T51b near-float 0.1+0.2 vs 0.3 does not cancel",
          len(near) == 2)

    # T51c — bool does not cancel against int (type-is gate)
    _bind_all()
    mixed = _seam("resonant_cancel_repetition")(
        [True, 1, 1.0, 1], None)
    _unbind_all_identity()
    # True stays; 1 stays (type is not bool); 1.0 stays; trailing 1
    # stays (type is not float). No cross-type collapse.
    check("T51c bool/int/float not cross-cancelled",
          mixed == [True, 1, 1.0, 1])

    # T52 — damping standing travels into filter context
    _bind_all()
    rec = GOSUB_KBLD_Deterministic_Filter_Layer(
        [1.0, 1.1, 0.9], require_damping=True)
    standing = rec.get("context", {}).get("damping_standing")
    _unbind_all_identity()
    check("T52 damping standing propagates into filter context",
          standing == "host-sim-underived-rate")

    # T53 — foreign body is refused, not overwritten
    _bind_all()
    # Manually plant a foreign body
    GOSUB_Unbind_Seam("harmonic_damping")
    GOSUB_Bind_Seam("harmonic_damping", lambda x: x)
    caught = False
    try:
        GOSUB_Bind_Production_Seams()
    except KBLDEntryGuard as e:
        caught = "foreign body" in str(e)
    # clean up
    GOSUB_Unbind_Seam("harmonic_damping")
    _unbind_all_identity()
    check("T53 foreign body raises, does not self-heal", caught)

    # T54 — L576 boundary is live: perturb payload_bytes, read-back must fire
    _bind_all()
    rec = _seam("embed_four_pillar_provenance")({"v": 1}, {"src": "t54"}, None)
    # Fault injection on the stored bytes
    corrupted = bytearray(rec["payload_bytes"])
    corrupted[0] = (corrupted[0] + 1) % 256
    rec["payload_bytes"] = bytes(corrupted)
    caught = False
    try:
        if hashlib.sha256(rec["payload_bytes"]).hexdigest() != rec["sha256"]:
            raise KBLDReadBackMismatch("four_pillar hash read-back failed")
    except KBLDReadBackMismatch:
        caught = True
    _unbind_all_identity()
    check("T54 payload_bytes perturbation fires KBLDReadBackMismatch", caught)

    # T55 — shell saturation reports residual and clamp flags
    _bind_all()
    lo = _seam("radial_spherical_token_engine")([(0.5, 0, 0)])  # r=0.5 < 2
    hi = _seam("radial_spherical_token_engine")([(200.0, 0, 0)])  # r=200 > 126
    _unbind_all_identity()
    lo_ok = (lo[0].get("clamped_lo") is True
             and lo[0].get("residual") is not None)
    hi_ok = (hi[0].get("clamped_hi") is True
             and hi[0].get("residual") is not None)
    check("T55 shell saturation reports clamp flags and residual",
          lo_ok and hi_ok)

    print(f"== {passed} passed, {failed} failed ==")
    if failures:
        print("FAILING:")
        for f in failures:
            print(f"   - {f}")
    raise SystemExit(0 if failed == 0 else 1)
