# SESSION_PATTERN_MAP_2026-11-28_VOICE_SEAT_CIRCULAR_LOOP

Local: artifacts/SESSION_PATTERN_MAP_2026-11-28_VOICE_SEAT_CIRCULAR_LOOP.md
Size: 8062 bytes, 273 lines
SHA-256: ae611825b197ff480b0c395034c85ed69219aab2329df3b823d273567856fe3e

## Outline (15 sections)

1. Architecture overview — Kreis diagram
2. Twelve-o'clock dispatcher (if-then-else: wake / close / pause)
3. Front-door translator (before Vosk)
4. Vosk STT (English only)
5. English middle ring (oxaloacetate — regenerated, never consumed)
6. Ollama llama3.2:3b thinking layer
7. Piper TTS out (AirPods)
8. Back-door translator (after Piper)
9. End phrases (good night, that's all for the day)
10. Three-layer immutable core (chattr +i, boot SHA check, no-write process)
11. Thin regex filters (pre and post)
12. Edge additions (bots, old connectors — outer only)
13. Stick languages (English resident, others on stick)
14. Bidirectional index
15. Ten-step build order (produce-validate-mitigate-re-test-distribute each step)

## Dispatcher Logic

- If wake word → open 5-second window → Vosk → English text → brain
- If close word → exit loop → seal check
- If pause word → wait at gate, no brain call
- Mutually exclusive → if-then-else, not separate if-thens, not GOSUB

## Core Protection

- Layer 1: chattr +i on core files
- Layer 2: boot-time SHA-256 vs sealed manifest; mismatch = alert, no start
- Layer 3: core runs as separate process, no write permission to own source tree

## Bidirectional Index

Design section ↔ build step, both directions. Cross-refs to 13 prior sealed skills 2026.

## Open Items

- Vosk models-path miss superseded by front-door translator design
- Language front/back door GOSUBs, recipient text channel, loop-back wire remain open

Pointer skill: session-map-2026-11-28-voice-seat-circular-loop