"""Word door for KBLD9 / Shepherd. Hex is the numeric face of text.

Not a sensor-only path. UTF-8 bytes become hex so the validator
can bound a word stream. Empty is cycle, not a stored zero.
Non-hex is HOLD. Roundtrip must match.
Recreate 2026-10-07. Original body not on shelf or in 120d ledger mail.
SHA-256 of this face at seat: 7929e4f56193afd1e42a28d87ce98995a37cad381d1a501cf68621ced6d13fff
"""
from __future__ import annotations

HEX = set("0123456789abcdef")


def word_to_hex(text: str) -> str:
    if text is None:
        return "HOLD"
    raw = text.encode("utf-8")
    if not raw:
        return "0≡cycle"
    return raw.hex()


def hex_to_word(h: str) -> str:
    if h in ("0≡cycle", "HOLD", "", None):
        return h or "HOLD"
    s = h.strip().lower()
    if len(s) % 2 or any(c not in HEX for c in s):
        return "HOLD"
    return bytes.fromhex(s).decode("utf-8")


def receive_word(text: str) -> dict:
    face = word_to_hex(text)
    back = hex_to_word(face) if face not in ("HOLD", "0≡cycle") else face
    ok = (text == "" and face == "0≡cycle") or back == text
    return {"in": text, "hex": face, "out": back, "status": "PASS" if ok else "HOLD"}
