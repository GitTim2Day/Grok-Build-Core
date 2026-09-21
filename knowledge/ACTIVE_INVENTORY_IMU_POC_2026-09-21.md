# ACTIVE INVENTORY — IMU POC 2026-09-21

Stamp: 2026-09-21T13:02:20-0400
Chair: Timothy H. Norman
Host: Grok Build / Grok 4.7
Sibling of: session-map-2026-09-14-pi5-grokcli-adxl (not a merge)
Plant: closed-system-vascular-plant LOAD this sitting (pointer SHA-256 6db4037fe8797d99d4f124736a6a8149b116dc3e21cfddff62b12c441ef5eed6)

## Pin (held this sitting)

| Lock | State |
|---|---|
| Grok CLI on shepherd Pi 5 | **1.0.25** — do not unpinned update |
| Pi flash | **NO** — not this sitting |
| curl \| bash installer | **NO** until Timothy names it |
| Installer SHA | **known** (ASSERTED — bytes not re-fetched this turn) |
| Shepherd copy of installer | **OPEN** |
| Failure pattern | #51 blame-the-nearest-binary; #19 asserted-seal-without-bytes |

No flash. No CLI bump. No silent fourth hole.

## Active inventory ADD (this sitting)

| ID | Board | Job | Bus (typical — confirm on wire) | Standing |
|---|---|---|---|---|
| MAG-QMC | QMC5883P | heading | I2C ~0x2C | ACTIVE afferent. Not HMC. |
| IMU-GY521 | GY-521 (MPU-6050 class) | accel + gyro | I2C 0x68 / 0x69 | ACTIVE afferent. POC floor. |

HMC5883L stays on the **old rec list**. It is not this board. **Do not load an HMC driver on the QMC.**

ADXL355 stays the **upgrade path**, not the POC floor. Upgrade only after a bind ticket exists and VAL's.

Addresses above are **asserted typical**, not earned. First act on the Pi, when Timothy is there: `i2cdetect -y 1`.

QMC5883P datasheet face (Adafruit/QST): default 7-bit 0x2C. Still not a bus scan.

## Logical process (so work can move)

Closed plant I/O:

1. **Input** — raw capture on the bus. Not inferred. Not regenerated.
2. **Output** — collecting duct only: one bind ticket, or dump.
3. **Maintenance** — CLI pin 1.0.25, hash, no curl\|bash.

Flow:

```
GY-521 + QMC5883P  (afferent raw)
    → Shepherd clean
    → one bind ticket
            → Cortex gets the bound event (not three raw streams)
            → Efferent = same ticket back to GPIO / voice / motor token
            → No ticket, no fire
ADXL355 upgrade bed: only after that ticket exists and VAL's
```

Plant names:

| Name | Job |
|---|---|
| Afferent MAG-QMC + IMU-GY521 | Input holes |
| Shepherd clean | Glomerulus / one-pass filter |
| Bind ticket | Collecting duct |
| Cortex | Muscle — standing load, bound event only |
| Efferent GPIO/voice/motor | Typed injector. Sensor = ticket present. Shutoff = no ticket |
| ADXL355 | Upgrade bed after VAL — not POC floor |
| HMC5883L driver on QMC | Leak. Dump. |
| curl \| bash | Silent fourth hole. Forbidden until named. |

## Code (logical, this sandbox)

- `artifacts/afferent_efferent_poc.py` — bind-ticket path. No I2C. No Pi.
- Tests VAL locally: no-ticket-no-fire, HMC-on-QMC reject, ADXL gated, NaN dump.

Bus scan is **not** claimed from this chair.

## GOSUB_TO_NEXT +1

`i2cdetect -y 1` dump from shepherd, **or** say when the boards are on the bus.

Do not invent the scan. Do not flash. Do not bump CLI.

## Append row (this sitting)

`2026-09-21T13:02:20-0400 · MAG-QMC + IMU-GY521 ADD to afferent/efferent POC; CLI 1.0.25 pin held; Pi not flashed; no curl|bash · HIT local bind-ticket tests · OPEN: i2c scan, installer shepherd copy`

Status: ACTIVE inventory add. Addresses ASSERTED. Ticket path EARNED locally. Bus VAL OPEN.

SHA-256 019e523c49d6b3b360acf50bdb3be64729d64109bcdef86debc5377891db80b8
