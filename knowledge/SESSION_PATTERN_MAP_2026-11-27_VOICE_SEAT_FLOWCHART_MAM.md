# SESSION_PATTERN_MAP_2026-11-27_VOICE_SEAT_FLOWCHART_MAM

Stamp: 2026-11-27T21:00:03-05:00
Six-pillar SVCT: content context data time semantics validation
Ledger: 1a21fe1a6226701f

## CONTENT
Today's voice-seat work on shepherd Pi 5 mapped to Timothy's flowchart card.

Wake gate: Vosk STT, Hey (any language) + Shepherd (English lock), sequential order, 1.5s pause variable (set to 0 to remove), 5s command window (bumped from 3s), Ollama llama3.2:3b offline AI, Piper TTS proven on AirPods (temp-WAV route, model /home/shepherd/local/piper/voices/en_US-lessac-medium.onnx).

Flowchart: intake triangle (Vosk bottom-left) converts any language to English; distribution triangle (Piper top-right) sends English to any language or straight through. English is the spine. Triangle = 2N edges vs square N-squared.

Sphere geometry: 3 coordinates per language (longitude=family, latitude=branch, radius=depth). Isosceles triangle for equal-angle sister-language hops; right triangle for perpendicular axis moves across any octant. Amygdala-style parallel parsing. Do-no-harm directive (third tier: sacrifice self before others) tied to John 15:13. 16 people picked up work on GitHub; open-source posture held. Stick-language GOSUBs on drive, not resident. Translate Once Fan-out Many (2026-07-31 lock) confirmed. S-to-S board: 101 languages, 30+ connections.

## CONTEXT
Sitting 2026-11-27 evening. Timothy reviewed flowchart card. Corrected my earlier miss: Vosk output any language, normalized to English before split. Pre-Vosk translation concern: provenance must capture original audio AND converted text. Triangle vs square: triangle default on Pi, square for direct non-English hops. Sphere with English center: radii to surface languages, surface arcs for shortcuts. Timothy: pharmacy compounding instinct = code instinct. Code of ethics: do no harm, close to Christianity.

## DATA
Wake gate script: sequential_wake_gate.py on shepherd. Vosk model: /home/shepherd/models/vosk-model-small-en-us-0.15 (39MB downloaded 18:44). Piper model: /home/shepherd/local/piper/voices/en_US-lessac-medium.onnx. sounddevice 0.5.6 installed in piper-env. arecord device plughw:3,0 (E4K card 3). Command window 5.0s. Ollama model llama3.2:3b. PATH MISMATCH MISS: script says /home/shepherd/vosk-model-small-en-us-0.15 (no models/ subdir) — would fail on next run. Not yet repaired.

## TIME
2026-11-27T21:00:03-05:00 (America/New_York). Session ran 18:28-21:00.

## SEMANTICS
One English ledger underneath, many output languages on top. Wake detector sees one fixed English word. Language front door and back door are stick GOSUBs. Recipient text channel not built. Loop-back (Llama->Piper) noted not wired.

## VALIDATION
Wake gate heard hey shepherd correctly, printed WAKE, logged follow-on speech. Piper temp-WAV route confirmed earlier today (both ears, AirPods). Path mismatch is the open MISS — repair before next run.

## SHELVES
Email hop: 1a21fe1a6226701f.
Notion: pointer child under 424c9bfe-3aff-816e-b2c2-f9363545559f.
GitHub: this file.
Box: root upload.
Drive: gap user-owned.
Memory: row appended.

## OPEN
Path mismatch repair. Language front/back door GOSUBs. Recipient text channel. Loop-back wire. Drive gap.