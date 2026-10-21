10 REM CUBE TURN DISPATCH. SAME IF AS cube_turn.py gosub_parse.
20 REM THIS FILE WAS NOT RUN ON THIS SEAT. BWBASIC WAS NOT PRESENT.
30 REM GOSUB 100 PARSE. GOSUB 200 INVERSE ONE TOKEN.
100 REM PARSE token$ -> face$, times, miss
110 miss = 0
120 IF LEN(token$) = 0 THEN miss = 1: RETURN
130 face$ = LEFT$(token$, 1)
140 IF INSTR("UDFBLR", face$) = 0 THEN miss = 1: RETURN
150 rest$ = MID$(token$, 2)
160 IF rest$ <> "" AND rest$ <> "'" AND rest$ <> "2" AND rest$ <> "2'" THEN miss = 1: RETURN
170 IF INSTR(token$, "2") > 0 THEN times = 2: RETURN
180 IF INSTR(token$, "'") > 0 THEN times = 3: RETURN
190 times = 1
200 RETURN
300 REM INVERSE OF ONE PARSED TOKEN
310 IF times = 2 THEN inv$ = face$ + "2": RETURN
320 IF times = 3 THEN inv$ = face$: RETURN
330 inv$ = face$ + "'"
340 RETURN
