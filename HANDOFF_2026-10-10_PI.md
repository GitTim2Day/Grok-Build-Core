# HANDOFF 2026-10-10 (chat -> Pi 5)

Author: Timothy Norman (sole author). Claude = tool/validator.
State at 09:50 ET: everything below is on GitHub main (Grok-Build-Core), verified from a
fresh clone. Run the steps in order; each is one line. Report outputs back to Tim.

## Done in chat (EARNED in the sandbox, ASSERTED on the Pi until run there)
- mapbook/: address finder (Py/C++ 15/15 key) + OSM streamline (Py/C++, spec v1.6,
  defects S1-S6, 2,200 fuzz 0 mismatches, mutants 31/31). Pi run pending.
- edge-canvas-kit runner v2: need-driven reader, no thread (16/16 leak tests).
- edge-canvas-kit mask v2: known names -> John Q. Public / Jane Doe / Richard Roe /
  Mary Major (same set for demos and test forms). Self-check 327 pass; mutants 71/76,
  the 5 survivors need Chromium (4) or bwbasic (1).
- routes/route_check_pi.sh: reads the 21 register sources blocked from chat.
- Notion register: 6 GOV-FIRST rows; 28 rows moved to EARNED, 21 BLOCKED (Pi reads them).
- Daily BOLO scheduled task 07:49 ET (GOV-FIRST sources first).

## Pi steps (in order)
1. sudo apt install -y g++ zlib1g-dev bwbasic
2. cd ~/work && (git clone https://github.com/GitTim2Day/Grok-Build-Core.git || (cd Grok-Build-Core && git pull))
3. mkdir -p ~/work/maps && wget -P ~/work/maps https://download.geofabrik.de/north-america/us/georgia-latest.osm.pbf
4. cd ~/work/Grok-Build-Core/mapbook && bash run_pi.sh ~/work/maps/georgia-latest.osm.pbf
5. cd ~/work/Grok-Build-Core && bash routes/route_check_pi.sh
6. cd ~/work/Grok-Build-Core/edge-canvas-kit && python3 selfcheck.py && python3 mutants.py
   (with bwbasic installed the BASIC lane runs; Chromium only if Tim chooses)
7. Daemon census (one line, writes ~/work/daemon_census.txt):
   { echo "== running"; systemctl list-units --type=service --state=running --no-pager --no-legend; echo "== enabled at boot"; systemctl list-unit-files --type=service --state=enabled --no-pager --no-legend; echo "== timers"; systemctl list-timers --all --no-pager --no-legend; echo "== user"; systemctl --user list-units --type=service --state=running --no-pager --no-legend; echo "== cron"; crontab -l; ls /etc/cron.d; echo "== ports"; sudo ss -tulpn; echo "== my processes"; ps -u $USER -o pid,etimes,rss,cmd --sort=-rss | head -25; } > ~/work/daemon_census.txt 2>&1; wc -l ~/work/daemon_census.txt

8. Add the boot rule to the Pi's CLAUDE.md (append, do not rewrite):
   printf '\n## Phase 0 (Tim 2026-10-10)\nFirst thing in any new chat or process: if the daily BOLO scheduled task has not run today after 07:49 ET, or any task failed with a usage limit in the last 8 days, run it once before anything else. Fetch URLs directly; never ask Tim to paste them. Read the newest HANDOFF_*.md in ~/work/Grok-Build-Core.\n' >> ~/work/CLAUDE.md && tail -4 ~/work/CLAUDE.md && sha256sum ~/work/CLAUDE.md

## What to report
- Step 4: seconds, the three output sizes and SHA-256 lines, first 3 address rows.
- Step 5: the printed lines (HTTP code per source) and the TSV path.
- Step 6: TOTAL line and MUTANTS line.
- Step 7: the census file.
- Step 8: the last 4 lines and new SHA-256 of CLAUDE.md.

## Open decisions for Tim
- Address finder Q1-Q3 (PO boxes, non-US, street-only rows into the book).
- Daemon attack order after the census: runner done; next camera OCR -> GOSUB OCR_ONE,
  accelerometer -> data-ready interrupt, canvas server -> socket activation + idle stop.
- Chromium vs Google Chrome for the UI smoke test (Chromium preferred if already present).
- Usage limit: weekly source watch and monthly register review failed their last runs.
