# SESSION_PATTERN_MAP_2026-11-25_NEURAL_CHANNEL_OPERATORS

**Source:** Gmail paste from Timothy (For Eve Voice seat, 2026-11-25 21:58 EST). Originally neural_channel_operators.py on shepherd Pi 5 Downloads.
**Disk copy:** 4496 bytes. SHA-256: b0db62bf7a189581f0548641f8f7ee948c00fcc44fe7c3846e98ffe1e44ff18
**Error-test:** 5/5 pass. Clean HIT, empty QUARANTINE, None QUARANTINE, tamper MISS, two-item HIT. No defects. Mitigate: nothing to fix.
**Open:** now_ny returns UTC placeholder (000 offset); production stamp pending.

## Five-step channel

1. **Gate** — Do No Harm check first. Fail/empty/invalid → QUARANTINE. Pass → stream.
2. **Split** — parallel fork: content path + context path (amygdala bidirectional parse).
3. **Tag** — salience + provenance stamp + tag_sha on each path.
4. **Merge** — recombine into one index row: toc_id, content, context, status ACTIVE, stamp, row_sha.
5. **Verify** — hash check + required keys. Returns HIT or MISS.

Pipeline: process_channel = Gate → Split → Tag(parallel) → Merge → Verify.

## Design locks

- Append-only. Full enumeration. String-based. No float64.
- Do No Harm first. Self-control boundary.
- Salience sibling annotation (not mutation of content).
- Six-pillar compatible: content, context, data, time, semantics, validation.
- Sibling of salience tagging map and amygdala channels map. Not a merge.

## Shelves

- Gmail: ledger hop (this sitting)
- Notion: pointer page
- GitHub: this file + map
- Box: uploaded
- Drive: no upload tool from this seat
- Memory: appended

## Pointer skill

session-map-2026-11-25-neural-channel-operators
