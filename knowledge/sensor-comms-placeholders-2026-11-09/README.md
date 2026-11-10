# SENSOR / COMMS / HIVE PLACEHOLDERS — 2026-11-09

Design-only. No installs. No device access. No uploads/emails.
Status of every row: **PLACEHOLDER**. Nothing assigned or claimed built.

Generated: 2026-11-09 America/New_York (box clock EST).
Request window: Timothy ~8:22–8:24 PM ET (sensor USB + GPIO match + COMM/hive).

## Files
- `SENSOR_COMMS_PLACEHOLDERS_2026-11-09.tsv`
- `SENSOR_COMMS_PLACEHOLDERS_2026-11-09.jsonl`
- `README.md` (this file)

## Columns
`slot_id`, `family` (SENSOR|COMM|HIVE), `signal`, `transport`, `matched_existing_placeholder`, `backup_role`, `status`, `notes`

Rules: never invent an earned id; unmatched → `UNDEF`. Medical signals carry design flag `non-diagnostic, isolation required` only.
SUGGESTED transport fallback from EDGE_TRANSPORT_MATRIX (not locked): USB=1 → WiFi=2 → BT=3; Cellular rank UNDEF.

## Earned sources (path + sha256[:16])
- `/workspace/project-pack-src-cache-2026-10-06/gbc/basic/edge_io_ports.md` — `e572613e246c2158`
- `/workspace/project-pack-src-cache-2026-10-06/gbc/knowledge/pi5-gpio-attachments-not-clock-2026-09-12.md` — `95591a10ec5f73d5`
- `/workspace/project-pack-src-cache-2026-10-06/gbc/edge-canvas-kit/knowledge/EDGE_DEVICE_IO_FLOW_2026-10-05.md` — `a15894d399d2f9f2`
- `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_IO_LAYER_2026-10-06.md` — `5189bac4cb10ce93`
- `/workspace/project-pack-src-cache-2026-10-06/gbc/knowledge/ACTIVE_INVENTORY_IMU_POC_2026-09-21.md` — `423c54150a0e4c6d`
- `/workspace/project-pack-src-cache-2026-10-06/gbc/docs/session-scan-2026-10-05/EDGE_FULL_INVENTORY_AS_FOUND_2026-10-05.md` — `d25c0b960b34f01d`
- `/workspace/pi5-drive-survey-2026-11-09/SMALL_TEXT_HEADS_DIGEST.md` — `7c8013a28f4159c7`
- `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_TRANSPORT_MATRIX_2026-10-05.md` — `a46eadc4003d1831`
- `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_HW_INVENTORY_2026-10-05.md` — `afb88fe7756c653d`
- `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_CELLULAR_NOTE_2026-10-05.md` — `df3ee7d9d2f8dd42`

## Counts (filled after write)
- Total rows: 54
- By family: {'SENSOR': 30, 'COMM': 14, 'HIVE': 10}
- matched_existing_placeholder ≠ UNDEF: 45
- matched_existing_placeholder = UNDEF: 9
- GPIO-addition / unmatched-sensor rows (SC-G-*): 10

## Top unmatched / GPIO-addition placeholders (SC-G-*)
- `SC-G-001` GPIO breakout T-Cobbler / ribbon → matched=pi5-gpio-attachments-not-clock T-Cobbler breakout jumpers ribbon|EDGE_FULL_INVEN…
- `SC-G-002` GPIO expander (MCP23017/PCA9555 class) → matched=UNDEF
- `SC-G-003` PCA9685 PWM driver (signal only) → matched=EDGE_IO_LAYER §6.1 PCA9685|EDGE_IO_LAYER gaps live PCA9685 UNDEF
- `SC-G-004` relay/driver module (efferent) → matched=EDGE_IO_LAYER gpio_backend.py|EDGE_IO_LAYER §6.3 GPIO electrical limits
- `SC-G-005` onboard RTC clock slot (not DS3231) → matched=pi5-gpio-attachments-not-clock J5 ML-2020 RTC OPEN do-not-buy-DS3231
- `SC-G-006` Pico 2 PIO precision GPIO organ → matched=pi5-gpio-attachments-not-clock Pico 2 PIO|hot-swap-edge-gpio local-brain RP2040
- `SC-G-007` HMC5883L magnetometer OLD-REC → matched=ACTIVE_INVENTORY HMC5883L OLD-REC|EDGE_FULL_INVENTORY C3#31
- `SC-G-008` SHILLEHTEK pre-soldered accelerometer → matched=EDGE_FULL_INVENTORY C2b#37 SHILLEHTEK LIST-2025
- `SC-G-009` generic Sensors GPIO branch (sketch) → matched=EDGE_DEVICE_IO_FLOW DiagramA Sensors GPIO|EDGE_DEVICE_IO_FLOW DiagramA sensors
- `SC-G-010` HDMI video capture / vision RO → matched=EDGE_IO_LAYER hdmi-video channel|EDGE_DEVICE_IO_FLOW USB/HDMI|EDGE_TRANSPORT_MAT…

## Memory gaps (≤10) from 2026-11-09 Pi survey digest — important, not yet recorded elsewhere as standing memory
1. PI5_USB_PORT_POLICY (digest): microSD=OS; USB3 blue1=Radioactive; USB3 blue2=cam; one USB2 black always free; BT=kbd/mouse; Ethernet primary — path Seagate:/_MAIDEN_BRAIN/00_inbox/desktop_ops_2026-07-27/PI5_USB_PORT_POLICY.txt via /workspace/pi5-drive-survey-2026-11-09/SMALL_TEXT_HEADS_DIGEST.md
2. Hive travel kit 2026-07-20 + GOSUB_HIVE_TRAVEL_SETUP pack/arrive/work/depart hooks to USB lifecycle/safe_remove/remember_map — Seagate:/SVCT_HIVE_TRAVEL/* via SMALL_TEXT_HEADS_DIGEST.md
3. HIVE_TRAVEL_DEVICE_CONNECTION_MAP device facts: A15 a15-cortex; Seagate Expansion P/N 1TEAP6-500 S/N [redacted-serial]; Anker dock; Orin; sticks — digest only (no credentials)
4. TTT bus policy: hot=Ollama↔Grok live; cold=Seagate L2 flush; ollama http://127.0.0.1:11434; no_keys_phi — Seagate:/SVCT_TTT_BUS/pointer.json + GROK_OPEN_LATEST.md via digest
5. kbld_augmented_ollama.py SEALED v1 (30993 B, sha6f94daefe21dac97…); DEFAULT_MODEL qwen2.5:7b; Pi5 PARKED; adjuvant/non-authoritative — Seagate:/svct_spines/deploy/ via digest
6. GOSUB_USB_LIFECYCLE + GOSUB_USB_SAFE_REMOVE (hot-plug/swap/shutdown drain; safe-remove by letter/label) — Maiden inbox desktop_ops_2026-07-27 via digest
7. sense_voxel presence packs (wifi/bluetooth counts + room sensors) mirrored Seagate + _RADIOACTIV — digest § Wi-Fi/USB/Bluetooth
8. Room presence note 2026-07-29: Bluetooth AirPods/JBL/[redacted-device]; USB drives E/F/H; Wi-Fi Up [redacted-lan-ip]; Pi5 PARKED_UNPLUGGED — SVCT_TTT_BUS batch via digest
9. Maiden policies: APPEND_NOT_REPLACE; NO_PURGE_UNLESS_COMPROMISED; RETURN_TRIP_50_PERCENT battery — Seagate:/_MAIDEN_BRAIN/99_policy/ via digest
10. SVCT_POCKET_BALANCE_ANKER: pocket balance on Seagate; lean pack on _RADIOACTIV; Anker hub + iPhone piggyback — desktop_ops via digest

## Standing separation
- Placeholders only. No wiring, pairing, flashing, purchase, or live backend.
- Skills loaded: hot-swap-edge-gpio, channel-core-edge, first-principles-tim.
- Fail-closed: truncate not round; no ±∞; no stored zero at core; archive never delete.

## File hashes (sha256)

- `SENSOR_COMMS_PLACEHOLDERS_2026-11-09.tsv` — `7c62f2c4b47d0541b3ba2a00a6a8f60970f21b793bc419c2b66c7ae9d9225900` (12724 bytes)
- `SENSOR_COMMS_PLACEHOLDERS_2026-11-09.jsonl` — `388bc207355bffa37d9a4ca492f23275e8529a5778be6c866fafb2c7fd3cc1d0` (19118 bytes)
- `README.md` — see `SHA256SUMS.txt`
