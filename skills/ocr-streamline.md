# ocr-streamline

**Family:** ONE-JOB
**GOSUB ID:** OCR_CLEAN
**Status:** ACTIVE
**Date:** 2026-10-10
**Direction:** clean
**Cost class:** Low

## Purpose
Clean OCR text with the streamline method. One entry, one exit. BASIC GOSUB logic and the Python twin. BASIC commands BOX, LINE, CIRCLE, TRIANGLE are real subroutines, not comments. The sealed route file is not mutated.

## Skill value
GOSUB_ACCURACY_FLOOR(matched, reference length). Percent error. Truncate toward zero at 1e-6. Zero means the cleaned text matches the sealed fixture. It is not a grade of zero.

- SKILL_VALUE: 0.000000
- BEFORE_FLOOR, Python ends-only: 88.461538
- BEFORE_FLOOR, BASIC ends-only: 100
- FAST_OVER_SLOW: 1.231793 (same contract, 400 rounds)

Both twins printed SUMMARY: ALL PASS. bwbasic 3.20 ran the BASIC file.

## Contract
1. FOLD_EXACT — enumerated glyph fold only (ligatures, quotes, dashes, box drawing).
2. COLLAPSE — TAB to space, drop CR and FF, collapse spaces, trim.
3. BOX_EDGE — strip vertical LINE runs on the two ends. Interior pipes stay.
4. LINE_RULE — drop a line whose marks are only `-_=+~`.
5. CIRCLE_MARK — drop a line whose marks are only `()`.
6. TRIANGLE_MARK — drop a line whose marks are only `^/\`.
7. Second pass is identity.

No 0/O swap. No fitted cutoff. Empty in, empty out. A zero reference length is an error.

## Twins
- `basic/ocr_streamline.bas` SHA-256 `5b447469db86b0d05fcd1bca595690dc446a8a528ba3a70ccd5df2c7c55a119d`
- `basic/ocr_streamline.py` SHA-256 `d78ba18d08afa4091b094f544071c7fa229055c875b09bd3d7f75dc78fa042f9`

Rex_MD_Fortress carries the same two files under `04_Clinical_Decision/`.

## Append
2026-10-10T07:56-04:00 · OCR streamline clean · HIT both twins ALL PASS · VAL skill value 0.000000 · miss ends-only floor 88.461538 / 100 · open sealed route not mutated
