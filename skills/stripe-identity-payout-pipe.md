# Stripe identity + payout pipe (GOSUB: STRIPE_ID_BANK)

Method saved. No ID pages, no card faces, no routing stored.

## Three jobs stay split
1. Identity — ID + live selfie.
2. Bank — checking destination for payouts.
3. Pudding — money movement (separate tell).

## Identity
- Most people: driver's license. One ID. Unmasked in Stripe only.
- Selfie must be live. Passport-studio original or ID portrait as selfie fails liveness.
- Passkey already registered ≠ identity verified.
- Camera permission + Face ID / key sign-in ≠ identity verified.

## Bank
- Payout bank = checking behind the debit (BoA), not X/Cross River card PAN.
- Instant bank-link first; micro-deposits fallback. Numbers stay in Dashboard.
- Native Stripe app cannot add a bank. Use Safari → dashboard.stripe.com only.

## Tap path (Safari)
1. Header: The Shepherd.
2. Top banner: View account status. No banner = nothing currently due.
3. Settings (gear) → Business → Account details = identity.
4. Business → Bank accounts and currencies → Add bank account.
5. In the app: Home banner or top-left account icon → Settings → Business. Stop. Do not open Developers.

## Developers trap
Developers page is settings. Nothing to paste. Wrong wing for the green check.

## Chat rule
Chat is for error text, not documents. Never send ID, card, or check photos to Grok, Notion, Drive, GitHub, or email.

## Crib sheet (routing not on card)
- MICR line on an unused check: left = 9-digit ACH routing, middle = account, right = check number.
- Best: unused check with VOID written on it.
- Use ACH routing, not wire routing from a bank webpage.

## Status 2026-09-08 ~18:00 EDT
Identity: OPEN. Bank: OPEN. Pudding: pudding=0 morning.

## Navigation iteration (appended 2026-09-08 ~18:08)
Hamburger/sidebar and settings sub-pages still imperfect — see knowledge/navigation-iteration-log-2026-09-08.md. Append corrections as they surface.
