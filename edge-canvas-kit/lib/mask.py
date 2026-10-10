"""mask.py -- personal-data masking (DM-5) for copies placed in knowledge/ and agent output.

v2 (2026-10-10, supersedes v1): names are replaced by obviously bogus placeholders
instead of a [NAME-MASKED] tag, so reports and test forms still read naturally.

Fail-closed: when unsure, mask. Masks emails, phone-like numbers, long bare digit runs
(order/serial/account-like), @handles that carry digits and street-address lines.
Decimal fractions such as 0.70710678 and hex hashes are left alone.

Names (deterministic, no guessing at what "looks like" a name):
  * Only KNOWN names are replaced: the list passed in, or lib/known_names.txt.
  * One pass, longest name first, whole words, case-sensitive -> no cascades
    (a placeholder is never masked again).
  * Placeholders are handed out in order of first appearance in the text, so the same
    real name gets the same stand-in throughout one text: John Q. Public, Jane Doe,
    Richard Roe, Mary Major, then Person 5, Person 6, ...
  * The author's own name is not masked (v1 masked only the surname "Norman";
    Timothy said on 2026-10-10 that his work may carry his name).
Names in structured forms (e.g. CMS-1500 boxes 2 and 4) belong to field masking in the
form's own extractor, by position, not here.
"""
from __future__ import annotations
import os
import re

RULES = [
    ("EMAIL", re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)+")),
    ("PHONE", re.compile(r"(?<![\w.])(?:\+?1[\s.\-]?)?\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?![\w.])")),
    ("HANDLE", re.compile(r"(?<![\w@])@[A-Za-z][A-Za-z0-9_]*\d[A-Za-z0-9_]*")),
    ("ADDRESS", re.compile(r"\b\d{1,6}\s+(?:[A-Z][a-z]+\s+){1,3}(?:Street|St|Avenue|Ave|Road|Rd|Lane|Ln|Drive|Dr|Boulevard|Blvd|Court|Ct|Way|Highway|Hwy)\b\.?")),
    ("NUM", re.compile(r"(?<![\w.\-/])(?!\d{4}-\d{2}-\d{2}(?![\d\-]))\d[\d\-]{6,}\d(?![\w.])")),
]

PLACEHOLDERS = ("John Q. Public", "Jane Doe", "Richard Roe", "Mary Major")
NAMES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "known_names.txt")


def placeholder(i: int) -> str:
    """i counts from 0 in order of first appearance."""
    if i < len(PLACEHOLDERS):
        return PLACEHOLDERS[i]
    return "Person %d" % (i + 1)


def load_names(path: str = NAMES_FILE) -> list:
    """One name per line; blank lines and lines starting with # are skipped.
    Placeholders and names shorter than 2 characters are ignored (never masked)."""
    out = []
    try:
        with open(path, encoding="utf-8") as fh:
            for ln in fh:
                n = ln.strip()
                if n and not n.startswith("#") and len(n) >= 2 and n not in PLACEHOLDERS:
                    out.append(n)
    except OSError:
        pass
    return out


def _clean(names) -> list:
    seen, out = set(), []
    for n in names:
        n = n.strip()
        if len(n) >= 2 and n not in PLACEHOLDERS and n not in seen:
            seen.add(n)
            out.append(n)
    return out


def _name_rx(names, keep=()):
    """Alternation of names (and protected placeholders), longest first."""
    if not names:
        return None
    alts = sorted(set(names) | set(keep), key=lambda s: (-len(s), s))       # longest first
    return re.compile(r"(?<!\w)(?:" + "|".join(re.escape(n) for n in alts) + r")(?!\w)")


def mask(text: str, names=None):
    """-> (masked_text, counts{rule: n})."""
    counts = {}
    for tag, rx in RULES:
        text, n = rx.subn(f"[{tag}-MASKED]", text)
        if n:
            counts[tag] = n
    names = _clean(load_names() if names is None else names)
    rx = _name_rx(names, keep=PLACEHOLDERS)
    if rx is not None:
        given = {}
        hits = [0]

        def swap(m):
            real = m.group(0)
            if real in PLACEHOLDERS:
                return real                                  # protected: never masked again
            hits[0] += 1
            if real not in given:
                given[real] = placeholder(len(given))
            return given[real]

        text = rx.sub(swap, text)                            # one pass: no cascade
        if hits[0]:
            counts["NAME"] = hits[0]
    return text, counts


def residue(text: str, names=None) -> list:
    """Post-mask audit: any rule or known name still matching = list of tags (should be empty)."""
    tags = [tag for tag, rx in RULES if rx.search(text)]
    rx = _name_rx(_clean(load_names() if names is None else names), keep=PLACEHOLDERS)
    if rx is not None and any(m.group(0) not in PLACEHOLDERS for m in rx.finditer(text)):
        tags.append("NAME")
    return tags
