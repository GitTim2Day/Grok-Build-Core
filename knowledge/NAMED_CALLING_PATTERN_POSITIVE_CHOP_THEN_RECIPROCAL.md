# Named Calling Pattern: Positive-Chop-Then-Reciprocal
# Practical-floor case for extreme negative exponents
# Not a new primitive. Composition of existing sealed primitives.
# SHA-256: 4d41505731cc06c90e84b53d7866f6e0a700ba3a8833c97449a8b11b699584a9

## Purpose
Restore a negative exponent of the form 10^{-n} (n large) without generating a zero from direct string truncation of the decimal form.

## Sequence (calling order)
1. Start with the positive magnitude of the exponent (or the positive power).
2. Apply GOSUB_TRUNCATE_TOWARD_ZERO to reduce that positive magnitude by 1 (chop the positive exponent).
3. Apply GOSUB_RATIO_RECIPROCAL to the reduced positive result.
4. Direction is reapplied after the reciprocal (sign is pure direction).

## Example
Target: 10^{-45}
- Positive magnitude of exponent: 45
- Chop: 45 truncated toward zero by 1 → 44
- Reciprocal of 10^{44} → 10^{-44}
- Result is usable floor; no zero appears.

## Contracts
- Magnitudes remain positive until direction is reapplied.
- Truncation is toward zero only.
- Reciprocal is exact (GOSUB_RATIO_RECIPROCAL).
- Does not introduce a new atomic operation.
- Compatible with direction-only arithmetic and exponent turning point.

## Status
Sealed as named calling pattern / artifact.
Pointer only. Body is this file.

Timestamp: 2026-11-16T17:36-05:00 America/New_York
Ledger hop: 1a1e681d80cf9c12
Notion: 41ac9bfe-3aff-813e-a46e-f08872969331