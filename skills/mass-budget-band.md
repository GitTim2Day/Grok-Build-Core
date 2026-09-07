# mass-budget-band

**Date:** 2026-09-07
**Tags:** mass, budget, band, actuator, process, gosub
**Status:** Active — GOSUB member (bidirectional)
**GOSUB ID:** MASS_BAND

## Purpose
Treat actuator mass as a band, not a point, and sum bands to a rough total without pretending precision.

## When to use
- A spec gives mass ranges per joint or subsystem.
- You need a quick mass sanity check for a platform class.

## Required inputs
- The mass contribution column.
- The platform mass class (e.g. 70 kg).

## GOSUB contract
- **Forward call:** MASS_BAND(sheet) → low-sum, high-sum, fraction of platform, exclusions.
- **Reverse call:** MASS_BAND(band) → rows whose mass range sits in that band.
- **Shared state:** reads the mass column; writes only to the audit log.
- **Direction tag:** forward | reverse.

## Steps
1. **Read each cell as a range.** Low–high, not a single number.
2. **Sum lows and sum highs separately.** Report the band, not a midpoint.
3. **Compare to platform mass.** Actuation hardware as a fraction of body mass; flag if >50%.
4. **Note exclusions.** Tendons, wiring, structure are usually outside the actuator band.
5. **Report:** total band, fraction of platform, exclusions.

## Rules
- Bands, not points. Midpoints are for communication only.
- Do not double-count shared structure.
- Bidirectional: reverse returns the same rows the forward pass summed.

## Anti-patterns
- Summing midpoints as if exact.
- Including structure in the actuator total.
- One-directional only.

## Example
Optimus matrix: ~23–35 kg actuation hardware across 11 sections for a 70 kg class; tendons and structure excluded.
Reverse: "high band" → Hip, Knee, Shoulder (largest actuator masses).
