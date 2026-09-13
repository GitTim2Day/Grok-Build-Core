#!/usr/bin/env python3
"""transcribe_whisper.py
Pending feature: local Whisper STT wrapper for Pi 5.
Bypasses Grok/iPhone dictation. Error-tested: no silent failure, no invented text.
Usage:
  python3 transcribe_whisper.py --record 5
  python3 transcribe_whisper.py --file audio.wav
  python3 transcribe_whisper.py --list
"""
from __future__ import annotations
import argparse, os, subprocess, sys, tempfile, time

WHISPER_DIR = os.path.expanduser("~/whisper.cpp")
MODEL = os.environ.get("WHISPER_MODEL", "base.en")
MODEL_PATH = os.path.join(WHISPER_DIR, "models", f"ggml-{MODEL}.bin")

def find_binary() -> str:
    for p in (os.path.join(WHISPER_DIR, "build", "bin", "whisper-cli"),
              os.path.join(WHISPER_DIR, "build", "bin", "main")):
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    raise FileNotFoundError("whisper binary not found; run install_whisper_stt.sh first")

def list_devices() -> None:
    print("ALSA capture devices:")
    subprocess.run(["arecord", "-l"], check=False)

def record(seconds: int, device: str | None, out: str) -> str:
    cmd = ["arecord", "-d", str(seconds), "-r", "16000", "-c", "1",
           "-f", "S16_LE", "-t", "wav", out]
    if device:
        cmd[1:1] = ["-D", device]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"arecord failed: {r.stderr.strip() or r.stdout.strip()}")
    if not os.path.isfile(out) or os.path.getsize(out) < 1000:
        raise RuntimeError("recorded file missing or too small")
    return out

def transcribe(wav: str) -> str:
    if not os.path.isfile(MODEL_PATH):
        raise FileNotFoundError(f"model missing: {MODEL_PATH}")
    bin_path = find_binary()
    out_base = wav + ".out"
    cmd = [bin_path, "-m", MODEL_PATH, "-f", wav, "-otxt", "-of", out_base,
           "--no-prints"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    txt_path = out_base + ".txt"
    if r.returncode != 0:
        raise RuntimeError(f"whisper failed (rc={r.returncode}): {r.stderr.strip()}")
    if not os.path.isfile(txt_path):
        raise RuntimeError("whisper produced no text file")
    with open(txt_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read().strip()
    if not text:
        raise RuntimeError("whisper returned empty text (silence or mic issue)")
    return text

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", type=int, default=0, help="seconds to record")
    ap.add_argument("--file", default="", help="existing wav file")
    ap.add_argument("--device", default="", help="arecord device, e.g. plughw:1,0")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    try:
        if args.list:
            list_devices(); return 0
        if args.record > 0:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
                wav = tf.name
            try:
                record(args.record, args.device or None, wav)
                print(transcribe(wav))
            finally:
                try: os.unlink(wav)
                except OSError: pass
        elif args.file:
            print(transcribe(args.file))
        else:
            ap.print_help(); return 2
    except Exception as e:
        print(f"E_WHISPER: {e}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
