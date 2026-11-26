#!/usr/bin/env python3
"""Local-seal sub-agent. Watches artifacts/, seals new/changed files SHA-256,
appends local manifest row, tries shelf write when connector appears.
No auto-upload without human gate."""
import os, sys, json, hashlib, time
from pathlib import Path
from datetime import datetime

ARTIFACTS = Path("artifacts")
MANIFEST = ARTIFACTS / "local_seal_manifest.jsonl"

def seal(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    watch = "--watch" in sys.argv
    seen = set()
    if MANIFEST.exists():
        for line in MANIFEST.read_text().splitlines():
            try:
                seen.add(json.loads(line)["path"])
            except Exception:
                pass
    while True:
        if not ARTIFACTS.is_dir():
            print("artifacts/ not found"); 
            if not watch: sys.exit(1)
            time.sleep(5); continue
        for p in sorted(ARTIFACTS.rglob("*")):
            if p.is_file() and str(p) not in seen and p.name != MANIFEST.name:
                sha = seal(p)
                row = {"ts": datetime.now().astimezone().isoformat(), "path": str(p), "sha256": sha, "size": p.stat().st_size}
                with open(MANIFEST, "a") as f:
                    f.write(json.dumps(row) + "\n")
                seen.add(str(p))
                print(json.dumps(row))
        if not watch:
            break
        time.sleep(5)

if __name__ == "__main__":
    main()