# SESSION PATTERN MAP 2026-11-22 BW BASIC PURE STRING CUT

Stamp: Sunday, November 22, 2026 11:30:55 AM America/New_York

HIT: Pure string cut route locked on Pi 5 shepherd.
VAL: bwbasic /tmp/string_cut.bas produced
  SRC=0.70710678
  CUT=0.707106
MISS: none on the contract.
OPEN: drop GOSUB into brain_control.bas; archive prior numeric path.

## Contract
- Source remains a string.
- Cut built with LEFT$/MID$/INSTR only.
- No numeric value reaches PRINT.
- Truncate toward zero.
- Places is the parameter (test case places=6).
- Expected: 0.70710678 → 0.707106

## GOSUB
```
1000 REM GOSUB_STRING_CUT
1010 DOT = INSTR(SRC$, ".")
1020 IF DOT = 0 THEN CUT$ = SRC$ : RETURN
1030 WHOLE$ = LEFT$(SRC$, DOT - 1)
1040 FRAC$ = MID$(SRC$, DOT + 1)
1050 IF LEN(FRAC$) > PLACES THEN FRAC$ = LEFT$(FRAC$, PLACES)
1060 CUT$ = WHOLE$ + "." + FRAC$
1070 RETURN
```

## Pair log confirmation (same sitting)
pair_log.txt also shows LEFT$ cuts matching the contract:
  1 ,0.70710678,0.707106
  2 ,3.14159265,3.141592
  3 ,1.41421356,1.414213
  4 ,2.71828182,2.718281
  5 ,1.61803398,1.618033

## Posture
Archive, do not delete, the prior numeric PRINT path.
This is the route.

Pointer skill: session-map-2026-11-22-bw-basic-string-cut
SHA-256: 1d87bf1d68c896272d5046a42554340382dfc5387d64033118ed4ac6a16ebae5
Ledger hop: 1a20418d80a197fe
