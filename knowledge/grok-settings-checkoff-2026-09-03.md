# Grok Platform Settings Check-off List (2026-09-03)

**Owner:** Timothy H Norman  
**Status:** Append-only. Manual gate for the boot system.

The platform does not auto-inject the Notion/GitHub gate. These toggles make it reliable.

## 1. Memory / Personalization (Data Controls)
- [ ] grok.com or app → profile → Settings → Data Controls
- [ ] Toggle **Personalize Grok with your conversation history** ON
- [ ] Confirm memories visible + deletable
- [ ] (Optional) Personalize Grok using X — only if desired

## 2. Custom Instructions (global, ~4,000 char limit)
- [ ] Settings → Customize → Custom Instructions
- [ ] Paste: "On every new session run notion-first-session-boot: query Timothy Skills & KB first, load GitHub Grok-Build-Core/knowledge, check Gmail drafts + flagged links, then state status. Append-only. Never overwrite."
- [ ] Save + open a **new** chat to verify

## 3. Skills
- [ ] Confirm notion-first-session-boot + session-boot-flagged-links-2026-09-03 active
- [ ] New skills = Notion pages in Timothy Skills & KB with is_skill true

## 4. Custom Agents (optional, 4 slots)
- [ ] Create "Timothy Continuity" agent with boot gate as system prompt

## 5. Workspaces / Projects
- [ ] Create/open "Grok Build" workspace
- [ ] Upload key exports if always-in-context needed
- [ ] Workspace instructions → Notion living index

## 6. Connectors
- [ ] Gmail, Drive, GitHub, Notion, Calendar connected + authorized
- [ ] Re-auth if Notion agent-session scope missing

## 7. Model & Mode
- [ ] Frontier model (Grok 4.x) + Expert/Heavy for complex builds

## 8. Privacy
- [ ] Improve-the-model OFF (no training)
- [ ] Private Chat (ghost) for sensitive work

**Note:** Custom Instructions changes apply only to new conversations.

Appended 2026-09-03 20:40 EDT. Append-only.
