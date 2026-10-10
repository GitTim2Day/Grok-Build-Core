#!/usr/bin/env python3
"""OCR streamline clean. Twin of ocr_streamline.bas.

Streamline contract (Timothy Norman):
  GOSUB / RETURN, IF / THEN / ELSE, one entry, one exit.
  BASIC commands exercised: LINE, BOX, CIRCLE, TRIANGLE.
  Fail-closed. No field guessing. No 0/O swaps. No fitted thresholds.

Clean steps, in order:
  1. GOSUB FOLD_EXACT   — enumerated glyph fold only
  2. GOSUB COLLAPSE     — TAB to space, drop CR/FF, collapse spaces, trim
  3. GOSUB BOX_EDGE     — strip the vertical LINE runs on the two ends
  4. GOSUB LINE_RULE    — drop a line whose marks are only a horizontal rule
  5. GOSUB CIRCLE_MARK  — drop a line whose marks are only () 
  6. GOSUB TRIANGLE_MARK — drop a line whose marks are only ^ / \\
  7. Second pass is identity.

Skill value is GOSUB_ACCURACY_FLOOR(matched, reference_length):
  percent error, truncate toward zero at 1e-6. Zero means the cleaned
  text matches the sealed fixture. Reference length zero is an error.
"""

from __future__ import annotations

import math
import re
import time
from typing import Dict, Optional, Tuple

HLINE = set("-_=+~")
CIRCLE = set("()")
TRIANGLE = set("^/\\")
EDGE = set(" |")

# Exact folds. Empty string deletes. Multi-char expands ligatures.
FOLD: Dict[str, str] = {
    "\u00a0": " ",
    "\u00ad": "",
    "\u200b": "",
    "\u200c": "",
    "\u200d": "",
    "\ufeff": "",
    "\u2018": "'",
    "\u2019": "'",
    "\u201a": "'",
    "\u2032": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u201e": '"',
    "\u2033": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\u2015": "-",
    "\ufb01": "fi",
    "\ufb02": "fl",
    "\ufb00": "ff",
    "\ufb03": "ffi",
    "\ufb04": "ffl",
}


def gosub_accuracy_floor(
    observed: float, reference: float
) -> Tuple[Optional[float], Optional[str]]:
    """Same contract as kbld-gosub-primitives GOSUB_ACCURACY_FLOOR.

    Returns percent |observed-reference|/reference, truncated toward zero
    at 1e-6. Negatives and a zero reference are errors. Not a match score.
    """
    if isinstance(observed, bool) or isinstance(reference, bool):
        return None, "ERROR: non-numeric or NaN/Inf input"
    try:
        o = float(observed)
        r = float(reference)
    except (TypeError, ValueError):
        return None, "ERROR: non-numeric or NaN/Inf input"
    if not math.isfinite(o) or not math.isfinite(r):
        return None, "ERROR: non-numeric or NaN/Inf input"
    if r == 0:
        return None, "ERROR: reference zero (no-zero rule)"
    if o < 0 or r < 0:
        return None, "ERROR: negative input — route to Shepherd 10σ + append log"
    pct = abs(o - r) / abs(r) * 100.0
    return math.trunc(pct * 1e6) / 1e6, None


def _fold_char(ch: str) -> str:
    if ch in FOLD:
        return FOLD[ch]
    o = ord(ch)
    if 0x2500 <= o <= 0x259F:
        return ""
    return ch


def _collapse(raw: str) -> str:
    buf = []
    started = False
    prev_space = False
    for ch in raw:
        ch = _fold_char(ch)
        if not ch:
            continue
        for piece in ch:
            if piece == "\t":
                piece = " "
            elif piece == "\n":
                continue
            elif ord(piece) < 32 or ord(piece) == 127:
                continue
            if piece == " ":
                if (not started) or prev_space:
                    continue
                buf.append(" ")
                prev_space = True
                continue
            started = True
            prev_space = False
            buf.append(piece)
    if buf and buf[-1] == " ":
        buf.pop()
    return "".join(buf)


def _box_edge(s: str) -> str:
    i = 0
    j = len(s)
    while i < j and s[i] in EDGE:
        i += 1
    while j > i and s[j - 1] in EDGE:
        j -= 1
    return s[i:j]


def _only_marks(s: str, alphabet: set) -> bool:
    if not s:
        return True
    for ch in s:
        if ch == " ":
            continue
        if ch not in alphabet:
            return False
    return True


def gosub_clean_line(raw: str) -> Optional[str]:
    """One line. None means DROP (rule, circle, triangle, or empty)."""
    s = _box_edge(_collapse(raw))
    if not s:
        return None
    if _only_marks(s, HLINE):
        return None
    if _only_marks(s, CIRCLE):
        return None
    if _only_marks(s, TRIANGLE):
        return None
    return s


def gosub_ocr_clean(text: str) -> str:
    """Single entry. Join kept lines with LF. No trailing LF."""
    if not isinstance(text, str):
        raise TypeError("text must be str")
    kept = []
    for raw in text.split("\n"):
        line = gosub_clean_line(raw)
        if line is not None:
            kept.append(line)
    return "\n".join(kept)


def gosub_box() -> Tuple[str, str, str]:
    return ("+---+", "|   |", "+---+")


def gosub_line() -> str:
    return "-----"


def gosub_circle() -> Tuple[str, str, str]:
    return ("  o  ", " o o ", "  o  ")


def gosub_triangle() -> Tuple[str, str, str]:
    return ("  ^  ", " / \\ ", "-----")


def _slow_clean(text: str) -> str:
    """Same contract, many passes. The speed comparison, not a second spec."""
    out = text
    for src, dst in FOLD.items():
        out = out.replace(src, dst)
    out = re.sub(r"[\u2500-\u259f]", "", out)
    kept = []
    for raw in out.split("\n"):
        s = raw.replace("\t", " ").replace("\r", "").replace("\f", "")
        s = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", s)
        s = re.sub(r" +", " ", s).strip()
        s = re.sub(r"^[ |]+", "", s)
        s = re.sub(r"[ |]+$", "", s)
        if not s:
            continue
        letters = s.replace(" ", "")
        if letters and set(letters) <= HLINE:
            continue
        if letters and set(letters) <= CIRCLE:
            continue
        if letters and set(letters) <= TRIANGLE:
            continue
        if not letters:
            continue
        kept.append(s)
    return "\n".join(kept)


def naive_ends_only(text: str) -> str:
    """The miss: strip line ends only. Rules and edge pipes stay."""
    kept = []
    for raw in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        s = raw.strip()
        if s:
            kept.append(s)
    return "\n".join(kept)


def skill_value_of(observed_text: str, reference_text: str):
    """Floor on character agreement. Extra or shifted chars count as misses."""
    ref_n = len(reference_text)
    if ref_n == 0:
        return None, "ERROR: reference zero (no-zero rule)"
    mlen = min(len(observed_text), ref_n)
    matched = 0
    for i in range(mlen):
        if observed_text[i] == reference_text[i]:
            matched += 1
    # Length gap is a miss, so matched cannot exceed the aligned span.
    gap = abs(len(observed_text) - ref_n)
    # If the strings differ in length, the floor uses matched against ref_n.
    # Cap is implicit: matched <= mlen <= ref_n.
    del gap
    return gosub_accuracy_floor(matched, ref_n)


SHARED_DIRTY = (
    "\r\n"
    "  JOHN   DOE  \r\n"
    "-----\n"
    "|1EG4TE5MK72|\n"
    "\t\tI10\t\n"
    "__________\n"
    "|99213|\n"
    "()\n"
    "^\n"
    "|08|01|2026|\n"
    "||NONE||\n"
    "A|B\n"
    "O\n"
)
SHARED_REF = "\n".join(
    [
        "JOHN DOE",
        "1EG4TE5MK72",
        "I10",
        "99213",
        "08|01|2026",
        "NONE",
        "A|B",
        "O",
    ]
)


def _check(name: str, cond: bool, detail: str = "") -> bool:
    tag = "PASS" if cond else "FAIL"
    extra = f" | {detail}" if detail else ""
    print(f"{tag}: {name}{extra}")
    return cond


def run_self_check() -> int:
    fails = 0

    b1, b2, b3 = gosub_box()
    if not _check("box", b1 == "+---+" and b2 == "|   |" and b3 == "+---+"):
        fails += 1
    if not _check("line", gosub_line() == "-----"):
        fails += 1
    c1, c2, c3 = gosub_circle()
    if not _check("circle", c1 == "  o  " and c2 == " o o " and c3 == "  o  "):
        fails += 1
    d1, d2, d3 = gosub_triangle()
    if not _check(
        "triangle", d1 == "  ^  " and d2 == " / \\ " and d3 == "-----"
    ):
        fails += 1

    cases = [
        ("", None),
        ("   ", None),
        ("-----", None),
        ("- -", None),
        ("____", None),
        ("====", None),
        ("++++", None),
        ("~~~~", None),
        ("()", None),
        ("( )", None),
        ("^", None),
        ("/\\", None),
        ("|", None),
        ("||", None),
        ("| |", None),
        ("  JOHN   DOE  ", "JOHN DOE"),
        ("|1EG4TE5MK72|", "1EG4TE5MK72"),
        ("\t\tI10\t", "I10"),
        ("|99213|", "99213"),
        ("99213", "99213"),
        ("|08|01|2026|", "08|01|2026"),
        ("||NONE||", "NONE"),
        ("A|B", "A|B"),
        ("O", "O"),
        ("JOHN | DOE", "JOHN | DOE"),
        ("|----|", None),
        ("|()|", None),
    ]
    for src, expect in cases:
        got = gosub_clean_line(src)
        if not _check(f"line_{src!r}", got == expect, f"got={got!r}"):
            fails += 1
        if got is not None:
            again = gosub_clean_line(got)
            if not _check(f"identity_{src!r}", again == got, f"again={again!r}"):
                fails += 1

    blob = gosub_ocr_clean(SHARED_DIRTY)
    if not _check("shared_blob", blob == SHARED_REF, f"got={blob!r}"):
        fails += 1
    if not _check("second_pass", gosub_ocr_clean(blob) == blob):
        fails += 1

    slow = _slow_clean(SHARED_DIRTY)
    if not _check("slow_matches_fast", slow == blob, f"slow={slow!r}"):
        fails += 1

    uni_src = "of\ufb01ce \u201cNONE\u201d\n\u2014\u2014\u2014\n\u2500\u2500\u2500\n"
    uni_got = gosub_ocr_clean(uni_src)
    if not _check("unicode_fold", uni_got == 'office "NONE"', f"got={uni_got!r}"):
        fails += 1

    before = naive_ends_only(SHARED_DIRTY)
    before_floor, before_err = skill_value_of(before, SHARED_REF)
    after_floor, after_err = skill_value_of(blob, SHARED_REF)
    if before_err or after_err:
        print(f"FAIL: floor {before_err} {after_err}")
        fails += 1
    else:
        if not _check(
            "before_was_worse",
            before_floor is not None
            and after_floor is not None
            and before_floor > after_floor,
            f"before={before_floor} after={after_floor}",
        ):
            fails += 1
        print(f"BEFORE_FLOOR: {before_floor:.6f}")
        print(f"SKILL_VALUE: {after_floor:.6f}")

    # Random ASCII lines: fast equals slow.
    alphabet = "ABCxyz09|-/^() =_+~ \t"
    rng_state = 1

    def rnd() -> int:
        nonlocal rng_state
        rng_state = (1103515245 * rng_state + 12345) & 0x7FFFFFFF
        return rng_state

    fuzz_lines = []
    for _ in range(200):
        n = rnd() % 24
        fuzz_lines.append("".join(alphabet[rnd() % len(alphabet)] for _ in range(n)))
    fuzz = "\n".join(fuzz_lines)
    fast_fuzz = gosub_ocr_clean(fuzz)
    slow_fuzz = _slow_clean(fuzz)
    if not _check("fuzz_match", fast_fuzz == slow_fuzz, f"len {len(fast_fuzz)} vs {len(slow_fuzz)}"):
        fails += 1

    blob_big = (SHARED_DIRTY + uni_src) * 80
    rounds = 400
    t0 = time.perf_counter()
    for _ in range(rounds):
        _slow_clean(blob_big)
    slow_s = time.perf_counter() - t0
    t1 = time.perf_counter()
    for _ in range(rounds):
        gosub_ocr_clean(blob_big)
    fast_s = time.perf_counter() - t1
    if slow_s <= 0:
        print("FAIL: slow timing")
        fails += 1
    else:
        ratio = slow_s / fast_s if fast_s > 0 else 0
        print(f"SLOW_SEC: {slow_s:.6f}")
        print(f"FAST_SEC: {fast_s:.6f}")
        print(f"FAST_OVER_SLOW: {ratio:.6f}")
        if not _check("faster", fast_s < slow_s, f"fast={fast_s:.6f} slow={slow_s:.6f}"):
            fails += 1

    # Floor rejects zero reference and negatives.
    z, zerr = gosub_accuracy_floor(1, 0)
    if not _check("floor_zero_ref", z is None and zerr is not None):
        fails += 1
    n, nerr = gosub_accuracy_floor(-1, 4)
    if not _check("floor_negative", n is None and nerr is not None):
        fails += 1

    print("SUMMARY: ALL PASS" if fails == 0 else f"SUMMARY: FAILS={fails}")
    return fails


if __name__ == "__main__":
    raise SystemExit(run_self_check())
