---
name: time-capture-auto-2026-10-18
description: Fresh-clock capture. Every reply opens and closes with a time that came from a fetch made in the last 60 seconds; otherwise it says STALE or UNVERIFIED. Never guess or invent a time.
---

# time-capture-auto-2026-10-18 (generic fresh-clock capture)

Tool: `/workspace/time-capture-2026-10-18/timecap.sh` (bash) or `timecap.py` (Python). Same stamp, same lines.
Stamp: `/workspace/time-capture/last_fetch.json` (override with `--stamp PATH` or `$TIMECAP_STAMP`).

## Steps
1. **Start of every reply:** run `timecap.sh open` and lead the reply with its first line, verbatim.
2. **Before the final send:** run `timecap.sh close` and include its first line, verbatim, at the end.
3. **Never state a time that did not come from a fetch in the last 60 s.** No time from memory, from
   an earlier message, from a file mtime, or from a calculation of "about now".
4. **If the line says UNVERIFIED, say so** ("Time UNVERIFIED: ..."). Do not substitute a time.
   If it says STALE, quote the STALE line as is; do not refresh it by hand.
5. Seconds are truncated, never rounded. The zone is America/New_York (EDT/EST).
6. Boot step: after BOOT.bas 0.70710678 and SOURCES_OF_TRUTH, run `timecap.sh open`.

## Lines you can get
- `Time (fresh fetch): 12:10 PM EDT, fetched 12:10:47`  (stamp ≤ 60 s old; exit 0)
- `Time: 12:10 PM EDT — STALE, fetched 61 s ago`  (stamp > 60 s old; exit 1)
- `Time UNVERIFIED: no fetch available`  (missing, corrupt or hash-fails; exit 2)
- `Time UNVERIFIED: clock skew detected`  (wall age vs monotonic age differ > 2 s, or stamp in the future; exit 3)
- `Time UNVERIFIED: stamp is from a different boot (monotonic check impossible)`  (exit 3)
- `Time UNVERIFIED: external clock skew detected (...)`  (open/close only; HTTP Date off by > 5 s; exit 3)
- second line on open/close: `External check: ok (...)` or `External check: skipped (...)` — a skipped
  external check is reported, never a failure on its own.

## Limits (say them when relevant)
- The clock read is the shared box clock (set to America/New_York), not Timothy's own PC clock,
  which the box cannot reach.
- The sha256 in the stamp detects corruption and casual edits; it is not a signature.
- A line ending in `[TEST CLOCK]` came from a fake test clock and must never be quoted as the time.
