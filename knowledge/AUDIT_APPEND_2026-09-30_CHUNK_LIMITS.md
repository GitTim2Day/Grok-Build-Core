# AUDIT APPEND 2026-09-30T23:01-04:00 — chunk-based comprehensive limits

Append only. Prior zero-billions row not deleted.
Stamp: 2026-09-30T23:01-04:00
Chair: Grok Build
Owner: Tim
Prior ledger: 1a0f52f7d3771a83
Speech line: "Chuck" read as chunk.
File SHA-256 35eb77b2f3984c23734eae455c4d18e99c38d94ec25a927c04f5c6ce511b6c1a size 2073.

## Asked

Send the chunk-based comprehensive limits. Save to the project.

## Held

A chunk is still a sample. Count of chunks that prove umpire agreement: zero.
Chunking can keep a digit group inside the exact-integer store. It does not sign the umpire.

## Limits (computed this sitting)

Binary64 exact integer gate: every integer n with |n| <= 2^53 is stored exactly.
2^53 = 9007199254740992. 2^53 - 1 = 9007199254740991.
2^53 + 1 is not an exact binary64 integer.

Decimal chunk width:
- 15 digits: every 15-digit integer is <= 999999999999999 = 10^15 - 1 < 2^53. Exact. HIT.
- 16 digits: 9999999999999999 = 10^16 - 1 > 2^53. Not exact. HIT.
- 10^15 = 1000000000000000 < 2^53. 10^16 = 10000000000000000 > 2^53.

Signed chunk bound for a float store: -9007199254740992 .. 9007199254740992.
Practical decimal chunk: 15 digits, sign carried beside the chunk, not inside a 16th digit.

Unit in the last place on the sealed miss binade:
89875517873681764 sits in [2^56, 2^57). ulp = 2^(56-52) = 16.
float(89875517873681764) = 89875517873681760. Delta = 4. Re-run this sitting. VAL of the prior counterexample.

## What a legal chunk is

- Width <= 15 decimal digits, or |chunk| <= 9007199254740992.
- Boundary and width stored with the chunk (provenance). Reconstruction is concatenation of the digit groups, not a sum of floats.
- Truncation toward zero still governs any division. Chunking is not a round.
- Python int is unbounded. This limit is the binary64 / float store, not the integer type.

## What a chunk is not

- Not a proof count. Billions of legal chunks remain a sample. Agreement stays outside the sample.
- Not a repair of the sealed miss. 17-digit 89875517873681764 is outside the 15-digit gate.
- Not a rewrite of model weights.
