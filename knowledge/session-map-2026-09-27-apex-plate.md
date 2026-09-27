---
name: session-map-2026-09-27-apex-plate
description: >
  Pointer for the 2026-09-27 apex-plate sitting. Load when the cone plate
  x^2 + y^2 = s^2 z^2, the apex (0, 0, 0), or the two-way channel-need note
  from that sitting is named. Sibling of earlier SVCT maps, not a merge.
---

# session-map-2026-09-27-apex-plate

Stamp: 2026-09-27T11:34:00-04:00

Append: 2026-09-27T11:34-04:00 · apex plate + two-way need · HIT plate unrevised, s unfitted, channels not merged · VAL plate SHA-256 dbcd144aa1fd3e631e510dba1991caba1e1378220bcc6e50e99f0fe02160cb39 · miss no other plates in this transcript · open next plate only if named

## Status

- HIT: the attached plate was kept. Equation on the title is `x^2 + y^2 = s^2 z^2`, meeting stated at `(0, 0, 0)`. Z is labeled pole. Legend names X, Y, Z (pole), and the origin point only.
- VAL: plate PNG SHA-256 `dbcd144aa1fd3e631e510dba1991caba1e1378220bcc6e50e99f0fe02160cb39`. Attachment bytes SHA-256 `74d6bdcfebf38d5f8680f1a21f7372e9c3b52420077f9ad2f29eb7dd27203160`. Plate pixels 1500×1571.
- s is a symbol. No numeric s. No pixel fit. Tick labels readable as −2, −1, 0, 1, 2 are grid marks, not a measurement of s.
- Two dark lines through the apex are visible and unlabeled. Reading them as rulings is a reading of the ink, not a printed label.
- Consequence of the written equation only: `rho = |s| |z|` with `rho = sqrt(x^2 + y^2)`. Parametrization `x = s z cos theta`, `y = s z sin theta`, theta free. At z = 0 the only point is the origin, so the two nappes meet only there.
- Channels are NOT a consequence of the cone. `mergedWithChannels` is false.

## Two-way need (his words, this sitting)

With every channel two-way, need can be detected from either end.

- Bottom-up: a node raises need on its return path. Vision loses lock, hearing picks up speech, or a sensor crosses a threshold, and the node signals the dispatcher instead of waiting to be polled.
- Top-down: the dispatcher raises need on the outbound path. A printed report can wake speech, or a request to identify an object can wake vision at full resolution.
- Idle nodes can sit at a low rate or asleep, and wake only when either side flags need. That saves power, which matters on the Anker pack, and cuts CPU and log volume.
- The edge handles need locally first. The cloud API is called only when the edge flags something it cannot resolve. The channels decide when to escalate.

## Miss

This transcript contains one plate and the channel note above. Other charts, diagrams, and earlier math were not in the transcript and were not copied in to look complete. They stay in their own skills. Not a merge.

## Open

Next plate only if named.

## Shelves

- Ledger hop message_id 1a0e3870f86678b8
- Notion page 3e8c9bfe-3aff-817e-9515-ea9da08169ae in Timothy Skills & KB
