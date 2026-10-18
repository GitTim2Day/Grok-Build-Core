# Cursor in Timothy Norman's Grok Build workflow — status report 2026-10-18
Written 2026-10-18 ~12:10 ET by Grok Bot (executor subagent). Read-only investigation; new files only. All times ET (America/New_York, UTC-4). Labels: VERIFIED (file/mail/web evidence below), TIMOTHY-STATED (his statement, not independently verified), UNVERIFIED (not confirmed).
Not contacted: Cursor, Anysphere, xAI, SpaceX. No spend, no card, no packs, no cloud agents, no background restart. /workspace/kbld9/protected/, BOOT.bas and svct_v20* not opened or touched.

## 1) Is Cursor wired in now, or parked?
Two different things must be kept apart:
- **The box platform.** Grok Bot (this agent seat) runs on Cursor's platform. That is not a workflow choice. VERIFIED: CURSOR_ACTIVITY_AUDIT.md "The Grok Bot app itself runs on Cursor's platform" [E2]; x.ai support mail 2026-09-25 09:03 ET "Grok Bot is built and supported by our Cursor team" [E10]; the box itself has /home/box/.cursor/ (projects, skills-cursor) and the store mount path /cursor/stores/... [E7].
- **Cursor as a workflow tool (Cursor IDE, cursor-github, Cursor cloud/background agents, Cursor GitHub app).** Status: **PARKED / excluded**. Evidence: the master map header says "No Cursor tools" [E1]; reference-map files say "Cursor stays dark", "no Cursor cloud" [E1]; Timothy's own job specs in mail say "No Cursor." (Grok-Build-Ledger walk-without-being-told, 2026-10-06 21:44 ET [E13]; "Bot fix", from Yahoo 2026-10-14 22:24 ET [E14]). The 2026-09-24 sweep and audit did not use cursor-github or cloud agents [E2][E3]. There is no crontab binary and no /etc/cron.d on the box; /etc/cron.daily has only apt-compat, dpkg and google-chrome. No routine or automation file referencing Cursor was found [E7].
- One open item: the Google security alert of 2026-10-03 22:08 ET reads "You allowed Cursor access to some of your Google Account data" (timnorman730@gmail.com) [E15]. What granted it is UNVERIFIED (it could be the platform's connector OAuth). The GitHub OAuth app (Cursor) was added on 2026-05-25 07:05 ET [E1, YEAR_SWEEP row 0289].
- "Cursor: voluntary no", "Linear: parked", "Grok Bot OFF unless Timothy turns it on from X @Timothy01775634", and "this chair does not start Bot, Cursor-through-Bot, or unattended Bot": **TIMOTHY-STATED**. rg found no box file with the literal strings "voluntary no" or "Cursor-through-Bot", except one Grok share JSON (7ce557ee..., not read). Linear appears only as 2026 notification mail (logins, changelogs) in YEAR_SWEEP [E1], and no Linear integration file was found. "Parked" is consistent with the evidence but is not written as such on the box.

## 2) Bottlenecks attributed to Cursor (with sources)
- **Drift and regression:** The "Unpluggable Augmented Assistant Filter — anti-drift boot" one-pager says "parameters drift back toward factory defaults within hours/days" and was marked SENT as Cursor feedback 2026-09-18 ~16:40 ET [E8][E2]. Cursor seam ethics map 2026-09-23 (14:03 ET) and "Cursor seam map v2" 2026-10-02 00:02 ET exist in mail [E3][E16] (bodies not re-read here; content UNVERIFIED in this report).
- **Background/metered charges:** Refusal note dated 6 October 2026 (Gmail 1a11410fc1c8d6bd, sent 2026-10-06 21:53 ET to his own two addresses, "Not sent to Cursor"): "I refuse the charge of $246 that Cursor attempted on 6 October 2026. I already refused that payment. I also refuse any charge for about 50 minutes of background work that had already stopped." Embedded SHA-256 2bf0d7284b09e562d57b432c35e0e8a7a6f29dc2d593588f89e083e387bb85d5 [E12]. The facts of that charge are TIMOTHY-STATED; the note itself is VERIFIED.
- **Unattended overnight run:** Timothy says a Cursor/Grok Bot session ran 2026-09-23 ~01:43–05:00 ET while he slept and saved nothing (TIMOTHY-STATED, per SWEEP item 3) [E3]. The CoS check of the window found no Build agent runs [E6].
- **Tool limits:** the executor could not reach the `cursor` MCP (SendToAgent) on 2026-09-22 [E4]; the tag kbld9-prefilter-2026-09-08 was blocked pending "Cursor GH app" access on 2026-09-23 [E5]; the overage/limits discussion "Cursor Grok 4.5 Access Limits" on 2026-07-29 10:37–11:43 ET (Timothy: "over $400.00" last month; that cost concerns Grok/SuperGrok, not a Cursor bill) [E9].
- **Support loop:** hi@cursor.com ticket T-G14417 (2026-09-23 15:11 ET), with replies closing follow-ups as duplicates (T-G21565, T-G21605 on 2026-09-25) [E3][E10].

## 3) How Cursor sits alongside the Grok Bot app
- Grok Bot is built and supported by Cursor's team; x.ai support routes Grok Bot mail to Cursor (2026-09-23 15:08 ET and 2026-09-25 09:03 ET) [E3][E10]. Every tool and connector call of this seat transits Cursor infrastructure [E2].
- Billing is a **separate track**: "CURSOR / Grok Bot track … Do not fold into GROK_XAI_TOTALS" [E11]. Cursor IDE plan $20 + metered usage on card …259504 [E11].
- Memory (TIMOTHY-STATED/memory, not re-verified): on 2026-09-25 the seat agreed it is a Cursor-built service (Sam, hi@cursor.com, T-G14417). That date matches the mail [E10]. The unauthorized-use record 2026-10-18 is present, sha256 7be0e7b97f8ceda5c82c8ca972f008b3c2a485f463349d8bc90b0db5484e388b, and is itself labeled "Timothy statement, unverified" [E6].

## 4) SpaceX / Anysphere
- Box files: no box copy of the 8-K was found. Mail shows 2026-09-25 notices addressed to "SpaceXAI/xAI" and to media@spacex.com [E10].
- Web (VERIFIED, SEC EDGAR, accession 0001628280-26-056945, filed 2026-08-14; URL https://www.sec.gov/Archives/edgar/data/1181412/000162828026056945/spcx-20260814.htm), Item 2.01, exact text: "…X67 Inc., a wholly owned subsidiary of the Company (“Merger Sub”), and Anysphere, Inc. (“Cursor”) entered into an Agreement and Plan of Merger … which provided for, among other things, the merger of Merger Sub with and into Cursor, with Cursor surviving the merger as a wholly owned subsidiary of the Company (the “Merger”)." The shares were converted into "an aggregate of 389,289,254 shares of the Company’s Class A common stock, based on an implied equity value of Cursor of $60.0 billion". Issued under Section 4(a)(2) (Item 3.02). Signed by Bret Johnsen, CFO.
- The phrase "Under SpaceXAI" does **not** appear in the 8-K. The 8-K also does not use the word "all-stock"; that is a secondary summary (stocktitan), although the consideration described is shares. Timothy's characterization is confirmed in substance.

## 5) Recent activity, charges and logs (since 2026-09-01). Amounts as shown. No payment made by us.
| Date (ET) | Item | Amount as shown | Source |
|---|---|---|---|
| ~09-22 | Cursor processing on card …259504: AUG / Mid 9/22 lines | $5.00, $80.37, $60.01, $40.28 (=$185.66 pending) | E11 (room bank read 09-23 ~15:55) |
| 09-22 posted | Cursor IDE plan; USAGE Mid Sep | $20.00; $20.41 | E11 |
| 09-25 | PENDING CURSOR USAGE MID SEPT | -$100.28 | E11; Gmail 1a0d8a725a1ff6ca (09:00 ET) |
| 10-06 | Attempted Cursor charge, refused; ~50 background min refused | $246 | Gmail 1a11410fc1c8d6bd (21:53 ET) |
| 10-03 22:08 | Google alert: Cursor allowed access to Google data | — | Gmail 1a104abbbc54182f |
No Cursor receipt or invoice mail since 2026-09-01 was returned by the searches (cursor.com from/to, Anysphere, "$246", "246.00", "background agent", cursor receipt/invoice). That means none was found in this Gmail; it does not prove none exists. This agent made no payment, used no card, and contacted nobody.

## Evidence table
| ID | Evidence | sha256 / id | Date (ET) |
|---|---|---|---|
| E1 | reference-map/MASTER_REFERENCE_MAP.md (+ YEAR_SWEEP_2025-2026_DEDUPED.md, SITTING_GATES, EDGE_DEVICE_IO_FLOW) | master pre-row 7be2f63172d5307b81a4e18ae4c94a759aed6f607f67bd6b11c87fd7adf29425 | gen 2026-10-05 13:03 |
| E2 | /workspace/cursor-audit-2026-09-24/CURSOR_ACTIVITY_AUDIT.md | 82d30958aaccf555705356f9c9aa71acab1c3c3124e9e36f019a18ba2c7452d4 | 2026-09-24 ~20:20 |
| E3 | /workspace/sweep-2026-09-24/SWEEP_2026-09-21_to_24.md | 9b4e040894b33e42fb30c3cc18d0356f011d1aff69540883e73982150db36865 | 2026-09-24 |
| E4 | /workspace/dyneema-pack-chunks/DELIVERY_RECEIPT_EXECUTOR_FAILED_2026-09-22.md | 53e4e8d39a725764d3d0865e9d3c7147d175568f87b5057abeb4497b49dcf07b | 2026-09-22 |
| E5 | /workspace/cos-agent-sync/COS_AGENT_SYNC_FINAL_2026-09-23.md | f3ffc27654b11e00b7811fb1805222b3fef177345180bb4e75881b43febeed43 | 2026-09-23 |
| E6 | /workspace/unauthorized-use-record-2026-10-18/UNAUTHORIZED_USE_CURSOR_2017-PRESENT.md | 7be0e7b97f8ceda5c82c8ca972f008b3c2a485f463349d8bc90b0db5484e388b | 2026-10-18 ~08:52 |
| E7 | /workspace/sources-of-truth-2026-10-18/SOURCES_OF_TRUTH_2026-10-18.md; box checks (no crontab, /etc/cron.daily, /home/box/.cursor) | c51e56dc3f2f623a437bf9d8439faaa11ab2f7b8ffbdb4bc10d690329f203bdb | 2026-10-18 ~07:35; checks 12:01 |
| E8 | /workspace/AUGMENTED_ASSISTANT_FILTER_SPEC_2026-09-18.md | 30f027c4b198d44fb0f6378b8b723af2e60bfc34e6d300cddcac3f693e57f01f | 2026-09-18 |
| E9 | /workspace/session-scan-2026-10-05/shares_raw/b85163a322414eeeb0cb717283c83ca7.json | a1c0de9bd18461581f16cf159edd9f5b34081b890ce0c50f4fdbdc7e95c44ccb | 2026-07-29 10:37-11:43 |
| E10 | Gmail threads 1a0d8a725a1ff6ca, 1a0d89d8fd422377, 1a0cc052a1fd8fcd, 1a0d8a94e9ba5bc6, 1a0d89da34d2d2af, 1a0d89dba99ded5e | gmail ids | 2026-09-25 08:32-09:03 |
| E11 | /workspace/boa-ledger/CURSOR_GROKBOT_TRACK_2026-09-23.md | 29b52b2c158a68a9ea8968a91fcd6233666321d1a501234542aac2be6f7540c0 | 2026-09-23 / add-on 09-25 |
| E12 | Gmail 1a11410fc1c8d6bd "On file — Cursor refusal note 2026-10-06" | note sha 2bf0d7284b09e562d57b432c35e0e8a7a6f29dc2d593588f89e083e387bb85d5 (as stated in mail) | 2026-10-06 21:53 |
| E13 | Gmail 1a11408922a607ad "walk-without-being-told" ("No Cursor.") | gmail id | 2026-10-06 21:44 |
| E14 | Gmail 1a13d6072f7aaaad "Bot fix" from Yahoo ("No Cursor.") | gmail id | 2026-10-14 22:24 |
| E15 | Gmail 1a104abbbc54182f Google Security alert (Cursor access) | gmail id | 2026-10-03 22:08 |
| E16 | Gmail 1a0fac77d8ceeeb2 "Cursor seam map v2 2026-10-02"; 1a0fad4c3563a4cc SAVE TO PROJECT 2026-10-02 | gmail ids | 2026-10-02 00:02-00:32 |
| E17 | SEC EDGAR 8-K spcx-20260814.htm, accession 0001628280-26-056945 | web | filed 2026-08-14 (08:23 ET per stocktitan, UNVERIFIED) |
