# Bluetooth Whitelist / Blacklist Spec — 2026-09-13

**Status:** Policy sealed 2026-09-13 12:20 EDT. Build the whitelist. Blacklist is the remainder.
**Host:** shepherd@raspberrypi
**Tool:** bluetoothctl (must be inside [bluetooth]# prompt)

## Standing rule
- Always keep Bluetooth **speaker** devices reachable.
- CPAP machines are **not** always-on comms. Connect only when extracting health / Rex MD Fortress data. Default scan action: drop.
- Prior scan log is stored, not trashed. Role of ResMed changed from always-allow to extract-only.

## Whitelist (keep / connect)
- **Speakers (always)**
  - JBL Clip 4 — F8:5C:7E:A2:E5:FC. Pairing button → CHG.
  - Any later named speaker we claim — add when name or pairing button proves it is ours.
- **Audio (keep)**
  - AirPods / case candidate — **44:16:83:C0:D1:4B**. Apple Key **0x004C**. Value **10 06 72 1d b6 d6 97 80**. RSSI hit −40 and −36. Type 0x10 Nearby. Lock name with `info 44:16:83:C0:D1:4B` while lid open.
- **Watch (visible, do not block)**
  - KBLD9 keyboard/trackpad.

## Extract-only (default DROP)
- ResMed 701194 CPAP — 4C:5B:B3:DE:F4:C1.
- Documented so we can find it. Connect only for a Rex MD Fortress / health extract session, then disconnect.

## Blacklist (filter out)
- Apple 0x004C except confirmed audio above.
- Rotating MACs: DA:3C:2F:46:52:26, ED:CB:D4:47:04:02, C1:2D:1A:92:4D:FC, 48:57:02:19:DF, 62:C8:1C:AE:8F:2A, 77:67:50:39:39:6C.
- KSBT03C101386585 — ED:53:C3:70:A1:26 unless claimed.
- Everything not on the whitelist.

## Boot chain
1. GitHub first — this file + bluetooth-device-tracking/docs/session-boot-handoff-2026-09-13.md
2. Notion second — skill bluetooth-speaker-whitelist-pattern in Timothy Skills & KB + Whisper Mode 3dac9bfe-3aff-81a3-a75d-d76ffa1bc7b1
3. Email third — Grok-Build-Ledger to timnorman730@gmail.com CC Yahoo

## Pitfall
`scan` / `pair` / `trust` / `connect` are bluetoothctl subcommands. Confirm `[bluetooth]#` first.
