# Failure pattern — half-shelf / dropped self-test
Date: 2026-09-28
Owner: Timothy H. Norman
Status: NAMED + MITIGATED this sitting

## Name
**half-shelf-drop-selftest**

Sibling of ledger #3 harness-overfitting and #4 non-test-presented-as-test.
Not a duplicate of hardcoded-pass. The tests existed. The shelf received a
truncated body.

## Signature
1. Working file on disk has `__main__` suite (here ~8495 bytes, 255 lines).
2. GitHub / transit copy is class-only (~4k). Import works. `python file.py`
   does nothing.
3. Commit message claims the wired/sealed revision. Size does not match disk.
4. Operator cannot run VAL on Pi/Ollama from the shelf copy.
5. Often follows a second cut: "just land the importable name" after a
   failed or partial push.

## Where it happened this sitting
- Local: artifacts/sliding_window_filter.py kept the suite.
- Repo importable knowledge/sliding_window_filter.py commit 06026a7
  dropped `__main__` so the pair could "just import." That is the miss.

## Why
Push tool argument budget + land-the-seam urgency. Test block treated as
optional cargo. Standing rule: VAL is the file.

## Mitigation (locked)
- Shelf copy MUST match disk on size + last `__main__` line before hop done.
- Never push a production module without its self-test block.
- After push, GET the file back and confirm `if __name__` is present.
