# SESSION_PATTERN_MAP_2026-11-12_TRUNCATE_TOWARD_ZERO

Sitting 2026-11-12T16:12-05:00 · truncate-toward-zero contract sealed

## HIT
- String-based truncate toward zero, no float64.
- Identical Python and C++ adapters.
- Error-test loop run to completion: 17 core + 10 edge cases, both adapters 27/27.
- Contract: strip whitespace, keep sign, truncate fractional digits at places, places < 0 leaves unchanged, scientific and multi-dot left as-is.

## VAL
- Python: truncate_toward_zero.py
- C++: truncate_toward_zero.cpp
- Both passed the same suite without mitigation required.

## MISS
- None on the contract.

## OPEN
- SVCT string token that stores the truncated value + provenance so both adapters read/write the same token.
- Places default remains 6 unless later named.

## FILES
- truncate_toward_zero.py
- truncate_toward_zero.cpp

## NOTES
- bwBASIC default PRINT rounds to ~6 significant digits. Truncation is external, string-based.
- Values saved as strings, deconcatenated on use.
- Identical results required across adapters.

Map SHA-256: dff2de26b5910303a1e6f214b6d92df539dd335e49fd6a9a88cc1682b492d2da
Python SHA-256: 43d18af788482251b9b3ca73ad8e83c3db740a11349af0b3380f64a6dabbfb51
C++ SHA-256: fa867d41ae8e56970b2c27e3ab1e6802ae439e2dc991a59b755102152c9e2be4
Ledger: 1a1d19b56761def5
