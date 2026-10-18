---
name: bwbasic-boot-restore
description: At load or boot, on every seat, run restore_bwbasic.sh check before BOOT.bas. It makes sure bwbasic 2.20 (with the 3.20 build and the hybrid) is present and hash-verified, restores whatever is missing from the saved sources, then runs BOOT.bas and fails closed unless it prints 0.70710678.
version: 2026-10-18
---
# bwbasic-boot-restore

## Why
A box restart (~09:30 ET, 2026-10-18) removed /usr/bin/bwbasic (2.20), /opt/bwbasic-3.20b and /opt/bwbasic-hybrid. /workspace survived. BOOT.bas needs 2.20 to print 0.70710678.

## Boot step (every seat)
1. `bash /workspace/bwbasic-restore-2026-10-18/restore_bwbasic.sh check`
   - Exit 0 means 2.20 is present, the /opt binaries match their seals, and BOOT.bas printed 0.70710678.
   - Any other exit means STOP and report the last log line from `logs/`. Do not continue past boot.
2. Only after that run any other boot steps (SOURCES_OF_TRUTH, timecap, ...).

## Modes
- `check` (default): verify, repair whatever is missing, then boot.
- `verify`: read-only, then boot.
- `restore`: forced reinstall and rebuild, then boot.

## What it restores (idempotent; every step checks before acting)
| piece | how | expected sha256 |
|---|---|---|
| bwbasic 2.20 | `apt-get install bwbasic` (Debian 2.20pl2-14, free). Fallback: build orig.tar.gz + 4 Debian patches with gcc into /usr/local/bin/bwbasic | 0334b1cc270b7e10e26135927a5c18d44f0291c4871903898c33b2bb535f9b8f (apt). A source build has no seal; its BOOT output must match 64830efb… |
| /opt/bwbasic-3.20b/bwbasic320 | `gcc -o bwbasic320 -ansi -pedantic -Wall bw*.c -lm` in a copy of /workspace/bwbasic320-2026-10-18/src/x | 85627c86a8ac51c44a67c403bd0c300dd8aa49cbfd0ed97006c1a8e37dbd5e9a |
| /opt/bwbasic-hybrid/bwbasic-unified | `gcc -O2 -o bwbasic-unified bw*.c -lm` in a copy of …/bwbasic-hybrid-2026-10-18/unified/src | 2f7e6cd7579f219e786a1a0fc644ab38dcaf44914be887dfa551baa7a5327a27 |
| /opt/bwbasic-hybrid/bwbasic-hybrid | copy of src/bwbasic-hybrid | bcbac33583d4f26945a99356a3c5d833eb07fddda804acd4d70c676918c0753d |

- Sources are verified before any build: the hybrid SHA256SUMS (minus its /opt lines) and sources/S320_INPUTS.sha256.
- If a rebuild's hash differs, the sealed saved binary is installed instead and the mismatch is logged.

## Rules
- Never edit BOOT.bas; it is only hash-checked (a8a21b61…7901) and run.
- Never touch /workspace/kbld9/protected/ or svct_v20*.
- Run in a clean temp cwd, because a stray profile.bas in the cwd changes the banner.
- No spend. apt is from the standard Debian repos only.
