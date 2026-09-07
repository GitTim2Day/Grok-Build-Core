# upgrade-trigger-map

**Date:** 2026-09-07
**Tags:** upgrade-trigger, decision, roadmap, process, gosub
**Status:** Active — GOSUB member (bidirectional)
**GOSUB ID:** TRIGGER_MAP

## Purpose
Map every upgrade trigger in a spec to a concrete condition and a fallback path, so the decision table becomes a roadmap instead of a wish list.

## When to use
- A matrix has a "Decision Trigger for Upgrade" column.
- You need to sequence upgrades by priority or dependency.

## Required inputs
- The trigger column.
- The alternative column for each row.

## GOSUB contract
- **Forward call:** TRIGGER_MAP(sheet) → per-row condition → action → fallback list.
- **Reverse call:** TRIGGER_MAP(condition) → rows that fire on that condition.
- **Shared state:** reads the trigger + alternative columns; writes only to the audit log.
- **Direction tag:** forward | reverse.

Pair with TRIGGER_SEQ (decision-trigger-sequence) for sheet-wide dependency order. This skill maps rows; that skill sequences the build.

## Steps
1. **List triggers per row.** One line each: condition → action.
2. **Classify by type.** Payload, terrain, mass, torque threshold, thermal, always-on.
3. **Order by dependency.** Always-on (distal mass) first; threshold-based (torque >200 Nm) later.
4. **Attach the fallback.** Every trigger needs its alternative path from the matrix.
5. **Report:** ordered trigger list with fallbacks, plus any row with no trigger (flag it).

## Rules
- A trigger without a fallback is incomplete.
- Always-on triggers are not optional.
- Bidirectional: reverse returns the same rows the forward pass listed.

## Anti-patterns
- Treating every trigger as equal priority.
- Leaving a row with "always" but no alternative.
- One-directional only.

## Example
Hip: torque >200 Nm or rough terrain → add limited-slip diff. Wrist: always (distal mass) → proximal actuators + Dyneema. Compound pulley: motor thermal limit → optional 2:1–3:1 stage.
Reverse: "distal mass" → Wrist, Fingers/Hand.
