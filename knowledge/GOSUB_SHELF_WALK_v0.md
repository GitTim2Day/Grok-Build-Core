# GOSUB_SHELF_WALK v0 — PROPOSAL
2026-09-28. One walker. Two tables. Confirm then +1.
Does not replace hop-skip-secretary-boot-2026-09-09. It is the machine that runs that order.

## Prefer

Sequential stack. Not a call tree.

- One GOSUB walks a numbered list.
- Each rung returns HIT, VAL, or MISS.
- HIT without VAL is not enough to advance (same as GOSUB_TO_NEXT).
- MISS stops. Later rungs do not run. The miss is named.
- Adding a shelf = append a row. Do not rewrite the walker.
- BOOT table and SAVE table share the walker. Different rows.

A nest of GOSUBs (mail calls Notion calls GitHub) breaks when you insert Drive. A stack does not.

## Walker (pseudocode)

```
100 REM GOSUB_SHELF_WALK
110 I = 1
120 IF I > N THEN STATUS$ = "OUTPUT_OK" : RETURN
130 NAME$ = RUNG(I)
140 GOSUB 1000                          : REM dispatch NAME$
150 IF HIT = 0 OR VAL = 0 THEN STATUS$ = "STOP" : MISS$ = NAME$ : RETURN
160 RECORD I, NAME$, HIT, VAL, ID$
170 I = I + 1
180 GOTO 120
```

Dispatch 1000 is a name table, not new logic: MAIL, NOTION, GITHUB, DRIVE, DISK, SECRETARY, SHEETS.
Unknown name = MISS. Do not invent a rung from a comment.

## SAVE stack (current lock)

| I | Name | HIT | VAL |
|---|---|---|---|
| 1 | MAIL | message_id exists | To Gmail AND CC Yahoo AND subject starts Grok-Build-Ledger AND label applied |
| 2 | NOTION | page id exists in Timothy Skills & KB | Skill name + hashes in body |
| 3 | GITHUB | commit sha on GitTim2Day/Grok-Build-Core main | path under knowledge/ ; do not treat compacted bytes as the local hash |
| 4 | DRIVE | file_id in Grok_Build_Archives_2026 | name matches |
| 5 | DISK | file exists this sitting | SHA-256 matches the recorded hash |

Sheets stay OFF unless named. Secretary PDF stays OFF unless named.

## BOOT stack (current lock)

| I | Name | HIT | VAL |
|---|---|---|---|
| 1 | NOTION_GATHER | collection listed | names only, not claimed loaded |
| 2 | BOOT_SET_LOAD | each of 1-8 fetched | body applied; GATHER ≠ LOAD |
| 3 | PLANT | closed-system-vascular-plant present | SHA-256 6db4037fe8797d99d4f124736a6a8149b116dc3e21cfddff62b12c441ef5eed6 |
| 4 | LEDGER_LAST | last Grok-Build-Ledger mail readable | if none, last SAVE failed — say so, do not skip |

BOOT ≠ SAVE. Do not run SAVE rungs because a sitting started.

## Add / do not break

To add a shelf: new row at the end, or a named insert with the number bumped in writing.
Do not delete a row. Archive it: STATUS$ = SUPERSEDED, keep the number.
Do not run two walkers in one pass.

## This sitting proof

SAVE 2026-09-28 reflex lock:
1 MAIL HIT/VAL 1a0ea2b60273f820
2 NOTION HIT/VAL 3e9c9bfe-3aff-81e8-bdfb-eeac225cd024 (late; catch-up)
3 GITHUB HIT 05fc1db7 — VAL miss on tests bytes (compacted copy)
4 DRIVE HIT/VAL 1WPqO5MZ… and 1S-T5BVd… (late; catch-up)
5 DISK HIT this sitting — sandbox may drop later; disk is cache

Walker would have STOPPED at 3 if VAL required byte-identical tests. That miss stays visible.
