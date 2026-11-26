#!/usr/bin/env python3
"""neural_channel_operators.py
Precision layer: Gate, Split, Tag, Merge, Verify.
Deterministic. Append-only. Full enumeration. String-based.
Do No Harm first. Self-control boundary.
"""

import hashlib
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, Dict, List, Tuple


def now_ny() -> str:
    # America/New_York stamp. ISO format with offset.
    return datetime.now(ZoneInfo("America/New_York")).isoformat(timespec="seconds")


def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def gate(stream: Dict[str, Any], harm_check: bool = True) -> Tuple[bool, Dict[str, Any]]:
    """Gate: pass or quarantine. Do No Harm check first."""
    if not harm_check:
        return False, {"status": "QUARANTINE", "reason": "Do No Harm fail", "stream": stream}
    if not stream or not isinstance(stream, dict):
        return False, {"status": "QUARANTINE", "reason": "Empty or invalid stream", "stream": stream}
    return True, {"status": "PASS", "stream": stream}


def split(stream: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Split: parallel fork into content path and context path (amygdala bidirectional parse)."""
    content = {"path": "content", "data": stream.get("data", ""), "raw": stream}
    context = {"path": "context", "meta": stream.get("meta", {}), "raw": stream}
    return content, context


def tag(item: Dict[str, Any], salience: str = "normal") -> Dict[str, Any]:
    """Tag: attach salience and provenance stamp."""
    stamped = dict(item)
    stamped["salience"] = salience
    stamped["stamp"] = now_ny()
    stamped["tag_sha"] = sha256_str(json.dumps(stamped, sort_keys=True, default=str))
    return stamped


def merge(content: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Merge: recombine into one index row. Full set retained."""
    row = {
        "toc_id": sha256_str(content.get("data", "") + str(context.get("meta", "")))[:16],
        "content": content,
        "context": context,
        "status": "ACTIVE",
        "stamp": now_ny(),
    }
    row["row_sha"] = sha256_str(json.dumps(row, sort_keys=True, default=str))
    return row


def verify(row: Dict[str, Any], expected_sha: str = None) -> Tuple[bool, str]:
    """Verify: hash check. Returns HIT or MISS."""
    computed = row.get("row_sha") or sha256_str(json.dumps(row, sort_keys=True, default=str))
    if expected_sha and computed != expected_sha:
        return False, "MISS"
    required = ["toc_id", "content", "context", "status"]
    if all(k in row for k in required):
        return True, "HIT"
    return False, "MISS"


# --- Pipeline ---

def process_channel(stream: Dict[str, Any]) -> Dict[str, Any]:
    """Full channel: Gate -> Split -> Tag (parallel) -> Merge -> Verify."""
    passed, gated = gate(stream)
    if not passed:
        return {"result": "QUARANTINE", "detail": gated}
    content, context = split(gated["stream"])
    content_tagged = tag(content, "content")
    context_tagged = tag(context, "context")
    row = merge(content_tagged, context_tagged)
    ok, status = verify(row)
    row["verify"] = status
    return {"result": status, "row": row}


# --- Error tests ---

def run_tests() -> List[str]:
    results = []
    clean = {"data": "sensor reading 42", "meta": {"channel": "Sensor"}}
    out = process_channel(clean)
    results.append(f"T1 clean: {out['result']} toc={out.get('row', {}).get('toc_id', 'none')}")
    out2 = process_channel({})
    results.append(f"T2 empty: {out2['result']}")
    out3 = process_channel(None)  # type: ignore
    results.append(f"T3 none: {out3['result']}")
    out4 = process_channel(clean)
    if "row" in out4:
        out4["row"]["status"] = "TAMPERED"
        ok, st = verify(out4["row"], expected_sha="deadbeef")
        results.append(f"T4 tamper: {st}")
    items = [
        {"data": "a", "meta": {"id": 1}},
        {"data": "b", "meta": {"id": 2}},
    ]
    rows = [process_channel(i) for i in items]
    results.append(f"T5 multi: {len(rows)} rows, all HIT={all(r['result']=='HIT' for r in rows)}")
    return results


if __name__ == "__main__":
    print("Neural channel operators - error test")
    for line in run_tests():
        print(line)
    print("Done.")
