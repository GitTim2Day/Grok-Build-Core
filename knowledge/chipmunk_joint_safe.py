#!/usr/bin/env python3
"""CHIPMUNK_GATE + GOSUB_JOINT_COMMAND_OK
Adjuvant workbench only. Does not replace Tesla FSD or Optimus firmware.
Stdlib only. Truncate toward zero. Fail closed.
Rev 2 — 2026-09-14 error-test / mitigate / retest.
"""
from __future__ import annotations

import math
from typing import Any, Dict, Optional, Tuple

LIFE_CLASSES = {
    "chipmunk",
    "squirrel",
    "bird",
    "cat",
    "dog",
    "deer",
    "person",
    "child",
    "animal",
}

SMALL_W = (0.04, 0.35)
SMALL_H = (0.04, 0.30)
A_BRAKE = 4.0
REACTION_S = 0.8
LEVER_M = 0.050
T_PEAK_LO = 180.0
T_PEAK_HI = 250.0
F_REF_6BW = 4120.0
F_DESIGN = 8000.0
F_CA = 45000.0


def _finite(x: Any) -> bool:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return False
    return math.isfinite(v)


def gosub_truncate_toward_zero(value: float, places: int = 6) -> float:
    factor = 10 ** places
    if value >= 0:
        return math.trunc(value * factor) / factor
    return -math.trunc((-value) * factor) / factor


def classify_object(
    cls: str,
    width_m: float,
    height_m: float,
    moving: bool,
) -> Tuple[Optional[str], Optional[str]]:
    if not _finite(width_m) or not _finite(height_m):
        return None, "reject:size-not-finite"
    if width_m < 0 or height_m < 0:
        return None, "reject:size-negative"
    name = (cls or "unknown").strip().lower()
    small = SMALL_W[0] <= width_m <= SMALL_W[1] and SMALL_H[0] <= height_m <= SMALL_H[1]
    if name in LIFE_CLASSES:
        return "LIFE", None
    if name == "debris" and (not moving) and (not small):
        return "DEBRIS", None
    if name == "debris" and moving:
        return "LIFE_ASSUMED", "moving-labeled-debris"
    if small or moving:
        return "LIFE_ASSUMED", "unknown-small-or-moving"
    if name == "debris":
        return "DEBRIS", None
    return "UNKNOWN", "unknown-still-large"


def stop_distance_m(speed_mps: float) -> float:
    v = max(0.0, float(speed_mps))
    return (v * v) / (2.0 * A_BRAKE) + v * REACTION_S


def chipmunk_gate(sample: Dict[str, Any]) -> Dict[str, Any]:
    """Least-harm action. Supervised L2 adjuvant. supervisor_ready defaults False."""
    out: Dict[str, Any] = {
        "action": "REJECT_INPUT",
        "label": None,
        "ttc_s": None,
        "stop_m": None,
        "note": None,
        "closed": False,
    }
    need = ("range_m", "host_speed_mps", "width_m", "height_m")
    for k in need:
        if not _finite(sample.get(k)):
            out["note"] = "reject:%s" % k
            out["closed"] = True
            return out
    range_m = float(sample["range_m"])
    host = float(sample["host_speed_mps"])
    if range_m < 0 or host < 0:
        out["note"] = "reject:negative-kinematics"
        out["closed"] = True
        return out

    label, note = classify_object(
        str(sample.get("class", "unknown")),
        float(sample["width_m"]),
        float(sample["height_m"]),
        bool(sample.get("moving", False)),
    )
    if label is None:
        out["note"] = note
        out["closed"] = True
        return out

    along = sample.get("object_along_mps")
    if _finite(along):
        closing = max(0.0, host - float(along))
    else:
        closing = host
    stop_m = stop_distance_m(host)
    ttc = None if closing <= 0.0 else range_m / closing
    out["label"] = label
    out["stop_m"] = gosub_truncate_toward_zero(stop_m, 4)
    if ttc is not None:
        out["ttc_s"] = gosub_truncate_toward_zero(ttc, 4)

    life = label in ("LIFE", "LIFE_ASSUMED")
    left = bool(sample.get("lane_clear_left", False))
    right = bool(sample.get("lane_clear_right", False))
    supervisor = bool(sample.get("supervisor_ready", False))

    if life and stop_m >= range_m:
        out["action"] = "STOP"
        out["note"] = note or "cannot-stop-short"
        out["closed"] = True
        return out
    if life and (not supervisor) and ttc is not None and ttc < 2.0:
        out["action"] = "STOP"
        out["note"] = note or "unsupervised-ttc-under-2s"
        out["closed"] = True
        return out
    if life and supervisor and ttc is not None and ttc < 2.0:
        out["action"] = "HANDOFF"
        out["note"] = note or "ttc-under-2s"
        return out
    if life and supervisor and ttc is not None and ttc >= 1.2 and (left or right):
        out["action"] = "YIELD"
        out["note"] = note or ("yield-left" if left else "yield-right")
        return out
    if life:
        out["action"] = "SLOW"
        out["note"] = note or "life-in-path-can-stop"
        return out
    if label == "DEBRIS":
        out["action"] = "HOLD"
        out["note"] = note or "debris"
        return out
    out["action"] = "STOP"
    out["note"] = note or "unknown-fail-closed"
    out["closed"] = True
    return out


def joint_force_n(torque_nm: float, lever_m: float = LEVER_M) -> Optional[float]:
    if not _finite(torque_nm) or not _finite(lever_m) or lever_m <= 0:
        return None
    return abs(float(torque_nm)) / float(lever_m)


def gosub_joint_command_ok(cmd: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "ok": False,
        "severity": "REFUSE",
        "force_n": None,
        "note": None,
    }
    if not _finite(cmd.get("torque_nm")) or not _finite(cmd.get("lever_m", LEVER_M)):
        out["note"] = "reject:torque-or-lever"
        return out
    torque = float(cmd["torque_nm"])
    lever = float(cmd.get("lever_m", LEVER_M))
    if lever <= 0:
        out["note"] = "reject:force"
        return out
    force = joint_force_n(torque, lever)
    if force is None:
        out["note"] = "reject:force"
        return out
    out["force_n"] = gosub_truncate_toward_zero(force, 3)
    if force >= F_CA:
        out["severity"] = "ESTOP"
        out["note"] = "above-expected-Ca"
        return out
    if force >= F_DESIGN:
        out["note"] = "above-design-static-8kN"
        return out
    station = str(cmd.get("station", "PROXIMAL")).upper()
    slack = bool(cmd.get("antagonist_slack", False))
    locked = bool(cmd.get("lock", False))
    wraps = bool(cmd.get("wraps_preload", False))
    workspace_life = bool(cmd.get("workspace_life", False))
    grip_n = cmd.get("grip_n")
    human_confirm = bool(cmd.get("human_confirm", False))
    if station == "DISTAL" and slack and not locked:
        out["note"] = "distal-slack-unlocked"
        return out
    if station == "PROXIMAL" and (not wraps) and abs(torque) >= T_PEAK_LO:
        out["note"] = "proximal-peak-without-preload-wraps"
        return out
    if workspace_life and _finite(grip_n) and float(grip_n) > 50.0 and not human_confirm:
        out["note"] = "workspace-life-high-grip-no-confirm"
        return out
    flag = None
    if abs(torque) > T_PEAK_HI:
        flag = "torque-above-250Nm-peak-band"
    elif force > F_REF_6BW:
        flag = "above-6xBW-reference"
    paired = bool(cmd.get("antagonist_paired", True))
    if str(cmd.get("mode", "position")) == "stiffness" and not paired:
        flag = (flag + ";stiffness-unpaired") if flag else "stiffness-unpaired"
    out["ok"] = True
    out["severity"] = "FLAG" if flag else "OK"
    out["note"] = flag or "inside-envelope"
    return out
