#!/usr/bin/env python3
"""KBLD9 / SVCT timestamp provenance extract — caller typed / voice SAVE 2026-09-22.

Source: /workspace/kbld9/kbld9_core_r7.py lines 340-376 (verbatim extract).
Source SHA-256: 465359bb0339d3acdd1b94282a0d9191fb663b734cd2b552e36baf5e75da31d8
Standing: wall-clock created_utc is parked OUTSIDE the content digest;
nonce is secrets.randbits(64), not time-derived; not a network TSA call.
Do not open sealed core beyond this extract.
"""
from __future__ import annotations

import hashlib
import json
import secrets
import time
from typing import Any, Dict, List, Optional, Union

__version__ = "9.0.7-core-extract"

# --- verbatim from kbld9_core_r7.py L340-376 ---
# ============================================================

def _sha256(data: Union[str, bytes, list]) -> str:
    if isinstance(data, list):
        data = json.dumps(data, sort_keys=True,
                          separators=(",", ":")).encode()
    elif isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def _timestamp_request(sha_hex: str) -> Dict[str, Any]:
    """Pure-stdlib RFC 3161 TimeStampReq-like structure. Nonce is
    cryptographically random (secrets), not time-derived: a predictable or
    colliding nonce defeats replay detection at the TSA boundary."""
    return {
        "version": 1,
        "messageImprint": {
            "hashAlgorithm": "SHA-256",
            "hashedMessage": sha_hex,
        },
        "nonce": secrets.randbits(64),
        "certReq": False,
        "extensions": [],
    }


def _build_provenance(input_sha: str, output_sha: str,
                      previous: Optional[str]) -> Dict[str, Any]:
    return {
        "input_sha256": input_sha,
        "output_sha256": output_sha,
        "timestamp_request": _timestamp_request(input_sha),
        "chain": [previous] if previous else [],
        "kbld9_version": __version__,
        "created_utc": int(time.time()),
    }

# --- end extract ---

if __name__ == "__main__":
    req = _timestamp_request(_sha256([1.0, 2.0]))
    assert req["version"] == 1
    assert isinstance(req["nonce"], int)
    prov = _build_provenance("a" * 64, "b" * 64, None)
    assert "created_utc" in prov and "timestamp_request" in prov
    print("OK extract smoke", prov["created_utc"], type(req["nonce"]).__name__)
