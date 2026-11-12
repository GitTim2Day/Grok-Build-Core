#!/usr/bin/env python3
# poc_motor_cortex_send.py
# String-only. Truncate-toward-zero on any numeric display. Identical contract for later C++.
# He handles Shepherd. Error-tested paths.
# Motor cortex / locomotion node POC: send to project (local file), printer (if ready).

import subprocess
import sys
from datetime import datetime

def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def main():
    stamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    report = [f"POC motor-cortex send {stamp}"]

    # 1. bwbasic present?
    code, out, err = run("which bwbasic")
    if code != 0 or not out:
        report.append("MISS: bwbasic not in PATH. Install first.")
        print("\n".join(report))
        return
    report.append(f"HIT: bwbasic at {out}")

    # 2. Capture string output (no float)
    code, out, err = run("echo 'PRINT 0.70710678' | bwbasic")
    raw = out or err or ""
    report.append(f"RAW string from bwbasic: [{raw}]")
    # Deconcatenate / truncate display toward zero (string slice for 6 places after point)
    if "." in raw:
        parts = raw.split(".")
        trunc = parts[0] + "." + (parts[1][:6] if len(parts) > 1 else "")
        report.append(f"TRUNCATED string: [{trunc}]")
    else:
        trunc = raw
        report.append("No decimal; kept raw string.")

    # 3. Printer check (HP driver via CUPS/lp)
    code, out, err = run("lpstat -p 2>/dev/null || echo 'NO_PRINTER'")
    report.append(f"Printer status: {out or err}")
    printer_ok = "idle" in (out or "").lower() or "enabled" in (out or "").lower()

    # 4. Local project file (POC send to project)
    local_path = "/tmp/motor_cortex_poc.txt"
    try:
        with open(local_path, "w") as f:
            f.write("\n".join(report) + "\n")
        report.append(f"HIT: wrote local project file {local_path}")
    except Exception as e:
        report.append(f"MISS: local write failed: {e}")

    # 5. Printer send if available
    if printer_ok:
        code, out, err = run(f"echo '{trunc} motor-cortex POC' | lp")
        if code == 0:
            report.append("HIT: sent to printer via lp")
        else:
            report.append(f"MISS: lp failed: {err or out}")
    else:
        report.append("SKIP: no ready printer; local file only")

    # 6. Final
    report.append("DONE. String path only. No float64.")
    print("\n".join(report))

if __name__ == "__main__":
    main()
