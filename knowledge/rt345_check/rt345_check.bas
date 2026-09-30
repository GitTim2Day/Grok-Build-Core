10 REM RT345_CHECK.BAS - 3-4-5 unit rule, integer-only (scaled by 5)
20 REM Values held as fifths: 7 = 35/5, 1.4 = 7/5. No floats.
30 F = 0 : T = 0
40 REM --- unit from the hypotenuse: H=7 -> 35 fifths
50 H5 = 35 : U5 = H5 / 5 : GOSUB 1000
60 REM --- unit from height 3 -> 15 fifths
70 H5 = 15 * 5 / 3 : U5 = 15 / 3 : GOSUB 1000
80 REM --- not plus: 3u+4u must not equal 5u
90 T = T + 1 : IF 3*U5 + 4*U5 = 5*U5 THEN F = F + 1 : PRINT "FAIL not plus" ELSE PRINT "PASS not plus 7u"
100 REM --- negative control 3-4-6
110 T = T + 1 : IF 3*3 + 4*4 = 6*6 THEN F = F + 1 : PRINT "FAIL neg control" ELSE PRINT "PASS neg control"
120 PRINT T - F; "/"; T
130 END
1000 REM GOSUB: rebuild legs from unit (fifths) and check squares exactly
1010 T = T + 1
1020 A = 3 * U5 : B = 4 * U5 : C = 5 * U5
1030 IF A*A + B*B = C*C THEN PRINT "PASS unit"; U5; "/5 sides"; A; B; C; "/5" ELSE F = F + 1 : PRINT "FAIL unit"; U5
1040 RETURN
