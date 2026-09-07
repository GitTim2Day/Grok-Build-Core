# KBLD-9

**Family:** CONTROL  
**GOSUB ID:** KBLD_ENGINE  
**Status:** PROMOTED  
**Direction:** bidirectional  
**Cost class:** High  
**Archived:** 2026-09-07

## Purpose
Noise-cleaning and audit engine for high-sigma data pipelines. The core that Shepherd's Staff and other filters plug into.

## Contract
- **Forward call:** KBLD_ENGINE(raw_stream, config) -> cleaned_stream, audit_chain
- **Reverse call:** KBLD_ENGINE.reverse(cleaned_stream, audit_chain) -> raw_stream, diff_report
- **Shared state:** IQR noise floor, golden-ratio damping factor, SHA-256 audit chain
- **Direction tag:** bidirectional

## Components
1. **IQR noise floor** — interquartile range gate; anything outside the floor is flagged as noise, not signal.
2. **Golden-ratio damping** — (1 + sqrt(5)) / 2 ≈ 1.618. Damps corrections so the filter doesn't overshoot and create new artifacts.
3. **SHA-256 audit chaining** — every transformation step hashed; the chain is tamper-evident. Any replay must reproduce the same hashes.

## Design target
9 to 9.5 sigma cleaning. Built for pipelines where a single contaminated row can poison downstream training.

## Why it matters
Shepherd's Staff is a specialized filter. KBLD-9 is the engine underneath — it handles general noise, not just pet contamination. Without the engine, every filter reinvents its own noise gate.

## Held for owner
- Exact sigma target per data domain (vision vs. tabular vs. time-series)
- Whether golden-ratio damping is fixed or adaptive

## Related
- Shepherd's Staff (pet-contamination specialization)
- KBL Pipeline (medical imaging modules)
- BrickFusion (multi-band sensor fusion)