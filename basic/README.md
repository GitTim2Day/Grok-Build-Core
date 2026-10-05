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

## Not published (sealed / fail-closed)
- Sealed `kbld-gosub-primitives` / MinRadius sealed bodies -- named in library-list; do not invent or unseal here.
- Share Catalog sealed set.

## Boot check
```
printf 'load "hybrid-boot/BOOT.bas"\nrun\nquit\n' | bwbasic
```
Required PRINT: `0.70710678`

## Lead filter
First character only; mid-line marks stay. Map `-`->`CHAR(45)`, `+`->`CHAR(43)`, `@`->`CHAR(64)`.
Restore uses remembered lead (`CH$` / returned `ch`). Fail-closed on mismatch.
```
python3 basic/lead_filter.py
bwbasic basic/lead_filter.bas  (stdin closed)
```
Required SUMMARY: `ALL PASS`
