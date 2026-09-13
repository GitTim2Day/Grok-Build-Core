#!/usr/bin/env python3
"""
bluetooth_filter.py — Draft filter for Pi 5 bluetoothctl scan output.
Based on live scan 2026-09-13. Whitelist/blacklist from knowledge/bluetooth-whitelist-blacklist-2026-09-13.md

Run on Pi: python3 bluetooth_filter.py  (or pipe bluetoothctl output)
Pure stdlib. No external deps.
"""
import sys
import re
from datetime import datetime, timezone

# From today's scan + spec
APPLE_MFG = "0x004c"
AIRPODS_PRODUCT = None  # TODO: capture exact product code from a clean AirPods scan

WHITELIST_MACS = {
    "F8:5C:7E:A2:E5:FC",  # JBL Clip 4
    "4C:5B:B3:DE:F4:C1",  # ResMed 701194 CPAP
}

BLACKLIST_MACS = {
    "DA:3C:2F:46:52:26",
    "ED:CB:D4:47:04:02",
    "C1:2D:1A:92:4D:FC",
    "48:57:02:19:DF",
    "62:C8:1C:AE:8F:2A",
}

WATCH_LIST = {
    "KBLD9",  # keyboard/trackpad — keep visible, don't block
}

LINE_RE = re.compile(
    r"\[(NEW|CHG|DEL)\]\s+Device\s+([0-9A-Fa-f:]+)\s*(.*?)\s*(?:RSSI:\s*0x[0-9a-fA-F]+\s*\((-?\d+)\))?$"
)

def normalize_mac(mac: str) -> str:
    return mac.upper().replace("-", ":")

def should_keep(mac: str, name: str, mfg: str | None) -> tuple[bool, str]:
    mac = normalize_mac(mac)
    if mac in WHITELIST_MACS:
        return True, "whitelist"
    if mac in BLACKLIST_MACS:
        return False, "blacklist-mac"
    if mfg and mfg.lower() == APPLE_MFG:
        # Keep only AirPods; everything else Apple is noise
        if AIRPODS_PRODUCT and AIRPODS_PRODUCT in (name or "").upper():
            return True, "airpods"
        return False, "apple-noise"
    if any(w in (name or "") for w in WATCH_LIST):
        return True, "watch"
    # Default: drop unknown noise
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
