# svct-gear-token-gap-2026-10-18
The golden-spiral gear's straight step mapped as a TOKEN GAP in the SVCT (Spherical Voxel Circular Token) ring, using Timothy H. Norman's 12-hour-clock / modular-wrap model.
Built 2026-10-18 ~11:56–12:05 EDT on the box. New files only. Prior folders (spiral-gear-tendon-2026-10-18, spiral-gear-video-2026-10-18) were read, not modified. No spend, no cloud agents. svct_v20*, BOOT.bas and kbld9/protected/ were not touched.

| file | what |
|---|---|
| MAPPING.md | ring position, shell, circular token, gap, edge competition; how fail-closed and re-sync follow from the lattice |
| COMPARISON.md | vs. video findings and AUDIT: consistent / changes / open gaps |
| svct_gear_token_gap.py | new module (stdlib) |
| test_svct_gear_token_gap.py → test_run_2026-10-18.txt | 22/22 OK |
| mutants_run.py → mutants_run_2026-10-18.txt | 12/12 killed (first pass mutants_run_2026-10-18_pass1.txt: 11/12; the survivor "resync ignores gap" was killed after adding the back-out-of-gap test) |
| mapping_numbers.py → mapping_numbers_run_2026-10-18.txt | re-sync jump per N, shells at zone edges |
| spiral_gear.py, interference_exact.json | byte-identical copies from the prior folder (table formula, measured overlap zones) |
| SHA256SUMS | sha256 of every file above (JOURNAL.md, added later, is not listed) |

Key measured results: the module equals the existing table bit-for-bit outside the gap (max diff 0.000e+00 rad). Outside the gap the error vs closed form is 9.514e-07 rad, against 4.223e-06 rad on the full prior set (reproduced). The overlap flag gives 107/1440 poses. At N=12 the re-sync jump is 2.288261048 rad.
Re-run: `python3 -B test_svct_gear_token_gap.py && python3 -B mutants_run.py && python3 -B mapping_numbers.py && sha256sum -c SHA256SUMS`
