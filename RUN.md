# Grok-Build-Core — Run notes (fail-closed)

Honest status as of 2026-09-18: partial. Root package manifest was ABSENT before this fix branch.

## Setup (only needed for hearing / optional gel numpy path)

```bash
python -m pip install -r requirements.txt
```

Most `kbld/` and `multilingual/` modules are **pure stdlib** and run without pip packages.

## Self-tests (from `kbld/README.md` and `__main__` blocks)

Tap live in-repo sources; preferred sealed/hardened stacks:

```bash
# Pure stdlib self-tests (no pip required)
python kbld/kbl_d_framework.py
python kbld/kbl_da_framework.py
python kbld/kbl_svct_stacks.py
python kbld/kbld_gosub_primitives_MinRadius_Lp_2026-08-28.py
python kbld/kbl_svct_stacks_MinRadius_Lp_2026-08-28.py
# README claims 68/68 self-tests on MinRadius_Lp rev 4c stacks file

python multilingual/lid_exact.py
python multilingual/tims_base_map.py
# edge_adapter_control / gosub_* need cwd=multilingual/ for sibling imports
```

Hearing pipeline (needs numpy/scipy; soundfile optional for file I/O):

```bash
python kbld/kbld_sophisticated_hearing.py
```

## ABSENT (do not invent / do not stub)

| Item | Status |
|------|--------|
| `kbld9_core_r4` (any path) | **ABSENT** — closest observed: `kbld/kbl_svct_stacks_MinRadius_Lp_2026-08-28.py` (rev 4c). **Not stubbed.** |
| `Tims_Tables_Base360_Full_Reference.csv` | **ABSENT** under `tims-tables/`. Present CSVs are Core Six / Presentation e4/e6 / Presentation Standards JSON only. **No fake Base360 CSV created.** |

Discipline: truncate not round; earned vs asserted; do not overwrite sealed paths under `knowledge/`.

## Blockers

1. No prior root lockfile — third-party pins unknown.
2. `kbld_svct_gel_stack.py` optional `spherical_memory_pro` — local/ABSENT as PyPI; gel path degrades when HAS_SVCT is false.
3. Multilingual adapters call external binaries (whisper.cpp, vosk, piper, bergamot, apertium) via PATH detection — not installed by this requirements.txt.
4. Drive-only binaries/archives are out of this Git tree.

## Append 2026-10-08 — MinRadius_Lp correction (Claude seat, Timothy's request)

`kbld/kbl_svct_stacks_MinRadius_Lp_2026-08-28.py` (git) FAILS: NameError at T3. Its "68/68" is ASSERTED.
`kbld/kbld_gosub_primitives_MinRadius_Lp_2026-08-28.py` (git) runs, but is a condensed port, not the sealed file.
Exact Drive bytes now live beside them as new leaves:

```bash
python kbld/kbl_svct_stacks_MinRadius_Lp_2026-08-28_DRIVE_D2_restored_2026-10-08.py   # 75 passed, 0 failed
python kbld/kbld_gosub_primitives_MinRadius_Lp_2026-08-28_DRIVE_D3_restored_2026-10-08.py   # ALL GREEN
```

CSVSON readiness needs `PYTHONPATH=basic` (script hard-codes `/workspace/conflict-nodes-build`); then 102/102 and CRJ 12/12.
TXT-RCRJ: run `make_samples.py` first; the selfcheck then needs `bwbasic` on PATH.
Record: `knowledge/CORRECTION_2026-10-08_MINRADIUS_LP_HALF_SHELF.md`. Which copy is live: Timothy decides.

## Append 2026-10-08 (late) — BASIC interpreter for the self-checks

```bash
sh scripts/build_bwbasic_3.20b_2026-10-08.sh /some/empty/dir   # pinned, hash-checked, gnu89 build
export PATH=/some/empty/dir/bin:$PATH
python csvson/txt_rcrj/selfcheck.py      # 162/162 with bwbasic present
python edge-canvas-kit/selfcheck.py      # 2 fails left, both 2.20-specific expected text (see record)
```

Use 3.20b, not 3.00 (3.00 breaks every IF on lines 1000+). 3.20b rounds `\` by default; `OPTION ROUND TRUNCATE` restores truncation.
New 8-place cut to Timothy's rules: `basic/cut8_2026-10-08.*` (BASIC, C++, Python key). Record: `knowledge/BWBASIC_VETTING_2026-10-08.md`.

## Append 2026-10-09 — boot notes (Claude seat)

`csvson/txt_rcrj/selfcheck.py` needs its samples generated first: `cd csvson/txt_rcrj && python3 make_samples.py && python3 selfcheck.py` → 162/162.
Boot 2026-10-09 08:50 ET (x86_64, Python 3.13.16, bwbasic 3.20b): all green except the three known items —
`kbl_svct_stacks_MinRadius_Lp_2026-08-28.py` NameError (the half-shelf; restored D2 leaf passes 75/75) and the edge kit's 3 recorded fails.
Today's additions also pass: vcf_to_jsonl 15/15, base-360 21/21, UDN 11/11, R3 28/28, R2 28/28.
