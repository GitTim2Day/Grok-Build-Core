# Correction — MinRadius_Lp git copies were half-shelf; Drive bytes restored as new leaves

Stamp: 2026-10-08T20:30-04:00
Owner: Timothy. Seat: Claude, at Timothy's request ("Do both").
Scope: kbld/ MinRadius_Lp pair only. Append only. No sealed path overwritten.
Not in scope: the 2026-10-08T12:33 comparison-protocol freeze. That record is untouched.

## What was found (boot of HEAD 87fe209)

| File (git, sealed path) | Bytes | SHA-256 | Self-test |
| --- | --- | --- | --- |
| kbld/kbl_svct_stacks_MinRadius_Lp_2026-08-28.py | 29074 | f0e0fa2c718517985b6707e4488e69f966c31c861c1ee80adbca8a61bcd66b65 | FAIL, exit 1. NameError at T3: GOSUB_Error_Test_Mitigate_Retest_Loop not defined. Also undefined in file: MAGIC, _safe_float. 15 checks, header says 68/68. |
| kbld/kbld_gosub_primitives_MinRadius_Lp_2026-08-28.py | 21351 | 5330cc57e2f7e8279ac34d98a2c55052161ad84d42a2c7b918fff45eecb83e67 | Runs green, but 18 defs and 7 asserts. Not the sealed file. |

Drive mirrors (folder 1Q-MCJwaATYmV5rGDa1Ci_ALG589Tm5P4), pulled 2026-10-08:

| Drive | File ID | Bytes | SHA-256 | Self-test |
| --- | --- | --- | --- | --- |
| D2 stacks | 1UYbFOz0CdRp2z-K32PeXimHHNQYYET8k | 72694 | 6e91bbc17d4a7d06f81441632f8453d81a2c12a5fc7d831da8091f8e0e3d6600 | 75 passed, 0 failed, exit 0 |
| D3 primitives | 19rjEiTrwUh99GQ5INSE3SYrGM4x5mshK | 44851 | 6c57ae4a86e24e87f4d72455d4d89f6075f504093339f27b76eb9f6fb2f7c073 | ALL GREEN, 33 defs, 79 asserts, exit 0 |

Byte counts match CATALOG_2026-09-21 rows D2 and D3 ("hashes not compared" there; compared now).

## Diagnosis

Named pattern: half-shelf. The 2026-09-08 port ("Ported from Drive 2026-09-08") condensed the files instead of copying bytes. 154 of the 717 git lines in the stacks file do not appear in the Drive copy. The stacks port dropped the loop body its own self-test calls. The primitives port dropped 15 functions and most of the suite.

Label drift: the stacks header and kbld/README.md say 68/68. The Drive bytes run 75/75 (T51–T55 were added after the label). The count is 75. The 68 label is ASSERTED, not EARNED.

## Remedy (new leaves, exact Drive bytes)

- kbld/kbl_svct_stacks_MinRadius_Lp_2026-08-28_DRIVE_D2_restored_2026-10-08.py — SHA-256 6e91bbc1…6600, 72694 bytes, 75/75, exit 0.
- kbld/kbld_gosub_primitives_MinRadius_Lp_2026-08-28_DRIVE_D3_restored_2026-10-08.py — SHA-256 6c57ae4a…c073, 44851 bytes, ALL GREEN, exit 0.

Neither imports the other. Each runs standalone (python -I, alone in its folder).
The broken sealed paths stay where they are as the record of the miss.

## Open, for Timothy

1. Which is live: the restored leaves (proposed) or a re-seal under the original names. Not decided here.
2. Primitives self-test uses bare assert (79). Under python -O those checks vanish. The stacks file uses plain if, per its own header. Flag only; not changed.
3. One other file carries "Ported from Drive": kbld/kbld_sophisticated_hearing.py. Its Drive original has no row in CATALOG_2026-09-21, so it was not compared in this pass.
4. BASIC lanes (edge kit, TXT-RCRJ) not run on this host: bwbasic absent.
