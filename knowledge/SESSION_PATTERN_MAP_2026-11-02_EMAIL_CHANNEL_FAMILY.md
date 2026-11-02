# EMAIL CHANNEL FAMILY MAP — 2026-11-02

## Three addresses, one channel family

Not three separate pipes. One logical channel with three endpoints.

### 1. Gmail — timnorman730@gmail.com
- Primary ledger recipient. Standing dual-To target on every Grok-Build-Ledger hop.
- Token permanently revoked this sitting (2026-11-02); re-authenticated via connected-services re-auth.
- Fresh token verified: test message 1a19e920364174e3, 18:20 EST.

### 2. Yahoo — timothy_h_norman@yahoo.com
- Secondary ledger recipient, same dual-To pattern.
- Old store under investigation: Yahoo killed Apple Mail IMAP pipe, moved to OAuth.
- Raw IMAP hostname no longer visible in Apple Mail on iPhone.
- Desktop IMAP blocked by password change.
- Yahoo Data Download export started 2026-11-02, in progress.
- Security timeline: password changed 2026-08-15, 2026-08-24, 2026-10-25.
- Oct 20: 800 notifications, blocked connections 21:47.
- Oct 25: attack notification while user away.
- Junk: 434 unread — likely attack traffic.
- Cursor (Anysphere) held OAuth to Yahoo+Gmail pre-acquisition; revoked this sitting.
- AgentMail Dashboard granted 2026-08-29 — same window; Google link killed.

### 3. Hotmail — timothy_h_norman@hotmail.com
- Third recipient on several Outlook-received emails.
- Not previously documented. Status unknown.

## Outlook observation

Outlook inbox receives from Yahoo address: 54 unread inbox, 434 unread Junk.
Yahoo pipes/forwards into Outlook. Outlook is a downstream sink, not a separate connector.

## Channel-family rule

Seal to the family = dual-To Gmail+Yahoo minimum. Hotmail added when confirmed active.
Yahoo export, when landed, gets hashed and sealed under this row — no separate map.

## Open items

- Hotmail status.
- Yahoo export completion.
- Oct 20–25 attack traffic vs Cursor token window correlation.

## Close stamp

Fetch-only, America/New_York. See ledger email for UTC.