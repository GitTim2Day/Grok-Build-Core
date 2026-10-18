# bwbasic 2.20 restore and hybrid rebuild — 2026-10-18 (America/New_York)

Work ran 12:26–12:40 PM EDT on the shared box. The as-found lookup is in /workspace/bwbasic-locate-2026-10-18/REPORT.md.

## As found (12:27 PM EDT)
- `which bwbasic`: none.
- /usr/bin/bwbasic, /opt/bwbasic-3.20b and /opt/bwbasic-hybrid were all absent.
- Hybrid SHA256SUMS: 434 OK, 2 missing (the two /opt binaries).
- No 2.20 binary or .deb anywhere. Sealed copies of the unified, hybrid and 3.20 binaries were present inside /workspace.

## Done
1. **bwbasic 2.20** (12:29 PM EDT): `sudo apt-get install -y bwbasic` installed Debian **2.20pl2-14** (80.1 kB, deb.debian.org trixie/main, free).
   - /usr/bin/bwbasic sha `0334b1cc270b7e10e26135927a5c18d44f0291c4871903898c33b2bb535f9b8f` **MATCHES** the recorded system seal (sys_bwbasic_before.sha256, run_core_tests.py EXPECT).
   - The banner reads "version 2.20 patch level 2".
2. **Rebuild from saved source** (12:31–12:32 PM EDT): all three builds are bit-exact.
   - `/opt/bwbasic-hybrid/bwbasic-unified`: `gcc -O2 bw*.c -lm` on unified/src gives `2f7e6cd7579f219e786a1a0fc644ab38dcaf44914be887dfa551baa7a5327a27`. **MATCH**.
   - `/opt/bwbasic-hybrid/bwbasic-hybrid`: the src/bwbasic-hybrid script gives `bcbac33583d4f26945a99356a3c5d833eb07fddda804acd4d70c676918c0753d`. **MATCH**.
   - `/opt/bwbasic-3.20b/bwbasic320`: `gcc -ansi -pedantic -Wall bw*.c -lm` on bwbasic320 src/x gives `85627c86a8ac51c44a67c403bd0c300dd8aa49cbfd0ed97006c1a8e37dbd5e9a`. **MATCH**. It is restored because bwbasic320-2026-10-18/README.md and bwbasic320_binary.sha256 define it.
   - Hybrid `sha256sum -c SHA256SUMS`: **436/436 OK**.
   - The hashes matched, so tests were optional. I ran them anyway from a scratch copy:
     - core **23/23**
     - mutation/detector **296/296** (A 24/24, B-active 72/72, B-inert 96/96, B-lowercase 48/48, C 26/26 + 6/6, rule-deletion 24/24 killed)
     - detector consistency on today's larger corpus: 1698 files, 439 unique, 419 agree on definite, 0 disagree, 20 Python-ambiguous where C picks 2.20
3. **Boot** (12:30 PM EDT): `bwbasic /workspace/hybrid-boot/BOOT.bas` printed **0.70710678**.
   - Exit 0.
   - The output sha `64830efb…4551` is byte-identical to the 2026-10-18 boot_run_220.txt record.
   - BOOT.bas sha a8a21b61…7901 was the same before and after.
   - The script's verify, restore and check runs at 12:34 PM EDT also gave BOOT PASS.
4. **Restore kit**: this folder plus a verified copy in reference-map/bwbasic-restore-2026-10-18/.
   - `restore_bwbasic.sh check|verify|restore` is idempotent and fails closed. It runs under flock.
   - It falls back to a source build of 2.20 if apt fails. That path was tested in scratch: the build is a0b8b110… (no seal) and its BOOT output is byte-identical.

## Incident (self-caused, fixed)
- The first core-test run from a copy rewrote the sealed `tests/results/core_tests.json`, because ROOT is hardcoded.
- I restored it from the pre-run copy (d6829f1f…, mtime preserved) at 12:32 PM EDT. Hybrid SHA256SUMS is back to 436/436 OK.

## Not done here
- Email, Notion, GitHub and Drive saves were held for user approval. The parent has the drafts.

## Files
restore_bwbasic.sh, SKILL_DRAFT.md (bwbasic-boot-restore), sources/S320_INPUTS.sha256, logs/ (apt, install, boot, tests, build repro, script runs), JOURNAL.md, SHA256SUMS.

## Iteration log
- `artifacts/bwbasic_iteration_log.jsonl` is append-only.
- Rows for iterations 1–3 are backfilled:true.
- Iteration 4 ran live at 12:38:57 PM EDT. All seals MATCH and BOOT PASS.
- The first row landed at 2026-10-18 12:38:39 PM EDT.
- Helpers: artifacts/logrow.py and artifacts/backfill_rows.py.
