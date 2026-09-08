# KBLD-9 Pre-filter Spec

GOSUB ID: KBLD_ENGINE
Family: CONTROL
Status: PROMOTED

## Contract
- Forward: KBLD_ENGINE(raw_stream, config) -> cleaned_stream, audit_chain
- Reverse: KBLD_ENGINE.reverse(cleaned_stream, audit_chain) -> raw_stream, diff_report

## Components
1. IQR noise floor — anything outside flagged as noise, not signal.
2. Golden-ratio damping (~1.618) — prevents overshoot and new artifacts.
3. SHA-256 audit chaining — every step hashed, tamper-evident.

## Design target
9 to 9.5 sigma cleaning (earned band). The floor itself is deterministic, not probabilistic.

## Role
Pre-filter that Shepherd's Staff and other filters plug into. Runs before any 10σ / 10×MAD claim is evaluated.
