10 REM sweep.bas -- BASIC twin of lib/sweep.py key values (Spectrum Sweep, 2026-10-06)
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
2000 REM ---- V$ = V cut to 8 places (V >= 0), zero-padded, never rounded
2010 VI = INT(V): VF = INT((V - VI) * 100000000)
2020 F$ = MID$(STR$(VF), 2)
2030 IF LEN(F$) < 8 THEN F$ = "0" + F$: GOTO 2030
2040 V$ = MID$(STR$(VI), 2) + "." + F$
2050 RETURN
3000 REM ---- one check, one node, then RETURN
3010 IF T THEN PC = PC + 1: RETURN
3020 FC = FC + 1: PRINT "FAIL check"; PC + FC
3030 RETURN
