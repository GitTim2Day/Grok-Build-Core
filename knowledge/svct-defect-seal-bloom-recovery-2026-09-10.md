# SVCT Defect Seal → Bloom → Recovery

**Skill:** `svct-defect-seal-bloom-recovery`
**Date:** 2026-09-10
**Status:** OPEN — validated on one case

## Pattern

When a sealed record has an intact hash but a false field: seal the defect, bloom a corrected version from an authoritative source, validate the repair against its neighbors, reissue. Old token stays as provenance.

## Case: SVCT voice-diarization token (Aug 18)

- Defect: token `b608614…` — hash intact, time pillar false. 11 of 14 burst timestamps wrong; errors stepped (+60, +120, +100, +80). Burst 10 ran backward. Seal v2 claimed 12:40:30 — impossible (936s into 239s file).
- Authoritative source: ffmpeg cut offsets.
- Repair: 12:27:49.5 — between burst 9 end (12:27:18) and burst 11 start (12:27:58). Inside file. Unlike Seal v2.
- Result: 14/14 corrected.
- Reissue: v1.1. Mark `b608614` SUPERSEDED. Do not delete.

## Four moves

1. Seal the defect — intact hash, false field, SUPERSEDED.
2. Bloom from authority — derive from the source that actually produced the data.
3. Validate against neighbors — repair must fall inside the adjacent range.
4. Reissue, don't rewrite — v1.1 carries the fix; v0 records the failure.

## Why it fits Grok Bot

Grok Bot skills = steps + decision rules + expected output + validation. This is that shape with a hard gate: neighbor validation makes a bad repair unshippable.

Addition worth offering: Grok Bot skills don't carry sealed objects with hashes. The token layer (provenance, integrity, custody) is the bloom — a skill that seals its own failures, then recovers from them.

## Open rungs

- [ ] Generalize beyond one case
- [ ] A15: 14 ffmpeg cuts, burst-1 transcription, Speaker 2 ID
- [ ] Cosine field per speaker (needs clean reference)
- [ ] Mint v1.1 formally

## Companions

- `svct-voice-diarization-context-2026-09-10`
- `gosub-session-boot-2026-09-09`
- `svct-pickup-timestamp-boot-2026-09-07`
