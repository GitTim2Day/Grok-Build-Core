# Flock connector links
Owner: Tim
Name: flock-connector-links-2026-10-20
When: he asks for Flock connections or methods. Not when he asks for their code.
Stamp: 2026-10-20T19:24-04:00
Sibling of FLOCK_SEARCH_MISS_2026-10-20.md. Not a merge. That file stands. This one is the links.

## What this is
The published connection list. No source body. No call to their API. No camera that is not his.

Wrong host: flock.com is a chat product. Its incoming-webhook page is not this system.
Right host: flocksafety.com and docs.flocksafety.com.

## Best links
1. https://docs.flocksafety.com/developer-hub/docs/flock-developer-platform-overview
2. https://docs.flocksafety.com/developer-hub/docs/authentication-overview
3. https://docs.flocksafety.com/developer-hub/docs/introduction
4. https://docs.flocksafety.com/developer-hub/docs/quickstart
5. https://docs.flocksafety.com/developer-hub/docs/user-level-oauth
6. https://docs.flocksafety.com/developer-hub/docs/developer-sandboxes
7. https://www.flocksafety.com/blog/video-without-limitations-flock-safetys-newest-solutions-for-law-enforcement
8. https://www.flocksafety.com/blog/flock-safety-cybersecurity-how-we-protect-customer-community-data

A third-party copy of their contract lives at apis.io and in a GitHub harvest. Those are not the contract. Use the six docs.

## Their methods
Two doors.
- Machine token. Server to server. Host api.flocksafety.com. Audience com.flocksafety.integrations. Needs a client id they issued.
- User token. A person signs in at login.flocksafety.com. The app inherits that person's device rights.

Ten named APIs, from their authentication table.

| API | Way | Token |
| --- | --- | --- |
| Vehicle Detections Search | out | user |
| Custom Hotlist v3 | both | user and machine |
| Device v4 | out | user |
| Device v3, devices they own | out | user and machine |
| Device v3, a sensor you register | in | machine |
| Hotlist alert subscription | out, webhook | machine |
| CAD | in | machine |
| Geolocation | in | machine |
| Inbound alerts | in | machine |
| Vehicle detections ingest | in, images from your camera | machine |

Their own roadside cameras use a private cellular link to their cloud. That sentence is on their security post. The wire is not published.

Wing Gateway is the product that takes cameras a customer already owns and puts the feeds in their platform. The blog names the box. It does not name ONVIF, RTSP, or a port. That protocol is a miss.

Sandbox is not a second internet. The sandbox page says use the production host api.flocksafety.com. Synthetic vehicles pass a test camera every 10 minutes. Access is an approved app. This chair has no app.

## For his connectors
He does not have a Flock app. Do not call api.flocksafety.com. Do not send a picture from a camera he does not own.

The shape worth keeping, pointed at shelves he owns:

1. Name the device. The only camera this project has named is the eMeet on the Pi, /dev/video0.
2. Store a still he took. Time, place, device name, hash. His mailbox or Notion. Not their cloud.
3. Search that shelf. Not their plate index.
4. On a hit, mail the ledger. That hop already exists.
5. Stop if the camera is not his. Stop if the host is flock.com.

BASIC:
IF the camera is not his THEN stop.
IF the still is his THEN store time, place, device, hash.
IF his rule hits THEN mail the ledger.
IF the host is api.flocksafety.com AND he has no approved app THEN do not call.

## Count
Ten of their APIs. Two auth methods. One gateway whose wire is unpublished. Three camera steps they publish in plain language: motion, plate read, vehicle signature. No line count. Their source was not opened. No algorithm inside those models was measured.

## Audit
HIT: the six doc pages and the two posts. The auth table was read.
VAL: in and out match that table. The gateway wire was not on those pages.
Miss: the introduction page did not return a full body on one fetch. The same URL's public text did name the APIs. No live call. No client id on this chair.
Open: the gateway protocol, only if he later has a manual that names it.
