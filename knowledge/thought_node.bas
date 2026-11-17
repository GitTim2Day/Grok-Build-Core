10 REM thought_node.bas
20 REM Identical string contract to Python and C++.
30 REM Verified by side-by-side token comparison on fixed timestamp.
40 REM Run on Pi 5 under bwbasic after setting the four variables.
50 
60 REM Example invocation (edit the four lines then RUN):
70 SPEECH$="turn left"
80 OCR$="arrow left"
90 MOTOR$="idle"
100 TS$="2026-11-17T12:05:00.000000-04:00"
110 
120 GOSUB 200
130 END
140 
200 REM --- thought routine ---
210 REM strip
220 SPEECH$=FNSTRIP$(SPEECH$)
230 OCR$=FNSTRIP$(OCR$)
240 MOTOR$=FNSTRIP$(MOTOR$)
250 
260 SPSTAT$="OK" : IF SPEECH$="" THEN SPSTAT$="FAIL"
270 OCRSTAT$="OK" : IF OCR$="" THEN OCRSTAT$="FAIL"
280 MOSTAT$="OK" : IF MOTOR$="" THEN MOSTAT$="FAIL"
290 
300 TOKEN$="THOUGHT|"+TS$+"|speech:"+SPSTAT$+":"+FNESC$(SPEECH$)+"|ocr:"+OCRSTAT$+":"+FNESC$(OCR$)+"|motor:"+MOSTAT$+":"+FNESC$(MOTOR$)
310 PRINT TOKEN$
320 RETURN
330 
400 REM FNSTRIP$ — leading/trailing whitespace removed
410 DEF FNSTRIP$(S$)
420 IF LEN(S$)=0 THEN FNSTRIP$="" : RETURN
430 START=1
440 FOR I=1 TO LEN(S$)
450 C$=MID$(S$,I,1)
460 IF C$<>" " AND C$<>CHR$(9) AND C$<>CHR$(10) AND C$<>CHR$(13) THEN START=I : GOTO 480
470 NEXT I
480 ENDP=LEN(S$)
490 FOR I=LEN(S$) TO 1 STEP -1
500 C$=MID$(S$,I,1)
510 IF C$<>" " AND C$<>CHR$(9) AND C$<>CHR$(10) AND C$<>CHR$(13) THEN ENDP=I : GOTO 530
520 NEXT I
530 IF START>ENDP THEN FNSTRIP$="" ELSE FNSTRIP$=MID$(S$,START,ENDP-START+1)
540 RETURN
550 
600 REM FNESC$ — escape pipes
610 DEF FNESC$(S$)
620 R$=""
630 FOR I=1 TO LEN(S$)
640 C$=MID$(S$,I,1)
650 IF C$="|" THEN R$=R$+"\|", ELSE R$=R$+C$
660 NEXT I
670 FNESC$=R$
680 RETURN
