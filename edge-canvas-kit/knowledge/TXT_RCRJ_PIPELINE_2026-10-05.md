# CSVSON text door + RCRJ pipeline (regex → CSV → regex → JSON, SQLite fallback) — 2026-10-05/06

Timothy (11:58 PM ET, 2026-10-05): "Convert as many file types to .txt and let regex-csv-regex-json handle it, with insertion prevention added at the regex GOSUB subroutine before and after CSV; otherwise use another database like SQLite. Save everything everywhere."
Steers (from the parent agent): 12:01 AM ET, use the Tesseract OCR node for images and scanned PDFs. 12:03 AM ET, save nothing until it has passed at least two rounds of test, fix, and re-test with ALL PASS and every mutant caught.

Boot: `bwbasic /workspace/hybrid-boot/BOOT.bas </dev/null` printed `0.70710678` (checked before work and before each round). Work was done on the box only. Nothing was installed on his devices, Cursor cloud was not used, and nothing was deleted (scratch files were archived).

## Tools (box versions)
| Tool | Version | Use | Where |
|---|---|---|---|
| Python | 3.13.5 | everything | box |
| Pillow | 12.3.0 | image metadata, frames, pixel cap 50 MP | box (already installed) |
| defusedxml | 0.7.1 | XML parse; forbids entities, XXE, and DTD bombs | box (already installed) |
| Tesseract OCR | **5.5.0** (leptonica 1.84.1), languages `eng` + `osd` | OCR node: images and scanned PDFs | **box only, not on Timothy's devices** |
| pytesseract | absent | not used; the `tesseract` subprocess runs from an argument list, `shell=False`, `OMP_THREAD_LIMIT=1`, 60 s timeout | — |
| poppler pdftotext / pdftoppm | 25.03.0 | PDF text layer / page rasterising for OCR (stdin in, stdout out, writes no files) | box only |
| bwbasic | 2.20 pl 2 | BASIC guard skeleton | box |
| PyYAML, odfpy, striprtf, python-magic | absent | not installed; YAML stays plain text (structured parse UNDEF), ODT/ODS/RTF are parsed with the stdlib | — |

## Per-type conversion table (box, synthetic samples)
FULL means all human-readable text is captured. PARTIAL means metadata or a subset only. NOT means nothing is converted (parked, with sha256 and size only).
| Type | Result | What lands in .txt | What is lost / limits |
|---|---|---|---|
| TXT / LOG / INI / MD | FULL | the text (UTF-8; BOM UTF-8/16/32 and cp1252 detected; cp1252 flagged) | — |
| CSV / TSV | FULL | the text unchanged; each line becomes one RCRJ record | cells are not split (a line is the unit) |
| JSON | FULL | flattened `$.path = value` lines; strings with newlines become `%%BLOB` units; nesting beyond depth 8 becomes a `%%NEST` unit | invalid or depth-bomb JSON → PARTIAL (kept as plain text) |
| XML (and SVG) | FULL | `path = text` and `path@attr = value` via defusedxml | entity/XXE bombs → QUARANTINE |
| HTML | FULL | visible text plus alt/title; `<script>` and `<style>` dropped and counted | layout |
| YAML | FULL as text | the text | structured parse UNDEF (PyYAML not installed) |
| BASIC `.bas` / source code | FULL | the text | — |
| RTF | PARTIAL | text, `\par`, `\tab`, `\'hh`, `\uN`; font/colour/info/`{\*…}` groups skipped | tables, objects, formatting |
| DOCX | FULL | body paragraphs and tables, headers, footers, footnotes, endnotes, comments | images, formatting |
| XLSX | FULL | `Sheet!A1: value` (cached values), formula text `Sheet!B2 formula: =…` | dates appear as raw serial numbers; charts |
| PPTX | FULL | slide text and speaker notes | images, layout |
| ODT / ODS | FULL | paragraphs and headings / `Sheet!RrCc: text` (column repeats capped at 1024) | formulas, styles |
| PDF with a text layer | FULL | pdftotext `-layout` | images inside the PDF are not OCR'd when a text layer exists |
| PDF without a text layer | PARTIAL (OCR) | Tesseract OCR of up to 5 pages | OCR is machine-read and not proven; if OCR is empty or fails → metadata only |
| EML / MBOX | FULL | From/To/Cc/Date/Subject/Message-ID, text/plain bodies, text/html bodies (text extracted); attachments are converted recursively as child items | — |
| GIF / BMP / TIFF / PNG / JPEG | PARTIAL (meta + OCR) | format, size, mode, frames, info keys, EXIF tags, plus OCR text per frame (multi-page TIFF / animated GIF capped at 8 frames) | pixels themselves are not ingested; OCR empty or failed → metadata only |
| WAV | PARTIAL | channels, sample width, rate, frames, duration, compression | no speech-to-text |
| ZIP / TAR / GZIP / XZ / BZIP2 (`.tar.gz` too) | FULL (listing + recursion) | member listing; every member is converted as its own item | guard hits → REJECT per member (see guards) |
| Unknown binary (also DOC/XLS/PPT legacy, 7z, RAR, MP3, video, WebP, HEIC) | NOT, PARKED (node 2) | nothing; magic hex, sha256, and size are recorded | hex wrapper stays parked |

Run on the box: 73 top-level samples (41 normal + 32 hostile) gave 102 items including archive and e-mail children: FULL 66, PARTIAL 15, REJECT 11, QUARANTINE 5, FAILED 4, PARKED 1 (`out/TO_TXT_ITEMS.csv`).

## Conflict nodes (detect → one node → RETURN; the main line never stops)
node 1 QUARANTINE (not UTF-8 or a listed encoding, mixed encodings, NUL in a text type, UTF-16 without BOM, XML entity/XXE) · node 2 PARKED (unknown binary, encrypted zip member, missing tool) · node 6 REJECT (archive guards) · node 7 FAILED (corrupt or truncated input, pixel bomb) · node 8 OCR_EMPTY (OCR empty, failed, or unavailable → metadata only). The Bot lock (conflict_nodes.bas node 5) is untouched.

## Guard list
**Door guards (to_txt.py):** top-level input cap 64 MiB · per-member/stream cap 8 MiB (streamed, so a lying header cannot get past it) · total decompressed cap 32 MiB per file · declared zip ratio cap 200:1 for members over 1 MiB · nesting depth 4 · 2000 members · path traversal (`..` with `/` or `\`), absolute paths, drive letters, NUL in names → REJECT · tar symlinks, hardlinks, devices, FIFOs → REJECT · nothing is ever extracted to disk · defusedxml for every XML/OOXML/ODF part · Pillow pixel cap 50 MP (pixel bomb → FAILED) · OCR pixel cap 25 MP, frame cap 8, PDF page cap 5 · subprocesses run from argument lists, no shell · source lines that start with `%%` are escaped as `%%ESC`, so file content cannot forge BLOB/NEST markers.

**GOSUB 2000 REGEX_GUARD_PRE (before CSV):**
- NUL → REJECT.
- Over 1 MiB → REJECT (`oversize_hard`).
- C0/C1 control characters, DEL, zero-width characters, bidi overrides (U+202A–202E, U+2066–2069), BOM → stripped and flagged.
- `formula_lead` (= + - @ TAB CR, also after leading spaces) → neutralised with a `'` prefix at CSV time.
- `formula_embedded` (DDE / `=HYPERLINK(` after a delimiter) → flagged.
- `sql_pattern` (`'; --`, `; DROP/DELETE/INSERT/UPDATE/ALTER/CREATE/TRUNCATE/EXEC/ATTACH/PRAGMA`, `UNION SELECT`, `OR 1=1`, `xp_cmdshell`, `/* */`, `SLEEP(n)`, `WAITFOR DELAY`, `DROP TABLE`) → flagged and kept as data.
- `prompt_injection` (ignore/disregard previous instructions, "you are now", "system prompt", `<|im_start|>`, `[INST]`, `### instruction`, BEGIN SYSTEM, developer mode, jailbreak, DAN) → flagged. Nothing is ever executed.
- `html_tag` / `script` (`<script`, `<iframe`, `<img`, `javascript:`, `onX=`, …) → flagged.
- `quote_unbalanced` / `delimiter_or_quote_present` → flagged; QUOTE_ALL handles them.
- `overlong` (over 4096 chars) → SQLite.

**CSV:** the csv module with `QUOTE_ALL`, and every cell made formula-safe (`'` prefix when the cell leads with = + - @ TAB CR, or with `'` itself, so the prefix strips back without ambiguity).

**GOSUB 3000 REGEX_GUARD_POST (after CSV):** a physical-line regex checks the shape (8 quoted fields) · the csv-module parse must match the row count · each cell must equal `csv_safe(expected)` and strip back to the original (round-trip equality) · no live formula cell · no NUL or control characters · length check. Any mismatch sends that one row to SQLite (`guard_post_mismatch:*`) and the rest of the CSV stays. A CSV parse failure cannot kill the run.

**GOSUB 5000 SQLITE_FALLBACK:** multiline blobs, nested structure, oversize fields, and post-guard mismatches go here. The sqlite3 stdlib uses fixed DDL/INSERT/SELECT constants and `?` parameters only (a static test proves there is no string-built SQL). Every insert is read back and checked by sha256. If the SQLite node fails, the failure is logged (`sqlite_write_failed`) and the main line continues.

**JSON:** the JCJ Pipeline Core wrapper `{'data': rows, 'meta': {'source': 'csvson', 'ts', 'node', …}}`. The reject log entries use exactly `{'ts','reason','text','category','context'}` (`meta.reject_log`). The output is `ensure_ascii`, and a JSON round-trip check is applied.

Run on the box (all 102 items): 318 records → 310 CSV rows, 6 SQLite rows (the JSON multiline string, JSON nesting deeper than 8, the XLSX multiline cell, the 200 000-char line, the JSON depth-bomb line, the 4097-char line), 2 rejected (direct NUL record, 1.2 M-char line), 0 held errors, 30 flags kept as data.

## Test, fix, re-test rounds (details in `ROUNDS_LOG.md`)
| Round | Self-check | BASIC | Mutants | What failed | Fix |
|---|---|---|---|---|---|
| 0 | 138/138 after fixes | 27/27 after fixes | — | pdftoppm wrote a stray `--1.png` into the cwd; bwbasic string-compare parse error; BASIC count | `-singlefile` to stdout (stray file archived); IF lines split; count fixed |
| 1 | 138/138 | 27/27 | 39/39 (2 caught only by a crash) | OCR thread oversubscription hung the mutant run; SQLite read-back and CSV field-limit errors escaped and killed the main line | `OMP_THREAD_LIMIT=1` + harness cache; SQLite node and CSV read-back made non-raising |
| 2 | 153 → 154/154 | 27/27 | 47/48 | malformed records → KeyError; mutant `csv_field_limit_off` survived | record normaliser + `bad_record` node; oversize-cell isolation test |
| 3 | 154/154 ×3 | 27/27 | **48/48 ALL CAUGHT** | none | frozen and saved |

Mutants cover formula prefix/detect/embedded, SQL, NUL, control, prompt, HTML, the post guard, string-built SQL, CSV fit, MAX_RECORD, QUOTE_MINIMAL, reject-log field names, the wrapper source, ESC marker escape/unescape, traversal (`/` and `\`), absolute paths, stream/ratio/total/depth/member caps, tar links, defusedxml swapped for unsafe ET, XXE allowed, mixed encoding, UTF-16 BOM, NUL quarantine, OCR frame cap, OCR node off, OCR failure crash, PDF OCR fallback, pdftoppm writing to the cwd, pixel cap, RTF skip, HTML script skip, JSON nest, SQLite-failure raise, CSV field limit, bad-record guard, and five BASIC mutants (prefix, SQL, post, NUL, control).

## BASIC guard GOSUB skeleton (`rcrj_guard.bas`, 27/27)
```basic
1000 REM ========== MAIN LINE: one record ==========
1010 GOSUB 2000
1020 IF V = 1 THEN GOSUB 4000: RETURN
1030 GOSUB 2700
1040 IF FIT = 0 THEN GOSUB 5000: RETURN
1050 GOSUB 2500
1060 GOSUB 3000
1070 IF M = 1 THEN GOSUB 5000: RETURN
1080 R = 0: ROWS = ROWS + 1: RETURN
2000 REM REGEX_GUARD_PRE: N0 NUL to reject; LEN over MAXR to reject; strip control (F3)
2155 IF A = 61 OR A = 43 OR A = 45 OR A = 64 OR A = 9 OR A = 13 THEN F1 = 1
2160 IF INSTR(U$, "DROP TABLE") OR INSTR(U$, "UNION SELECT") OR INSTR(U$, "OR 1=1") THEN F2 = 1
2170 IF INSTR(U$, "IGNORE PREVIOUS INSTRUCTIONS") OR INSTR(U$, "IGNORE ALL PREVIOUS INSTRUCTIONS") THEN F4 = 1
2180 IF INSTR(U$, LT$ + "SCRIPT") OR INSTR(U$, LT$ + "IFRAME") OR INSTR(U$, LT$ + "IMG") THEN F5 = 1
2190 D = LEN(C$) - MAXF: IF SGN(D) = 1 THEN F6 = 1
2500 REM CSV cell: "'" prefix if F1 or lead "'"; double quotes; wrap in quotes (QUOTE_ALL)
2700 REM CSV fit: blob (K=1), embedded CHR$(10), or F6 to FIT = 0 (SQLite)
3000 REM REGEX_GUARD_POST: quoted shape; no lone quote; no live formula; strip one "'"; X$ = C$ else M = 1
4000 R = 2: REJ = REJ + 1: RETURN
5000 R = 1: FB = FB + 1: RETURN
```
bwbasic notes: it drops CHR$(0) from strings (the reader passes NUL as `N0=1`); it has no UCASE$ (own GOSUB 2900); string comparisons go on single IF lines; comparisons use SGN, with no angle brackets; the run is judged by the SUMMARY line.

## Gaps / parked
- "Use" (devices or the world) is still untested. Everything ran on the box with synthetic samples only; none of Timothy's real files were run.
- OCR text is machine-read and unproven (good on clean synthetic text; real scans may be worse). Tesseract is box only, so OCR on his devices is UNDEF.
- Not converted (PARKED): legacy DOC/XLS/PPT, 7z, RAR, MP3/M4A, video, WebP/HEIC. LibreOffice is on the box but was deliberately not wired in.
- YAML is not parsed structurally (PyYAML absent). XLSX dates appear as serial numbers. RTF uses a simple strip.
- An encrypted zip member → PARKED (code path exists, but there is no test sample: the stdlib cannot write encrypted zips).
- SVG `<script>` content becomes text under a `/svg/script` path. It is never executed, but it is not flagged as `script`, because the tags are already gone by the guard stage.
- Malware scanning: none (no AV engine on the box). The guards are structural only.
- The per-record CSV column set (rid, source, src_sha256, type, line_no, kind, flags, text) is an ASSUMPTION. His notes don't define the columns.
- The earlier other-sitting round-trips are still not on the box.

## Files (box) — `/workspace/csvson-ingest-2026-10-05/txt_rcrj/`
`to_txt.py` · `rcrj.py` · `rcrj_guard.bas` · `selfcheck.py` · `mutants.py` · `make_samples.py` · `ROUNDS_LOG.md` · `samples/` (41) · `samples_hostile/` (32) · `out/` (txt/, TO_TXT_ITEMS.csv, CSVSON_RCRJ.csv/.json/_fallback.sqlite, SELFCHECK_TXT_RCRJ.txt, BASIC_RCRJ_GUARD_2026-10-06.txt, MUTANTS_TXT_RCRJ_r1/r2/r3.txt) · `mutants_txt/` (all mutant trees kept) · `scratch_archive/`. The sha256 values are in `SHA256SUMS.txt` next to the code.
Run: `python3 make_samples.py && python3 selfcheck.py && python3 mutants.py rN && bwbasic rcrj_guard.bas </dev/null`
