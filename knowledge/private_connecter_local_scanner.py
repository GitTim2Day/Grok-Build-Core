#!/usr/bin/env python3
"""
Private Connecter (TER) — Local File & Media Scanner agent-subroutine.
User-controlled. Runs only on his machine (Shepherd Pi5 / A15).
No public URL. No TOR. No xAI reach.
On-demand. Terminates. Human gate for any write.
Fail-closed. Appendable log.
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")
LOG_PATH = Path.home() / ".local" / "share" / "connecter" / "scanner_log.jsonl"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def now_ny():
    return datetime.now(NY).isoformat()

def append_log(entry: dict):
    entry["ts"] = now_ny()
    payload = json.dumps(entry, sort_keys=True, separators=(",", ":"))
    entry["sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry, separators=(",", ":")) + "\n")

def file_meta(full: str):
    st = os.stat(full)
    return {
        "path": full,
        "size": st.st_size,
        "mtime": datetime.fromtimestamp(st.st_mtime, NY).isoformat(),
        "ext": Path(full).suffix.lower()
    }

def scan_path(root: str, extensions=None, max_files=100):
    """Read-only. Accepts file or directory. Metadata only."""
    if not os.path.exists(root):
        return {"error": "path does not exist", "root": root}
    if os.path.isfile(root):
        try:
            meta = file_meta(root)
            if extensions and not any(meta["ext"] == ext or meta["path"].lower().endswith(ext) for ext in extensions):
                append_log({"action": "scan_file", "root": root, "returned": 0, "filtered": True})
                return {"root": root, "count": 0, "files": []}
            append_log({"action": "scan_file", "root": root, "returned": 1, "capped": False})
            return {"root": root, "count": 1, "files": [meta]}
        except OSError as e:
            return {"error": f"stat failed: {e}", "root": root}

    if not os.path.isdir(root):
        return {"error": "path not a directory or not accessible", "root": root}

    results = []
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in filenames:
            if name.startswith("."):
                continue
            if extensions and not any(name.lower().endswith(ext) for ext in extensions):
                continue
            full = os.path.join(dirpath, name)
            try:
                results.append(file_meta(full))
                count += 1
                if count >= max_files:
                    break
            except OSError:
                continue
        if count >= max_files:
            break
    append_log({"action": "scan", "root": root, "returned": len(results), "capped": count >= max_files})
    return {"root": root, "count": len(results), "files": results}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: private_connecter_local_scanner.py <path> [ext1,ext2]"}))
        sys.exit(1)
    root = sys.argv[1]
    exts = None
    if len(sys.argv) > 2:
        exts = [e.strip().lower() if e.strip().startswith(".") else "." + e.strip().lower()
                for e in sys.argv[2].split(",") if e.strip()]
    out = scan_path(root, exts)
    print(json.dumps(out, separators=(",", ":")))

if __name__ == "__main__":
    main()
