# BASIC interpreter — sourced, vetted, built, and the cut rebuilt to Timothy's rules

Stamp: 2026-10-08T22:50-04:00
Owner: Timothy. Seat: Claude, at Timothy's request ("look for the source … check it doesn't contain any viruses … run it through the JCJ pipeline … fill in the gap").
Append only. No sealed path overwritten. Nothing installed system-wide; all builds ran in a scratch folder.

## What the interpreter is

Bywater BASIC (bwbasic) is an **interpreter written in C**, not an assembler. The repo's BASIC was written against **bwbasic 2.20 pl2** (recorded in `csvson/txt_rcrj/TXT_RCRJ_PIPELINE_2026-10-05.md`). 2.20 source was not reachable from this sandbox (SourceForge, Debian salsa and PyPI refused by the egress policy). GitHub was reachable.

## Sources looked at (all GPL; used as an external tool, no code copied into the project)

| Candidate | Where | Pin | Verdict |
| --- | --- | --- | --- |
| bwbasic 3.00 | github.com/yantrabuddhi/bwbasic3 | a062bd4 (single re-upload commit, 2015) | Clean, but **rejected**: any `IF` on a line numbered 1000 or above fails ("No line number"); also its own build line uses `-ansi`, which hides `rint()` so CINT and `\` come out wrong |
| **bwbasic 3.20b** | **github.com/kenmartin-unix/Bwbasic-3.20b** | commit 48ad357ea42ee15c7770e1ba9ed11238bfab2e78; tarball `bwbasic-3.20b.tar` SHA-256 b93b56e7931ceffdbc60ee1f8c8bae7f09a102504311babc057e323871c8a909 (4,597,760 bytes) | **Selected.** Maintained line (Fedora ships 3.20g from the same maintainers). Has `OPTION VERSION "BYWATER-2"` and `OPTION ROUND TRUNCATE` |
| PC-BASIC (GW-BASIC clone) | github.com/robhagemans/pcbasic | 6a3a035 | Clean. Used as the second interpreter, per the basic-portability-gate skill |

Upstream identity note: the FreeBSD port lists bwbasic-3.30.zip (521,810 bytes, SHA-256 09a6fcfc3bd88f0e8af1ce3a65324898849ad2f26de547850c1f994d255f9064). That zip could not be fetched here, so no GitHub copy is hash-proven against SourceForge. The 3.20b identity is the pinned commit + tarball hash above. Status: VALIDATED by inspection, not EARNED against upstream.

## Virus / bot / duplicate checks (3.20b; 3.00 and PC-BASIC got the same)

- Tarball: no symlinks, hardlinks, devices, absolute paths or `..` traversal. Extracted with no owner/permission carry-over.
- No executables except three small shell helpers (strip leading spaces, draw a terminal grid, desktop launcher), all read in full. `loadbwbasic` runs `sudo make install` — **not run**.
- C source: no sockets, no network calls, no `fork`/`exec`/`dlopen`/`ptrace`/`mmap`, no inline assembly, no encoded blobs. URLs only in comments (citations).
- Every `system()`, `remove()`, `rename()` sits behind a BASIC command a program must call: SHELL, FILES, KILL, NAME, RENUM. Nothing runs on its own. The Edge Canvas Kit screen (`lib/runner.py` BASIC_DENY) already refuses all of these, plus OPTION.
- No self-copy: no `argv[0]`, no `/proc/self`, no write to its own binary. Writes only go to files a BASIC program names, plus fixed `LPRINT OUT` / `DEBUG OUT`.
- Duplicates (3.00 tree): 651 byte-identical groups, every one a test-fixture pair (expected vs recorded output, empty diff files). None in code.
- **RCRJ guard** (`scripts/scan_source_tree_2026-10-08.py`, the repo's own `to_txt` + `rcrj`): 3.20b 22 files / 51,174 lines → **0 rejects**, 0 prompt_injection, 0 script. 3.00: 24 / 31,145 → 0 rejects. PC-BASIC: 111 / 32,626 → 0 rejects. Flag counts (sql_pattern, formula_lead, html_tag) were read by eye: C comments `/* */`, wrapped arithmetic lines, `i < a`, the maintainer's HTML help-page writer, Python tuple unpacking.
- Compile: `gcc -O2 -std=gnu89 -Wall`, 3 minor warnings, no implicit declarations. Sanitizer build (ASan/UBSan) on 3.00 flagged one zero-length `memcpy` from NULL (bwb_str.c:92), harmless in practice.

## Build (reproducible)

`scripts/build_bwbasic_3.20b_2026-10-08.sh <empty dir>` → pins the commit, checks the tar hash, guards the tar, builds with gnu89, smoke-tests. Fresh run reproduced binary SHA-256 55279264351cf63a476089cabeac4a1b1f4ab0ad1e9992c6a227e15c0d60c720 (gcc 13.3.0, Ubuntu 24.04, x86_64). Binary hash is compiler-dependent; the tar hash is the source identity. Binary not committed (text + source only).

## Results with 3.20b on PATH

| Lane | Before (no bwbasic) | 3.00 | 3.20b |
| --- | --- | --- | --- |
| hybrid-boot BOOT.bas | — | 0.70710678 | 0.70710678 |
| csvson/txt_rcrj selfcheck | could not run | 161/162 | **162/162 ALL PASS** |
| basic/*.bas (6 programs) | not run | conflict_nodes fails (line-1000 IF) | **all 6 pass** (conflict_nodes 20/20, rcrj_guard 27/27, descending_power 8647, …) |
| edge-canvas-kit selfcheck | 318 pass, 4 skip | 333 pass, 4 fail | 334 pass, 3 fail; with the new sweep leaf 335 pass, 2 fail |

The 2 remaining edge-kit fails are in the self-check's expected text, written for 2.20 output, not in the BASIC:
1. `basic_timeout` feeds `10 GOTO 10`; 3.20b refuses a one-line self-loop as a syntax error on purpose. A two-line loop (`10 GOTO 20 / 20 GOTO 10`) still runs to the timeout.
2. `sweep_crosscheck_basic_vs_python` looks for `PASS= 10 FAIL= 0` with one space; 3.20b prints a space after every number, so the line reads `PASS= 10  FAIL= 0`. Values agree with the Python twin.
Not changed. Timothy decides.

`csvson/readiness/csvson_manifest_read.bas` needs the `out/` manifest the readiness script writes first; fixture, not a bug.

## Dialect findings that matter to the canon

- **3.20b default rounds integer division**: `7 \ 2` = 4, `8 \ 3` = 3. 3.00 truncates (3, 2), as GW-BASIC does. `OPTION ROUND TRUNCATE` restores truncation. Only `knowledge/embed-8x6-2026-09-24/embed_8x6.bas` uses `\` (lines 1120, 1150); its output was byte-identical under 3.00, 3.20b default and 3.20b truncate (its sums are even), and it matches its Python twin (ALL_GREEN).
- PC-BASIC reads `D+00` DATA exponents; Bywater rejects them ("Bad DATA"). Portable form: write doubles as long literals (8+ significant digits); short ones used here (1, 2, 19.5) are exact in binary.
- `PI` is a built-in constant in Bywater; it cannot be a variable name.
- The kit screen refuses any `#`, so double suffixes cannot be used in the kit lane. Bywater numbers are double anyway; GW-BASIC/PC-BASIC need `#`.

## The cut, rebuilt to Timothy's rules (2026-10-08, his words in conversation)

Rules given: round positive units only; carry the sign as a direction (× −1 out, × −1 back); round before you reduce so the value stays near non-drift; convert both 0 and −0 to 0. Also: prefer GOSUB, one call per line, IF and GOSUB on separate lines.

Steps, as built in `basic/cut8_2026-10-08.bas` (+ `.cpp`, `_key.py`, `_answer_key.txt`):
1. `IF V = 0 THEN V = 0` (−0 and 0 → 0). 2. Sign as direction. 3. Reduce first: split the integer part (exact). 4. Round the fraction once at 10 places; carry into the integer if it reaches 1. 5. Cut to 8 places. 6. Digits by integer arithmetic into a preset string (MID$ splice), never STR$ on a big value. 7. No negative zero.
Limit LM = 99999: 15 reliable significant digits = 5 integer + 8 places + 2 guard. Above it: REFUSED. (12345678.87654321 sits under the float noise floor at 10 places: IEEE stores …2104, Microsoft binary format …2099, so the two interpreters disagreed until the limit refused it.)

Results: 19 cases (both zeros, carries, noise case, 3 refusals) identical across **Python key, C++ (ASan/UBSan), Bywater 3.20b, Bywater 3.00, PC-BASIC**. Name scan against 444 Bywater words: no reserved, no embedded keywords, no two-letter collisions. Mutants: 10 rule-breaks, all caught. The zero-normalise mutant survives on Bywater (its sign test and guard already cover −0) but is caught in C++, where `floor(-0.0)` keeps the sign and `printf` prints `-0.00000000` — the rule is needed.

Where this fixed a live failure: `edge-canvas-kit/basic/sweep.bas` cut its 8 places with `STR$(VF)`; Bywater 3.x prints big integers as `5.44206E+7`, so the text came out `19.5.44206E+7`. New leaf `edge-canvas-kit/basic/sweep_cut8_2026-10-08.bas` (original untouched) uses the new cut: 10/10 PASS, every value equals the Python twin, passes the kit screen.

## Open, for Timothy

1. Point the kit at `sweep_cut8_2026-10-08.bas` (or re-seal sweep.bas), and whether to update the two 2.20-specific expectations in `edge-canvas-kit/selfcheck.py`.
2. Whether the house BASIC default should carry `OPTION ROUND TRUNCATE` (a `profile.bas` in the run folder). The kit screen refuses OPTION inside a program.
3. 2.20 pl2 itself is still not in hand; fetch on the A15 or Pi 5 (Debian/Raspberry Pi OS: `apt source bwbasic`) and record its hash if a byte-exact match to the old box is wanted.

## Correction 2026-10-08T23:25-04:00 (appended; body above unchanged)

"JCJ pipeline" in the request was carried out with the repo's **TXT → RCRJ guard** (`csvson/txt_rcrj/to_txt.py` + `rcrj.py`, regex → CSV → regex → JSON). The JCJ pipeline proper (`building_databases_logically.py` / `curation_dispatch_bundle.py`) is **not in this repo** and was **not run**. No KBLD9 core ran either (RUN.md lists `kbld9_core_r4` ABSENT). Every scan result above is an RCRJ-guard result.
