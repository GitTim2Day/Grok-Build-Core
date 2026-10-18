---
name: sms-send-router
description: Use when Timothy wants to send a US text message (SMS) from the Grok Build project. Routes one approved message through three tiers in a fixed order (Telnyx primary, Apple Messages via AppleScript first fallback, Twilio speed tier only on explicit choice), only after an email approval-card tap, with an append-only ledger and fail-closed reporting. Also lists the 10DLC / toll-free registration requirements. No account exists yet; Timothy decides any signup or spend.
---

# sms-send-router

Written 2026-10-18 for Timothy Norman's Grok Build project.

**Status: SKILL FILE ONLY.** No Telnyx or Twilio account exists yet. Nothing in
this skill signs up, buys a number, registers a brand or campaign, or sends a
text. Timothy decides any signup or spend. All prices below are the figures
Timothy supplied on 2026-10-18; they were not re-checked in this job, so check
them against the provider pricing pages before any spend.

## When to use
- Timothy asks to text someone (a US mobile number) from the project.
- A Grok Build workflow needs to deliver a short notice by SMS after Timothy
  approves it.
- Timothy asks what an SMS send would cost, or what registration would need.

Do not use it to send anything Timothy has not approved with the email
approval-card tap.

## Tiers (fixed order)

### Tier 1: Telnyx (PRIMARY)
- Cost per US text: about 0.75 to 0.85 cents (US$0.004 base + carrier fee
  US$0 to US$0.0045).
- One-time sole-proprietor 10DLC registration: US$19.50 (US$4.50 brand +
  US$15 vetting).
- Monthly: about US$3 all in (US$2 campaign + US$1 number).
- Send: one JSON POST to `https://api.telnyx.com/v2/messages` with header
  `Authorization: Bearer <TELNYX_API_KEY>`, body
  `{"from": "+1XXXXXXXXXX", "to": "+1XXXXXXXXXX", "text": "..."}`.
  The response `data.id` is the provider message id.
- Key: read from an environment variable or secret store only. Never put it
  in a file, ledger, email, or log.

### Tier 2: Apple Messages via AppleScript (FIRST FALLBACK)
- Runs on macOS with `osascript` driving Messages.app. It sends through the
  iPhone's Text Message Forwarding, so it reaches non-Apple phones as SMS/RCS
  at no extra cost (normal carrier plan).
- Requirements (all of them): iPhone powered on and online; Mac awake and
  logged in; Messages on the Mac and the iPhone signed in to the same Apple
  Account; Text Message Forwarding turned on for that Mac.
- Example:
  ```
  osascript -e 'tell application "Messages"
    set svc to 1st account whose service type = SMS
    send "MESSAGE TEXT" to participant "+1XXXXXXXXXX" of svc
  end tell'
  ```
- There is no provider message id or delivery receipt. Record the
  `osascript` exit code and record the result as `HANDED_TO_MESSAGES`, never
  `DELIVERED`.

### Tier 3: Twilio (SPEED TIER, explicit choice only)
- Used ONLY when Timothy explicitly chooses speed for this message. It is
  never an automatic fallback.
- Cost per US text: about 1.2 to 1.3 cents (US$0.0083 + carrier US$0.0035 to
  US$0.005).
- Registration: US$19 one-time + US$2/month. Number: US$1.15/month.
- Speed: 117 ms median API response vs Telnyx 470 ms (Knock benchmark,
  https://knock.app/sms-api-benchmarks/compare/telnyx-vs-twilio). That is API
  response time, not handset delivery time.
- Send: POST form to
  `https://api.twilio.com/2010-04-01/Accounts/<AccountSid>/Messages.json`
  (Basic auth, `To`, `From`, `Body`). The response `sid` is the provider
  message id.

## Router logic
1. If Timothy explicitly chose speed for this message -> Twilio only. If
   Twilio fails, report the failure. Do not fall back without asking.
2. Otherwise try Telnyx. On error or timeout -> try Apple Messages.
3. If a tier cannot be reached (no account, no key, Mac asleep, iPhone
   offline, network error), say so by name. Never skip a tier silently.
4. If every tier in the path fails, report failure. Nothing is sent and
   nothing is retried in the background.

## Approval flow (email approval card)
1. Draft the message (text + masked recipient) and show it.
2. An approval card goes to Timothy by email.
3. Nothing sends without the tap.
4. The tap triggers a webhook, which calls the router with the approved text,
   recipient and approval timestamp.
5. No tap, no send. An expired or declined card ends that send.
The router refuses any call that does not carry a valid approval (id +
timestamp) whose text hash matches the text being sent.

## Ledger (append-only)
One timestamped record per send attempt, appended, never edited or deleted:

| field | content |
|---|---|
| ts | send time, ISO 8601 with offset (America/New_York) |
| text_sha256 | full SHA-256 of the message text (never truncated in the record; shorten only for display) |
| recipient | masked, e.g. `+1 ***-***-1234` |
| approval_ts | time of the approval tap |
| tier | `telnyx` / `apple` / `twilio` / `none` |
| provider_msg_id | Telnyx `data.id`, Twilio `sid`, or `none` (Apple) |
| result | `ACCEPTED`, `HANDED_TO_MESSAGES`, `FAILED:<reason>`, `UNREACHABLE:<tier>` |

Each tier tried gets its own row, so a Telnyx failure followed by an Apple
send is two rows. Write with an exclusive lock (`flock`) and append mode only.

## Fail closed
- No tap, no send.
- An unreachable tier is reported by name.
- Never invent a delivery status. `ACCEPTED` means the provider accepted the
  API request; it is `DELIVERED` only if a provider delivery webhook says so.
- Never print the API key, the full recipient number, or the message text in
  a log or email; use the hash and the masked number.

## Registration requirements (before any Telnyx or Twilio send)
- **Sample messages** with opt-out wording, for example:
  "Grok Build: your report is ready. Reply STOP to opt out, HELP for help."
- **Recipient consent answers**: write down how each recipient opted in (for
  example, gave their number to Timothy in person or by email and agreed to
  receive project texts), when, and keep the record. Carriers ask for this
  in the campaign form.
- **HELP keyword**: reply with who is sending and how to reach Timothy.
  **STOP keyword**: stop all texts to that number and record the opt-out.
- **Sole-proprietor limits**: one phone number per sole-prop campaign, low
  throughput, US numbers only.
- **Toll-free numbers**: under the Feb 17 2026 toll-free business
  registration rule, a toll-free number needs business registration
  (verification) before it can send. Treat an unverified toll-free number as
  unreachable.

## Router pseudocode
```
function route(msg, recipient, approval, speed_chosen):
    if approval is missing or not tapped or expired:
        return FAIL("no approval tap, no send")
    if sha256(msg) != approval.text_sha256:
        return FAIL("approved text does not match, no send")

    if speed_chosen:
        path = [TWILIO]            # explicit choice only
    else:
        path = [TELNYX, APPLE]     # Twilio is never automatic

    for tier in path:
        if not reachable(tier):    # no account/key, Mac asleep, iPhone offline
            ledger.append(row(tier, "none", "UNREACHABLE:" + tier))
            report("tier " + tier + " unreachable")
            continue
        try with timeout:
            id = tier.send(msg, recipient)
            status = (tier == APPLE) ? "HANDED_TO_MESSAGES" : "ACCEPTED"
            ledger.append(row(tier, id or "none", status))
            return OK(tier, id, status)
        on error or timeout as e:
            ledger.append(row(tier, "none", "FAILED:" + e))
            report("tier " + tier + " failed: " + e)

    return FAIL("all tiers failed, nothing sent")

function row(tier, id, result):
    return {ts: now_ny(), text_sha256: sha256(msg),
            recipient: mask(recipient), approval_ts: approval.ts,
            tier: tier, provider_msg_id: id, result: result}
```

## Not done here (Timothy decides)
- Telnyx or Twilio signup, number purchase, 10DLC brand/campaign registration,
  toll-free verification, any spend.
- Building the approval-card webhook.
