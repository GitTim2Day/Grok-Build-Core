# Live bluetoothctl device log — 2026-09-13

Host: shepherd@raspberrypi
Prompt: [bluetoothctl]>

Devices are being added, changed, deleted, and changed again in real time.

```
[DEL] Device AC:15:18:28:01:FA LP
[NEW] Device AC:15:18:28:01:FA LP
[CHG] Device F8:5C:7E:A2:E5:FC RSSI: 0xffffffe1 (-31)
[DEL] Device 41:AD:92:80:52:44 41-AD-92-80-52-44
[NEW] Device 4C:5B:B3:DE:F4:C1 ResMed 701194
[CHG] Device 41:A5:9F:FA:E3:5E RSSI: 0xffffffe4 (-28)
[DEL] Device 4C:5B:B3:DE:F4:C1 ResMed 701194
[DEL] Device AC:15:18:28:01:FA LP
[CHG] Device 4C:5B:B3:DE:F4:C1 ResMed 701194
[NEW] Device 4C:5B:B3:DE:F4:C1 ResMed 701194
[NEW] Device AC:15:18:28:01:FA LP
[CHG] Device F8:5C:7E:A2:E5:FC RSSI: 0xfffffff8 (-40)
[DEL] Device 4C:5B:B3:DE:F4:C1 ResMed 701194
[CHG] Device 41:A5:9F:FA:E3:5E RSSI: 0xfffffffc (-36)
[CHG] Device 41:A5:9F:FA:E3:5E RSSI: 0xfffffff1 (-47)
[NEW] Device 4C:5B:B3:DE:F4:C1 ResMed 701194
[DEL] Device 4C:5B:B3:DE:F4:C1 ResMed 701194
[NEW] Device 4C:5B:B3:DE:F4:C1 ResMed 701194
[CHG] Device 41:A5:9F:FA:E3:5E RSSI: 0xfffffff9 (-55)
[DEL] Device F8:5C:7E:A2:E5:FC JBL Clip 4
[CHG] Device 41:A5:9F:FA:E3:5E RSSI: 0xfffffff4 (-44)
[CHG] Device 41:A5:9F:FA:E3:5E RSSI: 0xfffffff4 (-53)
[CHG] Device 41:A5:9F:FA:E3:5E RSSI: 0xfffffff4 (-68)
[CHG] Device 41:A5:9F:FA:E3:5E RSSI: 0xfffffff8 (-40)
[CHG] Device 62:C8:1C:AE:8F:2A RSSI: 0xfffffff4 (-68)
[NEW] Device DA:3C:2F:46:52:26 DA-3C-2F-46-52-26
[DEL] Device AC:15:18:28:01:FA LP
[NEW] Device AC:15:18:28:01:FA LP
[CHG] Device 41:A5:9F:FA:E3:5E RSSI: 0xfffffff4 (-51)
[DEL] Device 4C:5B:B3:DE:F4:C1 ResMed 701194
[DEL] Device DA:3C:2F:46:52:26 DA-3C-2F-46-52-26
[NEW] Device C1:2D:1A:92:4D:FC C1-2D-1A-92-4D-FC
[NEW] Device 4C:5B:B3:DE:F4:C1 ResMed 701194
[NEW] Device C4:D3:6A:02:19:DF C4-D3-6A-02-19-DF
[DEL] Device ED:CB:D4:47:04:02 ED-CB-D4-47-04-02
[DEL] Device C4:D3:6A:02:19:DF C4-D3-6A-02-19-DF
[DEL] Device 4C:5B:B3:DE:F4:C1 ResMed 701194
[NEW] Device 4C:5B:B3:DE:F4:C1 ResMed 701194
```

## Key facts
- CPAP machine detected as **ResMed 701194** (MAC 4C:5B:B3:DE:F4:C1).
- JBL Clip 4: F8:5C:7E:A2:E5:FC.
- Devices are dynamic — added, changed, deleted, re-added.
- On next session, ask Timothy to show the current monitor state to continue.

## Continuity
Load with notion-first-session-boot. This is a live stream, not a snapshot.