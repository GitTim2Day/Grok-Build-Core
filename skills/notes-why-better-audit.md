# notes-why-better-audit

**Date:** 2026-09-07
**Tags:** notes, rationale, audit, process

## Purpose
Audit the rationale column ("Notes / Why Better"): confirm each note is an engineering reason, not marketing, and that it matches the upgrade trigger and alternative.

## When to use
- A matrix has a notes or rationale column per row.
- You need to check whether the stated reason actually supports the recommended primary over the alternative.

## Required inputs
- The notes column.
- The recommended primary, alternative, and upgrade trigger columns.

## Steps
1. **List the rationale per row.** One line: reason → supports which choice.
2. **Check it is engineering, not marketing.** "Better shock absorption & longevity" is engineering; "superior performance" is marketing. Flag the latter.
3. **Cross-check against trigger.** The note should explain why the primary beats the alternative under the trigger condition. Flag notes that don't connect.
4. **Flag empty or generic notes.** A row with no rationale is incomplete.
5. **Report:** rationale list, engineering-vs-marketing split, trigger connection, gaps.

## Rules
- Rationale must be falsifiable (a testable claim), not a slogan.
- A note that doesn't reference the trigger or alternative is weak.

## Anti-patterns
- Accepting marketing language as engineering reason.
- Skipping the trigger-connection check.

## Example
Hip: "Adds load sharing & terrain adaptation" → supports diff under rough terrain. Knee: "Better shock absorption & longevity" → supports roller-screw + damper under high impact. Wrist: "Lower distal mass better force control" → supports proximal actuators, always-on trigger.
