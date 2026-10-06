# BASIC / GOSUB pack (unsealed, earned)

Pushed 2026-10-05 so GitHub holds the present primitives and deduped BASIC logic/commands.

## Present here
| Path | Role |
|---|---|
| `../hybrid-boot/BOOT.bas` | Shared session-start firmware; PRINT must be `0.70710678` via bwbasic |
| `save_to_project.bas` (+ `.py` / `.cpp` lean twins) | Save-to-project GOSUB streamline 2026-09-17 |
| `SHORTCUTS_EARNED_2026-09-18.md` | Deduped BASIC/GOSUB commands and gates |
| `SESSION_GOSUB_STREAMLINE_2026-09-17.md` | Streamline procedure |
| `STREAMLINING_GOSUB_METHOD.md` | What streamlining is (geometry + BASIC->Python/C++) |
| `descending_power_final.bas` | Compact GOSUB: print-only-final descending power sample (locked 8647 case) |
| `lead_filter.bas` (+ `.py`) | First-char lead filter: `-`/`+`/`@` to CHAR(45/43/64); CH$ memory; self-check |
| `need_gosub_one_node.bas` | Main line keeps moving; IF NEED=0 skip else GOSUB 1000 one-conflict/one-node; self-check |
| `conflict_nodes.bas` (+ `.py`) | NEED dispatch: conflicts are callable nodes (detect, call, return); Bot is the one hard skip; self-check |

## Not published (sealed / fail-closed)
- Sealed `kbld-gosub-primitives` / MinRadius sealed bodies -- named in library-list; do not invent or unseal here.
- Share Catalog sealed set.

## Boot check
```
printf 'load "hybrid-boot/BOOT.bas"\nrun\nquit\n' | bwbasic
```
Required PRINT: `0.70710678`

## NEED one-node GOSUB
```
bwbasic basic/need_gosub_one_node.bas  (stdin closed)
```
Required: `NEED_GOSUB ALL PASS` (NEED=0 and NEED=1 paths).

## Lead filter
First character only; mid-line marks stay. Map `-`->`CHAR(45)`, `+`->`CHAR(43)`, `@`->`CHAR(64)`.
Restore uses remembered lead (`CH$` / returned `ch`). Fail-closed on mismatch.
```
python3 basic/lead_filter.py
bwbasic basic/lead_filter.bas  (stdin closed)
```
Required SUMMARY: `ALL PASS`

## Conflict nodes (2026-10-05)
Timothy correction: a conflict does not kill the main line. Detect, call, return.
| NEED | Node | Effect |
|---|---|---|
| 0 | none | main line continues, no GOSUB |
| 1 | not UTF-8 | `Q=1` quarantine flag; calls no other door |
| 2 | hex binary wrapper | `PARK=1`; parked, not installed |
| 3 | hop request | `HELD=1`, `HR$="HOP"`; no action until Timothy turns it on |
| 4 | mail request | `HELD=1`, `HR$="MAIL"`; no action until Timothy turns it on |
| 5 | BOT | hard skip: `BOTSKIP=1` unless Timothy set `BOTON=1`; no node ever sets `BOTON` |
| other | unknown | `UNK=1` (fail-closed flag); main line still continues |
```
bwbasic basic/conflict_nodes.bas </dev/null
python3 basic/conflict_nodes.py
```
Required SUMMARY: `ALL PASS`
