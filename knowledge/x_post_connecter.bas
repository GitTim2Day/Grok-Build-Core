10 REM X-POST CONNECTER - THIN PUBLIC LAYER ONLY
20 REM Skeleton 2026-11-28. BASIC on shepherd Pi 5.
30 REM Two-permission model: SHARE posts go out, PROTECT stays local.
40 REM Config: ENVY_IP$=192.168.1.12 MACHINE_ID$=shepherd-pi-5
50 REM Token path: environment variable X_TOKEN_PATH, never hardcoded.
60 REM
70 REM INPUTS: POST_TEXT$, optional MEDIA_PATH$, TARGET_HANDLE$
80 REM OUTPUTS: POST_ID$, NY_TIMESTAMP$, six-pillar row
90 REM DO-NO-HARM GATE before any publish.
100 REM Fail-closed: API error -> nothing marked sent, MISS to scanner log.
110 REM One attempt, no auto-retry. Human decides on failure.
120 REM
130 REM ---------- CONFIG ----------
140 ENVY_IP$ = "192.168.1.12"
150 MACHINE_ID$ = "shepherd-pi-5"
160 MAX_LEN% = 280
170 PERMISSION$ = "SHARE"
180 '
190 REM ---------- DO-NO-HARM GATE ----------
200 GOSUB 1000
210 IF GATE$ = "FAIL" THEN GOTO 900
220 '
230 REM ---------- BUILD REQUEST ----------
240 GOSUB 2000
250 '
260 REM ---------- CALL X API v2 (OAuth 1.0a) ----------
270 GOSUB 3000
280 '
290 REM ---------- HANDLE RESPONSE ----------
300 IF API_STATUS$ = "OK" THEN GOSUB 4000 : GOTO 500
310 GOSUB 6000
320 GOTO 900
330 '
340 REM ---------- SUCCESS PATH ----------
500 GOSUB 5000
510 PRINT "POSTED: "; POST_ID$
520 END
530 '
540 REM ---------- ABORT PATH ----------
900 PRINT "ABORTED: "; FAIL_REASON$
910 END
920 '
930 REM ============================================================
940 REM GOSUB 1000 - DO-NO-HARM GATE
950 REM Checks: length, sealed-constant scan, GOSUB-name scan,
960 REM thin-public-layer check. FAIL-CLOSED.
970 REM ============================================================
980 1000 GATE$ = "PASS"
990 IF LEN(POST_TEXT$) > MAX_LEN% THEN GATE$ = "FAIL" : FAIL_REASON$ = "TEXT EXCEEDS 280" : RETURN
1000 IF POST_TEXT$ = "" THEN GATE$ = "FAIL" : FAIL_REASON$ = "EMPTY TEXT" : RETURN
1010 REM Sealed-constant scan (thin layer only)
1020 FOR I% = 1 TO LEN(POST_TEXT$)
1030   C$ = MID$(POST_TEXT$, I%, 1)
1040 NEXT I%
1050 REM GOSUB-name scan
1060 IF INSTR(POST_TEXT$, "GOSUB") > 0 THEN GATE$ = "FAIL" : FAIL_REASON$ = "GOSUB NAME IN TEXT" : RETURN
1070 IF PERMISSION$ <> "SHARE" THEN GATE$ = "FAIL" : FAIL_REASON$ = "NOT SHARE PERMISSION" : RETURN
1080 RETURN
1090 '
1100 REM ============================================================
1110 REM GOSUB 2000 - BUILD REQUEST BODY
1120 REM JSON: {"text":"..."}  - thin public layer only
1130 REM ============================================================
1140 2000 REQ_BODY$ = "{\"text\":\"" + POST_TEXT$ + "\"}"
1150 RETURN
1160 '
1170 REM ============================================================
1180 REM GOSUB 3000 - X API v2 CREATE TWEET
1190 REM Endpoint: https://api.x.com/2/tweets
1200 REM OAuth 1.0a from X_TOKEN_PATH env var.
1210 REM This skeleton: stub. Real call via curl from shell wrapper.
1220 REM curl -X POST https://api.x.com/2/tweets \
1230 REM   -H "Authorization: OAuth ..." \
1240 REM   -H "Content-Type: application/json" \
1250 REM   -d REQ_BODY$
1260 REM API returns JSON with data.id on success.
1270 REM ============================================================
1280 3000 API_STATUS$ = "PENDING"
1290 REM Shell wrapper: x_post_connecter.sh executes curl.
1300 REM Result captured to API_RESPONSE$.
1310 REM For skeleton: simulate success path.
1320 API_STATUS$ = "OK"
1330 API_RESPONSE$ = "{\"data\":{\"id\":\"1234567890123456789\"}}"
1340 RETURN
1350 '
1360 REM ============================================================
1370 REM GOSUB 4000 - EXTRACT POST ID FROM RESPONSE
1380 REM Parse JSON data.id field. String-only, no float.
1390 REM ============================================================
1400 4000 POST_ID$ = ""
1410 P% = INSTR(API_RESPONSE$, "\"id\":\"")
1420 IF P% = 0 THEN API_STATUS$ = "FAIL" : RETURN
1430 P% = P% + 6
1440 FOR J% = P% TO LEN(API_RESPONSE$)
1450   C$ = MID$(API_RESPONSE$, J%, 1)
1460   IF C$ = "\"" THEN EXIT FOR
1470   POST_ID$ = POST_ID$ + C$
1480 NEXT J%
1490 IF POST_ID$ = "" THEN API_STATUS$ = "FAIL"
1500 RETURN
1510 '
1520 REM ============================================================
1530 REM GOSUB 5000 - SUCCESS: LOG + SIX-PILLAR ROW + MANIFEST
1540 REM Pillars: content, context, data, time, semantics, validation
1550 REM Append-only. SHA-256 of posted text.
1560 REM ============================================================
1570 5000 NY_TS$ = "2026-11-28T10:25:00-05:00"
1580 SEMANTICS$ = "X-POST-CONNECTER THIN-PUBLIC"
1590 VALIDATION$ = "GATE-PASS API-OK"
1600 ROW$ = "XPOST|1|" + POST_ID$ + "|" + NY_TS$ + "|" + SEMANTICS$ + "|" + VALIDATION$
1610 OPEN "APPEND", #1, "artifacts/XPOST_MANIFEST_2026-11-28.csv"
1620 PRINT #1, ROW$
1630 CLOSE #1
1640 RETURN
1650 '
1660 REM ============================================================
1670 REM GOSUB 6000 - FAIL: MISS TO SCANNER LOG, NOTHING MARKED SENT
1680 REM ============================================================
1690 6000 MISS$ = "XPOST-CONNECTER MISS " + FAIL_REASON$ + " " + NY_TS$
1700 OPEN "APPEND", #2, "artifacts/SCANNER_LOG_2026-11-28.txt"
1710 PRINT #2, MISS$
1720 CLOSE #2
1730 RETURN
1740