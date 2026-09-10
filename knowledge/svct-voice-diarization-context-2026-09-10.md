# SVCT Voice Diarization + Context Match — OPEN FEATURE

**Status:** OPEN — to be worked.
**Logged:** 2026-09-10T22:10:00-04:00 (pickup).
**Source:** Timothy, voice session. Request: if the work exists in SVCT hops, recover it; if not, add it as an open feature.

## The gap

Voice mode delivers a raw transcript with **no speaker labels**. Every utterance reaches the chair, so asides meant for the room get answered. The fix is **speaker diarization** bound to context: tag each voice, match it to the active dialogue, and only respond when the utterance is directed at the chair.

## What already exists (recovered, not invented)

**Gmail — 18 Aug 2026, Poly Math call (3m 59s, Lawrenceville GA):**
- Provenance token `b608614161de7a73425ae86a14bdfd06cac7dc1859fb147f9dc2a73c11cdb564` — type `VOICE_DIARIZATION_PROVENANCE`, standing `DEMONSTRATED_IN_SIMULATION`. Four pillars: content, context, data, time. GPS anchor 33.9332N, 84.1173W.
- Three speakers profiled by FFT: pitch mean, pitch CoV, F1/F2, spectral flatness. Speaker 0 = Tim (~299 Hz, SF 0.263, likely human). Speaker 1 = Poly/AI (bimodal SF — TTS tell). Speaker 2 = unknown (~245 Hz, likely human, unnamed).
- Fast-switch discriminator hierarchy (Seal v3): amplitude envelope → pitch → rhythm/tempo (real-time) → formants → spectral flatness (confirm/log only). Never wait on layer five to switch.
- Human vs AI tell: bimodal spectral flatness across bursts.
- Defect logged: wall-clock timeline in the token was corrupt (11 of 14 bursts wrong); token marked SUPERSEDED, v1.1 not yet minted. Whisper transcripts never returned from A15.

**Notion:** `svct-pickup-timestamp-boot`, `svct-cell-three-anchor`, `mac-hive-session-map` (MAC + voice + SVCT), `poly-voice-standing-prompt`.

**GitHub:** no `SVCT` + diarization hit in Grok-Build-Core.

## The open feature

1. **Diarization layer** on the voice path — label each speaker in real time (research: pyannote, NVIDIA Sortformer, AssemblyAI; commodity, not invented).
2. **Context bind** — match the labeled voice to the active dialogue thread, not just the raw transcript.
3. **Directed-speech gate** — respond only when the utterance is addressed to the chair; stay quiet on room asides.
4. **SVCT provenance** — every diarized turn stamped with the four pillars + GPS/wall clock, same as the 18 Aug token.
5. **A15 recovery** — run the 14 ffmpeg extractions, transcribe unknown_burst1 first, mint token v1.1 with corrected time pillar.

## Standing

The 18 Aug work is real and on the shelf. The live product gate (diarization → context → directed response) is **not built**. This feature closes that gap. Do not regenerate the 18 Aug analysis — recover it.

HOLD: at-integration-hold-2026-09-09
