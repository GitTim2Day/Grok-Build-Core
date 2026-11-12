#!/usr/bin/env python3
"""svct_string_token.py — SVCT string token, five pillars.

Token format (sealed):
SVCT|1|{truncated}|{places}|{sha256_hex(stripped + '|' + places)}|{ny_timestamp}|VAL

Pillars: content · context · data · time · validation
"""
import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
from truncate_toward_zero import truncate_toward_zero


def _sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _ny_now() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%dT%H:%M:%S%z")


def svct_string_token(original: str, places: int = 6, timestamp: str = None) -> str:
    """Return sealed five-pillar SVCT string token. Identical across adapters."""
    if not isinstance(original, str):
        original = ""
    stripped = original.strip()
    truncated = truncate_toward_zero(stripped, places)
    payload = f"{stripped}|{places}"
    digest = _sha256_hex(payload)
    ts = timestamp if timestamp is not None else _ny_now()
    return f"SVCT|1|{truncated}|{places}|{digest}|{ts}|VAL"
