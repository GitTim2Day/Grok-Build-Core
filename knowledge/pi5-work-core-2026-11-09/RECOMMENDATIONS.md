# RECOMMENDATIONS (recommendations only; nothing was changed anywhere)

Byte figures are exact sums of file sizes as stored in work_core_2026-11-09.zip (INVENTORY.jsonl). On the Pi the real disk use can differ: a normal venv has `lib64 -> lib` and `bin/python3 -> python` as symlinks, which the zip stored as real copies, so the venv numbers below overstate the Pi by up to 116734710 + 26694848 bytes. Anything under ~/work that changed after 2026-10-16T21:53:28Z (newest mtime in the zip) is not covered.

## Top 5

1. **Pi: delete `~/work_core_2026-11-09.zip` (or wherever it sits) from the SD card — 773241627 bytes.** It is now held three ways: 9 Drive pieces (wc_part00…08, all sizes confirmed), and the rebuilt copy on the box whose sha256 matches efc3307eb84cf5a98764346b0bb0b4ceeb2eff96b97409780f2622f540c20215 and passes `unzip -t`. This alone more than doubles the ~670M free.
2. **Pi: move `work/maps/` off the card — 892121252 bytes** (or at least the derived `maps/streamlined_20261010_101614/`, 535063864 bytes, which can be rebuilt from the 357057388-byte `georgia-latest.osm.pbf`; the pbf itself is re-downloadable from download.geofabrik.de).
3. **Pi: move public / regenerable data off — 370801800 bytes:** `oeis_earn/run/PARI_BLOCKS.jsonl` + `inventory.jsonl` (125728198, regenerable with `pari_extract.py` / `inventory.py`), `rruff/data785/` + `rruff/broad785/` (140359374, public rruff.net; a sha256 manifest exists for broad785), `third_party/` (104714228, re-clonable at the HEADs recorded in `third_party/ACQUISITION_2026-10-13.md`). Kept on the box copy regardless.
4. **Project: update the Pi clone, then commit Tim's own source to Grok-Build-Core (by Tim / the Grok chair, not from the Pi, which is read-only by rule).** The clone is clean but behind: 8 files differ and 236 repo files (1781413 bytes) are missing locally. Commit candidates: 359 files, 6589279 bytes, listed in `COMMIT_CANDIDATES.tsv`.
5. **Project: keep DEVICE ONLY files out of every shared copy — 27 files, 319608 bytes** (`escalations/rules.txt`, `identity.txt`, `map/`, `records/`, `authorizations/`, `pending/`, `handoffs/`, `deliveries/`, `outbound/`). They are inside this zip, which now also sits in Drive as 9 pieces. No credentials need rotating (SECRETS.md: 0 live secrets).

## (a) Project

### Dedupe
| item | files | bytes affected | recommendation |
|---|--:|--:|---|
| all exact duplicates (sha256) | 6181 groups | 188120116 redundant | see INVENTORY_SUMMARY.md / DUPLICATES.json |
| of which inside venvs only | — | 155038736 | zip artifact (lib64 + bin/python copies, 116734710 + 26694848) plus normal pip duplication; ignore for the project; never commit venvs |
| non-venv duplicates | 451 groups | 33081380 redundant | 21392508 of it is inside `third_party/` (vendor STM32 headers repeated per firmware folder): leave as cloned |
| `escalations/hostile/run_*` outputs identical across before/after runs | — | 4351991 redundant | keep one copy + sha256 list when archiving |
| `circular_demo/` vs `kbld9_shadow_runs/` | 26 files in circular_demo | 4054465 redundant (exact); 28580784 total | keep `kbld9_shadow_runs/` and the two `circular_demo/*_report.txt`; archive the rest |
| `kbld9_recovery/diff/truncate_gold.json` = `extracted/.../cpp/truncate_gold.json` | 2 | 1459860 | keep the extracted copy, point the diff at it |
| `*.before_*`, `.draft1`, `.v1/.v2` edit backups | 75 | 1300473 | RULE 7 says archive bad code, so keep; bundle into one tar per folder |

### Commit to Grok-Build-Core (proposal; GitHub is read-only from the Pi)
- Candidate set (`COMMIT_CANDIDATES.tsv`): source and docs (.py .bas .cpp .h .hpp .md .sh .cmake .txt .json .tsv .csv) under jcj, jcj_bas, jcj_cpp, escalations, range_hybrid, portable-build (sources only), svct_model, svct_v20_in, dedupe, interlock, raman, memories, news, smoke, schedule, mcp, session_maps, kbld9_recovery (extracted/diff/results). 359 files, 6589279 bytes. By dir: kbld9_recovery 26/3113692, escalations 125/1600690, jcj 56/626796, session_maps 15/461647, jcj_cpp 9/192082, range_hybrid 26/133478, svct_v20_in 12/97844, raman 22/93358, dedupe 18/77205, svct_model 20/60229, interlock 3/34953, news 6/26084, jcj_bas 5/25509, memories 4/24017, portable-build 5/12886, smoke 4/3791, schedule 2/3099, mcp 1/1919.
- Excluded on purpose: mutation outputs (1471 files, 22797972 bytes), `__pycache__` (346 .pyc outside venvs, 12207164), compiled binaries (36 files, 3138400), `portable-build/build/` (1687201), `runs/` (873893), `.before_*` backups, DEVICE ONLY files, 4 already-in-repo vendor files, and `session_maps/2026-10-1{5,6}/MAP_2.json`, `MAP_3.json` (1502929 bytes; contain an SSH public key with a Windows user@host label — scrub first).
- `range_hybrid/` ports MIT code: commit with `docs/NOTICE.md`. Do not commit anything from `third_party/ketan__Bosch-GLM50C-Rangefinder` (no license).
- `kbld9_recovery/extracted/kbld9-handoff/kbld9_core_rev7.pdf` is not in the candidate set (binary); add deliberately if wanted.

### Archive (off the working set, keep in Drive/box)
| item | bytes |
|---|--:|
| `maps/` (public OSM + derived text) | 892121252 |
| `venv_oeis/` + `venv_csvson/` (reinstallable; save `pip freeze` first) | 273554215 |
| `rruff/` (public spectra; listings + manifest are small) | 143470894 |
| `oeis_earn/run/*.jsonl` + `.ids` (OEIS-derived) | 128897593 |
| `third_party/` (re-clonable at recorded HEADs) | 104714228 |
| `circular_demo/` | 28580784 |
| mutation outputs (`mutants_*_out/`, `jcj/mutants_out/`) | 22797972 |
| `portable-build/build/` | 1687201 |

### Secrets and sensitive data (paths only; details in SECRETS.md)
- Rotate: none.
- Confirm the test literals are synthetic: `work/jcj/selfcheck_jcj.py` line 373 (+2 older copies), `work/Grok-Build-Core/edge-canvas-kit/selfcheck.py` line 169.
- Remove from shared copies: DEVICE ONLY files above (319608 bytes); `work/runs/head1/log.txt` (captured Set-Cookie headers, 2 lines).
- Tighten `work/.claude/settings.local.json`: `Bash(git *)` (allows `git push`, against CLAUDE.md "never push") and `Bash(curl *)` (allows arbitrary upload).

### Data hygiene (from OEIS.md)
- `Grok-Build-Core/tims-tables/Tims_Tables_Core_Six_Ratios.csv`: derive Degrees from the Fraction column (360·p/q is an exact integer for all 8 rows) and drop the rounded `Radians (e-15)` / `Exact_Decimal` columns in favour of exact p/q.
- `test_base360.py` line 7: generate the divisors of 360 instead of listing them.

## (b) Pi 5 (98 percent full per Tim; about 670M free)

| action | bytes freed (zip sizes) | safe because |
|---|--:|---|
| delete the 773 MB zip itself after Tim confirms | 773241627 | Drive 9 pieces + verified box copy (sha256 match) |
| delete any leftover `wc_part*` pieces | up to 108241627 (pieces 07+08) | all 9 are in Drive at the right sizes |
| move/delete `maps/streamlined_20261010_101614/` | 535063864 | rebuildable from the pbf |
| move `maps/georgia-latest.osm.pbf` | 357057388 | public Geofabrik download |
| move `oeis_earn/run/PARI_BLOCKS.jsonl`, `inventory.jsonl` | 125728198 | regenerable from OEIS data |
| move `rruff/data785/`, `rruff/broad785/` | 140359374 | public rruff.net data |
| move `third_party/` | 104714228 | re-clonable at recorded HEADs |
| move `circular_demo/` | 28580784 | demo copy; reports kept |
| archive mutation outputs to a tar off the card | 22797972 | outputs, regenerable by re-running mutants |
| delete `__pycache__/` and venv `.pyc` | up to 141897390 (zip count incl. lib64 copies; 12207164 outside venvs) | Python rebuilds them on next run |
| (if not needed) delete `venv_oeis/` | up to 187639124 | reinstallable; mpmath 1.3.0, sympy 1.14.0 |

Also not in the zip but named in the notes, worth checking for size on the Pi: `~/work/oeis_data` (the OEIS checkout used by EARN), `~/work/tess_root`, `~/Desktop/STORE` (DEDUPE_INDEX: 115 files, 377796414 bytes moved there), `~/local` (cmake, bwbasic, piper, stt venvs). Suggested read-only check on the Pi: `du -xsh ~/* ~/.cache ~/Desktop/* 2>/dev/null | sort -h | tail -20`.
