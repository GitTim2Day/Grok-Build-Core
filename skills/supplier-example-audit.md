# supplier-example-audit

**Date:** 2026-09-07
**Tags:** supplier, audit, provenance, architecture, process

## Purpose
Audit the supplier examples in a spec or decision matrix: confirm they are real, plausible, and correctly classed, without treating them as commitments.

## When to use
- A matrix lists supplier examples per row (e.g. Harmonic Drive, Tolomatic, Maxon, Dyneema/DSM).
- You need to check whether the named suppliers actually make the class of part claimed.
- Before contacting or quoting a supplier from the sheet.

## Required inputs
- The supplier column or list.
- The part class per row (harmonic, roller-screw, tendon, etc.).

## Steps
1. **List suppliers per row.** One line each: supplier → part class.
2. **Check class fit.** Harmonic Drive / Leaderdrive / Nabtesco → strain-wave; Tolomatic / Thomson / Rollvis → roller-screw; Maxon / FAULHABER → small BLDC; Dyneema/DSM → UHMWPE fiber. Flag mismatches.
3. **Flag custom entries.** "Custom Tesla-style", "custom 3D-printed" are not suppliers — they are placeholders. Mark them as such.
4. **Separate examples from commitments.** The sheet names examples, not contracts. Do not imply a relationship exists.
5. **Report:** class-fit check, custom flags, commitment boundary. Then stop or offer the next step.

## Rules
- Examples are illustrative, not endorsements.
- Never invent a supplier that isn't on the sheet.
- Custom entries get their own flag, not a supplier check.

## Anti-patterns
- Treating "custom" as a real supplier.
- Quoting a supplier as if contracted.
- Skipping the class-fit check.

## Example
Hip: Harmonic Drive LLC, Leaderdrive, Nabtesco, custom Tesla-style → three real strain-wave makers + one placeholder. Knee: Tolomatic, Thomson, Rollvis → all roller-screw. Wrist: Maxon, FAULHABER, Dyneema/DSM → motors + fiber, correct split.
