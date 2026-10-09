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

## R8–R10 — Spectrum Sweep added to the Canvas tab (Timothy's ask 4:49 PM ET; built 4:50–5:15 PM ET)
Boot first: `bwbasic /workspace/hybrid-boot/BOOT.bas </dev/null` → `0.70710678` (4:50 PM). Pre-sweep copies archived first to
`archive/pre-sweep/` (box, outside the kit: server.py, selfcheck.py, mutants.py, ui_smoke.py, README.md, ROUNDS_LOG.md, agent.py,
ui/app.js, ui/index.html, ui/style.css, knowledge/KNOWLEDGE_MANIFEST.md, the R7 dist and the box harness, with ARCHIVE_SHA256.txt).
New: `lib/sweep.py`, `GET /api/sweep`, Canvas-tab "Spectrum sweep" (chart, modes, redshift slider, overlay, frames, audio off by default),
`basic/sweep.bas`, `cpp/sweep.cpp`. Every run via `safe_run.sh` (timeout + process cap + KIT_SELFTEST_ACTIVE=1), one at a time; mutants via
`run_mutants_serial.sh`; a `/tmp/kit-mutants-*` process count after every run.

Key values (truncated to 8 places, never rounded; Python Decimal = BASIC = C++): **y(100 MHz) = 19.54420602**, **y(500 THz) = 41.79770269**,
shift log2(1+z): z=1 → 1.00000000, z=3 → 2.00000000, z=0.5 → 0.58496250; sampler default (y = 42 − x/4, 90 steps) final **19.5**.

| Round | Time (ET) | Self-check result | Mutants | Found → mitigated |
|---|---|---|---|---|
| R8 | 4:55–5:00 | quick run1 317 / **1 fail** → quick run2 **318 PASS + 4 skip** · full **335 / 335** | **60 / 60** caught (43 old + 17 new), 1 UNTESTED, 0 leftovers | (1) test bug: my 43 Hz constant was wrong (130.8·2^−1.6 = 43.1479…, not 43.157) → test now checks int(...) == 43 and the decay end value. (2) review: a zero from the Decimal path printed as `0E-8` (scientific) → `_cut` formats with "f" and never returns `-0.00000000`; new test `sweep_trunc_never_scientific`, mutant `sweep_cut_scientific`. (3) review: more than 32 query fields raised ValueError → HTTP 500 → now 400 "too many query fields"; test `query_too_many_fields_400`, mutant `server_query_fields_500`. |
| R9 | 5:01–5:07 | full **337 / 337 ×3** · quick **320 + 4 skip** · bare device **303 + 5 skip** · cross-check ALL AGREE · UI smoke PASS | 60 caught, **1 SURVIVED** (`sweep_pow2_not_exact`), **1 NOT APPLIED** (`sweep_trunc_rounds`), 1 UNTESTED; 0 leftovers | (1) `sweep_trunc_rounds` pattern no longer matched after the R8 `_cut` change → pattern updated. (2) Survivor: with the exact power-of-two path removed, z = 0/1/3 still came out right through Decimal, so the tests could not see it. Probe: through Decimal alone, log2(16) cuts to **3.99999999 at both 50 and 70 digits** (wrong, and the stability check passes), and 2^6, 2^8, 2^−64 … differ between 50/70 (refused). So the exact path matters → tests now include z = 15 (1+z = 16 → 4.00000000) and log2 of 16, 2^6, 2^−64. |
| R10 | 5:08–5:14 | full **338 / 338 ×3** · quick **321 PASS + 4 skip** · bare device **304 PASS + 5 skip** · cross-check ALL AGREE (Python/BASIC/C++, tolerance 1e-7) · UI smoke PASS + screenshot | **62 / 62 caught**, 0 survivors, 1 UNTESTED (`ui_sandbox_origin_check_off`, unchanged); 0 leftovers after every mutant | none (confirmation round) |

New tests (89 sweep-related in the full run): endpoint + key values vs an independent Decimal reference, axis decades ascending (10^7..10^16,
100 MHz and 1 PHz labels), visible band exactly 400–790 THz (only band highlighted, log10 14.60–14.90), Latin labels in order and no
"Microondas" in the response or in lib/ui/server code, bands contiguous, octave sweep starts at exactly 100 MHz / crosses the visible window /
exits in Ultravioletum, redshift: shift = log2(1+z) for z = 1, 3, 15, 0.5, 1/3, 1100 on every sample and f_obs = f_emit/(1+z) exactly,
wavelength→RGB known points (440 blue, 490 cyan, 510 green, 580 yellow, 645 red, 380/780 edges = C++), ramps below/above visible, sample colours
follow the rule, decay formula label and shape (24.4 → toward 19.4; k = 0 flat; lift 0 toward 43 Hz), sampler final only (19.5, f 96982340.184 Hz
truncated), exact fractional steps (dx = 1/3), n = 2 walk = closed form, fps 32/64, overlay default Latin line + edit echo + line breaks refused,
23 cap/refusal probes (samples, z, f, k, A, xmax, lift, steps, |y|, mode, fps, unknown/duplicate parameter, long token, nan/inf/1/0),
main line continues after refusals, audio whole-octave transpose (36 for the default sweep) and off by default, on-screen note, precision note,
UI single-line overlay input, examples list, screens accept both twins, BASIC and C++ cross-checks, C++ self-check 15/15, query-field cap.
UI smoke adds: key values on the page, axis drawn upward, Latin labels, overlay sanitizer, visible band painted, sweep frame 0 colour in the
player, audio off, z = 0.5 shift 0.58496250.
New mutants (19): sweep_axis_order_flipped, sweep_redshift_multiply, sweep_label_microondas, sweep_decay_sign_flipped, sweep_samples_cap_off,
sweep_z_cap_off, sweep_visible_band_800THz, sweep_trunc_rounds, sweep_overlay_newline_allowed, sweep_rgb_blue_green_swap, sweep_pow2_not_exact,
server_sweep_unknown_params_allowed, ui_sweep_audio_on_by_default, basic_sweep_multiply_redshift, cpp_sweep_trunc_rounds, sweep_cut_scientific,
server_query_fields_500, ui_sweep_axis_flip, ui_sweep_overlay_multiline — all caught in R10.

Notes / limits (sweep):
- Representation only: nothing is emitted or detected. Band edges other than the visible window are approximate conventional ones, for display.
- My choices (not from Timothy's text, labelled in the UI/README): octave default end 1 PHz; decay defaults k = 1, x = 0..5 and the
  whole-octave lift L = 21 (so the image's curve sits on the radio axis); sampler default y = 42 − x/4, 90 steps; colour ramps outside the
  visible band; audio transposes so the top lands at or below 16 kHz (for the default 23-octave sweep only the top ~10 octaves are audible;
  the rest is silent, not compressed).
- `sweep_pow2_not_exact` is caught because the self-check stops on an uncaught refusal (SweepError) right after reporting the FAIL — fail closed,
  but not a tidy FAIL line for every later test.
- Stray count: the box-side `ps | grep /tmp/kit-mutants-` count was **1** after each pre-mutant R10 run (none in R8/R9). `ps` at 5:12 PM showed no
  such process and the mutants phase found 0 after every mutant; the process was not identified (it was gone before I looked). Far below the 50 limit.
- Audio and the visible-light colours were checked only headless (no speakers, no display); not run on a real Pi 5 yet.
- Correction (5:17 PM ET), stray count identified: the 1 match during R10 was my own launcher. R10 was started as `chmod … && nohup ./run_r10.sh &`;
  bash runs a backgrounded `&&` list in a subshell that keeps the launcher's full command text (which contained the search pattern) as its
  command line. `mutants.py` found exactly that 1 process at the baseline sweep and killed it (`STRAYS: 1 … after baseline; killed` in
  `logs/R10_mutants_full.txt`); `run_r10.sh` carried on and finished. R9 was started with a plain `nohup … &` and counted 0. The 1 seen after the
  post-log quick run was the Shell command that appended this log (its text contained the pattern). No test process was left behind.

## R11 — 2026-10-08 (Claude seat): Agent exhaust ladder + permission-gated dial-out

Timothy (2026-10-08 23:09, 23:12 ET): don't come back with "I don't know" until every resource has been tried; run offline as now, and when
more is needed dial out **with his permission**, even to an API he subscribes to, then come back and finish on the device (Pi 5, R1, A15, Orin);
Ollama is available offline.

Miss shown first: "what does the converter do with a formula cell" -> "I don't know", though the answer is in knowledge/. Cause: the rules
gate checked only the top hit (a README chunk, cover 1/3) while hits 2-3 (RCRJ guard docs, cover 2/3, score > 0.10) passed; no word forms.

Change (agent.py): rung 2 widened match (every top-10 hit through the same MIN_SCORE / MIN_COVER gates; cover counts word forms);
rung 3 Ollama own-knowledge (labelled unverified); rung 4 need raised + permission asked (/needs, /approve, /deny); providers in
workspace/providers.json (https only, kinds web/anthropic/openai, keys only in env vars, pre_approved off by default); needs log append-only.
Restored in the same round: answer_local_model had been cut by my block replacement (caught by selfcheck 500 + KeyError); every method of the
pre-edit file checked present after the fix.

Tests: selfcheck gains 13 ladder checks (offline; socket guard shows no outbound). Off-box answer key (scratch, mocks for Ollama, an https web
search, Anthropic-format and OpenAI-format APIs): phase A 15/15 offline, phase B 21/21; masked question verified at the receiving end
(0 rows carried the raw e-mail); keys never written to the log. Mutants: 6 new ladder mutants + the 6 existing agent mutants = 12/12 caught
(first run 11/12: ladder_widened_cover_gate_off survived; killed by the new check ladder_rung2_cover_gate_holds).
Not tested: a real search site or a real API (this box's egress refuses them); R1 as a client is untested (no R1 here).
