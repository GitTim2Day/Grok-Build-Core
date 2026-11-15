# SESSION PATTERN MAP 2026-11-14 GOSUB_BASIC_LIMIT

**Stamp:** 2026-11-14T20:40-05:00 America/New_York
**Status:** Sealed after pattern-match-map-audit-remap
**Pointer skill:** session-map-2026-11-14-gosub-basic-limit

## Pattern Match

Final GOSUB for BASIC source lines is validation and normalisation, not transformation. Prior crunch forms that joined lines or stripped spaces altered control flow (IF/REM targets, numbered GOSUB lines). The safe contract is GOSUB_BASIC_LIMIT: accept one terminator per item, reject embedded Unicode line-break characters, enforce length, optional ASCII-only, collect all failures, return (text, note). Input unchanged. Appendable.

## Map

- Function name: GOSUB_BASIC_LIMIT
- Exception: BasicLineError
- Contract: preserve content, LF join, length bound, separator rejection
- Use: final GOSUB before sealing existing .bas source; front of brain_control dispatch ID mapping to Python/C++
- Tests: all pass including prior gap characters (\x0b, \u2028, \x85, \v, \f, \u2029)

## Audit

Defects from earlier joining version closed. Stricter SEPARATORS set closes the splitlines gap. Fail-closed. Provenance note records check.

## Remap

Callable by agents and dispatch. Same ID sequence fed to BASIC (GOSUB targets), Python, and C++ for path comparison. Helpful for SVCT text forms, content, data, permanent memory storage: sealed form identical in meaning.

## Code

```python
class BasicLineError(ValueError):
    """One or more BASIC source lines failed validation."""

def GOSUB_BASIC_LIMIT(lines, max_len=255, ascii_only=False):
    """Validate BASIC source lines and return (text, note).
    Appendable. Accepts one CRLF, LF, or CR terminator per item.
    Joins with LF. Counts Unicode code points.
    Rejects any Unicode line-break characters inside the line body."""
    if isinstance(lines, (str, bytes)):
        raise TypeError("pass an iterable of lines")
    if type(max_len) is not int or max_len < 1:
        raise ValueError("max_len must be a positive integer")

    SEPARATORS = {
        "\n", "\r", "\v", "\f", "\x1c", "\x1d", "\x1e", "\x85",
        "\u2028", "\u2029"
    }

    out = []
    bad = []

    for n, raw in enumerate(lines, 1):
        if not isinstance(raw, str):
            raise TypeError(f"item {n}: expected str, got {type(raw).__name__}")

        if raw.endswith("\r\n"):
            line = raw[:-2]
        elif raw.endswith(("\r", "\n")):
            line = raw[:-1]
        else:
            line = raw

        if any(ch in SEPARATORS for ch in line):
            bad.append(f"item {n}: unexpected line separator")
        elif ascii_only and not line.isascii():
            bad.append(f"item {n}: non-ASCII")
        elif len(line) > max_len:
            bad.append(f"item {n}: {len(line)} > {max_len}")

        out.append(line)

    if bad:
        raise BasicLineError("\n".join(bad))

    return "\n".join(out), f"checked {len(out)} lines, limit {max_len}"
```

## Shelves

Email hop first (1a1dcdd714674b6a). Then Notion, GitHub, Drive, skills/memory.
