10 REM csvson_manifest_read.bas -- BASIC side reads the CSVSON ingest manifest (2026-10-05)
20 REM Counts status column (last field). Main line keeps moving; unknown status -> UNK flag, no stop.
30 OPEN "I", #1, "out/CSVSON_INGEST_MANIFEST.csv"
40 LINE INPUT #1, H$
50 N = 0: M = 0: T = 0: Q = 0: U = 0: F = 0: X = 0
60 IF EOF(1) THEN GOTO 200
70 LINE INPUT #1, L$
80 N = N + 1
90 P = 0
100 FOR I = LEN(L$) TO 1 STEP -1
110 IF MID$(L$, I, 1) = "," AND P = 0 THEN P = I
120 NEXT I
130 S$ = MID$(L$, P + 1)
140 IF S$ = "INGESTED_META_SHA" THEN M = M + 1: GOTO 60
150 IF S$ = "INGESTED_TEXT" THEN T = T + 1: GOTO 60
160 IF S$ = "QUARANTINE" THEN Q = Q + 1: GOTO 60
170 IF S$ = "UNK_FLAGGED" THEN U = U + 1: GOTO 60
180 IF S$ = "ROUNDTRIP_FAIL" THEN F = F + 1: GOTO 60
190 X = X + 1: GOTO 60
200 CLOSE #1
210 PRINT "ROWS"; N; "META_SHA"; M; "TEXT"; T; "QUAR"; Q; "UNK"; U; "FAIL"; F; "OTHER"; X
220 IF N = 30 AND M = 16 AND T = 11 AND Q = 1 AND U = 1 AND F = 1 AND X = 0 THEN PRINT "BASIC_READ PASS" ELSE PRINT "BASIC_READ FAIL"
230 END
