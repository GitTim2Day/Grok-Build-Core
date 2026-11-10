# SESSION_PATTERN_MAP_2026-11-10_SCENE_LOOP

Sitting 2026-11-10 scene loop eMeet C960 4K /dev/video0.

## HIT
- camera node confirmed /dev/video0 (usb-xhci-hcd.1-1), 1920x1080 MJPEG 60fps available
- tessdata fix found (~/vosk/tessdata, TESSDATA_PREFIX)
- full-frame OCR returned real text fragments; center-crop 960x540 cleaner
- combined sampler running pid 187112: five-second seals, alert frame on two consecutive crossings above 2.0 with 30-second cooldown, clear frame on ten-second quiet, heartbeat every 12 quiet seals, 800MB free-space cutoff
- first alert frame alert_20261110_125442.jpg 121003 bytes
- status at 13:09: 22 alerts, 32 clears, 474 log lines, diff 3.60-10.66, card 1.5G free
- OCR snippets: 'PI 5 edge: 1080p path, voice (Vosk/Piper), UT', 'Phase 1 medical integrity pipeline', 'node-channel / amygdala binding', 'coordinator'

## VAL
- DIFF_PCT 20.4981 (10:52 frame) and 37.6392 (full-frame 11:30), both above 2.0 threshold
- Heartbeat revision validated: QUIET_COUNT=5 at 11:55, then 0 after movement
- Error-tested: missing ffmpeg skips cleanly, consec cooldown 30s after alert, diff math holds at 100 and 0, consec fires once per crossing pair, heartbeat fires at twelve, append stays idempotent, SHA truncation sixteen

## miss
- full-frame OCR fragmented at 18 inches
- 3-inch distance gave empty OCR (focus/framing)
- ffplay blocked device until killed pid 171034
- ocr_snippet.txt empty on first three attempts before TESSDATA_PREFIX set
- memory file updated by another process after write (drift-type miss; validate-before-reply rule now in force)
- 12:52 and 2:33 status screenshots not received by chair

## open
- animal/intruder tags
- 2.0 threshold tuning from real data
- connecter_local.py integration with scene_log.txt
- Spanish OCR pass
- audio loop (rolling 10-second buffer, overwrite on silence, retain on delta, silence threshold to be earned)
- Seagate 2TB path flip when card fills
- date-named drive mounts
- Merkle tree / capillary bed framing for LAN/WAN memory
- Orin Nano flight port
- Rabbit R1 camera/mic/speaker alert path
- AirPods Pro private alert channel

## MAP
11 rows. XLSX SHA-256 a84077fdd9f99bf2f7d2514f4a88d72319997c1184a663e3a464bb937d1e8faa7. CSV sibling SHA-256 ca2f280d129d3163ca8d8d685f454ece3995c09161978be61341d140eba18257. Both in artifacts/connecter_suite. CSV backup follows standing 2026-11-04 eight-step rule.

## SHELVES
scene_loop local on Pi only (pid 187112). Email hop 1a1c6b6d3ff9d1b4. Sibling of connecter-suite 70d95ed77d0020497b0f6976561ea4425355e698439d2f014a8c92efe9286012, not a merge. Pointer only; body is the map.

## STANDING
validate before stating sent. Notification count is independent check (two emails = four notifications). Append-on-evoke thin row. Fresh clock before every about-time.