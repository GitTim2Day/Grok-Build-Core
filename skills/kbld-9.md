# KBLD-9

**Family:** CONTROL  
**GOSUB ID:** KBLD_ENGINE / GOSUB_MAD_Sigma_Guard  
**Status:** PROMOTED — face corrected 2026-09-09  
**Direction:** bidirectional  
**Cost class:** High  
**Archived:** 2026-09-07  
**Supersession:** knowledge/row-3c-kbld9-nab-retest-2026-09-08.md (CLOSED)

## Purpose
Fail-closed edge preprocessor. Noise-cleaning and audit engine for high-bar data pipelines. Shepherd plugs in here. Not a probability claim.

## Naming lock (Row 3C)
Do not call the floor “10-sigma” as if it were a Gaussian tail. Use **Shepherd 10-Sigma Equivalent or Better**. Deterministic floor (sigma_free, EV2 + harmonic + shell snap). MAD guard is an earned tool. Classical statistical sigma is not the identity.

## Contract
- **Forward call:** KBLD_ENGINE(raw_stream, config) -> cleaned_stream, audit_chain
- **Reverse call:** KBLD_ENGINE.reverse(cleaned_stream, audit_chain) -> raw_stream, diff_report
- **Shared state:** MAD / robust-z guard, shell / EV2 snap, SHA-256 audit chain
- **Direction tag:** bidirectional

## Components
1. **GOSUB_MAD_Sigma_Guard** — robust scale; flag extremes without invoking a probability tail.
2. **Shell / EV2 snap** — deterministic correction; do not invent a new damping constant on this face.
3. **SHA-256 audit chaining** — every transformation step hashed; replay must match.

IQR and golden-ratio damping were on the prior face. They are not the identity after Row 3C. Do not restore them as the selling line.

## Design target
Fail-closed edge preprocess. Retest already earned: NAB machine temp (22,696 rows) and UCI Wine Quality (never-trained). Both below the named robust-z bars. No probability invoked.

## Why it matters
Shepherd is the specialized filter. KBLD-9 is the engine underneath. Without the engine, every filter reinvents its own gate. Without Row 3C, the engine name lies about what the gate is.

## Held for owner
- Exact bar per data domain (vision vs. tabular vs. time-series) — still open
- Whether any damping factor is fixed or adaptive — still open; not re-asserted here

## Related
- knowledge/row-3c-kbld9-nab-retest-2026-09-08.md
- knowledge/shepherd-10-sigma-equivalent-or-better-2026-09-08.md
- Shepherd Staff (domain filter)
- KBL Pipeline (medical imaging modules)
