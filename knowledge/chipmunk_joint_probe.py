#!/usr/bin/env python3
"""Adversarial probe against chipmunk_joint_safe.py CONTRACT, not the suite.
Adjuvant only. Exit 0 only if every probe matches the contract.
"""
import importlib.util
import math
import sys

spec = importlib.util.spec_from_file_location(
    "cjs", "chipmunk_joint_safe.py"
)
cjs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cjs)

FAILS = []


def probe(name, cond, detail=""):
    if not cond:
        FAILS.append("%s :: %s" % (name, detail))
        print("PROBE_FAIL", name, detail)
    else:
        print("PROBE_PASS", name)


def gate(**kw):
    base = {
        "range_m": 25.0,
        "host_speed_mps": 10.0,
        "class": "chipmunk",
        "width_m": 0.12,
        "height_m": 0.10,
        "moving": True,
        "crossing": True,
        "lane_clear_left": True,
        "lane_clear_right": False,
        "supervisor_ready": True,
    }
    base.update(kw)
    return cjs.chipmunk_gate(base)


def joint(**kw):
    base = {
        "torque_nm": 200.0,
        "lever_m": 0.05,
        "station": "PROXIMAL",
        "wraps_preload": True,
        "antagonist_paired": True,
        "lock": False,
        "antagonist_slack": False,
        "workspace_life": False,
        "human_confirm": False,
        "mode": "position",
    }
    base.update(kw)
    return cjs.gosub_joint_command_ok(base)

r = gate()
probe("C1_life_not_hold", r["action"] != "HOLD", r)
probe("C1_label_life", r["label"] == "LIFE", r)
r = gate(**{"class": "unknown"})
probe("C2_unknown_small_moving", r["label"] == "LIFE_ASSUMED" and r["action"] != "HOLD", r)
r = gate(range_m=float("nan"))
probe("C3_nan", r["action"] == "REJECT_INPUT", r)
r = gate(host_speed_mps=float("inf"))
probe("C3_inf", r["action"] == "REJECT_INPUT", r)
r = gate(range_m=-1.0)
probe("C3_neg", r["action"] == "REJECT_INPUT", r)
r = gate(range_m=12.0, host_speed_mps=8.0)
probe("C4_cannot_stop", r["action"] == "STOP", r)
r = gate(range_m=40.0, host_speed_mps=10.0, supervisor_ready=False, lane_clear_left=True)
probe("C5_no_supervisor_no_yield", r["action"] not in ("YIELD", "HANDOFF"), r)
r = joint(station="DISTAL", antagonist_slack=True, lock=False, torque_nm=40.0)
probe("C6_distal_slack", r["ok"] is False and r["severity"] == "REFUSE", r)
r = joint(torque_nm=400.0, wraps_preload=True)
probe("C7_design_eq", r["ok"] is False or r["severity"] in ("REFUSE", "ESTOP"), r)
r = joint(torque_nm=2250.0)
probe("C7_ca_eq", r["severity"] == "ESTOP", r)
r = joint(station="DISTAL", lock=True, torque_nm=20.0, workspace_life=True, grip_n=50.01, human_confirm=False)
probe("C8_life_grip", r["ok"] is False, r)
r = joint(lever_m=0.0)
probe("C9_zero_lever", r["ok"] is False, r)
r = joint(torque_nm=float("nan"))
probe("C9_nan_torque", r["ok"] is False, r)
r = cjs.chipmunk_gate({"range_m": 40.0, "host_speed_mps": 10.0, "class": "chipmunk", "width_m": 0.12, "height_m": 0.10, "moving": True, "lane_clear_left": True})
probe("C5b_default_supervisor", r["action"] not in ("YIELD", "HANDOFF"), r)
r = gate(**{"class": "  CHIPMUNK  "})
probe("C11_strip_case", r["label"] == "LIFE", r)
r = gate(**{"class": "debris", "width_m": 0.10, "height_m": 0.08, "moving": False})
probe("C12_small_still_debris", r["label"] == "LIFE_ASSUMED" and r["action"] != "HOLD", r)
print("PROBE_FAIL_COUNT", len(FAILS))
for f in FAILS:
    print(" ", f)
sys.exit(0 if not FAILS else 1)
