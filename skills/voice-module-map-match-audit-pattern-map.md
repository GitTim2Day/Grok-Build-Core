# voice-module-map-match-audit-pattern-map

**Priority:** HIGH
**Date:** 2026-09-07
**Tags:** loop, validation, architecture, provenance, collaboration

## Purpose
After every voice-module interaction, re-run the map + match + audit + pattern-match pass and save the result into the skills and skill sets. This is the mechanism that makes the shelf cumulative across sessions instead of resetting each time.

## When to use
- A voice session just ended or a correction was made mid-session.
- The user says "add to the process," "save to skills," or "high priority."
- Before closing any session that touched the shelf, the matrix, or a skill file.

## Steps
1. **Map** — list what changed this session: new skills, patched contracts, resolved held calls, new files, new commits.
2. **Match** — compare against the existing shelf (Timothy Skills & KB + GitHub Grok-Build-Core/skills). Flag anything missing, duplicated, or drifted.
3. **Audit** — verify each change is real: Notion page exists at the right parent, GitHub commit is on main, no fabricated IDs or URLs.
4. **Pattern-match again** — look for the recurring failure mode (claiming done before verified, nesting pages under the wrong parent, skipping the write-scope check). Record it as a rule if new.
5. **Save** — write the result as a skill or update an existing one. Commit to GitHub, create or update the Notion row, append one log line. Never overwrite prior logs.

## Rules
- Never claim a save succeeded without verifying the artifact exists at the expected location.
- If a location cannot take the write (e.g. Drive has no create-file tool), say so immediately — do not simulate success.
- The user's correction is the source of truth; fold it into a skill, not just an apology.
- Direction is a tag, not a payload. No stored negatives.

## Anti-patterns
- Saving the conversation instead of the method.
- Creating pages under the wrong parent and calling it done.
- Fabricating URLs or IDs to make a report look complete.
- Skipping the pattern-match pass because "nothing changed."
