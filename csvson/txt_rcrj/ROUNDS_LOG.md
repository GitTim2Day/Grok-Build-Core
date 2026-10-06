# TXT → RCRJ build — error-test / mitigate / re-test rounds (2026-10-06 ET)
Gate (Timothy via parent, 12:03 AM ET): nothing saved anywhere until error-tested, mitigated, re-tested, mitigated again (≥2 loops), ALL PASS and every mutant caught.

## Round 0 — exploratory build (≈12:02–12:06 AM ET)
- FOUND: PDF-OCR path called `pdftoppm … - -`; poppler treats the 2nd `-` as an output *root*, so it wrote a stray file `--1.png` into the cwd and returned nothing on stdout (scanned PDF OCR empty).
  FIX: one page per call with `-singlefile` and no output root → PNG on stdout, no files written. Stray file archived (not deleted) at `scratch_archive/stray_pdftoppm_root_dash_page1_20261006-0004.png`. Added harness test `no_stray_files_written` + mutant `pdftoppm_writes_cwd`.
- FOUND: bwbasic 2.20 cannot parse string comparisons inside parenthesised AND expressions (`ERROR in line 6035`); also has no UCASE$/UPPER$, and drops CHR$(0) from strings.
  FIX: string tests moved to single `IF … THEN S1 = 1` lines; own uppercase GOSUB 2900; NUL passed by reader as N0=1 (documented).
- FOUND: BASIC harness expected 28 records; actual 26. FIX: count corrected and tightened (REJ=2, FB=3, ROWS=21, RECS=26).
- Re-test: Python self-check 138/138 ALL PASS · BASIC 27/27 ALL PASS.

## Round 1 — full harness + mutants (≈12:07–12:20 AM ET)
- FOUND: first mutant run hung >10 min: 4–6 parallel self-checks each launching tesseract with default OpenMP threads → CPU oversubscription (12 s CPU per tiny OCR). Run aborted; partial trees archived at `mutants_txt/r1_aborted_ocr_oversubscription/`.
  FIX: tesseract subprocess env `OMP_THREAD_LIMIT=1`; harness caches default-limit conversions (OCR monkeypatch tests use fresh runs). Self-check 7.1 s → 3.0 s.
- Re-test: self-check 138/138 ALL PASS · mutants 39/39 caught (30 s).
- FOUND (from how two mutants were caught — by a crash, not a FAIL line):
  1. `sqlite_string_built` → `RuntimeError: sqlite_readback_mismatch` escaped `rcrj.run` and killed the main line.
  2. `csv_fit_always_fits` → `_csv.Error: field larger than field limit (131072)` escaped on CSV read-back and killed the main line.
  Both violate "conflicts never kill the main line".
  FIX (round 1 → 2): `Fallback.put` never raises (returns None, error kept in `fb.errors` / `meta.sqlite_errors`), caller logs `sqlite_write_failed` and continues; CSV read-back raises `csv.field_size_limit` to 4×MAX_RECORD and wraps the parse (`post_csv_parse_error` → rows go to SQLite via GUARD_POST); per-record try around GUARD_PRE.
- Added round-2 hostile cases: backslash zip-slip (`..\evil2.txt`, `sub\..\..\evil3.txt`), absolute tar member, JSON depth bomb (50 000 nested arrays), XXE external entity, HTML-only e-mail with script, UTF-32 BOM, RTF `\u` + hidden `{\*…}` group, exact MAX_FIELD boundary (4096 in CSV / 4097 to SQLite), member-count cap, OCR of an image reading `=SUM(A1:A9)` (formula flag + `'` prefix), malformed records, forced SQLite-node failure.
- FOUND: malformed records (`{"text": None}`, missing `kind`) → `KeyError: 'kind'` escaped `rcrj.run`.
  FIX: record normaliser + `bad_record` reject node; `kind` defaulted to `line`; `line_no` coerced.
- FOUND: RTF font-table text leak was not under test. FIX: test `door_rtf_fonttbl_skipped` (+ mutant `rtf_skip_off`).

## Round 2 — full harness + hostile + mutants (≈12:20–12:24 AM ET)
- Self-check 153/153 ALL PASS · BASIC 27/27 ALL PASS · mutants 47/48 caught (no crash-catches left: every catch is a FAIL line).
- FOUND: mutant `csv_field_limit_off` SURVIVED — the raised CSV field-size limit is defence-in-depth that no clean-run test exercised.
  FIX: test `r2_post_oversize_cell_isolated_not_whole_file` — a 200 000-char cell injected after write must send only that row to SQLite and keep the rest of the CSV.
- Re-test after fix: self-check 154/154 ALL PASS.

## Round 3 — clean re-run of everything (≈12:24–12:26 AM ET)
- Boot `bwbasic /workspace/hybrid-boot/BOOT.bas </dev/null` → `0.70710678`.
- Self-check run 3× back-to-back: 154/154, 154/154, 154/154 ALL PASS (OCR results stable).
- BASIC `rcrj_guard.bas`: 27/27 ALL PASS (SUMMARY line read; exit code not used).
- Mutants: 48/48 caught, ALL CAUGHT, every catch a FAIL line (no crash catches). Output `out/MUTANTS_TXT_RCRJ_r3.txt`.
- Nothing failed in round 3 → code frozen at this point for saving.

| Round | Self-check | BASIC | Mutants | What failed | Fix |
|---|---|---|---|---|---|
| 0 | 138/138 (after fixes) | 27/27 (after fixes) | — | pdftoppm stray file, bwbasic string-compare parse, BASIC count | -singlefile stdout; IF-split; count |
| 1 | 138/138 | 27/27 | 39/39 (2 by crash) | OCR oversubscription hang; 2 crash paths killed main line | OMP_THREAD_LIMIT=1 + cache; non-raising SQLite node + CSV read-back |
| 2 | 153/153 → 154/154 | 27/27 | 47/48 | malformed-record KeyError; `csv_field_limit_off` survived | record normaliser; oversize-cell isolation test |
| 3 | 154/154 ×3 | 27/27 | 48/48 | none | — (frozen) |

## Round 4 — fixes A + B ported back from the edge-canvas-kit vendored copy (2026-10-06 ≈3:28–3:39 PM ET)
- Boot `bwbasic /workspace/hybrid-boot/BOOT.bas </dev/null` → `0.70710678`, exit 0. Old files archived in `archive_pre_port_20261006/` (to_txt.py f2fb5b36…, rcrj.py 55619f57…, selfcheck.py, mutants.py, ROUNDS_LOG.md, SHA256SUMS.txt; plus selfcheck.r4a.py).
- **Fix A (rcrj.py):** `run()` built the context string with `rec.get(...)` before checking `isinstance(rec, dict)`, so `None` / a string / a number raised AttributeError and stopped the main line. The dict check now comes first → `bad_record` reject node → the run continues.
- **Fix B (to_txt.py):** without defusedxml the source set `DefusedXmlException = Exception` and `xml_parse` raised, so every XML (and Office XML) went to QUARANTINE. Now: any DTD/ENTITY declaration (UTF-8 or UTF-16) → QUARANTINE; XML without a DTD → stdlib ElementTree; the stdlib refusal (`XmlForbidden`) is caught as QUARANTINE too. Unchanged when defusedxml is present.
- New tests (8): `r4_non_dict_record_no_raise`, `r4_non_dict_records_to_bad_record`, `r4_main_line_continues_after_non_dict`, `r4_nodefused_probe_ran`, `r4_nodefused_xml_full`, `r4_nodefused_dtd_quarantine`, `r4_nodefused_broken_same_as_box` (child process with defusedxml blocked; own process group, 60 s), `r4_det_none_in_process_dtd_quarantine`.
- New mutants (4) + 3 patterns updated to the new code: `non_dict_guard_off`, `dtd_fallback_check_off`, `fallback_exception_wide`, `fallback_refusal_uncaught`. Mutants now run serially by default (`MUTANT_WORKERS`, default 1), each in its own process group, killed as a group.
- Runs (all under `safe_run.sh`: timeout + process cap + `KIT_SELFTEST_ACTIVE=1`): self-check **161/161 ×3** → mutants r4 **51/52** (`fallback_refusal_uncaught` survived: no test had DET=None while defusedxml is installed) → test `r4_det_none_in_process_dtd_quarantine` added → self-check **162/162 ×3** (BASIC guard 27/27 inside) → mutants r4b **52/52 ALL CAUGHT**; 0 leftover processes.

| Round | Self-check | BASIC | Mutants | What failed | Fix |
|---|---|---|---|---|---|
| 4 | 161/161 ×3 → 162/162 ×3 | 27/27 | 51/52 → 52/52 | `fallback_refusal_uncaught` survived | DET-None in-process test |
