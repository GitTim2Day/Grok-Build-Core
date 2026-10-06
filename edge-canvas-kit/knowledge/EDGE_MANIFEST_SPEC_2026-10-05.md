# EDGE MANIFEST SPEC: integrity + provenance for BT / WiFi / USB delivery (docs only)
Generated: 2026-10-05 ~6:42 PM ET
Fail-closed. Docs only. Nothing paired, installed, purchased, flashed, or published. No GitHub push. No sealed primitives.
No implementation run on any phone, Pi, laptop, drone, Queen, Hive, or Swarm. No claim that hashlib, sha256sum, certutil, or any other hash tool is installed on Timothy's units.
Builds on: `EDGE_TRANSPORT_MATRIX_2026-10-05.md` · `EDGE_LOCKED_ANSWERS_2026-10-05.md` (F) · `EDGE_DEVICE_PORT_MAP_2026-10-05.md` · `EDGE_DEVICE_IO_FLOW_2026-10-05.md`
Boot continuity this pass: `bwbasic /workspace/hybrid-boot/BOOT.bas </dev/null` PRINT `0.70710678`, exit 0. That is math continuity, not proof that any manifest check here is live.

---

## 1) Purpose

Locked answer **F**: "Make the code so it can be sent BT, WiFi, or USB."
The transport matrix names a **sha256 manifest** as the integrity goal for every cell (goal only; not implemented; format was UNDEF).

This spec **drafts** that format so:

1. A receiving device can **refuse to run** code whose file hash does not match the manifest entry (**fail-closed**).
2. Every delivery keeps **provenance**: which file, which hash, which device class, which Hive unit (when applicable), which transport was used (Cellular | BT | WiFi | USB | UNDEF), and when (timestamp_ET).

Source tags (same vocabulary as the transport matrix / port map):

- **L** = Timothy's locked answers A–F
- **T** = Timothy's words
- **S** = sketch
- **R** = repo notes on box
- **P** = public, class-typical platform knowledge, **not verified on Timothy's unit**
- **SUGGESTED** = our proposal, **not locked**
- **UNDEF** = not earned

Nothing in this document is locked except the purpose link to **L-F** and the shared fail-closed standing rule. Field names, receipt shapes, signing, delivery options A/B/C, and fallback order are **SUGGESTED** or **QUESTIONS**.

---

## 2) Draft manifest fields (SUGGESTED, not locked)

One row (or object) per delivered file. Format on disk (JSON / CSV / BASIC DATA lines / other): **UNDEF**.

| Field | Type (SUGGESTED) | Required? | Meaning | Status |
|---|---|---|---|---|
| `path` | string | yes (SUGGESTED) | Relative path of the file inside the payload bundle | SUGGESTED |
| `sha256` | 64 hex chars | yes (SUGGESTED) | SHA-256 of file bytes; receiver refuses to run on mismatch | SUGGESTED (integrity goal from transport matrix) |
| `size_bytes` | non-negative integer | yes (SUGGESTED) | Byte length; cheap pre-check before hashing | SUGGESTED |
| `target_device_class` | string enum | yes (SUGGESTED) | One of: `pythonista_ios` · `android_later` · `pi5` · `laptop_asus_a15` · `smartphone_generic` · `ros2_node` · `drone` · `queen_maiden` · `hive_aggregate` · `swarm` · `UNDEF` | SUGGESTED names; class list from port map / L |
| `hive_unit_id` | string | optional | Stable id for one of ≥5 drones or optional Queen/Maiden (L-C). Omit or `UNDEF` when not a Hive delivery | SUGGESTED; id scheme UNDEF |
| `transport_used` | enum | yes (SUGGESTED) | `Cellular` \| `BT` \| `WiFi` \| `USB` \| `UNDEF` | SUGGESTED; matches L-F + F' (Cellular added 2026-10-05 ~6:50 PM ET) |
| `timestamp_ET` | string | yes (SUGGESTED) | When this row was written, America/New_York, e.g. `2026-10-05 18:42:00 ET` | SUGGESTED; exact format UNDEF |

**Cellular (F'):** `Cellular` = payload arrived over the device's own cellular link (e.g. a Pi add-on modem; class UNDEF, "Q-tel" = as-heard lead only). For a **smartphone tether**, whether to write `Cellular` or the local hop (`WiFi` / `USB` / `BT`) is a **QUESTION (UNDEF)**. Carrier, APN, SIM: not recorded and not invented. Box stub `manifest_check.py` now enforces `BT|WiFi|USB|Cellular|UNDEF` (exact case; updated 2026-10-05 ~6:48 PM ET). Self-check: 59 PASS / 0 FAIL (62 with optional lead_filter).

**Not included (UNDEF / not earned):** carrier / APN / SIM fields, digital signature fields, signer identity, certificate chain, encryption keys, compression codec, chunk size for BT, HTTP host/port, Apple ID, WiFi SSID.

**Refuse-to-run rule (GOAL, not implemented):**

1. Read manifest row for `path`.
2. If file missing → refuse.
3. If `size_bytes` mismatches → refuse (optional cheap gate).
4. Compute sha256 of file bytes; if ≠ `sha256` → refuse.
5. Only then may the device load/run that file.
6. Wrong or missing `transport_used` / empty manifest → treat as fail-closed UNDEF policy (not chosen).

No code implementing steps 1–6 is claimed on any device.

---

## 3) Receipt record per Hive unit (SUGGESTED fields; UNDEF where unknown)

Locked answer **C**: Hive = **≥5 drones** + optional **Queen (or Maiden)**.
Transport matrix §3 already wants "same manifest hash on every unit" plus a "per-unit receipt report" (goal, not implemented).

One **receipt** per unit that was targeted. Fan-out method (per-unit hand copy vs Queen relay): **UNDEF**.

| Field | Type (SUGGESTED) | Meaning | Status |
|---|---|---|---|
| `hive_unit_id` | string | Which drone or Queen/Maiden this receipt is for | SUGGESTED; id scheme UNDEF |
| `unit_role` | enum | `drone` \| `queen` \| `maiden` \| `UNDEF` | SUGGESTED |
| `manifest_sha256` | 64 hex | Hash of the **manifest file itself** (or of the whole bundle — which one: UNDEF) so units can prove they got the same list | SUGGESTED |
| `files_ok` | integer | Count of files that passed sha256 | SUGGESTED |
| `files_fail` | integer | Count that mismatched or were missing | SUGGESTED |
| `transport_used` | `Cellular` \| `BT` \| `WiFi` \| `USB` \| `UNDEF` | How this unit received the payload | SUGGESTED |
| `received_timestamp_ET` | string | When verification finished on the unit (or on the sender if unit cannot report — UNDEF) | SUGGESTED |
| `refuse_to_run` | boolean | `true` if any required file failed → unit must not run payload | SUGGESTED |
| `notes` | string | Free text; empty allowed | SUGGESTED |

**Still UNDEF for receipts:** how receipts travel back (device → host), receipt store location, Queen aggregation of N≥5 receipts, offline-only units, clock sync for `timestamp_ET`, what happens if Queen is absent.

No receipt is generated by this pass.

---

## 4) Integrity: sha256 only as goal; signing UNDEF

- **Integrity goal (from transport matrix, reiterated):** SHA-256 per file, checked on receipt; refuse to run on mismatch. **Goal only. Not implemented.**
- **Signing** (ed25519, PGP, code-signing certs, Apple notarization, etc.): **UNDEF** unless Timothy later earns it. This draft does **not** invent a signer or claim a key exists.
- Class-typical hash tools named in the transport matrix (P, not verified / not claimed installed on Timothy's units):
  - Pythonista / Python: stdlib `hashlib` (P)
  - Pi5 / Linux: `sha256sum` (P)
  - Windows laptop: `certutil -hashfile` / PowerShell `Get-FileHash` (P)
- Presence of those tools on Timothy's ASUS A15, Pi5, or phone: **UNDEF**. This doc does not install them.

---

## 5) iOS-first delivery options (QUESTIONS — not chosen)

Phase 1 phone target = **iOS / Pythonista** (L-A). Transport matrix already lists class-typical USB / WiFi / BT constraints (P). Timothy has **not** chosen which path is primary.

Open questions (do **not** invent an answer; do **not** treat as a widget for immediate re-ask):

- **Option A — USB file sharing:** computer → Pythonista app file sharing (Finder on macOS / Apple Devices or iTunes app on Windows, P). Whether Pythonista appears in file sharing on Timothy's phone: **UNDEF**. Whether Apple Devices/iTunes is on the ASUS A15: **UNDEF**.
- **Option B — Files / iCloud (or other Files-app provider):** copy or pull into the iOS Files app, then import into Pythonista (P). Apple ID use, provider choice, and Pythonista access to that location: **UNDEF**.
- **Option C — Home-network download into Pythonista:** pull over LAN/WiFi via Pythonista stdlib HTTP (`urllib`, P candidate; not written). Host, port, endpoint, and credentials: **UNDEF**.

BT for iOS remains **no generic file transfer (P)**; custom BLE via Pythonista `cb` only, protocol UNDEF (transport matrix §3c). Any of A/B/C can still carry a sha256 manifest; none is selected here.

---

## 6) Fallback order (SUGGESTED, not locked)

Same as transport matrix §2:

**USB → WiFi → BT**

Reasons unchanged (SUGGESTED only): USB = wired, no radio pairing, usually fastest; WiFi = needs network + credentials; BT = needs pairing and is usually slowest for files. iOS may force a change (no generic BT). Timothy can override. **Not locked.**

---

## 7) Explicit non-claims

- **No implementation** of manifest write, hash verify, refuse-to-run, or receipt emit on any device.
- **No claim** that hashlib / sha256sum / Get-FileHash / certutil / Pythonista / pip / apt / winget / BlueZ / SSH / adb are installed or enabled on Timothy's units.
- **Nothing paired, installed, purchased, flashed, or published.** No GitHub push this pass.
- **JBL Clip 4** and the **two cameras with mics** (L-E) remain **owned peripherals**, not code transport (transport matrix §4).
- Sealed kbld / MinRadius / GOSUB bodies are **not** part of this doc.
- BOOT.bas `0.70710678` = math continuity only.

---

## 8) Cross-links

- Transport matrix: `reference-map/EDGE_TRANSPORT_MATRIX_2026-10-05.md` (stable sha256 `d74ed48acb7ff6ad7ff2d6890762137e513f0ab6a7e1ca9dce471345b9fee8d6`). Integrity goal and SUGGESTED fallback order live there; this spec drafts the format those cells pointed at as UNDEF.
- Locked answers A–F: `reference-map/EDGE_LOCKED_ANSWERS_2026-10-05.md` (sha256 `a639384370a3f4c1969adff664349b289711817727b85d8c4717f73a324c4cbb`). F = transport; C = Hive ≥5 + optional Queen/Maiden; A = iOS first.
- Port map: `reference-map/EDGE_DEVICE_PORT_MAP_2026-10-05.md` (stable sha256 `6fdf49715bf8cd9230adde282e582cf102ebd195c6be27e9f59791ccf15da8b2`).
- Flow map: `reference-map/EDGE_DEVICE_IO_FLOW_2026-10-05.md` (stable sha256 `83b625f7b760871e6cdae88646608f1b640ea98794fb47c154089c2cf3031557`).
- Cellular note: `reference-map/EDGE_CELLULAR_NOTE_2026-10-05.md` (sha256 `df3ee7d9d2f8dd4297b47a7cb5f4469520205fc686d39b67861d75c2c62e4633`).
- Data movement policy: `reference-map/EDGE_DATA_MOVEMENT_POLICY_2026-10-05.md` (sha256 `3ff3189f34aee47385626a913ec1268cd3e2641e15b3f67ed308329f57f22953`); tie-in = §10 here.
- Hardware as seen: `reference-map/EDGE_HW_INVENTORY_2026-10-05.md` (sha256 `38cc51cc9b7eea980f6c1ebe2b7ab565cc5a8f65f3dd4ca71aec5cd622c9d908`).
- Master map: `reference-map/MASTER_REFERENCE_MAP.md` §14 (cellular amendment §16; data movement §19).

---

## 9) Remaining UNDEFs (this spec)

1. On-disk manifest serialization (JSON / CSV / other).
2. Whether `manifest_sha256` hashes the manifest file or the whole bundle.
3. `hive_unit_id` naming scheme; Queen/Maiden presence per deployment.
4. Receipt return path and store; Queen aggregation of ≥5 receipts.
5. Signing (yes/no, algorithm, keys) — stays UNDEF.
6. Which of iOS delivery options A / B / C Timothy wants first.
7. Final fallback order (still SUGGESTED USB → WiFi → BT); Cellular rank UNDEF.
8. Hash-tool presence on each of Timothy's units.
9. Policy when manifest is missing entirely vs partially corrupt.
10. `transport_used` value for a smartphone-tethered delivery (`Cellular` vs local hop).

---

## 10) Data-movement tie-in (DM-1 … DM-7, added 2026-10-05 ~6:55 PM ET)

Locked rules: `EDGE_DATA_MOVEMENT_POLICY_2026-10-05.md`. What they mean for this spec (all **SUGGESTED**, not locked; the box stub `targets/pythonista/phase1/manifest_check.py` was **not** edited for these):

| Optional field (SUGGESTED) | Values | Why |
|---|---|---|
| `op` | `ADD` \| `TAKE` \| `UNDEF` | DM-1: add to / take from files on demand or need |
| `data_tier` | `device` \| `direct` \| `lan` \| `cloud` \| `api` \| `UNDEF` | DM-2…DM-4: shows whether a file came by a local path or an online one |
| `masked` | `yes` \| `no` \| `n/a` | DM-5: anything sent to or returned from an API must say it was masked; `no` + `data_tier=api` = refuse (SUGGESTED) |
| `target_device_class` new value | `pi_zero2_w` | Pi Zero 2 W seen in photo (`EDGE_HW_INVENTORY_2026-10-05.md`); not yet in the stub enum |

- Refuse-to-run on sha256 mismatch applies the **same way on every tier**. A file that came from the cloud or an API is checked exactly like one from USB.
- DM-2: a device must be able to verify and run using **only** its local copy of the manifest and files. No step may need the internet to check a hash.
- iOS options (§5): home network now affirmed (DM-6), which makes Option C possible in principle; Option B (iCloud / Files provider) is a cloud path, so it could never be the only path. **A / B / C remain QUESTIONS — not locked.**
- Cellular (F') = online path for DM-2 purposes; `transport_used=Cellular` with `data_tier=cloud` or `api` (SUGGESTED pairing).

---

## Standing separation

- Manifest / provenance draft only. Not the descending-power sampler / live RGB. No hardware claimed running.
- Sealed kbld / MinRadius / GOSUB bodies excluded.

---

## Footer: hashes

| File | sha256 |
|------|--------|
| `EDGE_DEVICE_IO_SKETCH_2026-10-05.jpg` | `bb128b52a81a12e6db8b913241a48cc0dc52046719a34aa38f2fd2cbfe8d4659` |
| `EDGE_UNKNOWNS_ANSWERS_A-F_2026-10-05.jpg` | `a602b99edebc6c1ff119ed49b71d5ff51c1beb93781984d8a77b004bc76d49c9` |
| `EDGE_LOCKED_ANSWERS_2026-10-05.md` | `a639384370a3f4c1969adff664349b289711817727b85d8c4717f73a324c4cbb` |
| `EDGE_DEVICE_PORT_MAP_2026-10-05.md` (stable) | `6fdf49715bf8cd9230adde282e582cf102ebd195c6be27e9f59791ccf15da8b2` |
| `EDGE_DEVICE_IO_FLOW_2026-10-05.md` (stable) | `83b625f7b760871e6cdae88646608f1b640ea98794fb47c154089c2cf3031557` |
| `EDGE_TRANSPORT_MATRIX_2026-10-05.md` (stable) | `d74ed48acb7ff6ad7ff2d6890762137e513f0ab6a7e1ca9dce471345b9fee8d6` |
| `EDGE_CELLULAR_NOTE_2026-10-05.md` | `df3ee7d9d2f8dd4297b47a7cb5f4469520205fc686d39b67861d75c2c62e4633` |
| `EDGE_DATA_MOVEMENT_POLICY_2026-10-05.md` | `3ff3189f34aee47385626a913ec1268cd3e2641e15b3f67ed308329f57f22953` |
| `EDGE_HW_INVENTORY_2026-10-05.md` | `38cc51cc9b7eea980f6c1ebe2b7ab565cc5a8f65f3dd4ca71aec5cd622c9d908` |
| `EDGE_MANIFEST_SPEC_2026-10-05.md` | `bbe4ddef3c61192b0c5e6521c41d9881e6cbb428d554f2c21c09c5808e995668` |

How the manifest-spec sha256 above is made: SHA-256 of this file with the manifest-spec-hash cell left blank (empty backticks, the same stable method as the port map, flow map, and transport matrix). A full-file sha256sum after the fill differs by that cell only.
Prior stable hash before Cellular (~6:42 PM ET): `4a5ea32f918f11b64b364c9234d83d287c9cce113c42604ed24bdeee3d958d2e`.
Prior stable hash before §10 data-movement tie-in (2026-10-05 ~6:55 PM ET): `1fbaf056ff73f487019893e24478fcc5a5222c047129aeb23a8f4968bf292284`.
GitHub push: **SKIPPED**.
