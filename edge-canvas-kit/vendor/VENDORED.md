# vendor/ -- what was copied into the kit, and from where

| file | source (box) | source sha256 | kit sha256 | changed? |
|---|---|---|---|---|
| txt_rcrj/to_txt.py | csvson-ingest-2026-10-05/txt_rcrj/to_txt.py | f2fb5b36ad9a310d9de2a274147ca211248d65bf28da66937260fcd8658d64e7 | b20a8df5e3cc870f698f70a53034df66804bf5123686fd2770f3f9798c4f1ab0 | YES: KIT FIX 2026-10-06 (XML without defusedxml) |
| txt_rcrj/rcrj.py | csvson-ingest-2026-10-05/txt_rcrj/rcrj.py | 55619f577cfd997ac05410d67065532f44646b6600c102ad78dcc5f1e41e35a7 | b0382e5b5037c3334056397a1a68c414090ef9903a293fb9c7e79bcbafabbd17 | YES: KIT FIX 2026-10-06 |
| txt_rcrj/rcrj_guard.bas | csvson-ingest-2026-10-05/txt_rcrj/rcrj_guard.bas | e3ec12d5630d3a7699d7239094e73f04dd9c91bdf2c14f8d11193feedbfad8ce | e3ec12d5630d3a7699d7239094e73f04dd9c91bdf2c14f8d11193feedbfad8ce | no |

## KIT FIX 2026-10-06 -- rcrj.run() non-dict record
The source rcrj.py built the context string with `rec.get(...)` BEFORE checking `isinstance(rec, dict)`,
so a non-dict record (None, a string, a number) raised AttributeError and stopped the main line.
The kit copy checks the dict first; a non-dict record now goes to the `bad_record` node and the run continues.
Old kit copy archived (box): `/workspace/edge-canvas-kit-2026-10-06/archive/vendor-pre-fix/rcrj.py.vendored-55619f57`.
**PENDING: port back** to `/workspace/csvson-ingest-2026-10-05/txt_rcrj/rcrj.py` and to GitHub (not done in this run).

## KIT FIX 2026-10-06 -- to_txt.py XML when defusedxml is absent (found by the bare-device test round)
The source set `DefusedXmlException = Exception` when defusedxml is missing, so `except DefusedXmlException` caught the
"defusedxml missing" error and EVERY XML file (and the XML inside DOCX/XLSX/PPTX/ODT) went to QUARANTINE on a device
without defusedxml (Raspberry Pi OS does not ship it by default -- not verified on his Pi).
The kit copy: without defusedxml, any DTD / ENTITY declaration (UTF-8 or UTF-16) is refused -> QUARANTINE (fail closed);
XML with no DTD is parsed by the stdlib ElementTree (nothing to expand, no external entity to fetch). With defusedxml
present the behaviour is unchanged. Old kit copy archived (box):
`/workspace/edge-canvas-kit-2026-10-06/archive/vendor-pre-fix/to_txt.py.vendored-f2fb5b36`.
**PENDING: port back** to `/workspace/csvson-ingest-2026-10-05/txt_rcrj/to_txt.py` and GitHub (not done in this run).

## Optional imports in to_txt.py (degrade, never required)
- Pillow absent -> images PARKED (node 2). defusedxml absent -> stdlib XML parse with DTDs refused (see fix above).
- tesseract / pdftotext / pdftoppm absent -> OCR / PDF text nodes report and continue.
