10 REM Common firmware. Cut the far-right decimal character. No float.
20 GOTO 100
100 LET SKILL$ = "shared-library"
110 LET MEM$ = "seat-memory-plus-shared-user"
120 LET NUMMODE$ = "string-then-convert"
130 GOTO 200
200 GOSUB 400
210 GOSUB 500
220 END
400 IF SKILL$ = "" THEN GOTO 100
410 IF NUMMODE$ <> "string-then-convert" THEN GOTO 100
420 RETURN
500 LET A$ = "0.707106781"
510 LET P = INSTR(A$, ".")
512 IF INSTR(A$, "e") > 0 OR INSTR(A$, "E") > 0 THEN PRINT "REFUSED" : END
520 IF P = 0 THEN PRINT "REFUSED" : END
530 IF LEN(A$) - P < 2 THEN PRINT "REFUSED" : END
540 LET A$ = LEFT$(A$, LEN(A$) - 1)
550 PRINT A$
560 RETURN
