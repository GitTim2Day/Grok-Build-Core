# CSVSON ingest readiness — box-only test (2026-10-05, ~11:51 PM–12:00 AM ET)

Timothy asked: "Are all of these file types ready for CSVSON ingestion and use: public GIF / BMP / TIFF / XML / HTML / zip / gzip / xz / bzip2 / tar round-trips?"
Boot: `bwbasic /workspace/hybrid-boot/BOOT.bas </dev/null` printed `0.70710678` and exited 0. All work stayed on the box. Nothing was published, nothing was installed on his devices, and Cursor cloud was not used.

**Short answer: not all of them, and not for "use" yet.** On this box, each of the 10 types round-trips without loss and produces a CSVSON-style ingest record. XML, HTML, and the five archive/compression types pass at the level tested here. GIF, BMP, and TIFF are **partial**: the box records only their metadata and sha256, and their pixel content stays parked (node 2). Three things are still undefined or untested: the per-file record columns (the record does not define them), the step to "devices or the world," and protection against hostile input. The round-trips from the other sitting are **not on this box** and were not re-verified. Everything here comes from synthetic samples generated tonight.

## 1. What CSVSON means in the record (quoted)

| Source | Exact words |
|---|---|
| Drive `[DRIVE-ID-MASKED]` SESSION_PATTERN_MAP_2026-09-24_ROOTS_CSVSON.md (sha256 `e46bc54b…38bf9`; GitHub Grok-Build-Core commit `dafe03c`, `knowledge/`; Gmail `1a0d4352570fc3da`, same sha) | "JCJ was the proof: one thing at a time, so the place was not lost. JSON, regex, CSV or SQLite, regex, JSON." / "CSVSON is the goal. Short form: file type (MP3, PNG, WAV, TXT, and the rest) → that type's filter (regex or whatever it needs) → CSVSON → devices or the world. CSVSON joins the cortex nodes: motor, hearing, sight, smell." / "JCJ kept the place by doing one file. CSVSON is the join across file types and across cortex nodes. They are not the same organ." |
| Notion session-map-2026-09-24-roots-csvson (3e5c9bfe…0f55) | "JCJ is the one-file proof. CSVSON is the goal: file type, then its filter, then CSVSON, then a device or the world." Solvent: "The liquid is the error log… Filter that log. What is useful comes back… Nothing is dropped as gone." |
| Gmail `1a091fad0dd900f6` (2026-09-11 ENDPOINT) | "Complete = each type → door → filter → JCJ/CSVSON → GOSUB RETURN." |
| Notion on-demand-boot-2026-09-15 (highlight) | "…uses its own filter, then becomes CSV or SQLite. The C to J side can still use regex." / "JSON, then regex, then CSV or SQLite, then regex, then JSON." |
| Notion boot-ask-open-shelf-2026-09-24 (highlight) | "CSV is the status core for this unite. SQLite is the other legal middle in JCJ, for a database feed." |
| Gmail `1987233d26ba1cdb` (2025-08-03) | "CSVSON model for JSON-to-CSV/CSV-to-JSON regex filtering" / "CSVSON Model : Cleans data via regex (…), converts JSON-to-CSV and CSV-to-JSON, logs errors in amendable CSVs". The pseudocode body is cut off at "IMPORT json," in this mail. The regex as printed there looks garbled, so it was **not** applied here. |
| Gmail `1995f09415d8702c` (2025-09-18 Evolved J-C-J brief) | "supports CSVSON's hybrid CSV-JSON format" / "media_parser_hook: Parses text/image/audio, supports CSVSON (csvson: {"raw": input, "format": "csv_json_hybrid"})" / "CSVSON Integration: Processes RAW data to JSON, applies PHs, outputs to CSV/SQLite" (address/contact lines not reprinted) |
| Drive `[DRIVE-ID-MASKED]` EE3F43B4.pdf "JCJ Pipeline Core: JSON → CSV → JSON with Hooks & Placeholders" | "# PH1: Pre-CSV regex reject (bot filter)" / "# Hook: CSVSON parser – CSV → structured node tree → JSON" returning `{'data': df.to_dicts(), 'meta': {'source': 'csvson', 'ts': time.time(), 'node': node_id}}`. Reject log entries carry `'ts','reason','text','category','context'`. |
| Box `ev2_extract/Document (15) J-C-J.txt` (Gmail `1996286a4d01341b` attachment) | "…via a J-C-J/CSVSON pipeline…" / "Integrate CSVSON outputs with DESI/Euclid 2026 data…" (no ingest schema) |

**Searched for, not found:** the exact strings "CSV-REGEX-JSON" and "CSV REGEX JSON" turned up nowhere. I checked the box (rg), Gmail (the only phrase hit was the roots mail, through separate words), Drive fullText, Notion search, and GitHub code search. GitHub code search came back empty for "CSVSON" and "JCJ" in GitTim2Day, and it flagged its own results as incomplete (`incomplete_results: true`). The repo tree listing was cut off in the response, so GitHub coverage is the confirmed commit `dafe03c` only.

**Ingest record shape:** **PARTIAL.**
- **Defined in the record:** the envelope `{'data': [...], 'meta': {'source': 'csvson', 'ts', 'node'}}`, the per-input tag `csvson: {"raw", "format": "csv_json_hybrid"}`, and the reject-log fields `ts/reason/text/category/context`.
- **UNDEF:** the per-file column set for GIF/BMP/TIFF/XML/HTML/zip/gzip/xz/bzip2/tar. The columns used here are an **ASSUMPTION**, built from the literal reading: name, type, parent, magic_hex, magic_ok, size, sha256, utf8, door, nodes, q, park, unk, filter, roundtrip, roundtrip_sha_equal, status.
- **Order used** (per Timothy's 2026-10-05 steer): **CSV → regex extraction → JSON**, wrapped in the PDF's hook_csvson envelope. The "raw" field holds the file name only. Binary bytes are never carried, because the hex wrapper stays parked.

## 2. Per-type readiness (box, synthetic samples)

| Type | Samples | Type filter | Round-trip check (sha256 equal) | Ingest | Verdict |
|---|---|---|---|---|---|
| XML | sample.xml (+ copies inside zip, tar, tar.gz, and the gz/xz/bz2 payloads) | xml.etree | parse → serialize → reparse, C14N 2.0 sha equal; raw copy byte-identical | INGESTED_TEXT (text door, UTF-8 valid, 0 nodes) | **READY (box)**. A Latin-1 XML goes to QUARANTINE (node 1) and the run keeps going. |
| HTML | sample.html | html.parser | token rebuild is byte-identical; raw copy identical | INGESTED_TEXT | **READY (box)**. End tags are rebuilt lowercase, so real-world uppercase HTML may not rebuild byte-for-byte. |
| GIF | sample.gif (1 frame), sample_animated.gif (3 frames) | Pillow 12.3.0 | pixel decode → re-encode → decode, pixel sha equal, all frames; raw copy identical. Re-encoded bytes are **not** identical, because the palette is re-quantized. | INGESTED_META_SHA (Q=1 at text door, PARK=1) | **PARTIAL**: metadata + sha + dims/frames only; pixel content parked (node 2) |
| BMP | sample.bmp | Pillow | pixel sha equal; re-encode byte-identical; raw copy identical | INGESTED_META_SHA | **PARTIAL** (same reason as GIF) |
| TIFF | sample.tif (raw), sample_lzw.tif (LZW), sample_multipage.tif (3 pages) | Pillow (libtiff present) | pixel sha equal on all pages; raw copy identical | INGESTED_META_SHA | **PARTIAL**: multi-page and LZW covered; other compressions, 16-bit, and CMYK not covered |
| zip | sample.zip (xml, html, gif) | zipfile | members read → rewrite → read, member sha equal; testzip clean; archive bytes reproducible | INGESTED_META_SHA + 3 member records | **READY (box)**. No zip-bomb or path-traversal guard yet. |
| tar | sample.tar (xml, html, bmp) | tarfile | member sha equal; archive bytes reproducible | INGESTED_META_SHA + 3 member records | **READY (box)**. No path-traversal or link guard yet (extraction stays in memory). |
| gzip | sample.txt.gz, sample.tar.gz (nested gzip → tar → 3 members) | gzip | payload sha equal; payload re-ingested (XML → INGESTED_TEXT; tar → its 3 members) | INGESTED_META_SHA | **READY (box)**. No decompression-size cap yet. A truncated .gz gives ROUNDTRIP_FAIL and the run keeps going. |
| xz | sample.txt.xz | lzma | payload sha equal; payload re-ingested as XML | INGESTED_META_SHA | **READY (box)**. No size cap. |
| bzip2 | sample.txt.bz2 | bz2 | payload sha equal; payload re-ingested as XML | INGESTED_META_SHA | **READY (box)**. No size cap. |

Conflict handling follows `conflict_nodes.py` (sha `64b186c2…00ad8a`): detect the conflict, call one node, return to the main line.
- **Text door meets non-UTF-8:** node 1 sets the QUARANTINE flag (Q=1) and calls no other door.
- **Binary types:** node 1 (text door refused) plus node 2 (hex wrapper PARK=1). They ingest as metadata + sha256 only.
- **Unknown type:** sets the UNK flag.
- **Bot:** never enabled; this is checked on every State used.
- **Errors:** go to an appendable `CSVSON_ERROR_LOG.csv` (the "liquid").

## 3. Results

- `csvson_ingest_readiness.py` self-check: **102/102 PASS**. Mutation test: **11/11** caught (HTML comment drop, no PARK node, lossy TIFF, XML element drop, gzip tamper, tar member drop, Latin-1 not quarantined, unknown not flagged, Bot auto-on, stream payload not re-ingested, zip member tamper).
- `csvson_crj.py` (CSV → regex → JSON): **12/12 PASS**. The regex extraction agrees with Python's csv module cell for cell. Tampered sha, status, row shape, and header are each rejected and logged with the PDF's reject fields, and the rest of the run continues. Mutants: **4/4** caught.
- `csvson_manifest_read.bas` (bwbasic reads the CSV manifest and counts the status column): **BASIC_READ PASS**. It found 30 rows: META_SHA 16, TEXT 11, QUAR 1, UNK 1, FAIL 1, OTHER 0. This matches Python's count. The longest row is 253 characters, close to bwbasic's string limit. A truncated row would land in OTHER and fail closed.
- Totals: 30 records, the same set in both CSV and JSON: 17 top-level files (14 samples plus 3 negative controls) and 13 child records (zip 3, tar 3, gz/xz/bz2 payloads 3, tar.gz payload 1 plus its 3 members). Status counts: INGESTED_META_SHA 16, INGESTED_TEXT 11, QUARANTINE 1 (neg_latin1.xml), UNK_FLAGGED 1 (neg_unknown.bin), ROUNDTRIP_FAIL 1 (neg_truncated.gz). The last three are intentional negative controls.
- First run: 87/91. Cause: a self-check keying bug in which child records shadowed the top-level samples. It was fixed, and run 1 and run 2 outputs were archived to `out/archive/`, not deleted.

## 4. Gaps (fail-closed)

1. **The other sitting's round-trips are not on this box.** Not re-verified. Nothing here proves those files.
2. **The per-file ingest columns are UNDEF in the record.** The columns here are an assumption, inside the record's envelope.
3. **"Use" is untested.** That is the "→ devices or the world" step: Pi/A15 nodes, SQLite middle, DESI/Euclid. Neither the SQLite middle nor the PDF's polars/duckdb/clamd/yara hooks were built. Those libraries were not installed, and nothing was installed for this test.
4. **Image content is not CSVSON'd.** Pixels are not turned into rows; the hex wrapper stays parked (node 2). Images are PARTIAL until Timothy says how image content should enter CSVSON.
5. **Not hardened for hostile input:**
   - No decompression-bomb size cap.
   - No zip/tar path-traversal guard (everything stays in memory, so nothing is written from archives).
   - XML parsed with stdlib xml.etree, not defusedxml. defusedxml 0.7.1 is on the box but not wired in.
   - No malware scan (the PDF's PH5/PH6 hooks).
6. **Narrow coverage:** TIFF covers raw, LZW, and multi-page only. GIF covers palette with ≤256 colors and 3-frame animation; disposal and transparency edge cases are not covered. Real-world HTML with uppercase or odd markup is not covered.
7. **The 2025-08-03 regex filter was not applied.** It appears garbled in the mail ("^(?!. (bot|…") and was left as found.
8. **Scratch cleanup:** I removed the regenerable mutant sample copies under `/workspace/csvson-ingest-2026-10-05/mutants/*/samples` (my own scratch from this run, not Timothy's records). The mutant scripts and outputs remain.

## 5. Paths + sha256 (box)

Directory: `/workspace/csvson-ingest-2026-10-05/` (full list in `SHA256SUMS.txt`)
- `csvson_ingest_readiness.py` 76d2caded5676a67437b66307c5933f2e3ec8d2a40650fa6991ff220347a2247
- `csvson_crj.py` a0b6d2fc709a4496d9f11ff2ff774494578086f0463d05e56e67966a06d668b6
- `csvson_manifest_read.bas` 7bd3e4192a2aeeade1e8493830b02b55182feeea8dcf846e37bd3db2e1c5e4a6
- `out/CSVSON_INGEST_MANIFEST.csv` 2bf3170c9a98816d285a230a8b541c62ee54eae2d00053e729eb00d3376ef938
- `out/CSVSON_INGEST_MANIFEST.json` df720a12f0d681ee3045289bbafd01311c2e4c3ef52b22e19ae80642e22837e6
- `out/CSVSON_CRJ.json` e62f5d20fc0905d875b5257ef90c2ac12f10f6ffde5c48b40f0a1834c3a6d684
- `out/CSVSON_ERROR_LOG.csv` 0a487bffea1091cfc07aa595f9a5ac689cb8ce4f155a6b906f43168d32332f53
- `out/SELFCHECK_2026-10-05.txt` 8d8e40777d01d9c95033d393a9553fc2470807ca269a616b1bf3db64ecc412d8
- `out/SELFCHECK_CRJ_2026-10-05.txt` abe87e48f8da6628a7507c2e736f7dda268e3a301f9beffbb9934f5887092955
- `out/MUTANTS_2026-10-05.txt` 66e9b89067fe1864d85400fa5efb53234ea7f97519b00b087f08445ffed5ca4f
- `out/BASIC_READ_2026-10-05.txt` 087e4d31ee387fdec1ea6b6fe1515b548d6e689fb41571bf953a6e622bf531ae
- `sources/SESSION_PATTERN_MAP_2026-09-24_ROOTS_CSVSON.md` e46bc54b036fef13f602d0207bb7536341b88cebedfbd2b3eb34483ac1938bf9 (matches the ledger mail)

Run: `cd /workspace/csvson-ingest-2026-10-05 && python3 csvson_ingest_readiness.py && python3 csvson_crj.py && bwbasic csvson_manifest_read.bas </dev/null`
Note: re-running appends another block to CSVSON_ERROR_LOG.csv (append-only by design).

Not pushed to GitHub, Drive, Gmail, or Notion. Waiting on Timothy.
