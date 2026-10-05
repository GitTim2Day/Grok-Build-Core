10 REM need_gosub_one_node.bas
20 REM Timothy Norman
30 REM Standing 2026-10-05: append work; unused is archived, not deleted.
40 REM Pattern: main line keeps moving; one conflict -> one node GOSUB, then RETURN.
50 REM Unsealed BASIC pack (Grok-Build-Core basic/).
60 GOTO 9000
100 REM main line keeps moving
110 IF NEED = 0 THEN GOTO 200
120 GOSUB 1000
200 REM continue
210 RETURN
1000 REM one conflict, one node, then RETURN
1010 RETURN
9000 REM ========== SELF-CHECK (bwbasic) ==========
9010 PASS = 0
9020 FAIL = 0
9100 REM path NEED=0: skip GOSUB 1000
9110 NEED = 0
9120 GOSUB 100
9130 PASS = PASS + 1
9200 REM path NEED=1: take GOSUB 1000
9210 NEED = 1
9220 GOSUB 100
9230 PASS = PASS + 1
9300 PRINT "PASS="; PASS; " FAIL="; FAIL
9310 IF FAIL > 0 THEN PRINT "NEED_GOSUB FAIL": END
9320 PRINT "NEED_GOSUB ALL PASS"
9330 END
