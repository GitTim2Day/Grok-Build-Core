# SESSION PATTERN MAP 2026-11-13 CAMERA SNAPSHOT TRANSCRIPT FOR IDLE SECURITY AND DOORBELL CAMERAS

America/New_York · Friday, November 13, 2026 · 10:24 AM EST

## HIT
User asked whether the comic-style snapshot + transcript method should be considered for security cameras and doorbell cameras that are always-on but idle.

Answer given: Yes. Strong fit. Idle most of the time. Continuous video writes nearly identical frames. Snapshot-plus-transcript stores a frame only on meaningful change (person, motion, scene shift). Idle stores almost nothing beyond occasional heartbeat. Event-driven recorder. Space savings of hundreds of times versus full video. Fits Pi 5 edge node.

User then confirmed edge AI motion detection already covered for webcams including eMeet SmartCam C960 (USB ID 328f:0066) on shepherd Pi 5. That detection is the trigger that keeps storage near zero until change is flagged.

User directed: pattern match, map, audit, pattern match map again, and save to the project and all other resources. Worth keeping; can always archive and return later.

## MAP
- Trigger: edge AI motion / change detection (already seated on C960 and similar UVC webcams on Pi 5).
- Capture: one clear snapshot + spoken or environmental transcript of that moment.
- Idle posture: minimal or zero new storage.
- Closure: hop / hash per segment so the record remains append-only and provenance-tracked.
- Storage outcome: hundreds of times less than continuous video for the same coverage.
- Device fit: Pi 5 shepherd and similar edge nodes; doorbell and security cameras that stay powered but idle.
- Status: worth keeping as default posture for idle-always-on cameras. Can be archived and returned to later.

## AUDIT
- Motion detection layer already present on the seated C960 path. No new detector required.
- Snapshot-plus-transcript uses that existing trigger rather than writing continuous video.
- Space numbers previously discussed apply directly.
- No PHI, no P-I-N-N, no account numbers in this map.
- Archive-not-delete holds: keep the idea; can archive if later unused.

## REMAP
The method is a direct application of the already-seated edge motion detector. It turns an always-on idle camera into an event-driven, provenance-tracked recorder. Worth keeping on the shelves. Open for later implementation or archive.

## OPEN
None on this map. Implementation only if later named.

## SHELVES
Email hop: 1a1d583186a58559
Notion: 417c9bfe-3aff-8167-b6c0-f68a90982351
SHA-256 93712191c0a79da19758606ea17d5166919656a9de1810241c4b25d7334b4d71 size 2575
Pointer skill: session-map-2026-11-13-camera-snapshot-transcript
