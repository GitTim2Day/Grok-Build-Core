# /kbld — Harmonic / Framework Layer

Source files (Python) live in this folder and are mirrored on Drive:

- kbl_d_framework.py
- kbl_da_framework.py
- kbl_svct_stacks.py
- kbld_svct_gel_stack.py
- kblda_rtmp_us_east.py

Drive folder (appendable): https://drive.google.com/drive/folders/1Q-MCJwaATYmV5rGDa1Ci_ALG589Tm5P4

These are referenced here as the sealed domain branch. Full source is kept on Drive for size and binary safety; text extracts can be added as leaves when needed.

## Tap targets (now live in-repo)

- `kbl_d_framework.py` — KBLD Auditor: Knowledge / Belief / Logic / Discernment scoring with provenance hash chain.
- `kbl_da_framework.py` — KBLDA variant (no type hints), same loop.
- `kbl_svct_stacks.py` — GOSUB subroutine stacks: MAD 10-sigma guard, Error→Test→Mitigate→Retest loop, provenance attach.
- `kbld_svct_gel_stack.py` — Acceptable-range guard → Gel interpolation → SVCT 56-cell closed loop.
- `kblda_rtmp_us_east.py` — US East RTMP/OBS flow with explicit error handling.

The pre-filter used for Row 3C (KBLD-9) is the MAD sigma guard inside `kbl_svct_stacks.py`: `GOSUB_MAD_Sigma_Guard`. It is an earned component, not the identity of Shepherd's Staff.
