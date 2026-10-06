"""mask.py -- personal-data masking (DM-5) for copies placed in knowledge/ and agent output.

Fail-closed: when unsure, mask. Masks emails, phone-like numbers, long bare digit runs
(order/serial/account-like), @handles that carry digits, street-address lines, and the
surname. Decimal fractions such as 0.70710678 and hex hashes are left alone.
"""
from __future__ import annotations
import re

RULES = [
    ("EMAIL", re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)+")),
    ("PHONE", re.compile(r"(?<![\w.])(?:\+?1[\s.\-]?)?\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?![\w.])")),
    ("HANDLE", re.compile(r"(?<![\w@])@[A-Za-z][A-Za-z0-9_]*\d[A-Za-z0-9_]*")),
    ("ADDRESS", re.compile(r"\b\d{1,6}\s+(?:[A-Z][a-z]+\s+){1,3}(?:Street|St|Avenue|Ave|Road|Rd|Lane|Ln|Drive|Dr|Boulevard|Blvd|Court|Ct|Way|Highway|Hwy)\b\.?")),
    ("NUM", re.compile(r"(?<![\w.\-/])(?!\d{4}-\d{2}-\d{2}(?![\d\-]))\d[\d\-]{6,}\d(?![\w.])")),
    ("NAME", re.compile(r"\bNorman\b")),
]


def mask(text: str):
    """-> (masked_text, counts{rule: n})."""
    counts = {}
    for tag, rx in RULES:
        text, n = rx.subn(f"[{tag}-MASKED]", text)
        if n:
            counts[tag] = n
    return text, counts


def residue(text: str) -> list:
    """Post-mask audit: any rule still matching = list of tags (should be empty)."""
    return [tag for tag, rx in RULES if rx.search(text)]
