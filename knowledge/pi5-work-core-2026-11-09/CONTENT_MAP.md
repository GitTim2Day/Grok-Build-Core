# CONTENT MAP — work_core_2026-11-09.zip

What this is: a zip of `~/work` from Tim Norman's Raspberry Pi 5 (host "shepherd", user shepherd), 20410 files / 1639216430 bytes, file mtimes 2026-08-10T12:06:59Z … 2026-10-16T21:53:28Z (UTC). It is the working area of Claude Code sessions run on the Pi under `work/CLAUDE.md` rules ("supervised librarian node"): a read-only clone of Grok-Build-Core, the jcj/anyfile ingestion pipeline and its BASIC/C++ ports, de-identification/escalation tooling, KBLD9 recovery and shadow runs, a laser-rangefinder hybrid with third-party references, Raman/RRUFF identification, OEIS "EARN" re-runs, an OSM Georgia map extract, two Python venvs, and 51 CHECKPOINT notes.

Pointer format: `path` · short name · sha256[:16] · mtime (UTC).

Not in the zip: files that `archive/DEDUPE_INDEX.tsv` says were turned into symlinks to `~/Desktop/STORE` (115 rows for paths under ~/work, 377796414 bytes per the index), the STORE itself, `~/Desktop/Queries`, `~/local` (bwbasic, cmake, piper, stt), `tess_root`, `oeis_data`. `rruff/raw/` and `archive/mutation_runs/` are empty directories.

## Root files (work/)

63 files, 312482 bytes; mtime 2026-10-09T19:07:15Z … 2026-10-14T03:13:23Z; code: none; types: markdown 53, text 4, csv 3, backup 2, tsv 1

- `work/CLAUDE.md` · Pi rules for Claude (RULE 0 method, hard limits, boot) · 52e6323e1aa1f8a7 · 2026-10-14T01:01:54Z
- `work/MCP_MEMO_2026-10-13.txt` · MCP memo · a1e36282e9806317 · 2026-10-14T03:13:23Z
- `work/UPDATE_2026-10-13_capture.md` · update capture 10-13 · 1fea2bacfba29cbb · 2026-10-13T19:43:56Z
- `work/PORTABLE_BUILD_BUNDLE_2026-10-10_v2.txt` · portable-build text bundle v2 · cd55d49da2689eec · 2026-10-11T18:26:54Z
- `work/daemon_census.txt` · systemd daemon census of the Pi · 0391afbf2aaed1c5 · 2026-10-10T15:09:36Z
- `work/bashrc.backup` · .bashrc backup · 1746e8ac4ca9ead9 · 2026-10-09T19:07:15Z
- `work/claude-settings.json.backup` · Claude settings backup (theme only) · 27dafb2742d0da69 · 2026-10-09T19:38:21Z
- `work/route_check_20261010_101907.tsv` · URL route check · f4e3144418d15085 · 2026-10-10T14:19:19Z
- `work/SESSION_PATTERN_MAP_STATUS_2026-10-12_svct-deid-egress.csv` · session pattern-map status CSV · 56c225940b2101f3 · 2026-10-12T14:42:08Z
- `work/SESSION_PATTERN_MAP_STATUS_2026-10-13_pi5-wide.csv` · session pattern-map status CSV · 8819c9b654155f93 · 2026-10-13T06:46:18Z
- `work/SESSION_PATTERN_MAP_STATUS_2026-10-13_svct-delivery-rpi5.csv` · session pattern-map status CSV · 8ce53fc881de2c8b · 2026-10-13T06:41:46Z
- 51 CHECKPOINT_v8_*.md notes (2026-10-09 … 2026-10-13), 211196 bytes total; first `work/CHECKPOINT_v8_2026-10-09.md` · f8c2e34d90bdf25e, last `work/CHECKPOINT_v8_part52_2026-10-13.md` · 2d7068c8587b063d

## maps/

4 files, 892121252 bytes; mtime 2026-10-09T23:06:44Z … 2026-10-10T14:18:25Z; code: none; types: text 3, osm-pbf 1

OpenStreetMap Georgia (US) extract from Geofabrik (`georgia-latest.osm.pbf`, 357057388 bytes) and a pipe-delimited "streamlined" text derivation (road_nodes.txt 334937440, roads.txt 159882942, addresses.txt 40243482 bytes). Public, re-downloadable data; largest item in the archive (892121252 of all 1639216430 file bytes in the archive).

- `work/maps/georgia-latest.osm.pbf` · OSM Georgia PBF · 2ac4c2ef929d4a04 · 2026-10-09T23:06:44Z
- `work/maps/streamlined_20261010_101614/road_nodes.txt` · node id|lat|lon · aed91bc734fa392e · 2026-10-10T14:18:25Z
- `work/maps/streamlined_20261010_101614/roads.txt` · way id|class|name|n|node ids · 1687eebdb5e8410b · 2026-10-10T14:18:08Z
- `work/maps/streamlined_20261010_101614/addresses.txt` · address points · 6a5675d153615f10 · 2026-10-10T14:18:06Z

## venv_oeis/

8278 files, 187639124 bytes; mtime 2026-08-10T12:06:59Z … 2026-10-16T21:16:22Z; code: Python 4062, PowerShell 1; types: python-bytecode 4062, python-source 3880, empty 210, text-al 32, no-ext-text 31

Python 3.13 virtualenv for oeis_earn (mpmath 1.3.0, sympy 1.14.0, pip). lib64/ duplicates lib/ file-for-file in the zip; bin/python* are 3 copies of a 6673712-byte interpreter. Reinstallable; not project data.


## rruff/

2676 files, 143470894 bytes; mtime 2026-10-14T03:31:50Z … 2026-10-14T16:09:21Z; code: Python 2; types: text 2667, tsv 6, python-source 2, checksum 1

RRUFF Raman mineral spectra (public, rruff.net), 785 nm set: data785/ 2387 spectra, broad785/ 280; listings/ of remote zips read by HTTP range requests; scripts remote_listing.py / remote_extract.py. Note: rruff/raw/ is empty in the zip (DEDUPE_INDEX says the raw zips became symlinks into ~/Desktop/STORE).

- `work/rruff/remote_listing.py` · range-request lister · 1c22389ef383fd39 · 2026-10-14T15:34:30Z
- `work/rruff/remote_extract.py` · remote extractor · 37f6965ce6873f68 · 2026-10-14T15:35:27Z
- `work/rruff/unrated_unoriented_MEMBERS.tsv` · member list · 5ab3640483b1a7bc · 2026-10-14T13:54:35Z

## oeis_earn/

26 files, 129218225 bytes; mtime 2026-10-16T21:17:48Z … 2026-10-16T21:53:28Z; code: Python 14; types: python-source 14, jsonl 6, embedded-ide-or-fw-artifact 2, python-bytecode 2, text 1

2026-10-16 re-run of Tim's OEIS "EARN" scripts (gp_mini PARI interpreter, earn_formula, earn_pari) on the full OEIS data (400,361 entries); results: earn_pari EARNED 2747 of 6802 table entries. run/PARI_BLOCKS.jsonl and run/inventory.jsonl are large OEIS-derived intermediates. drive_orig/ = the unmodified Drive scripts.

- `work/oeis_earn/EARN_RESULTS_2026-10-16.md` · EARN results · 553abcb5fba5daa0 · 2026-10-16T21:53:28Z
- `work/oeis_earn/run/gp_mini.py` · gp_mini PARI subset · fb6a2af29d834658 · 2026-10-16T21:20:03Z
- `work/oeis_earn/run/PARI_BLOCKS.jsonl` · OEIS PARI blocks (derived) · e482c5d6a2dab07d · 2026-10-16T21:25:37Z
- `work/oeis_earn/run/inventory.jsonl` · OEIS inventory (derived) · 0b7c139227b69102 · 2026-10-16T21:22:29Z

## third_party/

1196 files, 104714228 bytes; mtime 2026-10-13T19:24:56Z … 2026-10-13T19:39:51Z; code: C/C++ header 437, C 301, Python 24, assembly 14, batch 6; types: c-header 437, c-source 301, embedded-ide-or-fw-artifact 126, git-hook-sample 70, git-internal 55

Read-only clones (depth 200, hooks disabled) of five open-source Bosch GLM / laser-tape rangefinder reverse-engineering repos, used as references for range_hybrid. iliasam__Laser_tape_reverse_engineering is 1029 files incl. a 39468527-byte git pack, PCB photos, Windows DLLs, STM32 firmware. ketan__… has NO license (marked not read, not used).

- `work/third_party/ACQUISITION_2026-10-13.md` · acquisition manifest · 4fe0fdd30610babc · 2026-10-13T19:39:51Z

## venv_csvson/

4369 files, 85915091 bytes; mtime 2026-08-10T12:06:59Z … 2026-10-13T23:40:02Z; code: Python 1865, PowerShell 1; types: python-bytecode 1865, python-source 1811, dicom 208, no-ext-binary 176, empty 94

Python 3.13 virtualenv for anyfile/jcj (Pillow, pydicom, openpyxl, xlsxwriter, numpy etc.). Same lib64/ duplication. Reinstallable.


## circular_demo/

26 files, 28580784 bytes; mtime 2026-10-14T22:08:31Z … 2026-10-14T22:13:46Z; code: none; types: json 8, text 6, jsonl 4, csv 4, sqlite 2

old/ vs new/ run of the same NDBC 41008 pipeline (stage outputs identical to kbld9_shadow_runs for the large files) with old/new reports; demonstrates the "circular" change.

- `work/circular_demo/new_report.txt` · new report · ed421577e829db84 · 2026-10-14T22:13:46Z
- `work/circular_demo/old_report.txt` · old report · 7b7c95a5fe989637 · 2026-10-14T22:08:35Z

## jcj/

1172 files, 22239105 bytes; mtime 2026-10-13T23:17:10Z … 2026-10-15T12:27:50Z; code: Python 380, C++ 1; types: text 414, python-source 380, python-bytecode 336, edit-backup 22, markdown 5

JCJ pipeline (JSON → regex → CSV/SQLite → regex → JSON) and `anyfile.py` (any file → .txt → protected regex GOSUB → JSONL/JSON-LD; DICOM/AV/image/PDF/Office). Default-deny metadata privacy rules. Heavy self-check and mutation-test outputs (`mutants_out/` 943 files). Also kbld9_stage/kbld9_shadow, numeric_stage, tools/runctl.py (process-group runner with hard time limits).

- `work/jcj/README.md` · jcj README · aaf87ca5d7c1c277 · 2026-10-13T23:46:38Z
- `work/jcj/jcj.py` · JCJ pipeline · 074e33b120ed5627 · 2026-10-15T11:53:56Z
- `work/jcj/anyfile.py` · anyfile front end · f455e7bcaddbff96 · 2026-10-14T03:11:52Z
- `work/jcj/numeric_stage.py` · numeric stage (median/MAD) · a5067ae0b0509170 · 2026-10-14T22:08:44Z
- `work/jcj/kbld9_stage.py` · KBLD9 stage · ed24854ab75723ae · 2026-10-15T03:03:55Z
- `work/jcj/REPO_FINDINGS_FOR_GROK_BUILD_CORE.md` · findings for the repo · 6b7c5039c5f3a2a9 · 2026-10-14T15:13:28Z
- `work/jcj/LIMITS.md` · limits · 8a46924d4d302249 · 2026-10-14T15:13:28Z

## kbld9_shadow_runs/

30 files, 15104519 bytes; mtime 2026-10-15T04:01:38Z … 2026-10-15T04:01:49Z; code: none; types: json 10, text 6, jsonl 6, csv 4, sqlite 2

Two 2026-10-15 shadow runs of the KBLD9 pipeline on public feeds: NOAA NDBC buoy 41008 realtime (6396 rows) and USGS all-day; stage1 csvson, stage2 jcj, numeric and KBLD9 reports.


## escalations/

328 files, 13773438 bytes; mtime 2026-10-12T12:57:22Z … 2026-10-16T03:37:56Z; code: Python 46, BASIC 35, C++ 16, shell 8; types: text 141, python-source 46, edit-backup 38, basic-source 35, cpp-source 16

De-identification ("DEID" v1–v6 in BASIC, Python, C++) and escalation/egress tooling for sending de-identified output only to Tim's edge devices; hostile-input hardening sweep (hostile/, 107 files, 10434246 bytes), append-only archive/, SVCT-anchored records. Contains DEVICE ONLY files (rules.txt, identity.txt, map/, records/, pending/, authorizations/).

- `work/escalations/README.txt` · README · 7ebe938dc2fb3e7e · 2026-10-12T20:34:48Z
- `work/escalations/tests/deid_v6.py` · DEID v6 Python · 4aaab5c66e542da4 · 2026-10-15T23:49:10Z
- `work/escalations/tests/deid_v6.cpp` · DEID v6 C++ · 374bc30d8d9149c7 · 2026-10-15T23:50:44Z
- `work/escalations/tests/deid_v6.bas` · DEID v6 BASIC · 1896fc52ecfc76e5 · 2026-10-16T03:37:56Z
- `work/escalations/hostile/HARDENING_SWEEP_2026-10-15.md` · hardening sweep report · 20ffdb2902e08153 · 2026-10-15T15:45:12Z

## Grok-Build-Core/

704 files, 3733408 bytes; mtime 2026-10-09T17:22:26Z … 2026-10-15T02:15:39Z; code: Python 95, BASIC 24, C++ 12, shell 6, JavaScript 2; types: markdown 331, git-internal 118, python-source 95, text 42, basic-source 24

Read-only git clone of GitHub GitTim2Day/Grok-Build-Core (local main 3caf6117, clean). README title: "Shepherd's Staff: A Deterministic Ten-Sigma Floor That Holds Without Probability" (KBLD-9 pre-filter, 10×MAD floor, SHA-256 audit chain). Subdirs: knowledge/ (294 files: session pattern maps, boot docs, skills), edge-canvas-kit/ (offline Canvas + browser UI + code editor + TXT→CSV→JSON converter + dev agent; `python3 server.py`), csvson/ (CSVSON ingest readiness and txt_rcrj), kbld/ (KBLD harmonic/framework layer), tims-tables/ (Tim's Tables CSV/MD), basic/ (BASIC+Python+C++ triples), mapbook/, multilingual/, hybrid-boot/, scripts/, skills/.

- `work/Grok-Build-Core/README.md` · repo README · 4fc27b08117b36fc · 2026-10-09T17:22:27Z
- `work/Grok-Build-Core/RUN.md` · run guide · 1dc826474210cc94 · 2026-10-09T17:22:27Z
- `work/Grok-Build-Core/CATALOG.md` · catalog · 3a6acd66fa1a06ef · 2026-10-09T17:22:27Z
- `work/Grok-Build-Core/HANDOFF_2026-10-10_PI.md` · Pi handoff · 056e093f2e7e31bc · 2026-10-10T14:09:05Z
- `work/Grok-Build-Core/edge-canvas-kit/README.md` · edge-canvas-kit README · 11a6731be7ff0b8d · 2026-10-09T17:22:27Z
- `work/Grok-Build-Core/edge-canvas-kit/server.py` · edge-canvas-kit entry point · 2f99f13efb5a1517 · 2026-10-09T17:22:27Z
- `work/Grok-Build-Core/kbld/README.md` · kbld README · 4598266f21fedf5c · 2026-10-09T17:22:27Z
- `work/Grok-Build-Core/csvson/README.md` · csvson README · f21e7311df410290 · 2026-10-09T17:22:27Z
- `work/Grok-Build-Core/tims-tables/Tims_Tables_Core_Six_Ratios.csv` · Tim's Tables core six ratios · 76c8a5273bd5ed5a · 2026-10-09T17:22:27Z

## kbld9_recovery/

34 files, 3624707 bytes; mtime 2026-09-18T20:28:53Z … 2026-10-14T03:03:44Z; code: Python 11, C++ 5; types: python-source 11, markdown 6, json 4, cpp-source 3, no-ext-binary 3

Recovery of the KBLD9 handoff pack (2026-09-19 tar.gz, Rev 7 "9.0.7-core", truncate/no-round): extracted Python gold, C++ header + selftest, probes (51/51), bench, and a diff of truncation behaviour; Pi 5 bench result JSON.

- `work/kbld9_recovery/extracted/kbld9-handoff/README.md` · handoff README · c4967183a8138661 · 2026-09-19T04:17:09Z
- `work/kbld9_recovery/extracted/kbld9-handoff/kbld9_core_r7.py` · KBLD9 Rev 7 core · 465359bb0339d3ac · 2026-09-18T20:38:18Z
- `work/kbld9_recovery/raw/kbld9-handoff_2026-09-19.tar.gz` · original pack · 1429ba772e97f3bb · 2026-10-14T03:01:14Z
- `work/kbld9_recovery/results/bench_python_pi5.json` · Pi 5 bench · 251538b9152fbdf3 · 2026-10-14T03:03:35Z

## session_maps/

21 files, 1981823 bytes; mtime 2026-10-16T01:40:36Z … 2026-10-16T04:03:28Z; code: Python 4; types: json 7, text 4, python-source 4, tsv 2, markdown 2

Session/day "map, audit, re-map" runs of 2026-10-15 and 2026-10-16 over STORE items, TODO, error log, memory notes (MAP_1..3.json, AUDIT*.txt, RESOLUTIONS tsv, map_session.py).

- `work/session_maps/2026-10-16/SESSION_MAP_2026-10-16.md` · session map 10-16 · d9426aa1c58403af · 2026-10-16T04:03:28Z
- `work/session_maps/2026-10-16/map_session.py` · mapper · eb95218b67f15b5d · 2026-10-16T04:02:04Z

## portable-build/

53 files, 1700087 bytes; mtime 2026-10-10T16:37:16Z … 2026-10-11T03:44:31Z; code: CMake 6, C++ 1; types: no-ext-binary 12, object-file 11, text 7, cmake 6, embedded-ide-or-fw-artifact 3

CMake presets to build the Grok-Build-Core C++ programs on several devices; pi5 preset verified (22/22 build, ctest 10/10); build/pi5 contains compiled outputs.

- `work/portable-build/README.md` · README · 1b2c8363dc6b2943 · 2026-10-11T03:44:31Z
- `work/portable-build/CMakeLists.txt` · CMake · eb3ffa5c80fa96f8 · 2026-10-10T16:37:16Z
- `work/portable-build/CMakePresets.json` · presets · 7e637f85509cfd1b · 2026-10-10T16:37:55Z

## dedupe/

137 files, 888997 bytes; mtime 2026-10-14T13:09:04Z … 2026-10-14T15:32:55Z; code: Python 61, shell 1; types: text 72, python-source 61, edit-backup 2, python-bytecode 1, shell-script 1

Read-only duplicate survey + execution tools (dedupe_tool.py, scan.py, link/relink/migrate scripts) with self-checks and mutation tests; drove the 2026-10-14 dedupe recorded in archive/DEDUPE_INDEX.tsv.

- `work/dedupe/dedupe_tool.py` · dedupe tool · 10ae9755c325498b · 2026-10-14T13:29:45Z
- `work/dedupe/scan.py` · duplicate scanner · 1aafabf3ce72ae23 · 2026-10-14T13:09:04Z

## runs/

889 files, 873893 bytes; mtime 2026-10-14T01:30:02Z … 2026-10-16T21:52:39Z; code: none; types: json 593, text 279, empty 17

889 small runctl run folders (cmd.json, status.json, log.txt) — one per supervised run.


## jcj_bas/

150 files, 833879 bytes; mtime 2026-10-14T17:25:15Z … 2026-10-15T13:14:03Z; code: BASIC 64, Python 3; types: text 80, basic-source 64, python-source 3, edit-backup 2, markdown 1

BASIC (Bywater BASIC 2.20) slice of the jcj insertion-protection core, with differential self-check against jcj.py and 110 mutants (143 output files).

- `work/jcj_bas/README.md` · README · 34c43682643694a5 · 2026-10-14T17:27:33Z
- `work/jcj_bas/jcjmini.bas` · BASIC core · 09deb2e6650e29d7 · 2026-10-14T17:26:28Z

## smoke/

8 files, 629248 bytes; mtime 2026-10-11T19:08:09Z … 2026-10-11T19:09:27Z; code: C++ 2; types: cpp-source 2, embedded-ide-or-fw-artifact 2, text 2, no-ext-binary 2

Two C++ smoke programs (octave_fold, sin_k_period: int64, no floats) with compiled binaries, outputs and answer keys.

- `work/smoke/sin_k_period.cpp` · sin_k_period · 9730f5351ff35c87 · 2026-10-11T19:08:09Z

## jcj_cpp/

39 files, 520294 bytes; mtime 2026-10-14T17:15:41Z … 2026-10-15T13:02:08Z; code: Python 5, C/C++ header 2, C++ 1; types: text 24, python-source 5, edit-backup 5, c-header 2, no-ext-binary 1

C++ port of the jcj core (`jcjcore`, linear-time NFA regex, Unicode tables generated from Python 3.13.5 unicodedata 15.1.0); compiled aarch64 binary included.

- `work/jcj_cpp/README.md` · README · 085ff4d0600467f9 · 2026-10-14T17:27:33Z
- `work/jcj_cpp/jcjcore.cpp` · C++ core · e8de4e01d85be6e3 · 2026-10-14T20:50:24Z
- `work/jcj_cpp/uni_tables.h` · generated Unicode tables · 895b4b25b11134bb · 2026-10-14T17:15:43Z
- `work/jcj_cpp/gen_tables.py` · table generator · 46611bc8f5c5d560 · 2026-10-14T17:15:41Z

## svct_model/

22 files, 253653 bytes; mtime 2026-10-12T12:07:02Z … 2026-10-12T12:21:46Z; code: BASIC 6, Python 2, C++ 2; types: text 10, basic-source 6, python-source 2, cpp-source 2, no-ext-binary 2

SVCT time-on-task model: exact-integer state machine in Python, C++, BASIC; events.txt/turns.txt inputs and identical outputs per language (differential test).

- `work/svct_model/svct_model.py` · model (Python) · 3260902c7067e4ae · 2026-10-12T12:07:24Z
- `work/svct_model/active_model.py` · active model · 35915a9987f40084 · 2026-10-12T12:19:53Z

## memories/

52 files, 226560 bytes; mtime 2026-10-14T17:12:11Z … 2026-10-14T21:54:48Z; code: Python 23; types: text 27, python-source 23, json 1, jsonl 1

memories.py — capture/ingest photos and files into a "memories" store (proposal), with self-check and 47 mutation outputs.

- `work/memories/memories.py` · memories tool · 57a358c9c9ee4d26 · 2026-10-14T17:12:11Z

## raman/

33 files, 206512 bytes; mtime 2026-10-14T03:47:39Z … 2026-10-14T16:08:57Z; code: Python 3; types: text 20, json 7, python-source 3, edit-backup 2, python-bytecode 1

raman_id.py: identify a Raman spectrum against the RRUFF library and measure accuracy (numpy); eval outputs per SNR/seed; mutation tests.

- `work/raman/raman_id.py` · Raman matcher · 34714df5373cdd1b · 2026-10-14T15:38:38Z

## range_hybrid/

28 files, 141988 bytes; mtime 2026-10-13T19:30:35Z … 2026-10-15T11:33:54Z; code: Python 10, shell 3, C 1, BASIC 1, C++ 1; types: python-source 10, text 6, markdown 5, shell-script 3, c-source 1

"svctrange": laser-rangefinder core in BASIC/Python/C++ with byte-identical output, Pi I/O wrapper (replay/serial/bosch — never run on hardware), reference build of the original MIT firmware math, 3-way + oracle + golden tests and mutation tests.

- `work/range_hybrid/README.md` · README · 0c08f502d24abc37 · 2026-10-13T19:43:20Z
- `work/range_hybrid/docs/SPEC.md` · spec · e8f76de115b87a24 · 2026-10-13T19:39:39Z
- `work/range_hybrid/core/svctrange.py` · core Python · 6e85249dca48f676 · 2026-10-13T19:31:12Z
- `work/range_hybrid/tests/run.sh` · test runner · 1ff033e909b6836b · 2026-10-13T19:36:36Z

## archive/

2 files, 110184 bytes; mtime 2026-10-14T13:18:26Z … 2026-10-16T00:06:24Z; code: none; types: archive-gz 1, tsv 1

DEDUPE_INDEX.tsv (229 actions: 118 file→symlink into ~/Desktop/STORE, 98 tree→archive, …) and a gz manifest of third_party. archive/mutation_runs/ is empty in the zip.

- `work/archive/DEDUPE_INDEX.tsv` · dedupe index · d6be6d59ac0c38ce · 2026-10-16T00:06:24Z

## inbox/

4 files, 101882 bytes; mtime 2026-10-14T03:06:52Z … 2026-10-14T12:52:04Z; code: none; types: xml 2, office-doc 1, tsv 1

MFSC Sensor Roadmap v1.docx and a feed snapshot (CBS, PBS).


## svct_v20_in/

12 files, 97844 bytes; mtime 2026-10-16T19:53:35Z … 2026-10-16T19:53:35Z; code: Python 2; types: markdown 7, python-source 2, text 2, tsv 1

SVCT v20 drafts (synthetic): permanent vs gel tables, chain_v19s full-width SHA-256 chain with Ed25519-signed head, registry table, key expire/void/fallback auth designs with self-test pass counts.

- `work/svct_v20_in/svct_v20/svct_v20_tables.py` · v20 tables · e37ce5d296d9fc0b · 2026-10-16T19:53:35Z
- `work/svct_v20_in/svct_v20/chain_v19s.py` · chain v19s · 7dbeecf238035d88 · 2026-10-16T19:53:35Z

## interlock/

8 files, 68422 bytes; mtime 2026-10-14T03:41:08Z … 2026-10-14T13:53:23Z; code: Python 3; types: text 4, python-source 3, python-bytecode 1

interlock_sim.py — pure-function simulation of the MFSC Tier-3 laser-enable interlock rules ("NOT A SAFETY DEVICE"), self-check and mutants.

- `work/interlock/interlock_sim.py` · interlock sim · 7984e50cbf162226 · 2026-10-14T03:41:08Z

## news/

13 files, 47352 bytes; mtime 2026-10-14T12:22:40Z … 2026-10-14T15:19:03Z; code: Python 3; types: text 7, python-source 3, edit-backup 2, python-bytecode 1

feedreader.py — personal RSS/Atom reader (robots.txt honoured, rate-limited) and two news briefs.

- `work/news/feedreader.py` · feed reader · 1c25c2cee61cfbdb · 2026-10-14T13:08:16Z

## svct_log/

2 files, 25734 bytes; mtime 2026-10-14T13:22:16Z … 2026-10-14T15:33:59Z; code: none; types: markdown 1, tsv 1

SVCT Drive parts log and part-ID TSV (2026-10-14).


## anyfile_runs/

24 files, 22041 bytes; mtime 2026-10-14T16:16:00Z … 2026-10-14T16:22:22Z; code: none; types: json 8, json-ld 4, csv 4, text 4, jsonl 4

4 sample anyfile runs (csv/json/jsonl/jsonld/manifest outputs).


## roadmap_v2/

1 files, 21100 bytes; mtime 2026-10-14T03:30:38Z … 2026-10-14T03:30:38Z; code: none; types: office-doc 1

MFSC Sensor Roadmap v2 DRAFT.docx.


## .claude/

1 files, 12196 bytes; mtime 2026-10-12T22:25:05Z … 2026-10-12T22:25:05Z; code: none; types: json 1

Claude Code project-local settings (permissions.allow, 120 entries). See CLAUDE_SETTINGS_SUMMARY.md.

- `work/.claude/settings.local.json` · Claude local settings · 30841f9ce529d9e0 · 2026-10-12T22:25:05Z

## schedule/

4 files, 3565 bytes; mtime 2026-10-14T03:13:23Z … 2026-10-14T17:07:27Z; code: Python 1; types: other-text 2, python-source 1, text 1

systemd user timer + service for a daily public-data run — prepared, NOT installed.

- `work/schedule/README_SCHEDULE.txt` · schedule README · 5cc7332a35ab0985 · 2026-10-14T03:13:23Z

## mcp/

1 files, 1919 bytes; mtime 2026-10-14T17:07:13Z … 2026-10-14T17:07:13Z; code: none; types: markdown 1

MCP_GOOD_FOR_NOT_GOOD_FOR.md — MCP note; nothing installed.


## Apparent purpose

A self-contained research and tooling workspace built by Claude Code sessions on the Pi under Tim's rules: exact integer/no-float processing, append-only records with SHA-256 chains (SVCT), three-language (BASIC/Python/C++) differential builds, heavy self-check + mutation testing, de-identification before any egress, and read-only use of GitHub and third-party code. Public datasets (OSM Georgia, RRUFF, NDBC/USGS, OEIS) are the bulk of the bytes; Tim-authored code and notes are a small fraction (see INVENTORY_SUMMARY.md and RECOMMENDATIONS.md).
