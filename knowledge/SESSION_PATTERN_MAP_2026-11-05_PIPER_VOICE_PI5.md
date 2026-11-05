# SESSION_PATTERN_MAP_2026-11-05_PIPER_VOICE_PI5

Sitting 2026-11-05 ~11:00-11:40 EST, shepherd Pi 5.

## Goal
Piper TTS voice engine on Pi 5 without sudo password. PipeWire 1.4.2 present. JBL Clip 4 paired (F8:5C:7E:A2:E5:FC). eMeet SmartCam C960 in blue USB 3 port.

## Path Taken
1. systemctl status piper: not found. which piper: empty. which espeak-ng: empty.
2. sudo apt update && sudo apt install -y espeak-ng: blocked after 3 incorrect password attempts.
3. mkdir -p ~/piper && cd ~/piper
4. wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
5. tar -xvzf piper_arm64.tar.gz
6. wget en_US-lessac-medium.onnx (60.27 MB) and en_US-lessac-medium.onnx.json (4885 bytes) from huggingface.co/rhasspy/piper-voices
7. Typo tessac caused 404; corrected to lessac. Extra .onnx suffix also 404.
8. Test: echo "Hello from the Pi" | ./piper --model en_US-lessac-medium.onnx --output_file hello.wav
   - Piper loaded voice in 0.35s, real-time factor 0.14, wrote 16-bit LE 22050 Hz mono wav.
   - aplay: Device or resource busy.
   - paplay: not installed.
   - bluetoothctl connect F8:5C:7E:A2:E5:FC: Connected yes.
   - aplay still silent.
   - wpctl status: JBL Clip 4 sink 96 at vol 1.00, but default sink was Scosche bluez_output.00_00_01_04_14_BF.1. Firefox held three active streams to JBL.
   - Closed Firefox entirely.
   - aplay -D pulse: unknown PCM.
   - pw-play hello.wav: SUCCESS, audible on JBL Clip 4.

## Learnings
- No-sudo forces prebuilt binary over apt.
- ./piper prefix required (dot-slash).
- aplay collides with PipeWire bluez5 ownership.
- pw-play is the PipeWire-native player and correct voice output path.
- Firefox holds PipeWire streams open.
- Default sink was Scosche, not JBL.
- Hugging Face URLs are case-sensitive.
- amd64 deb valid for Dell x64 only, not Pi Arm64.
- espeak-ng-data and libpiper_phonemize bundled in tarball.

## Validation
pw-play hello.wav produced audible speech on JBL Clip 4. PASS.

## Open
- wpctl set-default 96 for permanent JBL default.
- Integrate pw-play into Grok CLI voice output config.
- Test mic input path: eMeet as source 57.
- SHA-256 seal of this map file.

## Ledger
Hop 1a1acaa91b8a3d17 to timnorman730@gmail.com and timothy_h_norman@yahoo.com.

## Sibling
session-map-2026-11-04-full-session, not a merge.
