# voice-interaction-correction-capture

**Priority:** HIGH
**Date:** 2026-09-07
**Tags:** loop, validation, provenance, collaboration

## Purpose
Turn every user correction into a durable shelf entry so the same failure cannot recur in a future voice session.

## When to use
- The user pushes back on a claim, a save, or a process step.
- The phrase "you were warned," "that's on me isn't good enough," or similar appears.

## Steps
1. Name the failure precisely (what was claimed vs what was true).
2. Write the rule that prevents it (e.g. "verify before reporting," "say no to a location that can't take the write").
3. Save as a new skill or patch an existing one — GitHub + Notion, both verified.
4. Append one log line with timestamp and the rule text.

## Rules
- The correction outranks the original claim. Update the shelf, don't defend the claim.
- One correction, one rule. Don't bundle unrelated fixes.
