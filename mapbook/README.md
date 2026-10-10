# MAPBOOK — our own Mapper (edge-first, no Safari, no API key)

Author: Timothy Norman (sole author, Tim's Rule 1). Claude = tool/validator.
Started 2026-10-10. Status labels: EARNED = run here in the sandbox; ASSERTED = not yet run.

## What is here
| Part | Files | Status |
|---|---|---|
| Address finder (OCR text -> address records) | `MAPBOOK_ADDR_SPEC_v1.md`, `addr_find.py`, `addr_find.cpp`, `fixture_v1.txt`, `fixture_v1_expected.txt` | EARNED: Python + C++ match the 15-record key. BASIC twin not yet built. |
| OSM streamline (Georgia .osm.pbf -> addresses + roads) | `OSM_STREAMLINE_SPEC_v1.md` (v1.6), `osm_streamline.py`, `osm_streamline.cpp`, `make_osm_fixture.py`, `osm_fixture_expected/` | EARNED on synthetic data (see below). ASSERTED on the real Georgia file until the Pi run. |
| Test tools | `fuzz_osm.py`, `mutate.py` | EARNED |
| Pi runner | `run_pi.sh` | Dry run EARNED here; Pi run pending |

## Run on the Pi
```
cd ~/work && git clone https://github.com/GitTim2Day/Grok-Build-Core.git || (cd Grok-Build-Core && git pull)
cd ~/work/Grok-Build-Core/mapbook && bash run_pi.sh ~/work/maps/georgia-latest.osm.pbf
```
The script builds the C++ twin, self-tests both twins on the answer key, prints the input's
size + SHA-256, streamlines, times it, and prints output sizes + SHA-256. Output goes to a
new dated folder; nothing is overwritten.

## Results (sandbox, 2026-10-10)
- Answer key: both twins 3/3 output files byte-identical to the hand key, counts match.
- Fault files: 8/8 refused by both twins with the same reason (empty, no header,
  truncated, bad header sizes, unsupported feature, lzma, raw_size mismatch).
- Differential fuzz: 2,200 random files (half byte-corrupted), 0 mismatches, 0 crashes
  (C++ under AddressSanitizer + UndefinedBehaviorSanitizer).
- Mutation gate: Python 16/16 killed, C++ 15/15 killed.
- Speed on a 15.8 MB synthetic file (2,000,000 nodes, 240,000 ways): C++ 4.4 s,
  Python 20.2 s, outputs byte-identical. Real Georgia (340 MB) time is ASSERTED until the
  Pi run reports it.

## Defects found and fixed (spec first, then both twins)
- S1 empty file accepted as a zero-count success -> REFUSE, first block must be OSMHeader.
- S2 corrupted (non-UTF-8) names handled differently -> bytes pass through untouched.
- S3 Python crashed on corrupt zlib data and had no output cap -> capped inflate, REFUSE.
- S4 twins refused corrupt files for different first reasons -> one check order; a field
  with an unexpected wire type is ignored.
- S5 Python skipped the bounds check on 4/8-byte fields -> "truncated field".
- S6 C++ cut text at a zero byte -> all text written by byte length.
- Key gaps closed by mutation: no primary road, road nodes already in sorted order,
  no header-missing fault file.

## Coordinates
Integer nanodegrees; text form is hemisphere letter + value with 7 decimals by text chop
(never rounded). All-zero after the chop takes N/E, so there is no negative zero.

## Open (for Tim)
- Q1 PO Box lines, Q2 non-US formats, Q3 street-only rows into the book (spec v1 of the finder).
- BASIC twin of the address finder (PC-BASIC run).
- Pi run of `run_pi.sh` on the real Georgia extract: time, sizes, hashes.
