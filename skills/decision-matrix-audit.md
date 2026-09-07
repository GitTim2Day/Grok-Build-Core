# decision-matrix-audit

**Date:** 2026-09-07
**Tags:** decision-matrix, audit, spec, architecture, process

## Purpose
Audit a decision matrix or spec sheet before acting on it: confirm what each column means, what the sheet is and is not, and which numbers are design targets versus acceptance floors.

## When to use
- A spreadsheet or table arrives with columns like current / recommended / alternative, ratio, torque, tolerance, trigger, mass, cost, supplier.
- The user asks "what's this?" about a structured spec.
- You need to decide whether a row is a keep, change, or upgrade-trigger decision.

## Required inputs
- The matrix file or its extracted text.
- The domain (e.g. humanoid joints, 70 kg class).

## Steps
1. **Map columns, not rows.** For each column, state its role: baseline, primary, fallback, ratio, peak target, tolerance floor, skeletal requirement, upgrade trigger, rationale, mass band, cost class, supplier.
2. **Separate targets from floors.** Peak torque and ratio ranges are design targets; backlash/stiffness/elongation limits are acceptance floors. Do not treat a target as a floor.
3. **Identify the decision logic.** What triggers an upgrade (payload, terrain, mass, torque threshold)? What is always-on (e.g. distal mass)?
4. **State what the sheet is not.** Not a BOM, not a teardown, not a supplier commitment — a decision table.
5. **Report the audit:** column map, target-vs-floor split, trigger logic, exclusions. Then stop or offer the next concrete step.

## Rules
- Audit structure before recommending changes.
- Keep mass and cost as bands, not point estimates, unless the sheet gives them.
- No stored negatives; direction is a tag.

## Anti-patterns
- Reading the sheet as a parts list.
- Conflating peak torque with motor torque.
- Skipping the "what it is not" step.

## Example
Optimus joint-architecture matrix: 11 sections × 13 columns; knee primary = planetary roller-screw + lever + damper; upgrade trigger = high impact or mass >70 kg; distal arm always proximal-actuated.
