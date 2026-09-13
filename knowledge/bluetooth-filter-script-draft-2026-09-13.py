#!/usr/bin/env python3
"""
bluetooth_filter.py — Pi 5 bluetoothctl scan filter.
Policy 2026-09-13 12:20 EDT: speakers always; CPAP extract-only (default drop).
Pure stdlib. No external deps.
"""
import sys
import re
from datetime import datetime, timezone

APPLE_MFG = "0x004c"
AIRPODS_PRODUCT = None  # lock from `info` while lid open

# Always-on comms: speakers + confirmed audio
WHITELIST_MACS = {
    "F8:5C:7E:A2:E5:FC",  # JBL Clip 4 speaker
    "44:16:83:C0:D1:4B",  # AirPods / case candidate (Apple Nearby)
}

SPEAKER_NAME_HINTS = ("JBL", "CLIP", "SPEAKER", "SOUNDBAR")

# Health / Rex MD Fortress only — default DROP unless HEALTH_EXTRACT=1
EXTRACT_ONLY_MACS = {
    "4C:5B:B3:DE:F4:C1",  # ResMed 701194 CPAP
}

BLACKLIST_MACS = {
    "DA:3C:2F:46:52:26",
    "ED:CB:D4:47:04:02",
    "C1:2D:1A:92:4D:FC",
    "48:57:02:19:DF",
    "62:C8:1C:AE:8F:2A",
    "77:67:50:39:39:6C",
    "ED:53:C3:70:A1:26",  # KSBT03C unless claimed
}

WATCH_LIST = {"KBLD9"}

LINE_RE = re.compile(
    r"\[(NEW|CHG|DEL)\]\s+Device\s+([0-9A-Fa-f:]+)\s*(.*?)\s*(?:RSSI:\s*0x[0-9a-fA-F]+\s*\((-?\d+)\))?$"
)

def normalize_mac(mac: str) -> str:
    return mac.upper().replace("-", ":")

def health_extract_on() -> bool:
    import os
    return os.environ.get("HEALTH_EXTRACT", "0") == "1"

def should_keep(mac: str, name: str, mfg: str | None) -> tuple[bool, str]:
    mac = normalize_mac(mac)
    name_u = (name or "").upper()
    if mac in WHITELIST_MACS:
        return True, "whitelist"
    if any(h in name_u for h in SPEAKER_NAME_HINTS):
        return True, "speaker-name"
    if mac in EXTRACT_ONLY_MACS:
        if health_extract_on():
            return True, "health-extract"
        return False, "extract-only-default-drop"
    if mac in BLACKLIST_MACS:
        return False, "blacklist-mac"
    if mfg and mfg.lower() == APPLE_MFG:
        if AIRPODS_PRODUCT and AIRPODS_PRODUCT in name_u:
            return True, "airpods"
        return False, "apple-noise"
    if any(w in name_u for w in WATCH_LIST):
        return True, "watch"
    return False, "unknown-noise"

def parse_line(line: str):
    m = LINE_RE.match(line.strip())
    if not m:
        return None
    tag, mac, name, rssi = m.groups()
    return {
        "tag": tag,
        "mac": normalize_mac(mac),
        "name": name.strip(),
        "rssi": int(rssi) if rssi else None,
        "raw": line.strip(),
    }

def main():
    print(f"# bluetooth filter started {datetime.now(timezone.utc).isoformat()}")
    print("# policy: speakers always; CPAP extract-only unless HEALTH_EXTRACT=1")
    print("# tag | mac | name | rssi | decision | reason")
    for line in sys.stdin:
        parsed = parse_line(line)
        if not parsed:
            continue
        keep, reason = should_keep(parsed["mac"], parsed["name"], None)
        decision = "KEEP" if keep else "DROP"
        print(f"{parsed['tag']} | {parsed['mac']} | {parsed['name']} | {parsed['rssi']} | {decision} | {reason}")

if __name__ == "__main__":
    main()
