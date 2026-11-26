# SESSION_PATTERN_MAP_2026-11-25_SALIENCE_TAGGING

Sitting 2026-11-25T21:22 America/New_York · salience tagging mechanisms MAM

## Pattern Match

- amygdala-channels 2026-11-25 (SHA 136e211b399479483a436e4e493e8a6d005dc21142adda6e6fe9886be4a14105): biological precedent for urgency/relevance tagging before cycle spend.
- six-pillar SVCT 2026-11-23 (SHA pending): salience as sixth-pillar-compatible sibling annotation.
- scanner log 2026-11-25 (SHA 89fcbed0f04bde3b80bedc16b152841ec7c74f5d6b98973cbc67a30ce081a1df): append-only jsonl with ts + sha256; salience field slots beside existing fields without mutation.

## Map

Salience = annotation sibling to content. Never inside payload. Never mutates data.

Three layers:
1. Numeric priority score 0-1.
2. Decay half-life in hours; score fades unless reinforced.
3. Cross-reference: tag on one node can raise priority on related nodes without copying data.

Type: urgency | relevance. Distinguishes loud false alarm from quiet true fault.

Source: rule | human. Keeps the gate visible.

BASIC dispatch: each routine ID has a default salience band. Sense 1000 = 0.5 baseline. Alert 9000 = 0.9. A subroutine may raise or lower within its band; cannot exceed the human-set band. Placement stays human; execution stays machine.

Scanner log entry salience object:
{
  "score": 0.7,
  "type": "relevance",
  "trigger": "ext_filter_match",
  "decay_half_life_h": 24,
  "source": "rule"
}

Dispatch sort: score times remaining decay, not arrival order. Below threshold stops surfacing; row remains for provenance.

## Audit

- Salience is not importance. Magnitude and type both carried.
- Decay prevents stale tags crowding new ones.
- Cross-reference raises related priority without data copy.
- Human band cap prevents subroutine self-escalation.
- Append-only: every tag is a new row.

## Re-Map

No material MISS found. Pillars hold. Gate holds. Log stays appendable. Ranked attention without ranked mutation.

## Open

Pointer only. Wire salience field into scanner log only if named.
