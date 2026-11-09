# SESSION_MAP_2026-11-09_PI5_WORK_CORE MAP_v1 (pattern match and map)
Window: 2026-11-09 ~15:00 to 17:23 EST (Timothy t790u). Seat: Research. Append-only; never invent; UNVERIFIED when not checked. Pointer format: shelf · id/path · short name · SHA[:16] · date.

## Evidence items
1. [disk] Pi 5 "shepherd" ~/work zipped by Timothy: work_core_2026-11-09.zip 773241627 bytes, sha256 efc3307eb84cf5a98764346b0bb0b4ceeb2eff96b97409780f2622f540c20215. Drive full zip 1l8vN9il7ng5JFCRA7TlUcAbvyZZoLqi6 (over the 100 MB connector download limit).
2. [disk+Drive] 9 dd pieces bs=95000000 (wc_part00..08) uploaded to Drive between 12:21 and 15:32 EST (Drive modifiedTime 17:21:07Z..20:32:05Z); downloaded, each size+sha MATCH; cat 00..08 rebuilt the zip, sha MATCH, unzip -t OK.
3. [disk] Extracted 20410 files, 1639216430 bytes; analysis/ 13 files, SHA256SUMS 12/12 OK (inventory, content map, diff vs Grok-Build-Core, OEIS, secrets paths-only, recommendations).
4. [disk] Box restart ~16:52 EST: /workspace restored; extracted/ partial (14046 files); full re-extract extracted_r2/ 20410 files, sizes match INVENTORY.
5. [disk+connectors] RETRIEVAL_MAP_2026-11-09 written 16:15 EST (v1 f961450d22130927), appended through section 16 (parent) and 17 (this audit). Post-office card catalog RETRIEVAL_CATALOG_2026-11-09.tsv (C01..C66).
6. [disk] Post-office idea FOUND: /workspace/post-office-2026-10-20/README.md 3b67402c63b008ed (prototype 2026-10-20); applied as card catalog (active|held, never deleted).
7. [relay t782u-t784u] Georgia pbf ~/work/maps/georgia-latest.osm.pbf 357057388 bytes 2ac4c2ef929d4a04 deleted on Pi ~17:00 EST for Tesseract 5.5.4; Pi zip + wc_parts deleted after verification; Pi keeps maps/streamlined_20261010_101614 (all relayed; UNVERIFIED from box).
8. [disk] MAP_TEMPLATE georgia: header osmium/1.16.0, seq 4937, 2026-10-09T20:21:04Z, bbox -85.606800000/-80.743130000/35.003560000/30.353650000; streamlined schema 3 files; rebuild with osm_streamline.py 3/3 sha MATCH (210 seconds).
9. [Gmail+ledger] Ledger email "Grok-Build-Ledger 2026-11-09 Georgia map source record MAP_TEMPLATE (Research seat)" SENT via user card: Gmail 1a1c25c2c5178ad2, Mon 9 Nov 2026 14:09:43 -0800 (= 17:09:43 EST), to <mailbox redacted> only. LEDGER_QUEUE line 22 (queued), line 23 status_append "sent".
10. [parent] "Cohort pointers": named by the parent as a session topic; no cohort artifact found on box today (rg "cohort" found only older files). UNVERIFIED.
11. [relay t789u] Tesseract 5.5.0 → 5.5.4 in ~/work/tess_root (official tarball, leptonica 1.84.1, training off; /tmp/tess554 deleted; eng/osd unchanged; old libtesseract.so.5.0.5 kept by choice; df 29G/26G/1.7G/94%). Photo e6cb9489… 4716367 bytes sha256 b73b98fadd2c8a38 (section 16). Pi hashes not taken.
12. [relay] Camera ladder idea: DESIGN ONLY, NOT BUILT (motion detect → on-device OCR/vision → text only off device → Jetson/A15 escalation → iPhone live only on trigger; no install without OK).
13. [relay t790u] Pi memory reading 5:22–5:23 PM EST: available 3.1Gi of 7.9Gi; unused 1.2Gi; cache reclaimable 2.0Gi; swap 1.4Gi free of 2.0Gi, 630Mi used. Photo 9fe4aa01… not on box.
14. [boot] Boot file appends [WORKCORE-2026-11-09], [GEOMAP-2026-11-09]; open item 15 extended in place twice ("WORKCORE … makes 21.", "GEOMAP … makes 22.").
15. [Drive] wc_part09 1iKVWHnmK7990CHOnQRNvpM1qdZiS5zpE, 0 bytes, created 15:35:17 EST, in Drive root; not deleted.
16. [connectors] Saves: Notion 413c8669-9c94-810a-a91c-e8124855c29e (+Append 1–3); GitHub knowledge/pi5-work-core-2026-11-09/ (commits b705171d … 1513552e); Drive folder 1_Pf8YNWB4eLhaAWVBI59evpBfKVc45TP (27 items).
17. [Gmail/Drive/GitHub/Notion read-only] Other computer (Pi Grok, window "Tim Norman Drive and Gmail boot read - grok"): no saves attributable to it found today; see AUDIT section C.

## Patterns
P1 Map it, don't store it all: every off-device move gets a pointer (retrieval map, card catalog, MAP_TEMPLATE instead of the 357057388-byte pbf). [5,6,7,8]
P2 Verify by bytes: piece sha, rejoin sha, raw re-read, Drive re-download, streamline rebuild. [2,3,8,16]
P3 Fail closed on what the box cannot see: Pi state, photos not on box, cohort pointers. [7,10,11,13]
P4 Locked save order: ledger → Notion → GitHub → Drive → boot (archive first). [9,14,16]
P5 Free space on the Pi by moving copies off-device, then deleting with Timothy's OK. [7,11,15]
P6 Append-only with sealed versions; corrections as new rows/sections. [5,14]
