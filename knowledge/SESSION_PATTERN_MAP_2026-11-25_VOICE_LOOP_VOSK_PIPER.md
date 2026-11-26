# SESSION_PATTERN_MAP_2026-11-25_VOICE_LOOP_VOSK_PIPER

## Voice Loop (Vosk → Piper)

- Vosk STT (no-sudo, validated on shepherd) → Piper TTS (en_US-lessac-medium, proven 2026-11-23 read-aloud model)
- Device selector: JBL / AirPods Pro / any active Bluetooth sink
- Fail-closed: empty audio → no synthesis; non-ASCII transcript rejected before Piper
- Terminates when loop stops. No resident process.
- Error-test-mitigate: 1 defect (sudo in comment) → fixed → re-test clean
- Open: wire Whisper.cpp (locked 2026-11-17) as STT upgrade path later; OCR deferred to multi-camera work
- Sibling of neural_channel_operators and private_connecter_local_scanner. Not a merge.
- Drive gap: local-seal sub-agent queued.
