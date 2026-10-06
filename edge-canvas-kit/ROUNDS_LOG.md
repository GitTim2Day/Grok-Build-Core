# ROUNDS_LOG — edge-canvas-kit (2026-10-06, box build; times ET)

Boot before work: `bwbasic /workspace/hybrid-boot/BOOT.bas </dev/null` → `0.70710678`, exit 0 (12:26 PM).
Every self-check round also boots (test `boot_ok_0.70710678`, via bwbasic on the box; via the Python twin on the bare-device run).
Box extras present during full rounds: bwbasic 2.20p2, g++ 14.2 (installed on the box 12:29 PM for this test only — not on Timothy's devices),
tesseract 5.5.0, pdftotext, Pillow, defusedxml, google-chrome (headless UI smoke). No Ollama on the box (local-model path tested as "absent → rules").
"Bare device" = a copy of the kit run with `env -i PATH=<python3 only> python3 -S` (no bwbasic, no compiler, no OCR, no Pillow,
no defusedxml, no browser) to imitate a fresh Pi without extras.

| Round | Time (ET) | Self-check result | Mutants | Found → mitigated |
|---|---|---|---|---|
| R0 | 12:26–12:36 | build: boot `0.70710678` (bwbasic, exit 0); server, UI, agent, lib, vendored txt_rcrj, BASIC files, C++ twins (steer 12:28), rcrj non-dict fix (steer 12:33), knowledge/ masked copies (residue 0) | — | g++ front end missing on the box → installed **on the box only** to test the C++ lane. First UI smoke: sandboxed iframe never answered (CORP same-origin on the sandbox assets; virtual time does not wait for isolated iframes) → sandbox assets cross-origin CORP, verdict taken from a real-time run. Screens falsely refused `kill` in a C++ comment and `KILL`/`COMMON` in BASIC REM lines → comments/strings stripped, whole-line REM skipped. |
| R1 | 12:37 | 216 pass / 8 fail | — | (1) `dx="1/0"` → HTTP 500 ZeroDivisionError → now 400 "zero denominator refused". (2) Agent indexed `selfcheck.py`, so it "knew" the test's own out-of-scope probe questions → test files excluded from the agent index. (3) static-scan false positives (fake hosts in the test file, the word innerHTML in a comment, the words "shell=True" in a docstring) → scans narrowed to code; docstring reworded. |
| R2 | 12:38–12:42 | **224 / 224 PASS** | 29 / 33 caught | Survivors: `..` guard (equivalent: the hidden-segment rule also refuses `..`), JSON cap raised to 1 GiB (test read the cap from the server module), mask-email mutant (mutant itself was faulty — regex survived under another name), C++ mul-overflow check removed (masked by the add-overflow check). |
| R3 | 12:43–12:59 | run1 HUNG (killed by timeout at 600 s); run2 229 / 1; then **230 / 230 ×3** · quick 218 + 2 skip · bare device **200 / 1** | 33 / 35 caught | (1) New `--lan` banner test hung: child stdout was block-buffered → `python -u` + 15 s kill timer. (2) Server kept HTTP/1.1 keep-alive after an error without reading the body, so leftover body bytes were parsed as a second request → every ≥400 reply now sends `Connection: close`. (3) C++ run CPU limit = wall timeout raced (SIGXCPU vs timeout) → CPU limit = timeout + 2 s (BASIC too). (4) `lan_addresses()` used `getaddrinfo(gethostname())`, which can trigger a DNS query → replaced by `hostname -I` (local, no traffic) or a printed template. (5) C++ twin got direct mul/add overflow self-checks (13 → 15 checks). (6) Strict header-only 413 probe (5 s) for caps. **Bare device: every XML file went to QUARANTINE** (see vendored fix B). |
| R4 | 12:59–13:00 | 234 / 2, 234 / 2, 233 / 3 · bare **206 / 206 PASS** (+4 skip) | — | (1) Vendored fix B was only applied on bare devices: the DTD refusal raised `XmlForbidden`, which the box's defusedxml exception class did not catch → catch both. (2) UI smoke flake 1 of 3: the page pinged the JS sandbox before the iframe had loaded → sandbox now posts `ready`; the page waits for `ready`/`load` before posting. UI smoke then 5 / 5 PASS. Caps test now uses literal limits (kills the 1 GiB mutant). |
| R5 | 13:01–13:08 | **236 / 236 PASS ×3** · quick **223 PASS + 2 skip** · bare device **206 PASS + 4 skip** · UI smoke PASS | 37 / 38 caught (1 equivalent survivor `fsguard_dotdot_check_off`; 1 UNTESTED) | No new code faults. **But see the incident below:** the `server_lan_runs_allowed` mutant (R2, R3 and R5 runs) left a self-restarting `/selftest` chain behind each time. |
| R6 | 14:13–14:21 | quick **229 PASS + 4 skip**; full **244 / 244 PASS**; bare device **214 PASS + 4 skip**; one bounded real `/selftest` (top level → child `--quick` 229 PASS + 4 skip; nested call refused) | **42 / 43 caught** + 1 UNTESTED, serial, 0 strays after every mutant; then the one survivor closed → **2 / 2** | Recursion guard (see incident). New tests: `selftest_flag_set_in_harness`, `agent_selftest_refuses_when_active`, `api_selftest_refuses_when_active`, `agent_selftest_child_gets_flag`, `agent_selftest_child_own_group`, `agent_selftest_child_is_quick`, `selftest_flag_restored`, `quick_never_calls_selftest` / `full_selftest_calls_only_refused_paths` (all with a recorder in place of a real spawn). New mutants: `agent_selftest_guard_off`, `agent_selftest_child_flag_off`, `agent_selftest_same_group`, `selfcheck_quick_calls_selftest`, `server_lan_runs_allowed_full` — all caught. The long-standing equivalent survivor `fsguard_dotdot_check_off` is now killed by `traversal_reason_is_traversal` (a `..` must be refused with the traversal reason, not only by the hidden-segment rule). |

## Incident — runaway /selftest chain (found 1:24 PM, box unusable ~1:26–2:13 PM ET; Timothy killed ~830 processes)
- **What:** at 1:24 PM `ps` showed `selfcheck.py --quick` processes under `/tmp/kit-mutants-*/server_lan_runs_allowed/`. Shortly after,
  the box stopped answering (every Shell/Read call "Service temporarily unavailable") until Timothy killed ~830 of them (~2:13 PM).
- **Cause (confirmed from the logs and temp dirs):** the mutant `server_lan_runs_allowed` turns off the "no code runs over `--lan`" gate.
  The self-check's probe `lan_selftest_off_by_default` sent `/selftest` to the LAN server; with the gate off, the agent started
  `selfcheck.py --quick`, which sent the same probe to its own LAN server, and so on — a self-restarting chain. The outer test only
  saw a 120 s request timeout (all three runs logged `rc=1 120.4s`, i.e. "caught"), then exited; the chain was left orphaned because
  the agent used `subprocess.run(timeout=600)` without a process group, and the in-process server thread died with the test.
  One chain per mutants run: `/tmp/kit-mutants-spzxqlhg` (R2, 12:42), `-rkg409be` (R3, 12:59), `-1i6c4utd` (R5, 13:08).
- **Why it was not seen earlier:** the mutant counted as CAUGHT, and the leftover processes were not checked for after each mutant.
- **Fixes (R6):**
  1. `agent.py` — `/selftest` refuses when `KIT_SELFTEST_ACTIVE=1`; the child always gets `KIT_SELFTEST_ACTIVE=1`; the child runs in
     its own process group (`start_new_session`), 600 s limit, and the whole group is killed on timeout and after exit.
  2. `selfcheck.py` — sets `KIT_SELFTEST_ACTIVE=1` for itself before importing the kit; `--quick` never sends `/selftest`
     (counted and asserted); every child it starts (banner server, Python twins, UI smoke) runs in its own group, killed on teardown.
  3. `ui_smoke.py` — the browser runs in its own group; the whole group (renderers, GPU, zygote) is killed.
  4. `mutants.py` — one mutant at a time (`--only`), own process group + `KIT_SELFTEST_ACTIVE=1` + timeout per test, a sweep after each
     mutant that kills anything still running under the mutants temp dir and stops the run if more than 50 are found.
  5. Box harness (not shipped): `safe_run.sh` = `setsid timeout -s KILL` + `KIT_SELFTEST_ACTIVE=1` + process cap; `run_mutants_serial.sh`
     runs each mutant through it and checks for `/tmp/kit-mutants-*` processes after each one.
- **Process cap note:** `ulimit -u` (RLIMIT_NPROC) counts every task of the user, threads included, and the box already runs ~550 for
  this user, so a flat 200 would block every fork. The cap used is **(current tasks + 200)** — at most ~200 new tasks per test run.
- **Result:** R6 serial mutants: 0 leftover processes after every one of the 44 runs; the old runaway mutant now fails fast (4.3 s quick, 10.3 s full).
- Old copies archived: `archive/pre-R6-fixes/` (agent.py, selfcheck.py, mutants.py, ui_smoke.py, README.md). Leftover temp dirs in /tmp were not deleted.

## Vendored-code fixes (kit copy only — PENDING port back to `/workspace/csvson-ingest-2026-10-05/txt_rcrj/` and GitHub)
- **A. rcrj.py non-dict record** (Timothy/parent steer 12:33 PM). `run()` built `ctx` with `rec.get(...)` before `isinstance(rec, dict)`,
  so `None` / a string / a number raised AttributeError and stopped the main line (reproduced on the original: "old raises AttributeError").
  Now the dict check runs first → `bad_record` node → run continues. Tests: `rcrj_non_dict_record_to_bad_record`, `rcrj_bad_text_and_line_no_continue`;
  mutant `rcrj_fix_reverted` caught. Old copy archived: `archive/vendor-pre-fix/rcrj.py.vendored-55619f57`.
- **B. to_txt.py XML without defusedxml** (found by the R3 bare-device run). The source set `DefusedXmlException = Exception` when
  defusedxml is missing, so every XML (and DOCX/XLSX/PPTX/ODT XML) went to QUARANTINE. Now: any DTD/ENTITY (UTF-8 or UTF-16) → QUARANTINE;
  XML without a DTD → stdlib ElementTree. Unchanged when defusedxml is present. Tests: `xml_without_defusedxml_*`, `docx_without_defusedxml_text`,
  `convert_xml_entity_bomb_quarantined`; mutants `to_txt_dtd_check_off`, `to_txt_fallback_exception_wide`. Old copy archived:
  `archive/vendor-pre-fix/to_txt.py.vendored-f2fb5b36`.

## Not tested / parked
- Real Raspberry Pi 5, real phone over `--lan`, Windows `run.bat`, `run.sh --kiosk` (no display on the box).
- Ollama local-model path with a real model (no Ollama on the box) — only "absent → rules" and "localhost only" are tested.
- `ui_sandbox_origin_check_off` mutant (the page ignoring messages from other frames) is listed UNTESTED: the headless smoke has no hostile frame.
- C++/BASIC guards are deny-lists + rlimits, not an OS sandbox; code runs are localhost-only unless `--allow-remote-run`.
- `/selftest` was run for real once (bounded, top level); its recursion tests use a recorder instead of spawning.

## R7 — confirmation round after ROUNDS_LOG.md + README were added (14:21–14:26 PM ET; every run via safe_run, serial)
| Run | Result |
|---|---|
| Full self-check ×3 | **247 / 247 PASS**, 247 / 247, 247 / 247 (C++ lane, UI smoke, rcrj non-dict test and recursion tests included) |
| Quick | **232 PASS + 4 skip** (`--quick` skips the C++ compile, the UI smoke and both `/selftest` probes) |
| Bare device (no extras, `python3 -S`) | **217 PASS + 4 skip** (BASIC lane, scaffold-bas run, C++ compile, UI smoke = SKIP, never PASS) |
| Mutants (one at a time) | **43 / 43 caught**, 0 survivors, 1 UNTESTED (`ui_sandbox_origin_check_off`); 0 leftover processes after every mutant |
| UI smoke + screenshot | PASS (google-chrome headless, real time, default isolation); screenshot `logs/ui_smoke_final.png` (box, outside the kit) |
