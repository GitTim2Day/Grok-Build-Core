# SESSION_PATTERN_MAP_2026-11-12_SVCT_STRING_TOKEN

Sitting 2026-11-12T16:15-05:00 · SVCT string token sealed

## HIT
- Token format: SVCT|1|{truncated}|{places}|{sha256_hex(stripped + '|' + places)}
- Both Python and C++ emit identical tokens on the three test cases.
- Pure SHA-256 in C++ (no OpenSSL header dependency). Portable to Pi 5.

## VAL
- Python: svct_string_token.py
- C++: svct_string_token.cpp (self-contained)
- Test cases identical:
  - "  0.70710678  " places 6 → SVCT|1|0.707106|6|51a6b1d5138aca4a3715aa9097f66b6097be1fe8b07a7c1063dd20706ce5a12a
  - "-1.23456789" places 4 → SVCT|1|-1.2345|4|a17e047acb252d2fd0ae4b123fc7291edba41d4583123588f56a0262a83744b6
  - "42" places 2 → SVCT|1|42|2|1f8a19c70c4bb2f3fa5812d154972840672ff219c66d2d92f682ad39fed07145

## MISS
- None on identity.

## OPEN
- None on the token.

Ledger: 1a1d19eb073572b6
