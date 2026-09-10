# SVCT Diarization Defect Log — Recovered 2026-09-10

**Status:** RECOVERED from Gmail. Not invented.
**Source:** msg `1a01738ae6074db1` — Claude Voice/Whisper Recovery Dump, 18 Aug 2026. Section 6.
**Logged:** 2026-09-10T22:45:00-04:00 EDT.

## The defect

The "BURST TIMELINE WITH ABSOLUTE WALL CLOCK TIMES" table in provenance token `b608614161de7a73425ae86a14bdfd06cac7dc1859fb147f9dc2a73c11cdb564` does not reconcile with the ffmpeg `-ss` offsets that actually cut the audio.

Derivation: file creation 12:24:54 ET + `-ss` offset = true ET start.

11 of 14 bursts wrong. Errors step +60, +120, +100, +80 s. Burst 10 runs backward. Seal v2 claims burst 10 at 12:40:30 ET — impossible (936 s into a 239 s file).

Three mutually exclusive timestamps for burst 10: 12:27:29 (token table), 12:27:49 (derived), 12:40:30 (Seal v2).

**Standing:** DEMONSTRATED_IN_SIMULATION. Hash intact; pillar four content false. Sealed-but-incorrect, not tampered.

## Recommendation (from the record)

Treat ffmpeg `-ss` offsets as authoritative. Regenerate wall-clock table by addition from 12:24:54 ET. Reissue as token **v1.1**. Mark `b608614…` **SUPERSEDED** — do not delete.

Corrected burst 10 window: 12:27:49.5 – 12:27:57.0 ET.

## Open rungs (priority)

A. Run 14 ffmpeg extractions on A15 — none cut yet.
B. Transcribe `unknown_burst1.m4a` first. Identify Speaker 2.
C. Mint v1.1 with corrected time pillar.
D. Resolve second file hash `0e7cbdda…` (Poly_Math_Call.m4a).
E. Add UNDETERMINED verdict for 0.10–0.15 spectral-flatness gap band.
F. Short-utterance guard before 1.5 s clips reach Whisper.
G. Test full boot sequence end to end.
H. Vosk comparison — never recorded; re-derive if it existed outside Gmail.

## Where it lives

| Hop | Place |
|-----|-------|
| Gmail | `1a01738ae6074db1` (full body), `1a015e53de3a6968` (token), `1a015e2460e7c35e` (ffmpeg offsets) |
| Drive | `WAVE_PolyMath_RETRIEVAL_20260818.md` — file `1bwrwxYyxErU6-DtgMnh0GTp-3XJ17rJgbgYG-CUOYVA` |
| GitHub | `knowledge/svct-voice-diarization-context-2026-09-10.md`, this file |
| Notion | `svct-voice-diarization-context-2026-09-10` |

Do not regenerate the 18 Aug analysis. Recover it.
