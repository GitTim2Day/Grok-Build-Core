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
