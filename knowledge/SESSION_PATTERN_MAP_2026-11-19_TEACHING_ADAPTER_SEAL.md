# SESSION_PATTERN_MAP_2026-11-19_TEACHING_ADAPTER_SEAL.md
# America/New_York

**Stamp:** 2026-11-19T17:18-05:00  
**Process:** Teaching terminal path → successful run → seal

## Pattern Match

Terminal sequence observed:

1. `mkdir -p ~/work/Grok-Build-Core/python` — path created.
2. `nano ~/work/Grok-Build-Core/python/gosub_exponent_reciprocal.py` — file opened.
3. `python3 gosub_exponent_reciprocal.py` — wrong cwd, file not found.
4. `python3 ~/work/Grok-Build-Core/python/gosub_exponent_reciprocal.py` — SyntaxError (nano command pasted into file).
5. Second nano edit — content corrected.
6. Run succeeds:

```
0.70710678 -> 0.707106
-0.70710678 -> 1/0.707106
2 -> 2
-3 -> 1/3
1.23456789 -> 1.234567
```

## Map

Teaching process = exact path + exact content + exact result.

Misses visible:
- Relative path when cwd was ~.
- Nano command line pasted as first line of the .py file.

Correction held: full path, pure Python, contract output.

Contract verified on Pi 5:
- String truncate toward zero (6 places).
- Negative exponent → reciprocal of truncated positive magnitude.
- No float64.
- Identical posture for positive and negative.

## Audit

- Result matches sealed truncate-toward-zero + positive-chop-then-reciprocal.
- Teaching cost was the same discipline as the code: one exact sequence, no drift.
- No silent fitting. Misses stated as misses. Fix demonstrated before seal.

## Remap

Adapter sealed as Python twin of the GOSUB.
Ready for shelves.

**Pointer skill:** session-map-2026-11-19-teaching-adapter-seal
