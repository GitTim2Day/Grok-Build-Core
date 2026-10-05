# SESSION_GOSUB_STREAMLINE_2026-09-17
**Purpose:** Minimal GOSUB-style logic for save-to-project pattern-map → audit → second-pass → distribute.  
**Rule:** IF/THEN/ELSE, GOSUB/RETURN, DO UNTIL. Lean twins: BASIC + Python + C++. Fail-closed. Archive only. DRAFT mail never Send.

## Algorithm (one)
```
MAIN:
  GOSUB LOAD_FACTS
  GOSUB WRITE_MAP1
  GOSUB AUDIT
  IF audit_pass = 0 THEN GOTO FAIL_CLOSED
  GOSUB SECOND_PASS
  GOSUB STREAMLINE_CODE
  GOSUB DIST_NOTION
  GOSUB DIST_GITHUB   ' may BLOCKED
  GOSUB DIST_DRIVE
  GOSUB DIST_SHEETS_ROW
  GOSUB DIST_GMAIL_DRAFT  ' never Send
  GOSUB CONFIRM
  RETURN

LOAD_FACTS:
  DO UNTIL research_*.md scanned
    cite path only if file exists
  LOOP
  RETURN

AUDIT:
  FOR each claim
    IF earned THEN mark EARNED ELSE mark UNFOUND
  NEXT
  IF any fabricated URL THEN audit_pass=0 ELSE audit_pass=1
  RETURN

DIST_GITHUB:
  TRY create knowledge/SESSION_PATTERN_MAP_2026-09-17.md
  IF sealed OR denied THEN status=BLOCKED ELSE status=OK
  RETURN

DIST_GMAIL_DRAFT:
  IF create_draft available THEN draft only ELSE BLOCKED_SEND
  ' never call send_draft / send_message
  RETURN

FAIL_CLOSED:
  write gaps; stop inventing
  RETURN
```

## Lean twin files
- `/workspace/session_gosub_2026-09-17/save_to_project.bas`
- `/workspace/session_gosub_2026-09-17/save_to_project.py`
- `/workspace/session_gosub_2026-09-17/save_to_project.cpp`
- This doc: `/workspace/SESSION_GOSUB_STREAMLINE_2026-09-17.md`
