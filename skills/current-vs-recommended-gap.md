# current-vs-recommended-gap

**Date:** 2026-09-07
**Tags:** gap, current, recommended, audit, process, gosub
**Status:** Active — GOSUB member (bidirectional)
**GOSUB ID:** GAP_AUDIT

## Purpose
Audit the gap between "Optimus Current" and "Recommended Primary" per row: state what changes, why, and whether the change is justified by the trigger. Callable forward (audit gaps) or reverse (given a gap class, find the rows in it).

## When to use
- A matrix has a current baseline and a recommended primary per row.
- You need to decide which gaps are worth closing and in what order.
- Reverse: you want every architecture-swap gap, or every relocation gap.

## Required inputs
- The current and recommended columns.
- The upgrade trigger and notes columns.

## GOSUB contract
- **Forward call:** GAP_AUDIT(sheet) → gap list, classification, justification check, ordered impact.
- **Reverse call:** GAP_AUDIT(gap_class) → rows whose gap is of that class.
- **Shared state:** reads current + recommended columns; writes only to the audit log.
- **Direction tag:** forward | reverse.

## Steps
1. **List the gap per row.** Current → Recommended, one line.
2. **Classify the gap.** Architecture swap (harmonic→roller-screw), add-on (diff, damper), relocation (distal→proximal), ratio change.
3. **Check justification.** The gap should map to a trigger. A gap with no trigger is preference, not decision.
4. **Order by impact.** Always-on gaps (distal mass) first; threshold gaps (torque >200 Nm) later.
5. **Report:** gap list, classification, justification check, ordered impact.

## Rules
- A gap without a trigger is a preference, not a decision.
- Order by impact, not by row order.
- Bidirectional: reverse returns the same rows the forward pass classified.

## Anti-patterns
- Treating every gap as equal weight.
- Closing a gap that the trigger doesn't justify.
- One-directional only.

## Example
Knee: linear roller-screw+lever → planetary roller-screw+lever+damper (add damper, architecture refinement). Wrist: tendon-driven → proximal actuators+Dyneema (relocation, always-on). Hip: rotary harmonic → harmonic+optional diff (add-on, threshold). Differential: not emphasized → limited-slip (new, threshold >200 Nm).
Reverse: "relocation" → Wrist, Fingers/Hand.
