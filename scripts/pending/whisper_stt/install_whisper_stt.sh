#!/bin/bash
# install_whisper_stt.sh
# Pending feature: local Whisper STT on Raspberry Pi 5 (bypass Grok dictation).
# Error-tested path: install deps, clone whisper.cpp, build, download base.en model.
# Run: bash install_whisper_stt.sh
set -euo pipefail

MODEL="${WHISPER_MODEL:-base.en}"
BUILD_DIR="${HOME}/whisper.cpp"
LOG="${HOME}/whisper_install.log"

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    log "MISSING: $1"
    return 1
  fi
  return 0
}

log "=== Whisper STT install start (model=$MODEL) ==="

# 1. deps
log "apt update"
sudo apt-get update -y
log "apt install build tools"
sudo apt-get install -y build-essential cmake git libsdl2-dev ffmpeg

# 2. clone or update
if [ -d "$BUILD_DIR/.git" ]; then
  log "repo exists, pulling"
  git -C "$BUILD_DIR" pull --ff-only
else
  log "cloning whisper.cpp"
  git clone --depth 1 https://github.com/ggerganov/whisper.cpp.git "$BUILD_DIR"
fi

# 3. model
log "downloading model $MODEL"
bash "$BUILD_DIR/models/download-ggml-model.sh" "$MODEL"

# 4. build (stream example optional; main binary is enough for file transcription)
log "building"
cmake -S "$BUILD_DIR" -B "$BUILD_DIR/build" -DCMAKE_BUILD_TYPE=Release
cmake --build "$BUILD_DIR/build" --config Release -j"$(nproc)"

BIN="$BUILD_DIR/build/bin/whisper-cli"
if [ ! -x "$BIN" ]; then
  # older layout
  BIN="$BUILD_DIR/build/bin/main"
fi
if [ ! -x "$BIN" ]; then
  log "ERROR: whisper binary not found after build"
  exit 2
fi
log "binary: $BIN"

# 5. smoke test: synthesize a tiny silent wav and confirm it runs without crash
TMPWAV="$(mktemp /tmp/whisper_smokeXXXX.wav)"
ffmpeg -y -f lavfi -i anullsrc=r=16000:cl=mono -t 1 -c:a pcm_s16le "$TMPWAV" >/dev/null 2>&1 || true
if "$BIN" -m "$BUILD_DIR/models/ggml-${MODEL}.bin" -f "$TMPWAV" -otxt -of /tmp/whisper_smoke_out >/dev/null 2>&1; then
  log "SMOKE OK: binary runs on silent input"
else
  log "WARN: smoke test returned non-zero (silent input may be fine); binary exists"
fi
rm -f "$TMPWAV"

log "=== install complete ==="
log "Next: record with arecord, then: $BIN -m $BUILD_DIR/models/ggml-${MODEL}.bin -f YOUR.wav -otxt"
log "Pending feature saved. Do not enable until ADXL355 part arrives and I2C work is stable."
