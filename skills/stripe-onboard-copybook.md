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
- Personal offline AI (A15 / Pi) that can keep the full record on-device.

## When not to use
- Do not OCR government ID or checks **in Grok / Notion / mail / Drive**. That is the punch-card reader sitting on the **edge** (phone/A15, local-first). Stripe’s camera gets the unmasked document. This chat gets fields or nothing.
- Do not treat this as pudding.
- Do not skip the two ACCEPTs: current-address flag, phone.
- Do not open the mammalian/nephron build from this analogy. HOLD.

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
    05  ROUTING              PIC X(9).      *> FILLER on a hop. Keep on edge.
    05  ACCOUNT              PIC X(17).     *> FILLER on a hop. Keep on edge.
    05  ID-NUMBER            PIC X(20).     *> FILLER on a hop. Stripe only.
    05  SELFIE-LIVE-YN       PIC X.         *> must be Y. Not a studio file.
```

## Edge vs hop
Personal **offline** AI: reader and copybook on the same machine. ID numbers and account numbers never leave. No mask-for-chat. That is the time saver for a population of private machines.

This Grok sitting **is** a hop. MOVE SPACE to ROUTING ACCOUNT ID-NUMBER before chat, Notion, GitHub, or mail.

Stripe is always its own hop: live camera, unmasked DL + live selfie, even if the edge already read the card.

## Capillary / glomerulus (analogy only)
Local captures = capillary beds. The **glomerulus** is the filter tuft (not “legumerulus”). Filtrate = copybook after FILLER. The body does not drink the raw blood (ID photo, MICR, PAN). Nephron/mammalian model remains HOLD.

## Steps
1. **One grab.** DL, one voided or old check, phone in hand.
2. **Local read.** Edge OCR or their own eyes.
3. **Site check.** Offline: keep the full record on disk. Hop: blackout secrets first.
4. **ACCEPT ADDR-CURRENT-YN.** Then PHONE.
5. **Stripe window.** Unmasked DL + live selfie. Bank-link or typed checking.
6. **Stop.** Do not re-ask name and DOB. Not pudding.

## Rules
- Overlap is the point. Two ACCEPTs are not on the punch card.
- COBOL: one record, one pass, FILLER on hops, keep-all on edge.
- Append only.

## Anti-patterns
- Photographing punch cards into Grok so a cloud model can “read them.”
- Skipping ADDR-CURRENT-YN.
- Opening the kidney build from the analogy.
- Calling onboard complete “PUDDING ROSE.”
