# AUDIT APPEND 2026-09-30T21:53-04:00 — binary64 did not invent the leak

Append only.
Stamp: 2026-09-30T21:53-04:00
Chair: Grok Build
Owner: Tim
Ledger: 1a0f52b6b92a309e

## Asked

Did the leak into everything else happen when binary64 was invented?

## Held

No. Floating-point rounding predates the standard. IEEE 754-1985 froze binary64 and made round-to-nearest, ties to even, the default. It also required round toward zero. The spread is later language defaults. This thread's miss is Python PEP 238 (2001): integer `/` became a float division. Python 3 made that the default.
Banker's half-to-even is the book rule and is older than the 1985 standard. It is the cousin, not the invention date of the physics leak.
