---
name: time-capture-auto-v2
description: >-
  Use at the start and end of every reply, and as a boot step: state only times
  from a fresh clock fetch (60 s or newer); otherwise say STALE or UNVERIFIED,
  and never invent a time. Also use whenever a time or timestamp goes into a
  calendar event title or description: build that text with calnotice_v2.sh so
  it is human-readable and never contains a raw Unix timestamp (7+ digit runs
  render as phone links). Supersedes time-capture-auto-2026-10-18 (v1).
---
# Fresh-clock capture (v2)

v2 of `time-capture-auto-2026-10-18`. v1 is kept unchanged at
`/home/box/agent-data/workflows/time-capture-auto-2026-10-18/SKILL.md`
(sha256 e3f018dc5810e740a496a1c26bf8a413f817495e4cc750dc9e77e3cff61be3b5).
v2 adds the calendar-notice rule and the Known defects section.

Tool: `/workspace/time-capture-2026-10-18/timecap.sh` (bash) or `timecap.py` (Python). Both use the same stamp and print the same lines. The stamp is `/workspace/time-capture/last_fetch.json`. (Unchanged from v1; timecap.sh sha256 02e2eecbdf0c501b514da34d267b4abf7547e6ec5503099777f86c1c000c1954.)

## Steps
1. **At the start of every reply,** run `timecap.sh open` and lead the reply with its first line, verbatim.
2. **Before the final send,** run `timecap.sh close` and include its first line, verbatim, at the end.
3. **Never state a time that didn't come from a fetch in the last 60 s.** That rules out times from memory, from earlier messages, from file mtimes, and from guesses at "about now".
4. **UNVERIFIED:** say so, and don't substitute a time.
5. **STALE:** quote the line as is.
6. **Seconds:** truncate, never round.
7. **Boot step:** after BOOT.bas prints 0.70710678 and SOURCES_OF_TRUTH has been read, run `timecap.sh open`.
8. **Calendar text (new in v2):** any time put in a calendar event title or
   description is built with
   `/workspace/time-capture-calnotice-fix-2026-10-18/calnotice_v2.sh EPOCH "Title" ["Note"]`.
   Use its TITLE: line as the summary and its DESCRIPTION: line as the
   description. It prints e.g. `Stamped Sun Oct 18 2026 7:42:16 AM EDT.`
   - Never put a raw epoch (or any run of 7+ digits) in calendar text, not even
     as `epoch=...`. Keep the epoch in local logs only (`CALNOTICE_LOG`).
   - If calnotice_v2.sh refuses (exit 4), remove the digit run from the
     title/note; do not work around the check.
   - Quick form for a one-off: `TZ=America/New_York date -d @EPOCH '+%a %b %-d %Y %-I:%M %p %Z'`.
   - Do not edit or delete existing calendar events to apply this; it is for
     new text only, unless Timothy asks.

## Lines
- **Fresh:** `Time (fresh fetch): 12:10 PM EDT, fetched 12:10:47`. The stamp is 60 s old or less; exit 0.
- **Stale:** `Time: ... STALE, fetched N s ago`. The stamp is more than 60 s old; exit 1.
- **No fetch:** `Time UNVERIFIED: no fetch available`. The stamp is missing, corrupt or fails its hash; exit 2.
- **Skew:** `Time UNVERIFIED: clock skew detected`, or a different-boot or external-skew message; exit 3.
- **Test clock:** a line ending in `[TEST CLOCK]` came from a fake test clock. Never quote it as the time.

## Limits
- The clock is the shared computer's clock, not the user's own PC.
- The stamp's hash detects corruption; it isn't a signature.

## Known defects

### D-2026-10-18-01: calendar notice showed raw Unix digits rendered as phone link
- **Seen:** Sunday Oct 18 2026 calendar entry "GB: SVCT timestamp" (Google
  Calendar primary, event eab9r5pp3s379io4n28t1hlesk, created 7:46:30 AM EDT,
  start 3:30 PM EDT). The app showed "in 23 minutes" for the 3:30 PM slot, and
  the description's digits 1792323736 were auto-linked as a phone number (green
  phone icon, white handset).
- **Description text (v1):** "Grok Build work block (abbreviated summary slot).
  Timestamp 1792323736, actually stamped 7:42:16 AM ET."
- **What the digits are:** `date -d @1792323736` = Sun Oct 18 07:42:16 EDT 2026
  (11:42:16 UTC). That is the SVCT stamp time (created_utc of
  svct_timestamp_074216.json), not 3:30 PM; 3:30 PM is only the event's start slot.
- **Root cause:** no script on the box builds calendar text. The event was
  written by hand through a calendar create_event call with the raw epoch
  pasted into the description. timecap.sh / timecap.py never write calendar
  text, and their user-facing lines are already human-readable.
- **Fix:** v2 rule 8 + `calnotice_v2.sh`, which renders the time
  human-readable, keeps the epoch out of calendar text, and refuses (exit 4)
  any title/description containing a 7+ digit run.
  - Path: `/workspace/time-capture-calnotice-fix-2026-10-18/calnotice_v2.sh`
  - sha256: a9ebc90cc4e38fb0e78d7f607d873552686f7f09fd435d6966de47d285629618
  - Test: `test_calnotice_v2.sh` (sha256 05a848815e7417f9481d288fa9031e819456ec08ad838b306e5d272697add9e1), 9/9 PASS
    on 2026-10-18; greps every generated notice for `[0-9]{7,}` and fails if found.
- **Status:** fixed in v2 (above path and sha). The existing event was left
  as is (not edited or deleted).
