---
name: gmail-connecter
description: Gmail connector for Timothy Norman. Private path first. Send, draft-first compose, search with Gmail operators, full message read, label changes (archive/star/trash), forward, reply-all, custom label creation, send-as alias listing. No sudo, no extra charge. Sealed 2026-11-06.
---

# Gmail Connecter

## Purpose
Gmail as a connected service for Timothy Norman. Complements the calendar Connecter (private iCal primary, CONNECTORS fallback). Gmail is its own path — not merged into calendar duties.

## Capabilities
- **Send**: gmail_send_message (immediate, irreversible) or gmail_create_draft then gmail_send_draft (reviewable)
- **Search**: gmail_search with Gmail operators (from:, to:, subject:, newer_than:, older_than:, has:attachment, is:unread, label:)
- **Read**: gmail_get_message for full thread content
- **Labels**: gmail_modify_labels (mark read/unread, star/unstar, archive, trash, spam, important)
- **Drafts**: gmail_create_draft, gmail_update_draft, gmail_delete_draft, gmail_list_drafts, gmail_send_draft
- **Labels admin**: gmail_create_label
- **Send-as**: gmail_list_send_as (aliases and delegated addresses)

## Rules
- Draft-first for anything the user might want to review before sending
- Direct send only when the user explicitly says send
- No sudo, no elevation, no extra charge
- Mask-first: no PHI, no card numbers, no SSNs in generated fill
- Append-only ledger: every send gets a Grok-Build-Ledger email to timnorman730@gmail.com AND timothy_h_norman@yahoo.com with subject starting Grok-Build-Ledger, hashes, and shelf links
- Save order: email hop FIRST, then Notion, GitHub, Drive, then local

## Error handling
- If gmail_search returns empty, say so — do not invent messages
- If send fails, report the error verbatim; do not retry silently
- If a draft_id is stale, list drafts and use a fresh one
- Quarantine any failure as a status row before proceeding

## Pointer
Body on shelves: GitHub Grok-Build-Core/knowledge, Notion Timothy Skills & KB, Drive Grok_Build_Archives_2026, Gmail timnorman730@gmail.com. This file is the pointer only.
