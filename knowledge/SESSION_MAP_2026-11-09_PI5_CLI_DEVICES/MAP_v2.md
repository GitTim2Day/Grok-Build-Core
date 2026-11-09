# SESSION_MAP_2026-11-09_PI5_CLI_DEVICES MAP_v2 (re-map after audit)
OPEN: 2026-11-09T14:03:30Z (= 2026-11-09T09:03:30-05:00 EST display; HTTPS Date agreement to the second, +-1 s)
Scope: re-map of today's Pi 5 CLI / Gmail zip / device-build session after AUDIT.md. Nothing from MAP_v1 dropped. Fixes: INFERRED/UNVERIFIED labels tightened; device-menu pointers added; corrections M1–M3 kept.

## Checked (re-hashed or connector-verified)
- S21 post-boot fc15a5947acdd023… MATCH living SKILL; audit de33a3b5…; map v2 850c3685…; ledger queue 18 before this append; S21 findings 1. [E1]
- Pointer-only rule + POINTER_INDEX 5fc7d43a… [E2]
- Gmail 1a1c08f5e4df2914 2026-11-09 08:46:22 -0500 attachment zip 39927 sha aa0b0578cdca7f19… MATCH disk. [E7]
- Gmail 1a1bfc72beb82ec6 2026-11-08 20:13:38 -0500 subject-only; attachments none found. [E6]
- Export: conversations/projects/tasks none found; media_posts 1; billing empty; sessions 1; api_keys none found. Personal fields not published. [E8]
- Device menu files MATCH SHA256SUMS (md/txt/json). [E12]
- Exact spelling GitTim2Day: PASS (vowels i,i,a; consonants G,t,T,m,D,y). [save D4]

## UNVERIFIED / INFERRED (kept explicit)
- U1: Mode behaviors (asks / auto / never asks) INFERRED from names, not product-docs verified. [E4, A2]
- U2: Pi on-device signed-in state not live-verified from this box; evidenced by Timothy photos/turns. [E3, A3]
- U3: Photo "3 hours ago" / "5:07 AM" assistant reading vs Gmail Date 2026-11-08 20:13:38 -0500 — mismatch cause UNVERIFIED. Correction: use connector Date. [E9, A1]
- U4: A15 brand ASUS vs Acer UNCONFIRMED. [E11, A4]
- U5 (carried S21): unpaid-invoice failed-nightly cause UNVERIFIED on disk. [E1, A5]

## Patterns (v1 P1–P10 retained; audit-tightened)
P1. Fail-closed / verify-before-claim — unpaid invoice, photo time, mode behaviors, A15 brand, export PII redaction.
P2. Exact spelling + pointer-only sharing (t693u format; GitTim2Day gate).
P3. Pi 5 CLI recovery: Ctrl+C → `grok login --device-auth` → Allow → Grok 4.7 (high). CLI 1.0.25 stable.
P4. Mode-bar ambiguity: Normal unlabeled; Plan yellow; Auto review blue; Always approve (avoid; INFERRED). Shift+Tab cycles.
P5. Apples-to-apples: same model/effort, mode, prompt/inputs, fresh session, 2–3 repeats.
P6. Attachment discipline: paperclip/attach; subject text is not a file (proven by E6 vs E7).
P7. Wrong-account export: no conversations/projects/tasks — need export from the account that holds chats.
P8. Device-build matrix + ask-before-delete: never recommend deletion until every target device is listed.
P9. Cross-device records: .txt/.ods/.json/.jsonl + SHA-256; menu installs nothing.
P10. Locked save order (t713u): ledger queue only → Notion → GitTim2Day/Grok-Build-Core knowledge/ → Drive → boot append (archive-first). No email send. Never Yahoo/Cursor/kbld9/protected/BOOT.bas.

## Lessons learned (keep)
L1. Subject line ≠ attachment; always use Attach/paperclip (or drag into the message body).
L2. Ask about every target device before recommending delete of any installer/package.
L3. Mark name-inferred product behavior as INFERRED until docs or a live test confirm it.
L4. Prefer connector/Date headers over phone relative times ("3 hours ago") when dating mail.
L5. Keep amd64 .deb for A15 Linux dual-boot; Pi/Jetson need ARM64; Windows needs .exe/.msi; Rabbit is Android/web.
L6. Apples-to-apples needs model+effort+mode+prompt+fresh session+repeats, not model alone.

## Mistakes / corrections (append-only)
M1. Assistant dated subject-only zip email as "today 5:07 AM ET"; connector says 2026-11-08 20:13:38 -0500. CORRECTED.
M2. Assistant suggested deleting grok-bot_0.78.5_amd64.deb before learning A15 dual-boots Linux. CORRECTED by keep-for-A15-Linux guidance.
M3. Mode behavior claims were name-inferred. Labeled INFERRED in v2.

## Evidence index (v1 items E1–E14 all retained)
E1 S21 done / ledger 18 / findings 1 · E2 pointer rule · E3 Pi CLI recovery · E4 modes · E5 apples-to-apples · E6 subject-only mail · E7 from-downloads zip · E8 export empty chats · E9 photo/date correction · E10 amd64 .deb · E11 device guide + brand UNCONFIRMED · E12 device menu on disk · E13 Timothy deleted Pi zip dupes · E14 t713u map-audit+save order.

## Device-menu pointers (present at remap)
- workspace · /workspace/device-build-menu-2026-11-09/DEVICE_MENU.md · Device menu md · 086c6de5abf16a56 · 2026-11-09
- workspace · /workspace/device-build-menu-2026-11-09/DEVICE_MENU.txt · Device menu txt · b69613fb133ec964 · 2026-11-09
- workspace · /workspace/device-build-menu-2026-11-09/DEVICE_MENU.json · Device menu json · c65bae4a73c87c57 · 2026-11-09
- workspace · /workspace/device-build-menu-2026-11-09/SHA256SUMS.txt · Device menu sums · ed78e87362272bd9 · 2026-11-09

## Other pointers
- workspace · /workspace/inbox-zip-2026-11-09/4a8c7794-eb74-485d-9e50-43d3c85a60ab.zip · Grok export zip · aa0b0578cdca7f19 · 2026-11-09
- workspace · /workspace/boot-archive/boot-summary-2026-10-24_SKILL_archived_2026-11-09T1305Z_post-S21.md · post-S21 boot · fc15a5947acdd023 · 2026-11-09
- workspace · /workspace/boot-archive/NIGHTLY_AUDIT_S21_2026-11-08.md · S21 nightly audit · de33a3b5dce24aa5 · 2026-11-09
- workspace · /workspace/pointer-index-physics-math-2026-11-09/POINTER_INDEX.md · pointer index · 5fc7d43a46ab9282 · 2026-11-09

## Drop check
MAP_v1 patterns P1–P10, evidence 1–14, mistakes M1–M3, decisions D1–D7: all present in v2 (decisions execute in save phase). Drops: none found.

## Audit findings count
4 (A1–A4). Hash mismatches: none found.

CLOSE: ready for sealed save.
