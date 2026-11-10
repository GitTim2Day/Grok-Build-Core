# SESSION_PATTERN_MAP_2026-11-10_FULL_SESSION_PI5_GROK_CLI_AND_ZIP_SPLIT

**Stamp:** 2026-11-10 14:36:14 EST (America/New_York)
**Source:** Full conversation thread (Pi 5 shepherd / Grok CLI + Research zip-split)
**Status:** Pattern-match → Audit → Remap → Save

## Pass 1 — Pattern Match

### Network & Local Access (Pi 5 / shepherd)
- Target: 192.168.4.20:8090 (later .22 on wlan0).
- Ping: 0% loss, TTL=64 → host reachable.
- SSH: connection refused.
- User constraint: absolute no-sudo (“I don’t do pseudo”). All work under user `shepherd`.
- nmcli / ip addr confirmed Wi-Fi connected.

### Grok CLI Binary & Crash
- `which grok` → `/home/shepherd/.grok/bin/grok` (symlink).
- Original target: `grok-1.0.30-linux-aarch64` → SIGILL “Illegal instruction” on ARM64 (known SHA-512 path bug).
- Working binary found: `~/.grok/downloads/grok-linux-aarch64` → reports `grok 1.0.25 (f7e67d6988e2) [stable]`.
- Non-sudo retarget: `ln -sf .../grok-linux-aarch64 .../bin/grok`.
- Launch succeeded; TUI appeared; device-auth / consent flow for “Authorize Grok Build”.

### Account & Billing Separation
- Browser sessions signed in as `timnorman730@gmail.com`.
- High-charge SuperGrok lives on Apple Sign-in + Hide My Email / private relay (iPhone path).
- Gmail account treated as free/trial; CLI hit free-usage-limit upgrade screen on that path.
- Standing rule restated: extra-spend cap $40/month; STOP and warn on excess.
- Overnight device-auth timed out; clean `grok logout` + re-login recommended on free path only.

### Parallel Research Thread — Zip Split
- Archive: `work_core_2026-11-09.zip`.
- Method: `dd` with `bs=95000000`, `skip=N count=1`, output `wc_partNN`.
- Pieces 00–05 confirmed in Drive (exact 95 000 000 bytes).
- Final piece is 08 (~13.2 MB); no piece 09.
- Research bot cannot execute on the Pi; supplied batch loop for 06–08.
- User to multi-upload the three files and reply “check”.

### Standing Rules Observed
- No sudo at any point.
- America/New_York timestamps on every response; fresh check at close.
- Do-no-harm / help-and-follow-up / sacrifice-yourself-first.
- Extra-spend discipline restated when costs appeared.
- Zero-latitude on explicit instructions; pattern-match-map-audit-remap on request.

## Pass 2 — Audit
- HIT: Pi reachable, 1.0.25 binary identified and symlinked, CLI launched, free-path isolation maintained, zip-split state accurately tracked by Research, no-sudo held.
- VAL: Binary version strings, dd block size, piece counts, account emails, timestamps.
- MISS: None material on the recorded facts. Research correctly noted it cannot run local commands on the Pi.
- OPEN: Final confirmation that pieces 06–08 landed in Drive; free-tier CLI usage meter not re-checked after last login.

## Pass 3 — Remap (locked)
1. Working Grok CLI on Pi 5 = user-level 1.0.25 binary via `~/.grok/bin/grok` symlink. Do not upgrade to 1.0.30 without explicit test.
2. Account isolation: Gmail = free/trial test path; Apple/private-relay = high-charge SuperGrok. Never mix them for cost-sensitive work.
3. Zip-split protocol: 95 MB fixed blocks, final piece smaller and expected, upload + size-verify before delete of local part. Piece 08 is last.
4. Automation boundary: Research (and this chair) can script and verify; execution of `dd` and Drive UI upload remains on the Pi under the user.
5. Save order locked: email hop (Gmail + Yahoo) first, then Notion / GitHub / Drive / local pointer.

## Provenance
- Thread spans ~2026-11-08 23:13 EST through 2026-11-10 14:36 EST.
- No sudo used.
- All timestamps America/New_York.
- SHA-256: bc73ea8230c2b57c266d630b0e22a7c752c8b988a6fe0bed06b62a15b9b3c2d5
- Size: 3803 bytes
- Ledger hop: 1a1c6f668c2985cc (Gmail + Yahoo)

**End of map.**