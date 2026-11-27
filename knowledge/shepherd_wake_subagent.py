#!/usr/bin/env python3
"""Shepherd wake-word sub-agent glue.
English on Pi 5; languages on stick. Parallel Vosk scoring.
Chains via Gate/Split/Tag/Merge/Verify pattern. No sudo, no Bot.
"""
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

# Paths (adjust on shepherd)
VOSK_EN = Path.home() / ".local/share/vosk/vosk-model-small-en-us-0.15"
VOSK_STICK = Path("/media/usb/languages/vosk-model-hi")  # example Hindi; extend
OLLAMA = "http://127.0.0.1:11434/api/generate"
PIPER = Path.home() / ".local/bin/piper"
VOICE = Path.home() / ".local/share/piper/en_US-lessac-medium.onnx"
AIRPODS_WRAP = Path.home() / "airpods_piper.sh"
TTT_LOG = Path.home() / "shepherd_ttt.jsonl"
CACHE_SEC = 30

def gate(audio_chunk):
    """Gate: detect wake word 'Shepherd'."""
    # Stub: call vosk in practice
    return "shepherd" in audio_chunk.lower()

def split(text):
    """Split: parallel score English vs stick language."""
    # Stub scores; replace with actual Vosk
    en_score = 0.8 if "english" in text.lower() else 0.4
    stick_score = 0.7 if any(w in text.lower() for w in ["haan", "theek"]) else 0.3
    return {"en": en_score, "stick": stick_score, "text": text}

def tag(scores):
    """Tag: dominant language."""
    if scores["en"] >= scores["stick"]:
        return "en", scores["text"]
    return "stick", scores["text"]

def merge(lang, payload):
    """Merge: call Llama or stick GOSUB."""
    if lang == "en":
        # Local Ollama
        cmd = ["curl", "-s", "-X", "POST", OLLAMA,
               "-d", json.dumps({"model": "llama3.2:1b", "prompt": payload, "stream": False})]
        try:
            out = subprocess.check_output(cmd, text=True, timeout=10)
            return json.loads(out).get("response", "OLLAMA_FAIL")
        except Exception:
            return "OLLAMA_FAIL"
    else:
        return f"GOSUB_STICK:{payload}"  # wire UT2 later

def verify(result):
    """Verify: log TTT, speak."""
    entry = {"ts": datetime.now().astimezone().isoformat(), "result": result}
    with open(TTT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    if AIRPODS_WRAP.exists():
        subprocess.run([str(AIRPODS_WRAP), result], check=False)
    else:
        subprocess.run([str(PIPER), "--model", str(VOICE), "--output-raw"], input=result.encode(), check=False)
    return result

def main():
    print("SHEPHERD_WAKE sub-agent online")
    last_lang = "en"
    last_time = 0
    while True:
        # In practice: read from mic via Vosk
        chunk = input("simulate: ")  # replace with Vosk loop
        if not gate(chunk):
            continue
        now = time.time()
        if now - last_time < CACHE_SEC:
            lang = last_lang
        else:
            scores = split(chunk)
            lang, _ = tag(scores)
            last_lang = lang
            last_time = now
        result = merge(lang, chunk)
        verify(result)

if __name__ == "__main__":
    main()
