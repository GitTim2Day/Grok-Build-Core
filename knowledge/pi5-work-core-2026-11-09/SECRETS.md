# SECRETS SCAN — work_core_2026-11-09.zip (extracted, read-only)

**No secret values, partial values, or hashes of values appear in this file or in SECRETS_HITS.tsv.** Only path, line, key name and type.

## Method

1. Regex scan (scripts/secscan.py) over every text file (all 20410 files walked; binaries skipped; named-assignment pass on files < 50000000 bytes): OpenAI/Anthropic `sk-`, xAI `xai-`, GitHub `ghp_/gho_/ghs_/github_pat_`, AWS `AKIA/ASIA`, PEM private-key blocks, Google `AIza`, Google OAuth `GOCSPX-`/`ya29.`/`1//0`, Slack tokens and webhooks, Stripe, JWT, credentialed URLs `scheme://user:pass@host`, SSH public keys, Telegram, HF, Notion, Twilio SID, Discord, plus named assignments (`*api_key*`, `*token*`, `*password*`, `*secret*`, `*cookie*`, `*session_id*`, … = literal of ≥8 chars, placeholders/env lookups excluded).
2. Filename scan: `.env*`, `id_rsa/id_ed25519/…`, `*.pem/*.key/*.p12/*.pfx`, `credentials*.json`, `client_secret*.json`, `service_account*.json`, `token.json`, `.netrc`, `.git-credentials`, `.pgpass`, `.npmrc`, `.pypirc`, cookie files, `.ssh/`.
3. Yelp detect-secrets 1.5 (installed in a project-local venv, `--all-files --force-use-all-plugins`), excluding only `maps/` and `oeis_earn/run/{PARI_BLOCKS,inventory}.jsonl` (public OSM / OEIS data, 892121252 + 125728198 bytes) because the entropy plugins did not finish on them in 13 minutes. gitleaks and trufflehog are not pip-installable, so they were not used.
4. Targeted grep for salt / HMAC / signing / private-key material; manual triage of every non-venv hit by looking at the line shape with the value masked.

## Headline

- **High-confidence live credentials (API keys, tokens, passwords, private keys, credentials JSON, .env, SSH private keys, cookie jars): 0.**
- `.env` files: 0. SSH private key files: 0. PEM private-key blocks: 0. credentials/client_secret/token JSON files: 0. Cookie files: 0. `.netrc`/`.git-credentials`: 0.
- Raw hits: 10497 (regex 280, detect-secrets 10209, filename 4, manual 4).
- Verdicts: FP 10468, INFO 17, LOW 10, PII 2.

## Count by type × verdict

| type | verdict | hits |
|---|---|--:|
| Hex High Entropy String | FP | 9906 |
| Base64 High Entropy String | FP | 284 |
| named_secret_assignment | FP | 261 |
| url_with_credentials | FP | 8 |
| Base64 High Entropy String | INFO | 7 |
| named_secret_assignment | LOW | 6 |
| ssh_public_key | INFO | 4 |
| Basic Auth Credentials | FP | 4 |
| Artifactory Credentials | FP | 4 |
| pem_or_key_file | INFO | 4 |
| Secret Keyword | LOW | 3 |
| personal identifiers (device-only file) | PII | 2 |
| named_secret_assignment | INFO | 1 |
| Twilio API Key | FP | 1 |
| synthetic chain salt + Ed25519 public key + signature (header) | INFO | 1 |
| hard-coded fixed salt constant | LOW | 1 |

## Items worth a look (everything not FP), path · line · key · type

- `work/Grok-Build-Core/edge-canvas-kit/selfcheck.py` · line 169 · key `token` · named_secret_assignment — LOW: hard-coded token literal passed to start(lan=True) in a self-test (fixture; confirm synthetic)
- `work/Grok-Build-Core/knowledge/FIVE_SHELF_MANIFEST_2026-10-01T1531-0400.json` · line 6 · key `prior_manifest` · Base64 High Entropy String — INFO: Google Drive file/folder ID (identifier, not a credential)
- `work/Grok-Build-Core/knowledge/FIVE_SHELF_MANIFEST_2026-10-01T1531-0400.json` · line 24 · key `drive_encounter` · Base64 High Entropy String — INFO: Google Drive file/folder ID (identifier, not a credential)
- `work/Grok-Build-Core/knowledge/FIVE_SHELF_MANIFEST_2026-10-03T1314-0400.json` · line 16 · key `drive` · Base64 High Entropy String — INFO: Google Drive file/folder ID (identifier, not a credential)
- `work/Grok-Build-Core/knowledge/FIVE_SHELF_MANIFEST_2026-10-03T1314-0400.json` · line 34 · key `drive_live_folder` · Base64 High Entropy String — INFO: Google Drive file/folder ID (identifier, not a credential)
- `work/Grok-Build-Core/knowledge/FIVE_SHELF_MANIFEST_2026-10-03T1314-0400.json` · line 54 · key `drive_encounter_prior` · Base64 High Entropy String — INFO: Google Drive file/folder ID (identifier, not a credential)
- `work/Grok-Build-Core/knowledge/FIVE_SHELF_MANIFEST_2026-10-03T1314-0400.json` · line 58 · key `drive_live_set` · Base64 High Entropy String — INFO: Google Drive file/folder ID (identifier, not a credential)
- `work/Grok-Build-Core/knowledge/gosub_drive_drain.py` · line 1 · key `CANON_A` · Base64 High Entropy String — INFO: Google Drive file/folder ID (identifier, not a credential)
- `work/escalations/identity.txt` · line (whole file) · key `user, device, place, coord` · personal identifiers (device-only file) — PII: README marks it DEVICE ONLY, never shipped; it is in this archive
- `work/escalations/rules.txt` · line (whole file) · key `15 lines of form R|… (per README: names, email, place, paths)` · personal identifiers (device-only file) — PII: README marks it DEVICE ONLY, never shipped; it is in this archive
- `work/jcj/selfcheck_jcj.py` · line 373 · key `secret` · Secret Keyword — LOW: hard-coded literal assigned to `secret` in a self-test (fixture; confirm it is synthetic)
- `work/jcj/selfcheck_jcj.py.before_apostrophe_2026-10-15` · line 364 · key `secret` · Secret Keyword — LOW: hard-coded literal assigned to `secret` in a self-test (fixture; confirm it is synthetic)
- `work/jcj/versions/pre_sections_2026-10-14/selfcheck_jcj.py` · line 353 · key `secret` · Secret Keyword — LOW: hard-coded literal assigned to `secret` in a self-test (fixture; confirm it is synthetic)
- `work/runs/head1/log.txt` · line 11 · key `set-cookie` · named_secret_assignment — LOW: Set-Cookie response header from a public news site captured in a run log
- `work/runs/head1/log.txt` · line 16 · key `set-cookie` · named_secret_assignment — LOW: Set-Cookie response header from a public news site captured in a run log
- `work/session_maps/2026-10-15/MAP_2.json` · line 10223 · key `label` · ssh_public_key — INFO: SSH PUBLIC key (not secret) with Windows user@host label
- `work/session_maps/2026-10-15/MAP_3.json` · line 10838 · key `label` · ssh_public_key — INFO: SSH PUBLIC key (not secret) with Windows user@host label
- `work/session_maps/2026-10-16/MAP_2.json` · line 10545 · key `label` · ssh_public_key — INFO: SSH PUBLIC key (not secret) with Windows user@host label
- `work/session_maps/2026-10-16/MAP_3.json` · line 11172 · key `label` · ssh_public_key — INFO: SSH PUBLIC key (not secret) with Windows user@host label
- `work/svct_log/SVCT_DRIVE_PARTS_LOG_2026-10-14.md` · line 10 · key `originSessionId` · named_secret_assignment — INFO: session identifier, not a credential
- `work/svct_v20_in/svct_v20/REGISTRY_TABLE_v19z6.tsv` · line 1 · key `salt / pinned_pk / head_sig` · synthetic chain salt + Ed25519 public key + signature (header) — INFO: file is marked SYNTHETIC; code says salt is "not secret"; no private key stored
- `work/svct_v20_in/svct_v20/chain_v19s.py` · line 79 · key `LEGACY_FIXED_SALT` · hard-coded fixed salt constant — LOW: documented legacy weak salt; code replaces it with per-chain random salt
- `work/venv_csvson/lib/python3.13/site-packages/pip/_vendor/certifi/cacert.pem` · line (whole file) · key `(file)` · pem_or_key_file — INFO: public CA certificate bundle (certifi cacert.pem), no private key
- `work/venv_csvson/lib64/python3.13/site-packages/pip/_vendor/certifi/cacert.pem` · line (whole file) · key `(file)` · pem_or_key_file — INFO: public CA certificate bundle (certifi cacert.pem), no private key
- `work/venv_oeis/lib/python3.13/site-packages/pip/_vendor/certifi/cacert.pem` · line (whole file) · key `(file)` · pem_or_key_file — INFO: public CA certificate bundle (certifi cacert.pem), no private key
- `work/venv_oeis/lib64/python3.13/site-packages/pip/_vendor/certifi/cacert.pem` · line (whole file) · key `(file)` · pem_or_key_file — INFO: public CA certificate bundle (certifi cacert.pem), no private key

## Personal / device-only data in the archive (not credentials, but sensitive)

`work/escalations/README.txt` says these are DEVICE ONLY and "never shipped". They are present in this zip:
- `work/escalations/authorizations/SVCT_000001_1791847951_8556c56f9867065d.rec` (913 bytes)
- `work/escalations/deliveries/SVCT_000001_1791848144_8556c56f9867065d.rec` (999 bytes)
- `work/escalations/handoffs/SVCT_000001_1791848027_8556c56f9867065d.rec` (887 bytes)
- `work/escalations/identity.txt` (110 bytes)
- `work/escalations/map/A0001_map.txt` (962 bytes)
- `work/escalations/map/A0002_map.txt` (1189 bytes)
- `work/escalations/map/A0003_map.txt` (3966 bytes)
- `work/escalations/map/A0004_map.txt` (10897 bytes)
- `work/escalations/map/A0005_map.txt` (25571 bytes)
- `work/escalations/map/A0006_map.txt` (36014 bytes)
- `work/escalations/map/A0007_map.txt` (36089 bytes)
- `work/escalations/map/A0008_map.txt` (35925 bytes)
- `work/escalations/outbound/RPi5/8556c56f9867065d.txt` (830 bytes)
- `work/escalations/pending/33c834a1afffa7dd/engine_out.txt` (1093 bytes)
- `work/escalations/pending/33c834a1afffa7dd/meta.txt` (698 bytes)
- `work/escalations/pending/33c834a1afffa7dd/payload.txt` (165 bytes)
- `work/escalations/pending/33c834a1afffa7dd/preview.txt` (1376 bytes)
- `work/escalations/pending/8556c56f9867065d/engine_out.txt` (2560 bytes)
- `work/escalations/pending/8556c56f9867065d/meta.txt` (705 bytes)
- `work/escalations/pending/8556c56f9867065d/payload.txt` (830 bytes)
- `work/escalations/pending/8556c56f9867065d/preview.txt` (2112 bytes)
- `work/escalations/records/SVCT_1791825520.rec` (17472 bytes)
- `work/escalations/records/SVCT_1791827915.rec` (26561 bytes)
- `work/escalations/records/SVCT_1791836159.rec` (37084 bytes)
- `work/escalations/records/SVCT_1791836469.rec` (37159 bytes)
- `work/escalations/records/SVCT_1791836616.rec` (36995 bytes)
- `work/escalations/rules.txt` (446 bytes)

Also: 4 Bluetooth MAC addresses in `work/.claude/settings.local.json` allow-list entries; Windows user@host label next to the SSH public key in `work/session_maps/2026-10-15/MAP_2.json`, `MAP_3.json`, `work/session_maps/2026-10-16/MAP_2.json`, `MAP_3.json`; owner email addresses appear in git commit metadata and in several checkpoint/handoff notes (not enumerated).

## False positives, summarised

- FP: hash digest value (sha1/sha256/sha512-length hex): 9734
- FP: third-party library code in a Python venv: 690
- FP: long file path / command argument: 20
- FP: git sample hook variable: 6
- FP: parser variable named token: 6
- FP: runtime token variable/URL template, no literal: 5
- FP: hex digest/run id in record (no credential key name): 4
- FP: variable test, no literal: 1
- FP: token generated at runtime with secrets module: 1
- FP: Intel HEX firmware record: 1

Full list (every hit, no values): `SECRETS_HITS.tsv`.

## Rotate / remove (by path only)

- Rotate: **nothing found that needs rotation.**
- Confirm synthetic, then leave or replace with an obviously fake marker: `work/jcj/selfcheck_jcj.py` line 373 (and its two older copies), `work/Grok-Build-Core/edge-canvas-kit/selfcheck.py` line 169.
- Remove from any copy that leaves the Pi: the DEVICE ONLY files listed above; `work/runs/head1/log.txt` (captured Set-Cookie headers).
