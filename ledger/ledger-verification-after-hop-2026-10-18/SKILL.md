---
name: ledger-verification-after-hop
description: After the Grok-Build-Ledger email hop fires, search BOTH mailboxes (Gmail timnorman730@gmail.com and Yahoo timothy_h_norman@yahoo.com) for the ledger message, compare message IDs with the IDs the hop reported, retry briefly, and fail closed (pause the save before Notion, GitHub, Drive or local) on any miss or if Yahoo is not connected.
---

# ledger-verification-after-hop

Ordered by Timothy, 2026-10-18 2:17 PM ET.

## When it runs
Right after the Grok-Build-Ledger hop (the ledger email sent to both
timnorman730@gmail.com and timothy_h_norman@yahoo.com) fires, and before any
other shelf (Notion, GitHub, Drive, local) is written.

## Steps

1. **Search both mailboxes.** Run a search job against:
   - Gmail `timnorman730@gmail.com` via the `user-Gmail` `search_threads` tool;
   - Yahoo `timothy_h_norman@yahoo.com` via a connected Yahoo tool.

   Query: the subject prefix `Grok-Build-Ledger` plus the hop's fresh
   timestamp (the time captured when the hop fired), so an older ledger
   message cannot satisfy the check.

2. **Compare message IDs.** Compare the message IDs the search returns with
   the IDs the hop reported. A match on BOTH addresses = hop VERIFIED; the
   shelves proceed.

3. **Miss = pause.** A miss on EITHER address pauses the save before Notion,
   GitHub, Drive or local, with a warning that names the mailbox that did not
   receive it (for example: `LEDGER HOP MISS: timothy_h_norman@yahoo.com did
   not receive Grok-Build-Ledger <timestamp>; save paused`).

4. **Fail closed if Yahoo is not connected.** If no Yahoo connector/tool
   exists, the result is `Yahoo: UNVERIFIED (not connected), fail closed`.
   A blind pass is worse than no check, so never report Yahoo as verified
   without an actual Yahoo inbox result.

5. **Short retry window before calling a miss.** The message may not have
   landed yet. Retry a few times before declaring a miss, for example 3 tries
   at about 30 s, 60 s and 120 s after the send.

## Gmail Sent is not Yahoo receipt
Gmail's Sent copy only proves the message LEFT Gmail. It does not prove that
Yahoo RECEIVED it. Yahoo needs its own inbox check (step 1, Yahoo side).
Never count the Gmail Sent copy as the Yahoo result.

## Result lines (record in REPORT.md and JOURNAL.md)
- `Gmail: VERIFIED (id <message id>)` or `Gmail: MISS after N tries`
- `Yahoo: VERIFIED (id <message id>)` or `Yahoo: MISS after N tries`
  or `Yahoo: UNVERIFIED (not connected), fail closed`

