# SHELF HOLD lock 2026-09-28
Filtrate bench for new stack rungs. Not the live walker. Not iOS clipboard.

## Status
CANDIDATE → WALKED → APPROVED → INSTALLED
Only Timothy (sole author) may set APPROVED. A clean dry walk makes a row eligible. It does not install.

## Dry walk
A dry walk that leaves no record is not a walk.
Append a DRYWALK row (or fill walk_* on the candidate) holding:
- SHA-256 of the *stack copy* that was walked
- walker exit code (plain decimal text)
- HIT / VAL / miss

At install: re-hash the live stack. If it does not match walk_stack_sha256, the proof is stale. Walk again. Do not install.

## Hash
Always store sha256 and bytes as plain decimal text. Attach is optional. A row with no sha256 is not verifiable and stays CANDIDATE.

## Schema fields
id stamp name sha256 bytes attach want status refers walk_stack_sha256 walk_exit hit_val_miss approved_by open
want is BEGIN or END.
stamp is ISO local, no E-notation.
Do not delete rows. Supersede.

## Mirrors
The disk HOLD is the working copy for this chair.
GitHub and Notion hold mirrors of the rows, matched by id.
They never replace the disk copy.
A mirror miss does not change disk status.

H0000 is SCHEMA.
H0001 is CANDIDATE (shelf-walk-v0). Not installed.
