"""Caution GOSUB. Two faces. Hold before a change and before output.

Number stays a number. Word becomes hex. The caution watch does not
rewrite the record. It compares, appends a row, and holds.
SHA-256 at seat aef16655302f4ba92d43392773b9dc5d8035d01badc0fb18ce61b694470c08be
"""
from __future__ import annotations

import hashlib

HEX = set("0123456789abcdef")
SCRIPT = (".bat", ".js", ".ps1", ".exe", ".dll")


def gosub_face(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "numeric", value
    text = "" if value is None else str(value)
    if text == "":
        return "hex", "0≡cycle"
    return "hex", text.encode("utf-8").hex()


def gosub_hex_back(face: str):
    if face in ("0≡cycle", "HOLD"):
        return face
    s = face.strip().lower()
    if len(s) % 2 or any(c not in HEX for c in s):
        return "HOLD"
    return bytes.fromhex(s).decode("utf-8")


def _names(payload: dict) -> dict:
    return dict(payload.get("names") or {})


def gosub_caution(before: dict, after: dict) -> dict:
    """Ongoing watch. Does not repair. Holds if a script ending was put back."""
    b, a = _names(before), _names(after)
    reassembled = []
    for name, size in b.items():
        if name.endswith(".txt") and name[: -4].endswith(SCRIPT):
            bare = name[:-4]
            if bare in a and a[bare] == size:
                reassembled.append(bare)
    bh = before.get("sha256")
    ah = after.get("sha256")
    hold = bool(reassembled) or (bh and ah and bh != ah and "remove the .txt" in str(after.get("note", "")))
    return {
        "status": "HOLD" if hold else "PASS",
        "reassembled": reassembled,
        "sha_before": bh,
        "sha_after": ah,
        "row": "caution append",
    }


def gosub_before_change(record, feature) -> dict:
    face, out = gosub_face(record.get("value"))
    proposed = feature(record)
    watch = gosub_caution(record, proposed)
    if watch["status"] == "HOLD":
        return {"status": "HOLD", "face": face, "out": record, "watch": watch}
    return {"status": "PASS", "face": face, "out": proposed, "watch": watch}


def gosub_before_output(record) -> dict:
    face, encoded = gosub_face(record.get("value"))
    back = gosub_hex_back(encoded) if face == "hex" else encoded
    ok = face == "numeric" or back == (record.get("value") or "") or encoded == "0≡cycle"
    return {
        "status": "PASS" if ok else "HOLD",
        "face": face,
        "encoded": encoded,
        "sha256": hashlib.sha256(repr(encoded).encode("utf-8")).hexdigest(),
    }
