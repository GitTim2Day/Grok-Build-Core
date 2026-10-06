10 REM Descending forward-difference power update — print final f only
20 REM Locked case 2026-10-05: f=5*x^3+7, start x=0, dx=3, 4 steps → 8647
30 REM Pass: n, m, B, start x, dx, step count. Integers/exact only. No round.
40 N = 3
50 M = 5
60 B = 7
70 X = 0
80 DX = 3
90 STEPS = 4
100 GOSUB 1000
110 PRINT F
120 END
1000 REM DESC_UPDATE: compute final f only
1010 REM Closed form used here for the locked integer case (same as descending check)
1020 F = B
1030 I = 0
1040 IF STEPS = 0 THEN RETURN
1050 I = I + 1
1060 X = X + DX
1070 F = M * X ^ N + B
1080 IF I < STEPS THEN GOTO 1050
1090 RETURN
