# stripe-identity-payout-pipe

**Date:** 2026-09-08
**Tags:** stripe, payments, shepherd, validation
**Status:** Active method — pipe, not pudding
**GOSUB ID:** STRIPE_ID_BANK
**Siblings:** the-shepherd-stripe-go-live, no-photo-card-intake-stripe-tokenize
**Do not store:** government-ID pages, card fronts, routing, account numbers, selfies

## Purpose
Walk Stripe identity + payout-bank as two pipes with visible failure points, so the Dashboard sitting is one pass. Pudding (money movement) is a different tell. This skill does not move money and does not replace the pudding watch.

## When to use
- Stripe asks for ID + selfie, or Add a bank account to pay out funds.
- Someone is about to photograph a license, passport, or debit card into Grok, Notion, mail, or Drive.
- Someone wants to reuse a passport-studio original as the selfie.

## When not to use
- Do not treat Connect-approved, profile-unhide, Tax/Radar, or “what’s next” mail as this pipe or as pudding.
- Do not paste routing, account, PAN, DL number, or passport number into chat.
- Do not save ID or card photos to the project.

## Required inputs
- Which ID they will use (one). Default for most people: driver’s license.
- Which checking account sits behind the debit they intend (not the Visa PAN).
- Whether Stripe opened a live camera or a file picker.

## Steps
1. **Split three jobs.** Identity (ID + selfie). Bank (checking destination). Pudding (inbound or payout mail). Never collapse them.
2. **Pick one ID.** Driver’s license is the common path. Passport photo page also works. Cover is not an ID page. Stripe gets the page unmasked in Stripe’s camera/upload only.
3. **Selfie is a second capture.** Live person in front of the phone camera. Do not crop the passport-studio original or the ID portrait and call it the selfie. Stripe blocks **selfie liveness** (photograph or screen presentation attack). Recrop a live shot if needed (less ceiling, chin not tilted up). Same person as the ID; two sittings.
4. **Bank is checking, not the card.** For a BoA Visa debit, add the Bank of America checking account. Instant bank-link if the bank appears. Else routing + account typed in Dashboard. X/Cross River debit-flex is a card, not the ACH payout bank.
5. **Masking.** Mask numbers only if a photo would leave Stripe (finger or tape over number and MRZ). Never mask the page you upload to Stripe. Never send the page to Grok, Notion, Drive, GitHub, or email.
6. **Report.** ID chosen. Selfie live yes/no. Bank path (instant vs micro-deposit). What stayed out of the project (IDs, cards, numbers). Pudding unchanged unless a separate sweep says otherwise.

## Rules
- Failure points first: liveness vs studio file, DL vs passport, card vs checking, mask vs full page, chat vs Stripe window.
- Slow on the points. Fast in the Dashboard.
- Append only. Do not rewrite the-shepherd-stripe-go-live or the pudding protocol.
- If Dashboard rejects: send the error *text*, not the ID photo.

## Anti-patterns
- Gallery-picking the passport original as the selfie.
- Entering a Visa PAN as a bank account.
- Photographing the billfold into Grok “for coaching.”
- Calling bank-added or ID-verified “PUDDING ROSE.”
- Saving this sitting’s ID/card images into skills or KB.

## Example (this sitting)
DL chosen (most people). Passport put away. BoA checking for payouts. Live selfie to be cropped and uploaded in Stripe only. Instant bank-link preferred. Project received the method, not the documents. pudding=0 this morning; cleanup mapping still held.
