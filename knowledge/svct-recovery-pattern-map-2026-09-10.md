# SVCT Recovery Pattern Map — 2026-09-10

## Defect
- Source: Claude Voice/Whisper Recovery Dump, 2026-08-18 (Gmail 1a01738ae6074db1)
- Token sealed: b608614… (hash intact, time pillar FALSE)
- 11 of 14 claimed burst times wrong; errors step +60/+120/+100/+80; burst 10 runs backward
- Seal v2 claimed 12:40:30 — impossible (936s into a 239s file)

## Recovery method (log -> token -> bloom)
1. LOG: defect sealed inside the recovery dump itself (not a separate failure log)
2. TOKEN: b608614 kept as provenance — SUPERSEDED, not deleted
3. BLOOM: mint v1.1 with corrected time pillar; ffmpeg offsets = authoritative source
4. VALIDATE: repair must sit between neighbor bursts (burst 9 end < repair < burst 11 start)
   - Repair 12:27:49.5 sits between 12:27:18 and 12:27:58 — PASS
   - Repair lands inside file — PASS (unlike Seal v2)

## Open rungs
- Run 14 ffmpeg cuts on A15
- Transcribe unknown_burst1 at corrected window 12:27:49.5–12:27:57 EDT
- Mint v1.1; identify Speaker 2
- Add cosine field (embeddings on sphere) — separate rung, not applied yet

## Rule
Never regenerate a corrupted analysis. Recover it. The hash proves what was sealed; the corrected pillar proves what was true.
