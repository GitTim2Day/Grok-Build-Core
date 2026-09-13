# Pending Feature: Local Whisper STT on Raspberry Pi 5

**Status:** PENDING — do not enable until ADXL355 part arrives and I2C work is stable.
**Goal:** Bypass Grok/iPhone dictation. Run Whisper locally so devices can be spoken to directly.

## Why
Grok voice dictation mishears technical terms. Local Whisper gives full control over model, vocabulary, and error handling. Works on any device with a mic — no iPhone in the middle.

## Files
- `install_whisper_stt.sh` — installs deps, clones whisper.cpp, builds, downloads base.en model, smoke-tests.
- `transcribe_whisper.py` — records or transcribes a wav; prints text or `E_WHISPER: <reason>`. Never invents text.

## Install (on Pi)
```bash
bash install_whisper_stt.sh
```
Expect 8–12 minutes on Pi 5. Model ~144 MB.

## Use
```bash
python3 transcribe_whisper.py --list          # see mics
python3 transcribe_whisper.py --record 5      # speak, get text
python3 transcribe_whisper.py --file clip.wav
```

## Error policy (sealed)
- No binary → clear error, no crash.
- Empty/silent input → `E_WHISPER: whisper returned empty text`.
- arecord failure → surfaced, not swallowed.
- Model missing → surfaced before any claim.

## Next steps when ready
1. Run install on the Pi.
2. Test with E-Meet USB mic or JBL (if it has a mic).
3. Pipe output into the Grok prompt loop.
4. Port to other devices the same way.

## Sources
- whisper.cpp: https://github.com/ggerganov/whisper.cpp
- Pi 5 guidance: ggml-org discussions, solarsamuel/pi5_whisper_voice_assistant
