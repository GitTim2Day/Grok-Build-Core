# SESSION_PATTERN_MAP_2026-11-26_AIRPODS_PIPER_WRAPPER

America/New_York: 2026-11-26T23:21:58 EST

## HIT
AirPods Piper → pw-play confirmed. Default sink set via wpctl.
Short one-line bash wrapper sealed for clean voice-loop call.

### Wrapper (AirPods default)
```bash
#!/bin/bash
echo "$1" | piper --model /home/shepherd/piper/en_US-lessac-medium.onnx --output-raw | pw-play --raw --rate 22050 --channels 1 --format s16 -
```

Usage: `./speak.sh "text here"`

## VAL
Command ran clean on shepherd Pi 5. Real-time factor ~0.16. Terminated clean.
wpctl status confirms * AirPods as default sink.

## MISS
none on AirPods path.

## OPEN
Wire into voice loop on Pi 5.
JBL Clip 4 deferred to tomorrow.

Six-pillar SVCT: content · context · data · time · semantics · validation.
Do No Harm first. Append-only. No Bot.

Ledger hop: 1a21b3d2d8ba6295
Box: 2617991694085
Pointer skill: session-map-2026-11-26-airpods-piper-wrapper
Sibling of prior voice-loop / AirPods maps, not a merge.