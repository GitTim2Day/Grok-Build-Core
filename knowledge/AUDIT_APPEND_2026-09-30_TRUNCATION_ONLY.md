# AUDIT APPEND 2026-09-30T21:46-04:00 — truncation only, no round

Append only. Float path stays banned.
Stamp: 2026-09-30T21:46-04:00
Chair: Grok Build
Owner: Tim
Ledger: 1a0f5249e433ee8e

## Correction

The earlier miss was round-to-nearest on a binary64 cast. That is the probability method, even with no draw. Truncation toward zero would have left the integer where it was.

Rule now: no float on a lattice value. Division toward zero. Display is a decimal digit string or hex. Parse back must equal the integer. A hand-copied expected hex is not a check.

## Runs

First truncation file had three bad expected strings I typed: length hex, area hex, volume digits. Area digits 89875517873681764 held. Those three fails were assertion drift, not a new lattice miss. SHA-256 4e2ad004c8345cc90650742378847da21c0bd042535b35e85647e293456dfa03. Kept.

Hardened file SHA-256 c12e7f33321c8ff8f2cbe83ce9057654f6f25de37c49c5da6f2c26f27b8f07e9.
Two identical runs. 21 pass, 0 fail. SHA-256 2b32e55b1d3edad9a71719a63cf10133e8e2347a0bbd6ac1b9cad53fb48f9662. ALL_GREEN.
Area digits 89875517873681764. Area hex 13f4d4eacdd7564. Both round-trip.
Negative division truncates toward zero: -7/4 -> -1, not floor -2.
Octave bounds use integer powers of two, no log.

## Standing

Probability methods are not used for these identities. Readings from the prior row are still not promoted.
Answer key still open.
