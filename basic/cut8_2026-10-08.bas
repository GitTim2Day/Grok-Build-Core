10 REM cut8.bas v2 -- 8-place text cut. Timothy Norman rules 2026-10-08.
20 REM 1 zero normalised: -0 and 0 both become 0. 2 sign is a direction (x -1), work on magnitude.
30 REM 3 reduce first: split integer part. 4 round the fraction ONCE at 10 places, carry if it reaches 1.
40 REM 5 cut to 8 places. 6 digits by integer arithmetic into a preset string. 7 no negative zero.
50 REM Limit LM 99999: 5 int + 8 places + 2 guard = 15 reliable digits; above it REFUSED. DATA: long literals (8+ digits) for doubles.
60 DEFINT I-K
70 DM = 255: ML = DM - 1: NC = 19: LM# = 99999#
80 OPEN "O", #1, "cut8_bas.txt"
90 FOR I = 1 TO NC
100 READ NM$, V#
110 GOSUB 2000
120 PRINT #1, NM$ + " " + V$
130 PRINT NM$ + " " + V$
140 NEXT I
150 CLOSE #1
160 SYSTEM
2000 REM ---- V$ = cut8(V#)
2005 IF V# = 0 THEN V# = 0#
2010 S = 1
2020 IF V# < 0 THEN S = -1
2030 M# = V# * S
2040 P# = INT(M#)
2045 V$ = "REFUSED"
2050 IF P# > LM# THEN RETURN
2060 W# = INT((M# - P#) * 10000000000# + .5#)
2070 IF W# >= 10000000000# THEN GOSUB 2500
2080 Q# = INT(W# / 100#)
2085 ZR = 0
2087 IF P# = 0 THEN IF Q# = 0 THEN ZR = 1
2090 GOSUB 2200
2100 GOSUB 2300
2110 V$ = A$ + "." + F$
2115 IF S < 0 THEN IF ZR = 0 THEN V$ = "-" + V$
2120 RETURN
2200 REM ---- A$ = integer digits of P# (P# >= 0)
2210 N = 1: D# = 1#: PW# = P#
2220 FOR J = 1 TO 16
2230 IF PW# >= D# * 10# THEN N = N + 1
2240 IF PW# >= D# * 10# THEN D# = D# * 10#
2250 NEXT J
2260 A$ = STRING$(N, "0")
2270 FOR J = 1 TO N
2280 G = INT(PW# / D#)
2290 MID$(A$, J, 1) = CHR$(&H30 + G)
2292 PW# = PW# - G * D#
2294 D# = D# / 10#
2296 NEXT J
2298 RETURN
2300 REM ---- F$ = 8 fraction digits of Q# (0 <= Q# < 1E8)
2310 F$ = "00000000": D# = 10000000#
2320 FOR J = 1 TO 8
2330 G = INT(Q# / D#)
2340 MID$(F$, J, 1) = CHR$(&H30 + G)
2350 Q# = Q# - G * D#
2360 D# = D# / 10#
2370 NEXT J
2380 RETURN
2500 REM ---- carry: fraction rounded up to a whole unit
2510 P# = P# + 1#
2520 W# = W# - 10000000000#
2530 RETURN
9000 DATA "Y100", 19.54420602848818
9010 DATA "Y500", 41.797702692699715
9020 DATA "Z1", 1, "Z3", 2
9030 DATA "ZHALF", 0.5849625007211562
9040 DATA "SAMPLER", 19.5, "ZERO", 0, "NEGZERO", -0
9050 DATA "NEG", -0.58496250072, "TINYNEG", -0.000000001000000000
9060 DATA "NINES", 0.999999999, "NOISE", 0.30000000000000004
9070 DATA "BIG", 12345678.87654321, "ONE_ULP_UNDER", 2.9999999999999996
9080 DATA "CARRY", 0.99999999999, "NEGCARRY", -4.99999999999, "HUGE", 10000000000000000
9090 DATA "EDGE5", 99999.12345678, "OVER5", 100000.5
