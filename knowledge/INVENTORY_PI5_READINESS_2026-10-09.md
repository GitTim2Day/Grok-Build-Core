# Inventory — what we have, where it lives, what ran (Pi 5 readiness), 2026-10-09

Stamp: 2026-10-09T00:30-04:00. Seat: Claude, at Timothy's question ("do you have everything that will run properly on the Pi 5").
Labels: REPRODUCED = run here this session; FOUND-NOT-RUN; NOT FOUND (searched: this repo, GitTim2Day/tims-session-archive @7b5e907,
Drive by name, Gmail, Notion). Host: x86_64, Python 3.13.16, gcc 13.3.0, PC-BASIC (vetted clone), bwbasic 3.20b. **Nothing ran on a Pi.**
Pi-portability checks: all 191 Python files parse under Python 3.11 grammar (Raspberry Pi OS Bookworm); non-stdlib imports listed per item.

## Roots, square roots, equal-leg √2
| Item | Where | Run | Result |
| --- | --- | --- | --- |
| equal_leg √2 (Py, C++, BASIC) | archive 2026-10-02_part3/equal_leg | RUN_ALL.sh | REPRODUCED: 102/102 gold all three; fuzz Py/C++ 2000, BASIC 150; names scan; empty input fails; corrupted constant caught — ALL PASS |
| 3-4-5 root check (Py, C++, BASIC) | repo knowledge/rt345_check | C++ run | REPRODUCED C++ 8/8 (Python ran rc=0 in sweep) |
| tims_tables_345_unit (Py, C++, BASIC v2) | Drive | — | FOUND-NOT-RUN (repo rt345_check covers the method) |
| P = R² octave check | repo knowledge/octave_pattern/p_equals_r2.cpp | C++ run | REPRODUCED 15/15 |
| isqrt / ratio class / lattice / truncate primitives | repo kbld/…_DRIVE_D3_restored_2026-10-08.py | self-test | REPRODUCED ALL GREEN (bare asserts: vacuous under -O) |
| ratio_gosubs.py (39/39, SHA-256 31deca3d…) | Gmail attachment 2026-08-20 | — | FOUND-NOT-RUN (no attachment download from this seat); its ratio routines are integrated in the D3 primitives above |

## Integration, derivatives, descending power
| Item | Where | Run | Result |
| --- | --- | --- | --- |
| Gaussian edge v3 (derivative, first integral, Planck l_p = c·t_p) Py/C++/BASIC | archive 2026-10-02_part3/gauss | RUN_ALL_V3.sh | REPRODUCED 49/49 all three, byte-identical, 5/5 tamper controls caught — ALL PASS |
| gauss/n2.py (v2 draft) | archive | run | DEFECT: NameError `_as_erf` used at module level before it is defined. Superseded by v3 (passes). Not fixed (sealed archive). |
| descending forward-difference power (descend) Py/C++/BASIC | repo edge-canvas-kit | kit self-check + C++ | REPRODUCED (8647; C++ ALL PASS) |
| Wave-Integration Gel v0.1 | Notion | — | ASSERTED document only (no code) |

## Cuts, conversion, sealed text
| Item | Where | Run | Result |
| --- | --- | --- | --- |
| sig_cut v7 Py / C++ / SIGCUT.BAS v4 | archive 2026-10-02_part4/sigcut | differential + harness | REPRODUCED: 0 mismatches (C++ text ML 100/40, C++ double vs Py, BASIC ML 100/40); rounding + float-multiply mutants caught |
| cut8 (sign as direction, -0 → 0) Py key / C++ / BASIC | repo basic/cut8_2026-10-08.* | earlier this session | REPRODUCED 19/19 on 5 runtimes; 10/10 mutants |
| sealed_truncate, sliding_window_filter | repo knowledge/ | run | REPRODUCED PASS (needs numpy: `apt install python3-numpy` on the Pi) |
| fraction_canon_face, embed_8x6 (6×6 / 8×6 / 8×8 hybrid conversion) Py/C++/BASIC | repo knowledge/ | run | REPRODUCED (embed: ALL_GREEN, 3 BASIC builds byte-identical) |
| wave rule, mixer, link formula Py/C++/BASIC | archive 2026-10-03_wave_rule | vs stored gold | REPRODUCED: all three = gold (37 / 4 / 16 lines) |

## SVCT — permanent, gel, chain, hybrid
| Item | Where | Run | Result |
| --- | --- | --- | --- |
| svct_chain.py (spec v1.1) | Drive 1hwiqBUFtxOt71m8ThOmglkqY6Mopfri4 (8,985 B, SHA-256 07fa697a…0ff6) | selftest | REPRODUCED PASS |
| voxel_link.py (8×8 token, append-only link cache, PERMANENT→SUPERSEDED→ARCHIVED) | Drive 1Yoyc5vhjLOZkke3v2ibCupg0ZSQ9a1b5 (13,612 B, SHA-256 db92dc72…29a6) | self-test | REPRODUCED PASS |
| kbld_svct_gel_stack.py | repo kbld/ | run | REPRODUCED ALL GREEN (numpy; optional spherical_memory_pro absent → its path degrades) |
| svct_checkpoint.py | archive 2026-10-02_part3/checkpoint | `verify` | REPRODUCED OK 10 voxels |
| BOOKMEM v1 Py/C++ | archive 2026-10-04_bookmem_v1 | TESTS.sh | REPRODUCED ALL PASS (FIX1 key, FIX2 35/35, Py = C++) |
| secretary gate v1 Py/C++ | archive 2026-10-05_secretary_gate_v1 | vs KEY/KEYH, XKEY/XKEYH | REPRODUCED all equal |
| MinRadius_Lp stacks + primitives (restored) | repo kbld/ | self-test | REPRODUCED 75/75, ALL GREEN |
| hybrid boot (BASIC / Py / C++) | repo hybrid-boot | run | REPRODUCED 0.70710678 |
| brain_spec_v1.md, SVCT_CHAIN_SPEC_v1.1.md | Drive | — | FOUND (specs) |

## NOT FOUND anywhere searched
density_root.py (38/38 claimed), context_gel_shells.py, SphericalMemoryPro / spherical_memory_pro (NumPy), the "eleven sealed
June modules", ingest_gate.py. Also: knowledge/chipmunk_joint_safe.cpp in the repo is a 9-byte placeholder ("see local"); the C++ build is not on the shelf.
"Alternate functions": no item by that name found; ask Timothy which set he means.

## Not runnable here / needs something on the Pi
- gp_mini.py, earn_formula.py (OEIS): need mpmath + sympy (`pip install mpmath sympy` on the Pi; PyPI is blocked from this sandbox).
- kbld_sophisticated_hearing.py: numpy, scipy, soundfile. csvson converters: Pillow, defusedxml, python-docx/openpyxl/pptx (samples only), Tesseract.
- scripts/pi_adxl355_link.py: needs the real I2C bus (`E_NO_BUS /dev/i2c-1` here, as designed) and smbus2.
- knowledge/gosub_cache_boot.py is a shell snippet saved with a .py name (not Python).
