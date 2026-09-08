# /kbld — Harmonic / Framework Layer

All eight source files are **live in this repo** and tapable. Drive holds the appendable archive mirror.

## Live in-repo (tap these)

- kbl_d_framework.py
- kbl_da_framework.py
- kbl_svct_stacks.py
- kbld_svct_gel_stack.py
- kblda_rtmp_us_east.py
- **kbld_gosub_primitives_MinRadius_Lp_2026-08-28.py** — sealed GOSUB primitives, MinRadius = L_p, sigma_free precession accuracy, truncate-toward-zero C2 refuse, ratio class A/B hardened.
- **kbl_svct_stacks_MinRadius_Lp_2026-08-28.py** — rev 4c stacks: 68/68 self-tests, production seam bindings, breakdown_suspected bimodality guard, foreign-body refusal.
- **kbld_sophisticated_hearing.py** — deterministic phase cancellation + independent LMS/NLMS/FxLMS processes + psychoacoustic masking (Bark + ATH).

## Tap targets

- `kbl_d_framework.py` — KBLD Auditor: Knowledge / Belief / Logic / Discernment scoring with provenance hash chain.
- `kbl_da_framework.py` — KBLDA variant (no type hints), same loop.
- `kbl_svct_stacks.py` — GOSUB subroutine stacks: MAD 10-sigma guard, Error→Test→Mitigate→Retest loop, provenance attach.
- `kbld_svct_gel_stack.py` — Acceptable-range guard → Gel interpolation → SVCT 56-cell closed loop.
- `kblda_rtmp_us_east.py` — US East RTMP/OBS flow with explicit error handling.
- `kbld_gosub_primitives_MinRadius_Lp_2026-08-28.py` — the sealed floor primitives; MinRadius is L_p, not 1e-30.
- `kbl_svct_stacks_MinRadius_Lp_2026-08-28.py` — the hardened stacks; 68/68 green, production seams bound on demand.
- `kbld_sophisticated_hearing.py` — audio pipeline: daemon loops converted to explicit steppable processes.

The pre-filter used for Row 3C (KBLD-9) is the MAD sigma guard inside `kbl_svct_stacks.py`: `GOSUB_MAD_Sigma_Guard`. It is an earned component, not the identity of Shepherd's Staff.

## Drive-only archive mirror

Appendable living source (binaries + older snapshots): https://drive.google.com/drive/folders/1Q-MCJwaATYmV5rGDa1Ci_ALG589Tm5P4

Ported 2026-09-08. The three formerly Drive-only advanced sources now open from this folder.
