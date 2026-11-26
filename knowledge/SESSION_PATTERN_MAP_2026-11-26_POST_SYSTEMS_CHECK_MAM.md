# SESSION_PATTERN_MAP_2026-11-26_POST_SYSTEMS_CHECK_MAM

## 1. MCPub CONNECTER dry-run
1262 verified endpoints, 50 on page one. Latency 160-4353 ms. Six-pillar row sealed. Gmail 1a21882a655a508fe. Automation saved, schedule disabled, manual only. Token estimate 1500-3000/run, 22500-45000/day, ~1-2% SuperGrok bar.

## 2. CSVSONL
3 rows in, 3 rows out, round-trip true. SHA f6186cb707eeee9e8c076b44f552273295c86284e62a4f6b4bcf906a91d0253. JSONL append-only, each line one sealed record, streams without loading whole file. Edge-friendly for shepherd RAM ceiling. Pointer skill csvsonl. Sibling of CSVSON Research Monitor 2026-11-21, not a merge.

## 3. CSVSON ragged-row rule
Pad with empty fields, never drop keys silently. Empty string, not NAN — NAN is float, breaks no-float64 rule. Same contract as CSVSONL.

## 4. CSVSONLD concept
DSV variant, tab or pipe delimiter, same round trip.

## 5. Universal intake concept
One front door, CSV as lingua franca, every format a dialect in or out. When CSV can't accommodate (PNG, DICOM, WAV, TXT, PDF), switch to SQLite or SQL. WAL mode for audit chaining, KBL Phase 1 precedent.

## 6. Cross-ref rows
CSVSON (2026-05, 2M-row edge run, 90% RAM, 100% cleaned, parse_csvson in primary.py, CSVSON Research Monitor 2026-11-21 gosub_truncate_string fingerprint) → bidirectional index 4col SVCT (2026-11-25). JCJ pipeline (2026-05, bidirectional 3-4-col indexing before SQLite, proposed rename iR/CSV/iR/JSON, 1B-row discussed 2GB sandbox executed, KBL Phase 1 audit chaining SHA-256 WAL-mode) → bidirectional index 4col SVCT (2026-11-25) + sync spine (2026-11-26).

## 7. Link map
SESSION_PATTERN_MAP_2026-11-26_LINK_MAP.md — ancestor/sibling graph. Gmail hop 1a218804ebf79cb4.

## 8. Tomorrow's plan (post-ENVY)
Step 1: voice loop Vosk STT + Piper TTS on shepherd, JBL sink, eMeet mic. Step 2: Llama 3.2 1B thinking layer. Step 3: UT2 multilingual. Step 4: MP4 ingest — frame extraction at fixed intervals, Tesseract per frame, decode timestamps stamped, aligned to audio clock. Step 5: MP3 archive via ffmpeg from live WAV. MP4 container for video-audio sync. MP3 for sightless Pi 5 archive. WAV for live loop.

## 9. Gel/hybrid voxel storage
Gel temporary, hybrid keeps compressed MP3 + timestamped transcript text without raw WAV. Pi streams frames through Tesseract one at a time, never holds MP4 in memory.

## 10. Open items
Drive gap, now_ny swapped (commit 0abf8d60), AirPods selector not coded, ENVY test ~11:00, mesh layer design when named, UT2 step 3, thermal thresholds, phase-change sizing, LabCorp integration, renal-adjusted dosing, individualized thresholds.

Do No Harm first. Append-only. Six-pillar SVCT: content context data time semantics validation.