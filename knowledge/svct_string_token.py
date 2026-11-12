#!/usr/bin/env python3
"""svct_string_token.py — SVCT string token for truncate-toward-zero.

Token format (sealed):
SVCT|1|{truncated}|{places}|{sha256_hex(stripped_original + '|' + str(places))}

Both Python and C++ adapters must emit identical tokens.
"""
import hashlib
from truncate_toward_zero import truncate_toward_zero


def _sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def svct_string_token(original: str, places: int = 6) -> str:
    """Return sealed SVCT string token. Identical across adapters."""
    if not isinstance(original, str):
        original = ""
    stripped = original.strip()
    truncated = truncate_toward_zero(stripped, places)
    payload = f"{stripped}|{places}"
    digest = _sha256_hex(payload)
    return f"SVCT|1|{truncated}|{places}|{digest}"
