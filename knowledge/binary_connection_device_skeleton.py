#!/usr/bin/env python3
"""binary_connection_device_skeleton.py
One-file skeleton for the binary connection device.
Input: any source (STT, keyboard, Bluetooth, Wi-Fi, cellular, OCR).
Output: action or report (TTS, actuation, status).
Thinking, reasoning, calculations occur inside between input and output.
No sudo. Append-only provenance. Existing primitives only.
Designed 2026-11-06, sealed 2026-11-10.
Ties to: underwater device requirement, Optimus pipeline, scene loop.
"""
import hashlib
import os
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

SHELF = os.path.expanduser("~/binary_connection")
LOG = os.path.join(SHELF, "binary_log.txt")
os.makedirs(SHELF, exist_ok=True)

GENESIS = "0" * 64

def now_ny():
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %Z")

def last_hash():
    if not os.path.exists(LOG):
        return GENESIS
    with open(LOG, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    if not lines:
        return GENESIS
    return lines[-1].split(" · ")[-1]

def chain_hash(prev, payload):
    return hashlib.sha256((prev + payload).encode("utf-8")).hexdigest()

def receive(source, payload):
    """Any input source: stt, keyboard, ocr, bluetooth, wifi, cellular."""
    if not payload:
        print("REFUSED: empty payload")
        return None
    h = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    stamp = now_ny()
    prev = last_hash()
    line_payload = f"IN · {source} · {h[:16]} · {stamp}"
    running = chain_hash(prev, line_payload)
    line = f"{line_payload} · {running}\n"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())
    return h

def think(received_hash):
    """Placeholder for reasoning/calculation between input and output.
    Replace with actual math primitives, Vosk/Piper hooks, or KBLD calls.
    Must return a deterministic action or report string.
    """
    # TODO: bind real computation here
    return f"COMPUTED_ON · {received_hash[:16]}"

def act(action_or_report):
    """Output: TTS, actuation (rudders/fins/motor), or status report."""
    h = hashlib.sha256(action_or_report.encode("utf-8")).hexdigest()
    stamp = now_ny()
    prev = last_hash()
    line_payload = f"OUT · {action_or_report[:60]} · {h[:16]} · {stamp}"
    running = chain_hash(prev, line_payload)
    line = f"{line_payload} · {running}\n"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())
    return h

def verify_log():
    """Re-derive the chain from genesis. Fail closed on break."""
    if not os.path.exists(LOG):
        return True, "empty"
    prev = GENESIS
    with open(LOG, encoding="utf-8") as f:
        for i, ln in enumerate(f, 1):
            ln = ln.strip()
            if not ln:
                continue
            parts = ln.rsplit(" · ", 1)
            if len(parts) != 2:
                return False, f"line {i} malformed"
            payload, claimed = parts
            calc = chain_hash(prev, payload)
            if calc != claimed:
                return False, f"CHAIN BREAK line {i}"
            prev = claimed
    return True, "OK"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: binary_connection_device_skeleton.py <source> <payload>")
        print("sources: stt, keyboard, ocr, bluetooth, wifi, cellular")
        sys.exit(1)
    source, payload = sys.argv[1], sys.argv[2]
    rh = receive(source, payload)
    if rh is None:
        sys.exit(2)
    result = think(rh)
    act(result)
    ok, reason = verify_log()
    if not ok:
        print(f"VERIFY FAIL: {reason}")
        sys.exit(3)
    print("VERIFY OK")
