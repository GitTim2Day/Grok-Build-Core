# Table of Contents — Voice Seat Circular Loop

Extracted from SESSION_PATTERN_MAP_2026-11-28_VOICE_SEAT_CIRCULAR_LOOP.md as standalone reference.

## 15 Sections

1. Architecture overview with the Kreis diagram
2. The twelve-o'clock dispatcher (if-then-else: wake / close / pause)
3. Front and back door translators
4. Vosk (STT)
5. The English middle ring (permanent transcript)
6. Ollama llama3.2:3b (thinking layer)
7. Piper (TTS out)
8. End phrases (good night, that's all for the day)
9. Three-layer immutable core protection (chattr +i, boot SHA check, no-write process)
10. Thin regex filters (before core, after core)
11. Edge additions (bots, old connectors — outer surfaces only)
12. Stick languages (English resident, others on stick)
13. The bidirectional index (design section ↔ build step, plus 13 prior sealed skills)
14. Ten-step build order (produce-validate-mitigate-re-test-distribute between each)
15. Open items (Vosk path miss superseded by front-door translator; language GOSUBs; recipient text channel; loop-back wire; token file for X-post ConnectEr)

## Related Today's Seals

- Matrix-triangles-subjects map (session-map-2026-11-28-matrix-triangles-subjects)
- X-post ConnectEr (BASIC + shell wrapper, OAuth 1.0a)
- Convergence gate (session-map-2026-11-28-convergence-gate)
- Six-tool toolkit
- Direction-only Verilog adder
- H-bar strip across Maxwell, Bekenstein, Hawking

## Build Order Reminder

1. English loop + dispatcher
2. Loop-back wire
3. End phrases + seal check
4. Front-door translator (fasttext-langdetect, venv, no-sudo)
5. Back-door translator + language GOSUBs + recipient text channel

Six-pillar SVCT: content · context · data · time · semantics · validation.
