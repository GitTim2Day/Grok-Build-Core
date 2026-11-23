# SESSION_PATTERN_MAP_2026-11-23_EMAIL_INGEST_COUNT_VERIFY

America/New_York 2026-11-23T13:27-05:00

## HIT
High-importance fix for email ingest process before re-enabling.
Save full original email alongside any summary.
Explicitly count every numbered or bulleted item.
Verify every item appears in the summary.
If counts do not match, flag the email (do not mark fully processed).

No bot. Ingest remains paused until gate is wired and Gmail path confirmed.

## VAL
Fail-closed. Full original preserved.

## MISS
Specific message that lost items 3 and 4 not re-opened in this sitting.

## OPEN
Wire the gate into the live ingest path only after Gmail is signed in for that path.

Append-only. America/New_York.
