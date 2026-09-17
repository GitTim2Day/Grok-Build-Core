"""gosub_to_next_ABSENT_STUB.py — shelf stub only.

NOT the live gosub_to_next.py (nested GOSUB RETURN).
Claimed on Notion gosub-session-boot-2026-09-09: CLEAN 8/8.
No bytes on this chair 2026-09-16T22:42 EDT.
Recover-not-regenerate. Do not treat this as the original.

Named role: nested GOSUB / RETURN; advance only _to_next.
"""
from __future__ import annotations


class GosubToNextAbsent(RuntimeError):
    pass


def gosub_to_next(*_a, **_k):
    raise GosubToNextAbsent(
        "live gosub_to_next.py not on this shelf — recover bytes, do not reconstruct"
    )


if __name__ == "__main__":
    print("STUB_ONLY")
    print("CLAIMED CLEAN 8/8")
    print("ABSENT live body")
