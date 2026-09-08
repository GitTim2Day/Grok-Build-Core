# stripe-onboard-copybook

**Date:** 2026-09-08
**Tags:** stripe, payments, shepherd, validation, architecture
**Status:** Active method — one pass, COBOL-shaped. Not a cloud ID scanner.
**GOSUB ID:** ONBOARD_COPYBOOK
**Siblings:** stripe-identity-payout-pipe, no-photo-card-intake-stripe-tokenize, the-shepherd-stripe-go-live
**Do not store:** ID bitmaps, card bitmaps, check bitmaps, routing, account, DL/passport numbers, SSN

## Purpose
One sitting captures the overlapping fields so you do not walk the person back through the same facts. The license, the check, and two questions are the punch cards. Grok reads a **copybook**, not a photo library.

Think COBOL: fixed fields, FILLER for what must not leave the card, ACCEPT for what the card does not hold.

## When to use
- New person (or this household) going live on Stripe: identity + payout bank + contact.
- You are about to ask for the same name/address three times.
- Routing is not on the debit card.

## When not to use
- Do not OCR government ID or checks **in Grok / Notion / mail / Drive**. That is the punch-card reader sitting on the **edge** (phone/A15, local-first). Stripe’s camera gets the unmasked document. This chat gets fields or nothing.
- Do not treat this as pudding.
- Do not skip the two ACCEPTs: current-address flag, phone.

## The punch cards (one grab)

| Source | What it already encodes | What it does not |
|---|---|---|
| Driver’s license (most people) | Legal name, DOB, license address, photo | Whether that address is still home; phone |
| Voided / old / canceled check (MICR) | ACH routing, account, often name | Instant bank-link; liveness |
| Live selfie | Face now, liveness | Identity number |
| **ACCEPT** (must ask) | — | **Is the license address current?** **Phone number.** |

Passport is an alternate ID card (no street). Debit/credit plastic is **not** a routing card.

## Copybook (working storage, not the image)

```
01  ONBOARD-REC.
    05  LEGAL-NAME           PIC X(40).
    05  DOB                  PIC X(10).
    05  ADDR-ON-LICENSE      PIC X(80).
    05  ADDR-CURRENT-YN      PIC X.         *> ACCEPT. Required.
    05  ADDR-CURRENT         PIC X(80).     *> if N, ACCEPT the real one
    05  PHONE                PIC X(15).     *> ACCEPT. Required.
    05  EMAIL                PIC X(40).     *> already on Stripe if present
    05  ID-TYPE              PIC X(8).      *> DL or PASSPORT. One.
    05  BANK-PATH            PIC X(12).     *> INSTANT or MICR-CRIB
    05  ROUTING              PIC X(9).      *> FILLER to Grok. Dashboard only.
    05  ACCOUNT              PIC X(17).     *> FILLER to Grok. Dashboard only.
    05  ID-NUMBER            PIC X(20).     *> FILLER. Stripe only.
    05  SELFIE-LIVE-YN       PIC X.         *> must be Y. Not a studio file.
```

MOVE legal name / DOB / license address from the **local** read.
MOVE SPACE to ROUTING ACCOUNT ID-NUMBER before any line that leaves the phone (chat, Notion, GitHub, mail). That is the blackout. FILLER is not optional.

## Steps
1. **One grab.** Tell them: driver’s license, one voided or old check, phone in hand. Instant bank-link if their bank appears; check is the crib.
2. **Local read.** Edge OCR or their own eyes. Not this chat. Not a growing image folder.
3. **Blackout.** Keep name, DOB, license address in the copybook. Drop ID number, routing, account, photo bytes from anything that leaves the device.
4. **ACCEPT ADDR-CURRENT-YN.** If the license address is not home, ACCEPT the current one. Do not assume the punch card is still true.
5. **ACCEPT PHONE.**
6. **Stripe window.** Unmasked DL (or passport page) + **live** selfie in Stripe. Typed or bank-linked checking in Dashboard. Grok does not carry the bitmap.
7. **Stop.** Do not re-ask name and DOB. Do not call ID-verified pudding.

## Rules
- Overlap is the point. Name/DOB/address live on the DL. Routing lives on the check. Phone and “is this still home?” do not live on either — ask once.
- COBOL not BASIC: one record, one pass, FILLER for secrets, ACCEPT for what the card cannot know.
- Local reader. Cloud assistant sees the copybook after blackout, or sees nothing.
- Append only. Does not rewrite STRIPE_ID_BANK or the pudding watch.

## Anti-patterns
- Photographing the punch cards into Grok “so you can read them.”
- Skipping ADDR-CURRENT-YN because the license looks official.
- Using the passport studio file as the selfie.
- Uploading the check to Identity.
- Storing the raw images in skills/KB.

## Example (this sitting)
Offer: old check as crib. Weighed: keep as MICR read, not upload. DL chosen. Live selfie. BoA checking. New field from this idea: always ask if license address is current; always get phone. Automate the **checklist and blackout**, not a cloud scan of the cards.
