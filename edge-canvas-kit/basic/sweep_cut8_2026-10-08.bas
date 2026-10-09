10 REM sweep_cut8_2026-10-08.bas -- sweep.bas with the 2000 cut rebuilt to Tim's rules (no STR$ on big values)
15 REM Original kept unchanged at basic/sweep.bas. Bywater lane: no '#' suffix (kit screen); Bywater numbers are double.
16 LM = 99999
20 REM Mapping f = 130.8 * 2^y Hz, so y = LOG(f / 130.8) / LOG(2). Redshift f_obs = f / (1 + z).
30 REM Values are cut (truncated) to 8 places, never rounded. Exact powers of two give exact octaves.
40 REM Representation only: this program emits and detects nothing.
50 REM Cross-check tolerance with Python and C++: 1E-7 on the 8-place values (double precision here).
60 PC = 0: FC = 0
100 REM ---- key values
110 X = 100000000 / 130.8: GOSUB 1000: Y1 = Y
120 V = Y1: GOSUB 2000: PRINT "Y100 " + V$: K1$ = V$
130 X = 500000000000000 / 130.8: GOSUB 1000: Y5 = Y
140 V = Y5: GOSUB 2000: PRINT "Y500 " + V$: K5$ = V$
150 X = 2: GOSUB 1000: V = Y: GOSUB 2000: PRINT "SHIFT_Z1 " + V$: S1$ = V$
160 X = 4: GOSUB 1000: V = Y: GOSUB 2000: PRINT "SHIFT_Z3 " + V$: S3$ = V$
170 X = 1.5: GOSUB 1000: V = Y: GOSUB 2000: PRINT "SHIFT_ZHALF " + V$: SH$ = V$
200 REM ---- descending fixed-step sampler: y = 42 - x/4, x = 0..90, additions only, final value only
210 YS = 42: D = -0.25: N = 90: I = 0
220 IF I >= N THEN GOTO 250
230 YS = YS + D: I = I + 1
240 GOTO 220
250 V = YS: GOSUB 2000: PRINT "SAMPLER_FINAL " + V$
300 REM ---- self-checks
310 T = ABS(130.8 * 2 ^ Y1 - 100000000) / 100000000 < 1E-12: GOSUB 3000
320 T = ABS((Y5 - Y1) - LOG(5000000) / LOG(2)) < 1E-9: GOSUB 3000
330 T = 0: IF K1$ = "19.54420602" THEN T = 1
335 GOSUB 3000
340 T = 0: IF K5$ = "41.79770269" THEN T = 1
345 GOSUB 3000
350 T = 0: IF S1$ = "1.00000000" THEN T = 1
355 GOSUB 3000
360 T = 0: IF S3$ = "2.00000000" THEN T = 1
365 GOSUB 3000
370 T = 0: IF SH$ = "0.58496250" THEN T = 1
375 GOSUB 3000
380 T = (YS = 19.5) AND (YS = 42 - 90 * 0.25): GOSUB 3000
390 FO = 500000000000000 / (1 + 1): X = FO / 130.8: GOSUB 1000
400 T = ABS(Y - (Y5 - 1)) < 1E-9 AND FO < 500000000000000: GOSUB 3000
410 L1 = 299792458 / 400000000000000 * 1000000000: L2 = 299792458 / 790000000000000 * 1000000000
420 T = L1 > 749 AND L1 < 750 AND L2 > 379 AND L2 < 380: GOSUB 3000
430 PRINT "PASS="; PC; " FAIL="; FC
440 IF FC = 0 THEN PRINT "SUMMARY: ALL PASS"
450 IF FC > 0 THEN PRINT "SUMMARY: FAILS"
460 END
1000 REM ---- Y = log2(X); exact when X is a power of two
1010 Y = LOG(X) / LOG(2)
1020 R = INT(Y + 0.5)
1030 IF 2 ^ R = X THEN Y = R
1040 RETURN
2000 REM ---- V$ = V cut to 8 places. Tim 2026-10-08: zero normalised, sign as direction, split first,
2001 REM round fraction once at 10 places with carry, cut to 8, digits by integer arithmetic, no negative zero.
2002 REM Limit LM 99999 (5 int + 8 places + 2 guard = 15 reliable digits). Above it: REFUSED.
2005 IF V = 0 THEN V = 0
2010 SG = 1
2020 IF V < 0 THEN SG = -1
2030 MG = V * SG
2040 NI = INT(MG)
2045 V$ = "REFUSED"
2050 IF NI > LM THEN RETURN
2060 WF = INT((MG - NI) * 10000000000 + .5)
2070 IF WF >= 10000000000 THEN GOSUB 2500
2080 QF = INT(WF / 100)
2085 ZR = 0
2087 IF NI = 0 THEN IF QF = 0 THEN ZR = 1
2090 GOSUB 2200
2100 GOSUB 2300
2110 V$ = A$ + "." + F$
2115 IF SG < 0 THEN IF ZR = 0 THEN V$ = "-" + V$
2120 RETURN
2200 REM ---- A$ = integer digits of NI
2210 NN = 1: DV = 1: PW = NI
2220 FOR JJ = 1 TO 16
2230 IF PW >= DV * 10 THEN NN = NN + 1
2240 IF PW >= DV * 10 THEN DV = DV * 10
2250 NEXT JJ
2260 A$ = STRING$(NN, "0")
2270 FOR JJ = 1 TO NN
2280 G = INT(PW / DV)
2290 MID$(A$, JJ, 1) = CHR$(&H30 + G)
2292 PW = PW - G * DV
2294 DV = DV / 10
2296 NEXT JJ
2298 RETURN
2300 REM ---- F$ = 8 fraction digits of QF
2310 F$ = "00000000": DV = 10000000
2320 FOR JJ = 1 TO 8
2330 G = INT(QF / DV)
2340 MID$(F$, JJ, 1) = CHR$(&H30 + G)
2350 QF = QF - G * DV
2360 DV = DV / 10
2370 NEXT JJ
2380 RETURN
2500 REM ---- carry: fraction rounded up to a whole unit
2510 NI = NI + 1
2520 WF = WF - 10000000000
2530 RETURN
3000 REM ---- one check, one node, then RETURN
3010 IF T THEN PC = PC + 1: RETURN
3020 FC = FC + 1: PRINT "FAIL check"; PC + FC
3030 RETURN
