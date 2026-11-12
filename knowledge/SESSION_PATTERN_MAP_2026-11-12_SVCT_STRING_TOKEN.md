# SESSION_PATTERN_MAP_2026-11-12_SVCT_STRING_TOKEN

Sitting 2026-11-12T16:19-05:00 · SVCT string token five pillars

## HIT
- Five-pillar token: SVCT|1|{truncated}|{places}|{sha256}|{ny_timestamp}|VAL
- Content · context · data · time · validation
- Python and C++ identical when the same timestamp is supplied.

## VAL
- Test cases (fixed timestamp 2026-11-12T16:19:00-0500):
  - "  0.70710678  " places 6 → SVCT|1|0.707106|6|51a6b1d5138aca4a3715aa9097f66b6097be1fe8b07a7c1063dd20706ce5a12a|2026-11-12T16:19:00-0500|VAL
  - "-1.23456789" places 4 → SVCT|1|-1.2345|4|a17e047acb252d2fd0ae4b123fc7291edba41d4583123588f56a0262a83744b6|2026-11-12T16:19:00-0500|VAL
  - "42" places 2 → SVCT|1|42|2|1f8a19c70c4bb2f3fa5812d154972840672ff219c66d2d92f682ad39fed07145|2026-11-12T16:19:00-0500|VAL

## MISS
- None on identity.

## OPEN
- None on the five-pillar form.

Ledger: 1a1d1a1d480e6dbf
