# Bluetooth Whitelist / Blacklist Spec — 2026-09-13

**Status:** Draft — ready for Pi 5 implementation. Based on live scan today.
**Host:** shepherd@raspberrypi
**Tool:** bluetoothctl (must be inside [bluetooth]# prompt)

## Goal
Cut scan noise. Keep only devices we care about. Same pattern scales to non-Apple edge devices later.

## Blacklist (filter out / ignore)
- All Apple devices with manufacturer ID **0x004C** EXCEPT AirPods.
- Rotating private MACs seen today (likely Apple audio gear):  
  DA:3C:2F:46:52:26, ED:CB:D4:47:04:02, C1:2D:1A:92:4D:FC, 48:57:02:19:DF, 62:C8:1C:AE:8F:2A.
- KSBT03C… (smaller-brand keyboard/speaker) — noise unless identified as ours.
- Any device not on the whitelist.

## Whitelist (keep / allow)
- **AirPods** — Apple 0x004C but specific product code (keep this one).
- **JBL Clip 4** — MAC F8:5C:7E:A2:E5:FC. Confirmed ours. Pairing button triggers CHG.
- **KBLD9** — keyboard/trackpad. On watch list; keep visible.
- **ResMed 701194 CPAP** — MAC 4C:5B:B3:DE:F4:C1. Expected to cycle; turning it off stops spam. Keep on allowlist but monitor.

## Implementation notes (Pi 5)
1. Enter bluetoothctl: `bluetoothctl` → prompt shows `[bluetooth]#`.
2. `power on` then `scan on`.
3. Filter logic: check manufacturer data / name. Drop 0x004C unless AirPods product code. Drop rotating MACs above. Keep named devices on whitelist.
4. Optional: `block <MAC>` for persistent noise, or script a filter that only logs whitelist hits.
5. Test: press JBL pairing button → should show CHG on F8:5C:7E:A2:E5:FC only, no Apple spam.

## Pitfall to avoid
`scan`, `pair`, `trust`, `connect` are **bluetoothctl subcommands**, not shell commands. Always confirm `[bluetooth]#` prompt first. See `knowledge/pitfalls/bluetoothctl-shell-confusion-2026-09-13.md`.

## Next
- Implement filter script on Pi.
- Re-test with CPAP on/off and JBL pairing button.
- Extend whitelist pattern to other edge devices (non-Apple).
