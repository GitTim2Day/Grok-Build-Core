# SESSION_PATTERN_MAP_2026-11-19_CUT_AND_FIX

**Stamp:** 2026-11-19T20:47:00-05:00 America/New_York  
**Sitting:** cut-and-fix hardened adapters (Python + C++) for string truncation contract  
**HIT:** Character-only cut to places (default 6), leading-zero on blank/space integer side, no float64, identical results across languages.  
**VAL:** Full suite 0 fails both implementations (empty, spaces, signs, missing decimal, places=0, 0.70710678→0.707106).  
**miss:** none material on contract.  
**open:** wire into Pi 5 Python adapter and A15 C++ adapter; SVCT string token hold of original 45-place string.

## Contract locked
- Input: character string (from BW BASIC PRINT capture or equivalent).
- Output: cut to `places` fractional digits (pad with 0), leading 0 if whole part blank or space.
- Empty / pure spaces → "0".
- places ≤ 0 → integer side only (no trailing decimal).
- Pure character operations. No float64. Truncate toward zero on the digit string.
- Python and C++ produce identical results on the locked suite.

Pointer skill: session-map-2026-11-19-cut-and-fix
Sibling of session-map-2026-11-19-digit-by-digit-string-build and session-map-2026-11-12-truncate-toward-zero. Not a merge.

Full body with hardened code is in the ledger hop and local artifact. SHA-256 1ab7885a99d796f8467b2a877d03acee93a8b36deba871249530e47b43ff5227 size 3362.
