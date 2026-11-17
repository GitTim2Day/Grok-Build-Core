#!/usr/bin/env python3
# thought_node.py
# Reads three stamped channels. Emits one new string token under the same timestamp.
# No fusion rules. Failed channels recorded as FAIL.

def thought_from_three(channels, failed, ts):
    """Produce one THOUGHT token. Identical contract across languages."""
    parts = []
    for name in ("speech", "ocr", "motor"):
        text = channels.get(name, {}).get("text", "")
        status = "FAIL" if name in failed else "OK"
        # Escape any pipe characters so the token remains parseable
        safe_text = text.replace("|", "\\|")
        parts.append(f"{name}:{status}:{safe_text}")
    token = f"THOUGHT|{ts}|{'|'.join(parts)}"
    return token
