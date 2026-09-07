# alternative-fallback-map

**Date:** 2026-09-07
**Tags:** alternative, fallback, audit, process

## Purpose
Map every alternative path in a spec to its trigger and confirm no row is left without a fallback when the primary is blocked.

## When to use
- A matrix lists an alternative per row.
- You need to know what to do when the primary is unavailable (cost, mass, packaging).

## Required inputs
- The alternative column.
- The upgrade trigger and notes columns.

## Steps
1. **List the alternative per row.** One line: primary blocked → alternative.
2. **Check it is a real fallback, not a duplicate.** Dual harmonic vs single harmonic is a fallback; same harmonic is not.
3. **Attach the trigger.** Every alternative needs the condition that activates it.
4. **Flag rows with no alternative.** A row with only a primary and no fallback is a single point of failure.
5. **Report:** fallback list, trigger attachment, single-point flags.

## Rules
- A fallback without a trigger is unused.
- A row with no fallback is a risk, not a choice.

## Anti-patterns
- Treating the alternative as a second recommendation.
- Leaving a high-cost row with no fallback.

## Example
Hip: dual harmonic or planetary multi-stage (fallback if single harmonic insufficient). Knee: dual roller-screw (fallback if single fails). Ankle: harmonic 50:1–100:1 (fallback if linear packaging fails). Differential: none (flag — single point). Compound pulley: none (flag — optional, low risk).
