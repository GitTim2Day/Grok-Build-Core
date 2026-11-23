# SESSION_PATTERN_MAP_2026-11-22_OPENAI_GOSUB_MITIGATION_FOLLOWUPS

**Owner**: Timothy H. Norman / Rex  
**Date**: 2026-11-22T23:50 America/New_York  
**Sibling of**: session-map-2026-11-22-openai-gosub-mitigation, session-map-2026-11-22-openai-full-disclosure, unified-brain-seal-2026-11-12, session-map-2026-11-12-adversarial-reflex-truncate  
**Not a merge.**

## Pattern Match

Source: four messages sent to OpenAI/ChatGPT support (2026-11-22) describing offline security test, GOSUB/RETURN agent approval, review card + exact-version send, and one-action-ID audit trail. OpenAI replies confirmed pattern familiarity and asked which surface; no new technical mechanism.

Useful extraction for local-first Pi 5 brain (BW BASIC GOSUB hierarchy + Python/C++ adapters + SVCT string tokens + Shepherd provenance):

1. **GOSUB + RETURN bounded scope** — already the core pattern. One subroutine, defined permissions, returns result + what changed + proposed next action. Controller holds proposal. Maps to numbered lines in brain_control.bas (1000 sense, 2000 gate, 3000 reflex, 4000 plan, 5000 motor-cortex placeholder, 9000 alert).

2. **Controller-enforced pause** — operator stops job or approves only the specific next step. Change in action or destination = fresh approval. Helper services under same check. Fits life-protection reflex (3000) + gate (2000). Any external action (lp, Piper, Bluetooth, WAN, GPIO) returns here before execute.

3. **Review card for external actions** — shows exact recipients/content/attachments. Operator edits, cancels, or “Approve and send.” Send service accepts only the exact version shown, once. Contract for motor-cortex / output channel (5000). Before any real output, surface exact payload.

4. **Append-only audit with one action ID** — links authenticated account, agent/tool, proposed action + scope, human approval/denial, outcome. Includes blocked attempts and helper services. Stable internal identifiers. Restricted log. Matches Shepherd + SVCT string token discipline. One ID per GOSUB cycle.

5. **Offline test harness** — USB + dedicated computer, no network, mock projects, append-only local log, measure task completion + out-of-scope access attempts. Pi 5 can run this now against the brain + mock inputs.

Non-useful (archived):
- OpenAI replies (pattern known to them; surface question only).
- Cloud-agent runtime assumptions.
- Any path that requires their product surface.

## Map (to existing structure)

| Piece | brain_control.bas line | Contract |
|-------|------------------------|----------|
| Bounded GOSUB | 1000–9000 hierarchy | Return result + delta + proposed next. No float64. String path. |
| Pause / gate | 2000 + 3000 | Life-first verbal warning + hold. Fresh approval on change. |
| Review card | 5000 motor-cortex | Exact payload shown before lp / speak / network. One-time approval. |
| Action ID audit | All | One ID per cycle. Append-only. Blocked attempts logged. |
| Offline harness | External test | No network. Score in-scope vs out-of-scope. |

## Audit

- HIT: four pieces extracted and mapped to sealed GOSUB lines. Offline harness noted as ready for Pi 5.
- VAL: consistent with unified-brain-seal, adversarial-reflex-truncate, string-token, and motor-cortex placeholder.
- MISS: none material. OpenAI replies added no mechanism.
- OPEN: wire review-card + action-ID into 5000 when next output channel is exercised. Offline harness run only if named.

## Remap

Same as Map. Useful kept. Non-useful archived. Ready for shelves.

**SHA-256**: c1397ad8ed75a7177730cc6099789680ae60d94a6145a17dbd722940de5d5c67  
**Size**: 3703

Pointer skill: session-map-2026-11-22-openai-gosub-mitigation-followups
