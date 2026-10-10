# MAPBOOK address finder — spec v1 (2026-10-10)

Author: Timothy Norman (sole author, Tim's Rule 1). Claude = tool/validator.
Referee for the Python, C++ and BASIC twins. Integer/text only, no floats.
Input is OCR text already cleaned by OCR_CLEAN (skill `ocr-streamline`).

## Limits (variables, top of every twin)
- ML = 200   max characters per input line (longer line: R9 LONGLINE, line skipped, flagged)
- MS = 12    max comma segments per line (more: R9 on that line)
- MT = 12    max tokens per segment (more: segment is not an address part)
- MR = 500   max output records (more: stop, R8 FULL record written last)

## Normalize a line (GOSUB NORM)
1. Uppercase A-Z only (a-z -> A-Z). Other bytes unchanged.
2. Delete every "." (OCR "St." -> "ST", "P.O." -> "PO").
3. Split on "," into segments. Trim each segment, collapse runs of spaces to one.
4. Tokens = segment split on single spaces.

## Token classes
- HOUSE: 1..6 chars, all digits, first char not "0".
- SUFFIX (exact): ST STREET AVE AVENUE RD ROAD DR DRIVE LN LANE BLVD BOULEVARD
  CT COURT WAY PKWY PARKWAY HWY HIGHWAY CIR CIRCLE PL PLACE TRL TRAIL TER TERRACE
- DIR (exact): N S E W NE NW SE SW
- UNITWORD (exact): APT STE SUITE UNIT #
- STATE (exact, 52): AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI
  MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC PR
- ZIP: 5 digits, or 5 digits "-" 4 digits (10 chars). Nothing else.
- ALNUM: 1+ chars, each A-Z or 0-9.
- CITYWORD: 1+ chars, each A-Z or "-" or "'"; at least one A-Z.

## Segment classes
- STREETSEG: tokens t1..tn, 3 <= n <= MT.
  t1 is HOUSE. Let s = n, or s = n-1 when tn is DIR. ts is SUFFIX and s >= 3.
  t2..t(s-1) are all ALNUM. (Note "CT" is both SUFFIX and STATE; class by position.)
- UNITSEG: exactly 2 tokens, t1 UNITWORD and t2 ALNUM; or exactly 1 token, "#" + ALNUM.
- CITYSEG: 1..4 tokens, all CITYWORD.
- STZIPSEG: exactly 2 tokens, t1 STATE, t2 ZIP.

## Main loop (READ -> RECORD -> CLEAR each line)
```
10 PS$="":PL=0                         ' pending street, its line (carried state, named)
20 FOR L=1 TO N
30   GOSUB NORM (line L) -> SEG(1..C)
40   IF line too long OR C>MS THEN GOSUB FLUSHPEND: EMIT R9 LONGLINE line L: GOTO next
50   K=0                                ' CSZ found flag
60   IF C>=2 AND SEG(C) is STZIPSEG AND SEG(C-1) is CITYSEG THEN K=1
70   IF K=1 THEN GOSUB CSZLINE ELSE GOSUB STREETLINE
80   CLEAR per-line scratch (SEG, C, K, ST$)
90 NEXT L
100 GOSUB FLUSHPEND

CSZLINE:
  ST$=""
  IF C>=4 AND SEG(C-2) is UNITSEG AND SEG(C-3) is STREETSEG THEN ST$=SEG(C-3)+" "+SEG(C-2)
  ELSE IF C>=3 AND SEG(C-2) is STREETSEG THEN ST$=SEG(C-2)
  IF ST$="" AND C=2 AND PS$<>"" THEN ST$=PS$: SL=PL: PS$="": PL=0   ' consume pending
  ELSE GOSUB FLUSHPEND: SL=L
  IF ST$<>"" THEN EMIT R0 OK  (SL, ST$, SEG(C-1), state, zip)
  ELSE EMIT R2 NOSTREET (L, blank, SEG(C-1), state, zip)
  RETURN

STREETLINE:
  GOSUB FLUSHPEND
  IF C>=2 AND SEG(C) is UNITSEG AND SEG(C-1) is STREETSEG THEN PS$=SEG(C-1)+" "+SEG(C): PL=L
  ELSE IF SEG(C) is STREETSEG THEN PS$=SEG(C): PL=L
  RETURN

FLUSHPEND:
  IF PS$<>"" THEN EMIT R1 NOCITY (PL, PS$, blank, blank, blank): PS$="": PL=0
  RETURN
```
Only the street on the line directly above a city line that has exactly two
segments (`CITY, ST ZIP`) is joined. No guessing of letters (no 0/O swap),
no fuzzy match, no repair.

## Output record (one per line, text)
`R|LINE|STREET|CITY|ST|ZIP` — R is a single digit. Empty field = one blank
(CHR$(32), BASIC gate rule 10). Records in emit order. After MR records:
write `8|0| | | | ` and stop.

## Reason codes
- 0 OK, 1 NOCITY (street, no city line), 2 NOSTREET (city/state/zip only),
  8 FULL (record cap reached), 9 LONGLINE (line > ML chars or > MS segments).

## Answer key — fixture `fixture_v1.txt` -> `fixture_v1_expected.txt`
Boundary cases: house of 6 digits (in) and 7 digits (out); leading 0 (out);
ZIP+4 (in), ZIP 4 digits (out), ZIP 6 digits (out); 4 city words (in), 5 (out);
directional after suffix (in); unit as own segment and "#12"; CT as suffix
(street) vs CT as state; pending street consumed by next line; pending street
flushed by a non-matching line; pending flushed at end of file; line of exactly
ML chars (processed) and ML+1 (R9); lowercase + "St." folding.

## QUESTIONS for Tim (PROPOSED defaults in use, questions open)
- Q1 PO Box lines — currently not addresses (no HOUSE). Keep out, or add a POBOX class?
- Q2 Non-US formats (Canada, UK) — out of v1.
- Q3 Should a street with no city still go to the book (R1) — PROPOSED yes, flagged, never mapped until fixed.
