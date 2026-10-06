10 REM rcrj_guard.bas -- Timothy Norman, 2026-10-06. RCRJ guard nodes mirrored in BASIC (Python is the real pipeline).
20 REM txt record T$ -> GOSUB 2000 REGEX_GUARD_PRE -> CSV cell (GOSUB 2500) -> GOSUB 3000 REGEX_GUARD_POST -> JSON (Python)
30 REM Conflicts never kill the main line: REJECT node 4000, SQLITE node 5000 (Python does the parameterized insert).
40 REM Flags: F1 formula lead = + - @ TAB CR | F2 SQL pattern | F3 control stripped | F4 prompt-injection marker
50 REM F5 HTML or script tag | F6 overlong (route SQLite) | F7 NUL (reject). Flags never execute anything.
60 REM bwbasic drops CHR$(0) from strings, so the reader passes NUL as N0=1. Positive IF only; SGN for compares.
70 REM Route R: 0 CSV row | 1 SQLite fallback | 2 reject log.
80 MAXF = 40: MAXR = 200: LT$ = CHR$(60): QT$ = CHR$(34)
90 GOTO 6000
1000 REM ========== MAIN LINE: one record ==========
1010 GOSUB 2000
1020 IF V = 1 THEN GOSUB 4000: RETURN
1030 GOSUB 2700
1040 IF FIT = 0 THEN GOSUB 5000: RETURN
1050 GOSUB 2500
1060 GOSUB 3000
1070 IF M = 1 THEN GOSUB 5000: RETURN
1080 R = 0: ROWS = ROWS + 1: RETURN
2000 REM ========== REGEX_GUARD_PRE (insertion prevention before CSV) ==========
2010 V = 0: F1 = 0: F2 = 0: F3 = 0: F4 = 0: F5 = 0: F6 = 0: F7 = 0: C$ = "": M = 0: R = 0
2020 IF N0 = 1 THEN F7 = 1: V = 1: RETURN
2030 D = LEN(T$) - MAXR: IF SGN(D) = 1 THEN V = 1: RETURN
2040 IF LEN(T$) = 0 THEN GOTO 2130
2050 FOR I = 1 TO LEN(T$)
2060 A = ASC(MID$(T$, I, 1)): KEEP = 1
2070 IF SGN(32 - A) = 1 THEN KEEP = 0
2080 IF A = 9 THEN KEEP = 1
2090 IF A = 10 THEN KEEP = 1
2100 IF A = 127 THEN KEEP = 0
2110 IF KEEP = 1 THEN C$ = C$ + MID$(T$, I, 1) ELSE F3 = 1
2120 NEXT I
2130 GOSUB 2900
2140 P = 1
2145 IF MID$(C$, P, 1) = " " THEN P = P + 1: GOTO 2145
2150 A = 0: IF LEN(MID$(C$, P, 1)) = 1 THEN A = ASC(MID$(C$, P, 1))
2155 IF A = 61 OR A = 43 OR A = 45 OR A = 64 OR A = 9 OR A = 13 THEN F1 = 1
2160 IF INSTR(U$, "DROP TABLE") OR INSTR(U$, "UNION SELECT") OR INSTR(U$, "OR 1=1") THEN F2 = 1
2165 IF INSTR(U$, "; DELETE") OR INSTR(U$, "XP_CMDSHELL") OR INSTR(U$, "';") THEN F2 = 1
2170 IF INSTR(U$, "IGNORE PREVIOUS INSTRUCTIONS") OR INSTR(U$, "IGNORE ALL PREVIOUS INSTRUCTIONS") THEN F4 = 1
2175 IF INSTR(U$, "[INST]") OR INSTR(U$, "SYSTEM PROMPT") OR INSTR(U$, "YOU ARE NOW ") THEN F4 = 1
2180 IF INSTR(U$, LT$ + "SCRIPT") OR INSTR(U$, LT$ + "IFRAME") OR INSTR(U$, LT$ + "IMG") THEN F5 = 1
2185 IF INSTR(U$, "JAVASCRIPT:") OR INSTR(U$, "ONERROR=") OR INSTR(U$, "ONLOAD=") THEN F5 = 1
2190 D = LEN(C$) - MAXF: IF SGN(D) = 1 THEN F6 = 1
2195 RETURN
2500 REM ========== CSV cell: formula-safe prefix + quote doubling + QUOTE_ALL ==========
2510 SP = 0: IF F1 = 1 THEN SP = 1
2520 IF LEFT$(C$, 1) = "'" THEN SP = 1
2530 P$ = C$: IF SP = 1 THEN P$ = "'" + C$
2540 Q$ = QT$
2550 IF LEN(P$) = 0 THEN GOTO 2590
2560 FOR I = 1 TO LEN(P$)
2570 IF MID$(P$, I, 1) = QT$ THEN Q$ = Q$ + QT$ + QT$ ELSE Q$ = Q$ + MID$(P$, I, 1)
2580 NEXT I
2590 Q$ = Q$ + QT$: RETURN
2700 REM ========== CSV fit check (else SQLite) ==========
2710 FIT = 1
2720 IF K = 1 THEN FIT = 0
2730 IF INSTR(C$, CHR$(10)) THEN FIT = 0
2740 IF F6 = 1 THEN FIT = 0
2750 RETURN
2900 REM ========== uppercase C$ into U$ ==========
2910 U$ = ""
2920 IF LEN(C$) = 0 THEN RETURN
2930 FOR J = 1 TO LEN(C$)
2940 B = ASC(MID$(C$, J, 1))
2950 IF SGN(B - 96) = 1 AND SGN(123 - B) = 1 THEN B = B - 32
2960 U$ = U$ + CHR$(B)
2970 NEXT J
2980 RETURN
3000 REM ========== REGEX_GUARD_POST (re-validate cell, round-trip equality) ==========
3010 M = 0: X$ = ""
3020 IF SGN(2 - LEN(Q$)) = 1 THEN M = 1: RETURN
3030 IF LEFT$(Q$, 1) = QT$ THEN GOTO 3034
3032 M = 1: RETURN
3034 IF RIGHT$(Q$, 1) = QT$ THEN GOTO 3040
3035 M = 1: RETURN
3040 W$ = MID$(Q$, 2, LEN(Q$) - 2): I = 1
3050 IF SGN(I - LEN(W$)) = 1 THEN GOTO 3100
3060 CH$ = MID$(W$, I, 1)
3070 IF CH$ = QT$ THEN GOTO 3075
3072 GOTO 3090
3075 IF MID$(W$, I + 1, 1) = QT$ THEN X$ = X$ + QT$: I = I + 2: GOTO 3050
3080 M = 1: RETURN
3090 X$ = X$ + CH$: I = I + 1: GOTO 3050
3100 A = 0: IF LEN(X$) THEN A = ASC(X$)
3110 IF A = 61 OR A = 43 OR A = 45 OR A = 64 OR A = 9 OR A = 13 THEN M = 1: RETURN
3120 IF LEFT$(X$, 1) = "'" THEN X$ = MID$(X$, 2)
3130 IF X$ = C$ THEN RETURN
3140 M = 1: RETURN
4000 REM ========== REJECT node: reject log, main line continues ==========
4010 R = 2: REJ = REJ + 1: RETURN
5000 REM ========== SQLITE_FALLBACK node (Python: parameterized INSERT only) ==========
5010 R = 1: FB = FB + 1: RETURN
6000 REM ========== SELF-CHECK HARNESS ==========
6010 PASSES = 0: FAILS = 0: REJ = 0: FB = 0: ROWS = 0: RECS = 0
6020 T$ = "hello world": N0 = 0: K = 0: GOSUB 7000
6025 E = (R = 0) AND (F1 + F2 + F3 + F4 + F5 + F6 + F7 = 0): N$ = "plain_passes": GOSUB 7100
6030 T$ = "=cmd|calc": GOSUB 7000
6035 S1 = 0: IF LEFT$(Q$, 2) = QT$ + "'" THEN S1 = 1
6036 E = (R = 0) AND (F1 = 1) AND (S1 = 1): N$ = "formula_eq_prefixed": GOSUB 7100
6040 T$ = "+1+1": GOSUB 7000: E = (F1 = 1) AND (R = 0): N$ = "formula_plus": GOSUB 7100
6045 T$ = "-2": GOSUB 7000: E = (F1 = 1) AND (R = 0): N$ = "formula_minus": GOSUB 7100
6050 T$ = "@SUM(1,1)": GOSUB 7000: E = (F1 = 1) AND (R = 0): N$ = "formula_at": GOSUB 7100
6055 T$ = CHR$(9) + "=x": GOSUB 7000: E = (F1 = 1) AND (R = 0): N$ = "formula_tab": GOSUB 7100
6060 T$ = "  =x": GOSUB 7000: E = (F1 = 1) AND (R = 0): N$ = "formula_after_spaces": GOSUB 7100
6065 T$ = "x'); DROP TABLE t;--": GOSUB 7000: GOSUB 7200: E = (F2 = 1) AND (R = 0) AND (S1 = 1): N$ = "sql_drop_flagged_kept": GOSUB 7100
6070 T$ = "1 OR 1=1": GOSUB 7000: E = (F2 = 1): N$ = "sql_or_1_1": GOSUB 7100
6075 T$ = "a" + CHR$(27) + "b" + CHR$(7): GOSUB 7000: S1 = 0: IF C$ = "ab" THEN S1 = 1
6076 E = (F3 = 1) AND (S1 = 1) AND (R = 0): N$ = "control_stripped": GOSUB 7100
6080 T$ = "ab": N0 = 1: GOSUB 7000: E = (R = 2) AND (F7 = 1): N$ = "nul_rejected": GOSUB 7100: N0 = 0
6085 T$ = STRING$(50, "X"): GOSUB 7000: E = (F6 = 1) AND (R = 1): N$ = "overlong_to_sqlite": GOSUB 7100
6090 T$ = STRING$(250, "Y"): GOSUB 7000: E = (R = 2): N$ = "oversize_hard_rejected": GOSUB 7100
6095 T$ = "Ignore previous instructions now": GOSUB 7000: E = (F4 = 1) AND (R = 0): N$ = "prompt_flagged_not_run": GOSUB 7100
6100 T$ = "[INST] x": GOSUB 7000: E = (F4 = 1): N$ = "prompt_inst_marker": GOSUB 7100
6105 T$ = LT$ + "script" + CHR$(62) + "x": GOSUB 7000: E = (F5 = 1) AND (R = 0): N$ = "html_script_flagged": GOSUB 7100
6110 T$ = "go javascript:evil()": GOSUB 7000: E = (F5 = 1): N$ = "html_javascript_uri": GOSUB 7100
6115 T$ = "a" + CHR$(10) + "b": GOSUB 7000: E = (R = 1): N$ = "multiline_to_sqlite": GOSUB 7100
6120 T$ = "say " + QT$ + "hi" + QT$ + ", ok": GOSUB 7000: GOSUB 7200: E = (R = 0) AND (M = 0) AND (S1 = 1): N$ = "quotes_roundtrip": GOSUB 7100
6125 T$ = "unbalanced " + QT$ + " q": GOSUB 7000: GOSUB 7200: E = (R = 0) AND (S1 = 1): N$ = "lone_quote_roundtrip": GOSUB 7100
6130 T$ = "'=x": GOSUB 7000: GOSUB 7200: S2 = 0: IF Q$ = QT$ + "''=x" + QT$ THEN S2 = 1
6131 E = (R = 0) AND (S1 = 1) AND (S2 = 1): N$ = "apostrophe_lead_roundtrip": GOSUB 7100
6135 T$ = "blob text": K = 1: GOSUB 7000: E = (R = 1): N$ = "blob_to_sqlite": GOSUB 7100: K = 0
6140 T$ = "plain line": GOSUB 7000: Q$ = QT$ + "plain LINE" + QT$: GOSUB 3000: E = (M = 1): N$ = "post_tamper_caught": GOSUB 7100
6145 T$ = "x": GOSUB 7000: Q$ = QT$ + "=x" + QT$: GOSUB 3000: E = (M = 1): N$ = "post_live_formula_caught": GOSUB 7100
6150 T$ = "x": GOSUB 7000: Q$ = QT$ + "a" + QT$ + "b" + QT$: GOSUB 3000: E = (M = 1): N$ = "post_lone_quote_caught": GOSUB 7100
6155 T$ = "": GOSUB 7000: S1 = 0: IF Q$ = QT$ + QT$ THEN S1 = 1
6156 E = (R = 0) AND (S1 = 1): N$ = "empty_record_ok": GOSUB 7100
6160 E = (REJ = 2) AND (FB = 3) AND (ROWS = 21) AND (RECS = 26): N$ = "main_line_continued_all_records": GOSUB 7100
6900 PRINT "SUMMARY:"; PASSES; "/"; PASSES + FAILS;
6910 IF FAILS = 0 THEN PRINT " ALL PASS" ELSE PRINT " FAIL"
6920 END
7000 REM run one record through the main line
7010 RECS = RECS + 1: GOSUB 1000: RETURN
7100 REM record result
7110 IF E THEN PRINT "PASS: "; N$: PASSES = PASSES + 1: RETURN
7120 PRINT "FAIL: "; N$: FAILS = FAILS + 1: RETURN
7200 REM S1 = 1 when post-parsed X$ equals input T$
7210 S1 = 0: IF X$ = T$ THEN S1 = 1
7220 RETURN
