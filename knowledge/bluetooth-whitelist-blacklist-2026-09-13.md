# Bluetooth Whitelist / Blacklist Spec — 2026-09-13

**Status:** Draft — ready for Pi 5 implementation. Based on live scan today.
**Host:** shepherd@raspberrypi
**Tool:** bluetoothctl (must be inside [bluetooth]# prompt)

## Goal
Cut scan noise. Keep only devices we care about. Same pattern scales to non-Apple edge devices later.

## Blacklist (filter out / ignore)
- All Apple devices with manufacturer ID **0x004C** EXCEPT AirPods / confirmed case ads.
- Rotating private MACs seen today (likely Apple audio gear):
  DA:3C:2F:46:52:26, ED:CB:D4:47:04:02, C1:2D:1A:92:4D:FC, 48:57:02:19:DF, 62:C8:1C:AE:8F:2A,
  77:67:50:39:39:6C (hit −34 then DEL).
- KSBT03C101386585 — MAC ED:53:C3:70:A1:26. Cycles NEW/DEL; noise unless identified as ours.
- Any device not on the whitelist.

## Whitelist (keep / allow)
- **AirPods / case candidate** — MAC **44:16:83:C0:D1:4B**. Apple ManufacturerData.Key **0x004C**. Value **10 06 72 1d b6 d6 97 80**. RSSI sequence −50 → −40 → −70 → −51 → −36 → −47 → −58. Strong nearby. Type 0x10 = Apple Nearby (not the 0x07 AirPods pairing packet). Name not printed in this frame — run `info 44:16:83:C0:D1:4B` while the lid is open to lock the product string.
- **JBL Clip 4** — MAC F8:5C:7E:A2:E5:FC. Confirmed ours. Pairing button triggers CHG.
- **KBLD9** — keyboard/trackpad. On watch list; keep visible.
- **ResMed 701194 CPAP** — MAC 4C:5B:B3:DE:F4:C1. Expected to cycle; turning it off stops spam. Keep on allowlist but monitor.

## Delta vs prior frame (this photo)
- New named noise: KSBT03C101386585 ED:53:C3:70:A1:26 (NEW/DEL loop).
- Strong transient: 77:67:50:39:39:6C RSSI −60 / −46 / −34 then DEL — treat as rotating Apple MAC.
- First Apple payload on-screen: 44:16:83:C0:D1:4B Key 0x004C Value `10 06 72 1d b6 d6 97 80` with RSSI hitting −40 and −36.
- Also present (drop unless later named): 54:CB:3A:EF:DB:1F (−79/−67/−77), FF:CA:A4:49:CC:91, DE:80:7D:E3:2D:31, F0:6E:EC:CE:68:58, EB:D0:30:2E:29:B9, F7:BB:4A:4A:07:04.
- JBL and ResMed not in this frame.

## Implementation notes (Pi 5)
1. Enter bluetoothctl: `bluetoothctl` → prompt shows `[bluetooth]#`.
2. `power on` then `scan on`.
3. Filter logic: check manufacturer data / name. Drop 0x004C unless AirPods product code or this 0x10 Nearby payload on 44:16:83:C0:D1:4B while lid is open.
4. Optional: `block <MAC>` for persistent noise, or script a filter that only logs whitelist hits.
5. Confirm AirPods: lid open → `info 44:16:83:C0:D1:4B` → capture Name + full ManufacturerData.

## Pitfall to avoid
`scan`, `pair`, `trust`, `connect` are **bluetoothctl subcommands**, not shell commands. Always confirm `[bluetooth]#` prompt first. See `knowledge/pitfalls/bluetoothctl-shell-confusion-2026-09-13.md`.

## Next
- `info 44:16:83:C0:D1:4B` with case open.
- Re-test JBL pairing button and CPAP on/off.
- Extend whitelist pattern to other edge devices (non-Apple).
