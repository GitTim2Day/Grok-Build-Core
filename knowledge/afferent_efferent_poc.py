"""Afferent/efferent IMU POC path — logical bind ticket.

No I2C. No Pi flash. No HMC driver on QMC. ADXL355 is upgrade-only
after a ticket exists and VAL's.

Input: GY-521 + QMC5883P samples (asserted, not bus-earned).
Glomerulus: shepherd_clean.
Collecting duct: one bind ticket.
Efferent: same ticket to GPIO / voice / motor. No ticket, no fire.
Cortex receives the bound event, not three raw streams.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any

POC_FLOOR = ("MAG-QMC", "IMU-GY521")
UPGRADE = "ADXL355"
FORBIDDEN_DRIVER = {("MAG-QMC", "HMC5883L"), ("MAG-QMC", "HMC5883")}

ASSERTED_ADDR = {
    "MAG-QMC": (0x2C,),
    "IMU-GY521": (0x68, 0x69),
}

EFFERENT_TOKENS = ("GPIO", "VOICE", "MOTOR")


class PathError(ValueError):
    pass


def _finite_triplet(name: str, xyz: tuple[float, float, float]) -> tuple[float, float, float]:
    if len(xyz) != 3:
        raise PathError(f"{name}: need 3 axes")
    out = []
    for v in xyz:
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            raise PathError(f"{name}: non-numeric")
        fv = float(v)
        if not math.isfinite(fv):
            raise PathError(f"{name}: NaN/Inf dumped")
        out.append(fv)
    return (out[0], out[1], out[2])


def shepherd_clean(sample: dict[str, Any]) -> dict[str, Any]:
    """One-pass filter. Recycle finite; dump NaN/Inf/wrong-driver."""
    sid = sample.get("id")
    if sid not in POC_FLOOR:
        raise PathError(f"not POC floor: {sid}")
    driver = sample.get("driver")
    if driver is None:
        raise PathError(f"{sid}: driver unnamed")
    if (sid, str(driver)) in FORBIDDEN_DRIVER:
        raise PathError(f"{sid}: HMC driver forbidden on QMC")
    if sid == "MAG-QMC" and str(driver) != "QMC5883P":
        raise PathError(f"{sid}: driver must be QMC5883P, got {driver}")
    if sid == "IMU-GY521" and str(driver) not in ("GY-521", "MPU-6050"):
        raise PathError(f"{sid}: driver must be GY-521/MPU-6050, got {driver}")

    addr = sample.get("addr")
    typical = ASSERTED_ADDR[sid]
    addr_standing = "ASSERTED_TYPICAL"
    if addr is not None:
        if addr not in typical:
            raise PathError(f"{sid}: addr 0x{int(addr):02X} not in typical {tuple(hex(a) for a in typical)}")
        addr_standing = "ASSERTED_TYPICAL_MATCH"
        # still not earned — bus scan is GOSUB_TO_NEXT

    job = sample.get("job")
    if sid == "MAG-QMC":
        heading = _finite_triplet("MAG-QMC", tuple(sample["xyz"]))
        return {
            "id": sid,
            "job": job or "heading",
            "driver": "QMC5883P",
            "xyz": heading,
            "addr": addr,
            "addr_standing": addr_standing,
        }
    accel = _finite_triplet("IMU-GY521.accel", tuple(sample["accel"]))
    gyro = _finite_triplet("IMU-GY521.gyro", tuple(sample["gyro"]))
    return {
        "id": sid,
        "job": job or "accel+gyro",
        "driver": str(driver),
        "accel": accel,
        "gyro": gyro,
        "addr": addr,
        "addr_standing": addr_standing,
    }


def bind_ticket(cleaned: list[dict[str, Any]]) -> dict[str, Any]:
    """One ticket from both afferent streams. Cortex sees this, not raw."""
    ids = {c["id"] for c in cleaned}
    missing = [x for x in POC_FLOOR if x not in ids]
    if missing:
        raise PathError(f"bind refused, missing afferent: {missing}")
    extra = ids - set(POC_FLOOR)
    if extra:
        raise PathError(f"bind refused, extra stream: {sorted(extra)}")
    if any(c["id"] == UPGRADE for c in cleaned):
        raise PathError("ADXL355 is upgrade path, not POC floor")

    body = {
        "kind": "BIND_TICKET",
        "floor": list(POC_FLOOR),
        "streams": {c["id"]: c for c in cleaned},
        "addr_standing": "ASSERTED_TYPICAL_NOT_BUS_EARNED",
        "adxl355": "GATED_UNTIL_VAL",
    }
    digest = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    body["ticket_id"] = digest
    return body


def efferent_fire(ticket: dict[str, Any] | None, token: str) -> dict[str, Any]:
    """Typed injector. Sensor = ticket present. Shutoff = no ticket."""
    if token not in EFFERENT_TOKENS:
        raise PathError(f"unknown efferent token: {token}")
    if not ticket or ticket.get("kind") != "BIND_TICKET" or not ticket.get("ticket_id"):
        raise PathError("no ticket, no fire")
    if UPGRADE in ticket.get("streams", {}):
        raise PathError("ADXL355 gated")
    return {
        "fired": True,
        "token": token,
        "ticket_id": ticket["ticket_id"],
        "event": "BOUND",
    }


def cortex_event(ticket: dict[str, Any]) -> dict[str, Any]:
    if not ticket or ticket.get("kind") != "BIND_TICKET":
        raise PathError("cortex takes bound event only")
    return {
        "to": "CORTEX",
        "event": "BOUND",
        "ticket_id": ticket["ticket_id"],
        "raw_streams": False,
        "floor": ticket["floor"],
    }


def adxl355_upgrade_allowed(ticket: dict[str, Any] | None, val: bool) -> bool:
    if not ticket or ticket.get("kind") != "BIND_TICKET":
        return False
    return bool(val)


def ingest_and_bind(mag: dict[str, Any], imu: dict[str, Any]) -> dict[str, Any]:
    cleaned = [shepherd_clean(mag), shepherd_clean(imu)]
    return bind_ticket(cleaned)
