# EDGE DATA MOVEMENT POLICY: local-first, optional cloud, masked API (docs only)
Generated: 2026-10-05 ~6:55 PM ET
Fail-closed. Docs only. Nothing installed, paired, synced, uploaded, or published. No cloud account, API key, or provider chosen. No GitHub push. No sealed primitives.
Boot continuity this pass: `bwbasic /workspace/hybrid-boot/BOOT.bas </dev/null` PRINT `0.70710678`, exit 0. That is math continuity, not proof any data path here is live.

---

## 1) Timothy's words (voice, 2026-10-05 evening ET, T)

> "Well, we have to be able to add to and take from files on demand or on need. we need to be able to do it without the cloud. We can do it with the cloud from time to time. We can also do it with APIs from time to time. But if we do it with APIs, then the data will be masked from personal data, and, and anything that gets processed will be to get the job done and not share information on the internet. Yes, we do have a home network and, and what the needs is for the phone, the cell phone we'll also keep going on the box. But not only. Take a look at this picture. You'll understand a little bit more after, after you see what's in it."

Photos sent with it: `EDGE_DESK_SETUP_2026-10-05.jpg` and `EDGE_HW_INVENTORY_2026-10-05.jpg` (as-seen notes: `EDGE_HW_INVENTORY_2026-10-05.md`).

---

## 2) LOCKED rules (DM-1 … DM-7, from T above)

| # | Rule (locked) | Source |
|---|---|---|
| DM-1 | Devices must be able to **add to** and **take from** files **on demand** (someone asks) **or on need** (the system sees a need). | T |
| DM-2 | All of that must **work without the cloud**. | T |
| DM-3 | The **cloud is OK from time to time** (optional, occasional, never required). | T |
| DM-4 | **APIs are OK from time to time** (optional, occasional, never required). | T |
| DM-5 | If an API is used: **personal data is masked** first; processing is **only to get the job done**; **information is not shared on the internet**. | T |
| DM-6 | A **home network exists** and may be used. | T |
| DM-7 | The **cell phone's needs are kept**. Work **keeps going on the box, "but not only"**: the box is one place the work lives, not the only place. | T (wording "but not only" kept as said) |

Reading of DM-7 (interpretation, marked I): the devices (phone, laptop, Pi-class boards) must also carry and run the work themselves, so losing the box must not stop them. Ask Timothy if this reading is wrong.

---

## 3) Tiers (SUGGESTED structure built from DM-1 … DM-7, not locked)

| Tier | What | Needs internet? | Required? | Rule tie |
|---|---|---|---|---|
| **0 On-device** | Files on the device itself (phone app folder, laptop disk, microSD, USB stick) | No | **Yes, always works** | DM-1, DM-2 |
| **1 Direct link** | Device to device over **USB, BT, or WiFi direct / hotspot** (no internet) | No | Optional | DM-2, L-F |
| **2 Home network (LAN)** | Devices on Timothy's home WiFi / LAN; one device can serve files to others on the LAN | No (LAN only; internet uplink not needed) | Optional | DM-6 |
| **3 Cloud (occasional)** | Sync or backup to a cloud store, from time to time. **Which cloud: UNDEF** | Yes | **Never required** | DM-3 |
| **4 API (occasional, masked)** | Send a masked piece of work to an outside API, get the result back. **Which API: UNDEF** | Yes | **Never required** | DM-4, DM-5 |

Fail-closed rule (SUGGESTED): if Tier 3 or Tier 4 is not reachable, or its terms are unknown, the device **stays on Tiers 0–2 and keeps working**. No step may wait forever on the internet.

### Where the box sits
- The box is a **remote, internet-reached machine**. For DM-2 it counts as **online (Tier 3-like)**, not as local storage. (I)
- So: the box is where drafts, checks, and docs are built ("keep going on the box"), but **no device may need the box to run** ("but not only", DM-7). (I)

### Where each transport sits (ties to `EDGE_TRANSPORT_MATRIX_2026-10-05.md`)
| Transport | Tier when used | Offline-capable? |
|---|---|---|
| USB (cable, thumb drive, microSD) | 0 / 1 | Yes |
| BT | 1 | Yes |
| WiFi direct / hotspot without uplink | 1 | Yes |
| WiFi on home LAN | 2 | Yes (LAN only) |
| Cellular (Pi modem or phone tether, F') | 3 / 4 (it reaches the internet through a carrier) | **No**: cellular must not be the only path for DM-2 |
| Phone tether: local hop | 1 (the WiFi/USB/BT hop is local) | Yes for the hop; the upstream is online |

---

## 4) Add / take operations (DM-1) (SUGGESTED, not implemented)

| Operation | Meaning | Integrity |
|---|---|---|
| **ADD** | Write a new file, or add lines/records to an existing one | New file: sha256 into the manifest. Changed file: new sha256 + new manifest entry (old entry kept as history, I) |
| **TAKE** | Read a file or pull a copy out to another device; "take" does **not** mean delete unless Timothy says so | Receiver checks sha256 against the manifest; **refuse to run / refuse to use on mismatch** (`EDGE_MANIFEST_SPEC_2026-10-05.md` §2, §4) |
| On demand | A person asks (voice, tap, typed command) | Same checks |
| On need | The system detects it needs a file (for example a missing sensor driver) | **Need-detector: UNDEF** (same UNDEF as port map "on-need install") |

- Every ADD/TAKE writes a small local log line on the device (SUGGESTED fields: time ET, op, path, sha256, tier, transport). Log stays on the device (Tier 0).
- Deletion, overwrite-in-place, and conflict merge (two devices changed the same file): **UNDEF**. Default SUGGESTED: never overwrite silently; keep both copies and flag.
- Standing (Timothy 2026-10-05): **append freely**; unused work is **retired/archived, not deleted** — see `EDGE_APPEND_ARCHIVE_POLICY_2026-10-05.md` (AA-1…AA-3).

---

## 5) API masking (DM-5) (SUGGESTED checklist, not implemented)

Before anything goes to an outside API:
1. **Minimum needed only.** Send only the piece needed to get the job done (for example the math expression, not the whole file).
2. **Mask personal data.** Replace with placeholders such as `[NAME_1]`, `[PHONE_1]`. Candidates to mask (SUGGESTED list):
   - person names (including names seen on objects, for example an engraving on a case), handles, emails, phone numbers, street addresses
   - account numbers, card numbers, money details
   - location (GPS, EXIF in photos), home network names, device serials and order barcodes
   - faces and voices: **raw photos, video, and audio do not go to APIs by default** (send derived text only, if Timothy allows)
   - medical or family details
3. **The mask map stays local** (Tier 0). Results come back with placeholders; the device puts the real values back locally.
4. **No sharing on the internet.** The API call is a private request/response. Nothing is posted, published, or shared. (DM-5)
5. **Provider terms checked first.** If the provider's data retention / training-use terms are **unknown, do not send** (fail-closed). Provider: **UNDEF**.
6. **Log it locally**: time ET, what was sent (masked form), which provider, why.

Masking method (regex list, on-device model, or manual review): **UNDEF**.

---

## 6) Cloud (DM-3) (SUGGESTED, not implemented)

- Occasional only; schedule (daily, weekly, on WiFi only): **UNDEF**.
- Only **manifest-verified** bundles go up; the same sha256 checks apply coming back down.
- Encryption before upload: SUGGESTED; method **UNDEF**.
- Which cloud (iCloud, Google Drive, other): **UNDEF**. No account touched.
- Timothy's photos: stay on the box `reference-map/` only; **not uploaded anywhere else** this pass.

---

## 7) Phone needs kept (DM-7)

- Phone phase 1 = iOS / Pythonista (L-A). Pythonista files live on the phone (Tier 0) and must work offline.
- Delivery to the phone over the **home network** is now possible in principle (DM-6), but iOS delivery options **A / B / C remain QUESTIONS and are NOT locked** (`EDGE_MANIFEST_SPEC_2026-10-05.md` §5).
- Phone as cellular tether for Pi-class boards (F') = online tier; optional.

---

## 8) Non-claims

- No sync, server, share, API call, or upload set up anywhere.
- No masking code written. No provider chosen. No home network details recorded (SSID, IP, router: none asked, none stored).
- Nothing installed on Timothy's phone, laptop, Pi, or sensors.

---

## 9) UNDEF list (data movement)

1. Need-detector logic ("on need").
2. Conflict / merge rule when two devices change one file; delete rule.
3. Cloud provider, schedule, encryption method.
4. API provider(s), their retention terms, masking method.
5. Which device serves files on the home LAN (laptop? Pi?), and protocol (HTTP, SMB, rsync, other).
6. iOS delivery A / B / C (not locked).
7. Local log format and where it rolls up.
8. Whether drones / Hive / Swarm units use Tier 2 LAN or only Tier 1 direct links.

---

## 10) Cross-links

- Locked answers (DM section): `EDGE_LOCKED_ANSWERS_2026-10-05.md`
- Transport matrix (tier overlay §3f): `EDGE_TRANSPORT_MATRIX_2026-10-05.md`
- Manifest spec (§10 data-movement tie-in): `EDGE_MANIFEST_SPEC_2026-10-05.md`
- Port map (owned hardware + DM note): `EDGE_DEVICE_PORT_MAP_2026-10-05.md`
- Cellular note (F'): `EDGE_CELLULAR_NOTE_2026-10-05.md`
- Hardware as seen: `EDGE_HW_INVENTORY_2026-10-05.md`
- Master map: `MASTER_REFERENCE_MAP.md` §19

## Standing separation
- Data movement policy only. Not the descending-power sampler / live RGB. No hardware claimed running.
- Sealed kbld / MinRadius / GOSUB bodies excluded.

GitHub push: **SKIPPED**.
