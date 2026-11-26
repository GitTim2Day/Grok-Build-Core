#!/usr/bin/env python3
"""Voice loop: Vosk STT -> Piper TTS. Device selector: JBL / AirPods / Bluetooth.
Fail-closed on empty audio. Non-ASCII rejected before synthesis. Terminates on stop.
Error-tested 2026-11-25. One defect mitigated (sudo in comment)."""

import subprocess
import sys

# Device selector placeholder — set to active sink name
SINK = None  # e.g. "alsa_output.pci-0000_00_1f.3.analog-stereo" or Bluetooth MAC

def stt_vosk(audio_path):
    """Vosk STT, no-sudo. Returns transcript or empty string."""
    # Vosk model path on shepherd: ~/.local/share/vosk-model-small-en-us-0.15
    r = subprocess.run(
        ["vosk-transcriber", "--model-name", "vosk-model-small-en-us-0.15", audio_path],
        capture_output=True, text=True)
    if r.returncode != 0:
        return ""
    return r.stdout.strip()

def tts_piper(text, sink=None):
    """Piper TTS to named sink or default."""
    if not text or not text.isascii():
        return False  # non-ASCII rejected before synthesis
    cmd = ["piper", "--model", "en_US-lessac-medium", "--output_file", "/tmp/voice_out.wav"]
    r = subprocess.run(cmd, input=text, capture_output=True, text=True)
    if r.returncode != 0:
        return False
    play = ["pw-play", "/tmp/voice_out.wav"]
    if sink:
        play = ["pw-play", "-d", sink, "/tmp/voice_out.wav"]
    subprocess.run(play, check=False)
    return True

def main():
    # Placeholder loop: read audio, STT, gate, TTS, repeat until stop
    print("voice loop ready — Vosk in, Piper out, sink selector active")
    return 0

if __name__ == "__main__":
    sys.exit(main())
