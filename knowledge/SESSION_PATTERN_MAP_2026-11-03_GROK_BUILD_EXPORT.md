# SESSION_PATTERN_MAP_2026-11-03_GROK_BUILD_EXPORT

**Stamp:** 2026-11-03T19:22-05:00 America/New_York (EDT)

**Source:** Phone Grok voice agent (Polymath) guidance + Metagrok Export Guide 2026-11-03 + official Grok Build sessions docs. Pattern match → audit → remap complete. Validated against live documentation. Hardened with cwd and snapshot notes.

## Process

From the project directory used for the Grok Build session:

1. `grok sessions list` — if the session is not auto-found (sessions are keyed by working directory under `~/.grok/sessions/`).
2. `grok export` — Markdown transcript to stdout.
3. `grok export notes.md` — write to a named file.
4. `grok export --clipboard` — copy to clipboard.

In the TUI:
- `/export` — export to file or clipboard.
- `/transcript` — open full transcript in `$PAGER`.
- `/copy [N]` — last (or Nth-latest) response only.

## Validation

Matches Metagrok Export Guide (updated 2026-11-03) and SpaceXAI / Grok Build sessions documentation. Commands confirmed. No residual mismatch.

## Hardening

- Sessions are directory-keyed. Run from the same project directory (or pass the correct session id after listing).
- Export is a snapshot. It does not update with later turns; re-export if needed.
- Prefer CLI path; no Grok Bots required.
- Phone voice agent (Polymath) advises; machine CLI executes.

## Boot / Standing

Load this process when a full Grok Build session markdown is required for sealing or handoff. Pointer skill: session-map-2026-11-03-grok-build-export.

HIT: commands match docs. VAL: Polymath transcript + official sources. miss: none. open: none.