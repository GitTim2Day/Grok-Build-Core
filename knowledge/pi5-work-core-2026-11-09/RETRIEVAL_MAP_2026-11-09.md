# RETRIEVAL MAP — pi5 work_core 2026-11-09 (Research seat)

Purpose (Timothy, t775u): map how we got it and where we left it, so a later session goes straight to it. Pointer format: `shelf · id/path · short name · SHA[:16] · date`. Append-only: later save locations are appended in section 9, never edited above.

## 1. Provenance chain

1. Pi 5 "shepherd" · `~/work/` · live working tree · — · newest file mtime 2026-10-16T21:53:28Z (UTC)
2. Pi 5 · `~/work_core_2026-11-09.zip` · zip of ~/work made by Timothy · efc3307eb84cf5a9 · 2026-11-09 (773241627 bytes, 23734 entries = 20410 files + 3324 dirs, 1639216430 bytes uncompressed)
3. Drive · `1l8vN9il7ng5JFCRA7TlUcAbvyZZoLqi6` · full zip uploaded by Timothy · efc3307eb84cf5a9 · 2026-11-09. Not downloadable here: 773241627 bytes is over the 100 MB connector download limit (STATUS 11:15 EST FETCH FAILED).
4. Pi 5 → Drive · 9 pieces cut on the Pi with `dd if=work_core_2026-11-09.zip of=wc_partNN bs=95000000 skip=N count=1` (N = 0..8), each uploaded to Drive in Firefox, then `rm` on the Pi:

| piece | Drive id | bytes | sha256[:16] |
|---|---|--:|---|
| wc_part00 | 1zgsxhXQG0JML_sP8S0tsXJeamyyorsQZ | 95000000 | edaf5a9fb9880f87 |
| wc_part01 | 1ZQaNR3zRm9L5_H_dTiGt97E2MUtjeu48 | 95000000 | 65f643f0f90edd05 |
| wc_part02 | 1VQWIDFpN1VFWI4POuIYJAhu1qzehTdpl | 95000000 | 98a80542663e294c |
| wc_part03 | 1uWKivdNbuuHuk2knvFN68lQyG_Ue7Lcw | 95000000 | 9cd93b14d7fe9758 |
| wc_part04 | 1ShYQkZ0QXt6OyCgsjpt2g8vS0neKbKCA | 95000000 | d7b2f49a4dff7848 |
| wc_part05 | 1ZvVMAAJZf9wysMhAWOuJ6_TWElVlImjr | 95000000 | cd43cbfeeedce204 |
| wc_part06 | 1ZWCXGoe2z4Q2uKqEIrYZz9FHbeY-Uc3z | 95000000 | 66e067758cf6f726 |
| wc_part07 | 1ubHXYpmL4YE11MLwrYmfJ8Tjk6aMf2kr | 95000000 | 2a0b55b5c899f6c0 |
| wc_part08 | 1xFOwl6z_TxDBxgNzLpX33dNCEw-BunbE | 13241627 | b5135fca9cfcec7c |
| total | | 773241627 | |

5. box · `/workspace/pi5-work-core-2026-11-09/original/parts/` · 9 pieces via cursor DownloadFile (connection user-Google-drive), each size+sha verified · 2026-11-09
6. box · `/workspace/pi5-work-core-2026-11-09/original/work_core_2026-11-09.zip` · rebuilt by `cat` in order 00..08; sha256 MATCH, `unzip -t` no errors; chmod a-w · efc3307eb84cf5a9 · 2026-11-09
7. box · `/workspace/pi5-work-core-2026-11-09/extracted/work/` · `unzip`, then `chmod -R a-w` · 20410 files, 1639216430 bytes · 2026-11-09
8. box · `/workspace/pi5-work-core-2026-11-09/analysis/` · inventory and analysis (scripts in `scripts/`) · 2026-11-09

## 2. Exact rejoin recipe (any machine with the Drive connector)

```
# download the 9 Drive ids above as wc_part00 … wc_part08 (cursor DownloadFile, each < 100 MB)
for n in 00 01 02 03 04 05 06 07 08; do test -f wc_part$n || echo MISSING $n; done
cat wc_part00 wc_part01 wc_part02 wc_part03 wc_part04 wc_part05 wc_part06 wc_part07 wc_part08 > work_core_2026-11-09.zip
stat -c %s work_core_2026-11-09.zip     # expect 773241627
sha256sum work_core_2026-11-09.zip     # expect efc3307eb84cf5a98764346b0bb0b4ceeb2eff96b97409780f2622f540c20215
unzip -t work_core_2026-11-09.zip >/dev/null && echo OK
```
Per-piece check: compare each piece's size and sha256 with the table in section 1 before `cat`. Box already holds a verified copy (section 3): use it first.

## 3. Where every copy is left

| shelf | id/path | short name | SHA[:16] | bytes | status |
|---|---|---|---|--:|---|
| Pi5 shepherd | `~/work/` | live working tree (source of everything) | — |  | active (state after 2026-10-16T21:53:28Z unverified) |
| Pi5 shepherd | `~/work_core_2026-11-09.zip` | full zip of ~/work | efc3307eb84cf5a9 | 773241627 | present per Timothy; not re-verified on Pi |
| Drive | `1l8vN9il7ng5JFCRA7TlUcAbvyZZoLqi6` | full zip in Drive (over 100 MB connector download limit) | efc3307eb84cf5a9 | 773241627 | active |
| Drive | `1zgsxhXQG0JML_sP8S0tsXJeamyyorsQZ` | wc_part00 (dd piece 1 of 9) | edaf5a9fb9880f87 | 95000000 | active |
| Drive | `1ZQaNR3zRm9L5_H_dTiGt97E2MUtjeu48` | wc_part01 (dd piece 2 of 9) | 65f643f0f90edd05 | 95000000 | active |
| Drive | `1VQWIDFpN1VFWI4POuIYJAhu1qzehTdpl` | wc_part02 (dd piece 3 of 9) | 98a80542663e294c | 95000000 | active |
| Drive | `1uWKivdNbuuHuk2knvFN68lQyG_Ue7Lcw` | wc_part03 (dd piece 4 of 9) | 9cd93b14d7fe9758 | 95000000 | active |
| Drive | `1ShYQkZ0QXt6OyCgsjpt2g8vS0neKbKCA` | wc_part04 (dd piece 5 of 9) | d7b2f49a4dff7848 | 95000000 | active |
| Drive | `1ZvVMAAJZf9wysMhAWOuJ6_TWElVlImjr` | wc_part05 (dd piece 6 of 9) | cd43cbfeeedce204 | 95000000 | active |
| Drive | `1ZWCXGoe2z4Q2uKqEIrYZz9FHbeY-Uc3z` | wc_part06 (dd piece 7 of 9) | 66e067758cf6f726 | 95000000 | active |
| Drive | `1ubHXYpmL4YE11MLwrYmfJ8Tjk6aMf2kr` | wc_part07 (dd piece 8 of 9) | 2a0b55b5c899f6c0 | 95000000 | active |
| Drive | `1xFOwl6z_TxDBxgNzLpX33dNCEw-BunbE` | wc_part08 (dd piece 9 of 9) | b5135fca9cfcec7c | 13241627 | active |
| box | `/workspace/pi5-work-core-2026-11-09/original/work_core_2026-11-09.zip` | rebuilt zip (read-only) | efc3307eb84cf5a9 | 773241627 | active |
| box | `/workspace/pi5-work-core-2026-11-09/original/parts/` | 9 downloaded pieces (read-only) | — | 773241627 | active |
| box | `/workspace/pi5-work-core-2026-11-09/extracted/work/` | extracted tree, chmod -R a-w | — | 1639216430 | active |

Pi-side notes (from the chat; not verified from here): pieces 00–06 were `rm`-ed on the Pi after each upload; Timothy was told 07 and 08 can be deleted (done or not: UNVERIFIED). The 773 MB zip itself is still on the Pi as far as known.

## 4. Analysis files (box, `/workspace/pi5-work-core-2026-11-09/analysis/`)

- box · `analysis/CLAUDE_SETTINGS_SUMMARY.md` · CLAUDE_SETTINGS_SUMMARY · 4e6946d07aa81211 · 2026-11-09 (13784 bytes)
- box · `analysis/COMMIT_CANDIDATES.tsv` · COMMIT_CANDIDATES · c1113cbbd7a47f8b · 2026-11-09 (61909 bytes)
- box · `analysis/CONTENT_MAP.md` · CONTENT_MAP · 52238c2e7bde3cc1 · 2026-11-09 (22687 bytes)
- box · `analysis/DIFF_VS_GROK_BUILD_CORE.md` · DIFF_VS_GROK_BUILD_CORE · cd5ab403192b781c · 2026-11-09 (26952 bytes)
- box · `analysis/DUPLICATES.json` · DUPLICATES · 1c851eb90264c1e2 · 2026-11-09 (1985815 bytes)
- box · `analysis/INVENTORY.jsonl` · INVENTORY · f1d8e2703e709adb · 2026-11-09 (8411713 bytes)
- box · `analysis/INVENTORY.tsv` · INVENTORY · 4a92b2c8748be5c3 · 2026-11-09 (5533985 bytes)
- box · `analysis/INVENTORY_SUMMARY.md` · INVENTORY_SUMMARY · 180c1954e2df9b63 · 2026-11-09 (26471 bytes)
- box · `analysis/OEIS.md` · OEIS · d41278adcae6e3ad · 2026-11-09 (17221 bytes)
- box · `analysis/RECOMMENDATIONS.md` · RECOMMENDATIONS · 1b836afd93ae0569 · 2026-11-09 (8043 bytes)
- box · `analysis/SECRETS.md` · SECRETS · c7c0c98c3cfa2837 · 2026-11-09 (11275 bytes)
- box · `analysis/SECRETS_HITS.tsv` · SECRETS_HITS · 7081b877b2abb789 · 2026-11-09 (1638076 bytes)
- box · `analysis/SHA256SUMS` · SHA256SUMS · bb0d2a4544fa52fe · 2026-11-09 (1005 bytes)

Public copy set for project shelves (`/workspace/pi5-work-core-2026-11-09/publish/`, read-only; `CLAUDE_SETTINGS_SUMMARY.public.md` has 4 Bluetooth MACs redacted; INVENTORY.jsonl/.tsv, DUPLICATES.json, SECRETS_HITS.tsv kept off GitHub for size):
- box · `publish/CLAUDE_SETTINGS_SUMMARY.public.md` · 32b9ee9de7c94be6 · 2026-11-09
- box · `publish/COMMIT_CANDIDATES.tsv` · c1113cbbd7a47f8b · 2026-11-09
- box · `publish/CONTENT_MAP.md` · 52238c2e7bde3cc1 · 2026-11-09
- box · `publish/DIFF_VS_GROK_BUILD_CORE.md` · cd5ab403192b781c · 2026-11-09
- box · `publish/INVENTORY_SUMMARY.md` · 180c1954e2df9b63 · 2026-11-09
- box · `publish/OEIS.md` · d41278adcae6e3ad · 2026-11-09
- box · `publish/RECOMMENDATIONS.md` · 1b836afd93ae0569 · 2026-11-09
- box · `publish/SECRETS.md` · c7c0c98c3cfa2837 · 2026-11-09

Other box items: `STATUS_2026-11-09.md`, `STATUS_2026-11-09_append1.md` (rebuild), `STATUS_2026-11-09_append2.md` (analysis); `prep/gh_tree.json` (GitHub tree 39a65bfd…); `.venv/` (puremagic, detect-secrets; project-local); `scratch/` (no secret values). OEIS reference data: `/workspace/oeis_public/stripped.gz`, `names.gz`.

## 5. What is NOT in the zip

- `~/Desktop/STORE`: `work/archive/DEDUPE_INDEX.tsv` records 115 files under ~/work turned into symlinks into STORE (377796414 bytes per the index); those files are absent (e.g. `rruff/raw/`, `archive/mutation_runs/` are empty).
- `~/work/oeis_data` (OEIS checkout used by oeis_earn, named in EARN_RESULTS_2026-10-16.md) and `~/work/tess_root` (named in jcj/README.md): not in the zip.
- `work/maps` second round, 851M as stated in the parent session (relayed; size and path not verified from the box).
- `~/Desktop/Queries`, `~/local` (bwbasic, cmake, piper, stt), anything outside ~/work, and any change after 2026-10-16T21:53:28Z.

## 6. Post-office idea (applied)

Earned source: `/workspace/post-office-2026-10-20/README.md` (sha256 3b67402c63b008ed…, "Offline Post Office (prototype, 2026-10-20), Timothy Gmail mirror"): write-once cabinet files, a card catalog (`catalog.tsv`: id, labels, file_path, sha256, synced_at, status active|held, source), append-only CHANGES.log and SHA256SUMS; files never overwritten; missing items marked `held`, never deleted. Routine "Post office mail run" hourly 7–22 ET (session-map-2026-10-20 PATTERN_MAP_v2 E56).
Applied here: `RETRIEVAL_CATALOG_2026-11-09.tsv` is a card catalog with one card per copy (item_id, shelf, locator, short_name, sha256, bytes, date, status, source). Copies that go missing later get status `held`, never removed. When the queued ledger email (section 9) is released and lands under the Gmail label Grok-Build-Ledger, the post-office sync files it as a write-once .eml in `cabinet/Grok-Build-Ledger/`, giving an offline retrievable copy (future; not done here).

## 7. Open next steps

1. Timothy: delete `~/work_core_2026-11-09.zip` from the Pi (frees 773241627 bytes; 3 verified copies exist) and any leftover wc_part07/08. Your call; nothing done to the Pi.
2. Pi read-only check: `du -xsh ~/* ~/Desktop/* 2>/dev/null | sort -h | tail -20` to size STORE, oeis_data, tess_root, maps round 2.
3. Decide commit of the 359 candidate source files (COMMIT_CANDIDATES.tsv) to Grok-Build-Core.
4. Pi: `git pull --ff-only` in ~/work/Grok-Build-Core (8 files behind-changed, 236 missing).
5. Release of the queued ledger email needs Timothy's OK.
6. RECOMMENDATIONS.md (archive maps 892121252, venvs 273554215, rruff 143470894, OEIS-derived 128897593, third_party 104714228).

## 8. Card catalog

Full catalog: `RETRIEVAL_CATALOG_2026-11-09.tsv` (36 cards) and the `catalog` array in `RETRIEVAL_MAP_2026-11-09.json`.

## 9. Save locations (appended after each save; see below)


### 9.1 Saves made (2026-11-09 17:00 EST)

- ledger queue · `/workspace/boot-archive/LEDGER_QUEUE.jsonl` · line 21 "Grok-Build-Ledger 2026-11-09 Pi5 work_core retrieval map (Research seat)", status queued, not sent · file e5b60d7d2d204258 (pre 540cd80327adab00, first 20 lines unchanged) · 2026-11-09. Email send: none. Yahoo untouched.
- Notion · `413c8669-9c94-810a-a91c-e8124855c29e` · RETRIEVAL_MAP_2026-11-09_PI5_WORK_CORE (Research seat), parent 403c8669-9c94-8117-bb27-c05770647c38 · https://app.notion.com/p/413c86699c94810aa91ce8124855c29e · 2026-11-09
- GitHub · GitTim2Day/Grok-Build-Core main · `knowledge/pi5-work-core-2026-11-09/` (13 files, SHA256SUMS 61a4662d36a8e714) · commits b705171d565fbfe2494b9a6b7a942d8404b5b34f (1/4 map files), 9a314acc9552ab102457199d15117087ac0ad2a7 (2/4), bab94ab4ccf7a494dccce5cedec9902cbf51a40d (3/4), 8676502eaeb3e801f105b21df07fe4e77f94d80e (4/4) · raw re-read at 8676502e: 12/12 sha OK, SHA256SUMS byte MATCH · 2026-11-09. Repo raw files are publicly readable: only the public set went up (MACs redacted; no INVENTORY/DUPLICATES/SECRETS_HITS, no zip, no extracted content, no secret values).
- Drive · folder `1_Pf8YNWB4eLhaAWVBI59evpBfKVc45TP` "pi5-work-core-2026-11-09" under root 0AAYi34wb_WB0Uk9PVA · https://drive.google.com/drive/folders/1_Pf8YNWB4eLhaAWVBI59evpBfKVc45TP · 2026-11-09:
  - RETRIEVAL_MAP_2026-11-09.md (v1) 1bcpYRki_KzxZ__3EWUfl3kHdEVosGeIn · f961450d22130927
  - RETRIEVAL_MAP_2026-11-09.txt 1FSl2MEZXexqL-p2x9YZMHib2QtXmwlF6 · 29e96f0b31b66f6a
  - RETRIEVAL_MAP_2026-11-09.json 1m_U4zhPaMxPLgB10lT__KbH0OnHH5e26 · 2e6d52ce533ce316
  - RETRIEVAL_CATALOG_2026-11-09.tsv 1g0rFvPo4QSpkaQlMxqYpnZsR-oo5tPcM · 9d37419db09517cc
  - CLAUDE_SETTINGS_SUMMARY.public.md 1lN0GE4rUX9y58b5pHwr6tAM0ogqofYmO
  - COMMIT_CANDIDATES.tsv 1wxiqBqzWrrAQDabD94XRYwjM17Fy_eUE · c1113cbbd7a47f8b
  - CONTENT_MAP.md 1anmU5pkyeXAuaNRKVEQs4ntafZqdnAQl · 52238c2e7bde3cc1
  - DIFF_VS_GROK_BUILD_CORE.md 1HLzrFbWHxvWO7sXqOo7gXATh1Djn9uuy · cd5ab403192b781c
  - INVENTORY_SUMMARY.md 1GsAcsL0cJvQa5WkSnOQYvpEOGcDjhX56 · 180c1954e2df9b63
  - OEIS.md 1fnPjsoqu6aTH6k1upkrNRBu9k1D9BETs · d41278adcae6e3ad
  - RECOMMENDATIONS.md 1I0uCQ3wYdvE4cY5dcS_piWq_d1EOl5S5 · 1b836afd93ae0569
  - SHA256SUMS 1jHOMSccG07OoUnHNhNvjUPWGu4JrY0fc · 61a4662d36a8e714
  - SECRETS.md: NOT uploaded (approval card interrupted before an answer; not retried). Copies: box analysis/ and GitHub.

## 10. Pi-side moves on 2026-11-09 (appended; Timothy-approved, relayed by the parent session)

- Pi · `~/work_core_2026-11-09.zip` and `~/wc_part00..08`: deleted on the Pi after verification (relayed; not checked from here). Copies: Drive full zip 1l8vN9il7ng5JFCRA7TlUcAbvyZZoLqi6; 9 Drive pieces (section 1); box `original/` (sha efc3307eb84cf5a9 re-checked 16:59 EST).
- Pi · `~/work/maps/georgia-latest.osm.pbf` · 357057388 bytes · sha256 2ac4c2ef929d4a04ff1280051c62b5791bf062f70eac16cfdabd27e9f9e4a1ce · mtime 2026-10-09T23:06:44Z (Oct 9 19:06 EDT) · deleted on the Pi ~2026-11-09 5:00 PM EST to make room for the Tesseract 5.5.4 build (approved by Timothy). Where it still is:
  - box · `/workspace/pi5-work-core-2026-11-09/extracted_r2/work/maps/georgia-latest.osm.pbf` · 2ac4c2ef929d4a04 (re-hashed MATCH vs INVENTORY) · read-only
  - box · inside `original/work_core_2026-11-09.zip` member `work/maps/georgia-latest.osm.pbf` (deflate, 356559532 compressed bytes, local header at byte 249053946)
  - Drive · inside the zip 1l8vN9il7ng5JFCRA7TlUcAbvyZZoLqi6, and across pieces wc_part02..wc_part06 (1VQWIDFpN1VFWI4POuIYJAhu1qzehTdpl, 1uWKivdNbuuHuk2knvFN68lQyG_Ue7Lcw, 1ShYQkZ0QXt6OyCgsjpt2g8vS0neKbKCA, 1ZvVMAAJZf9wysMhAWOuJ6_TWElVlImjr, 1ZWCXGoe2z4Q2uKqEIrYZz9FHbeY-Uc3z); rejoin all 9 and unzip that member
  - public source · Geofabrik `https://download.geofabrik.de/north-america/us/georgia-latest.osm.pbf` · a re-download is a newer snapshot with a different sha; only the copies above match 2ac4c2ef929d4a04
- Pi keeps · `~/work/maps/streamlined_20261010_101614/` (relayed; in the zip as work/maps/streamlined_20261010_101614/addresses.txt, 40243482 bytes).
- Rule: map it, don't store it all. Every off-device move gets a pointer entry here.

## 11. Box restore note (appended)

- The box restarted about 16:52 EST and /workspace was restored; `extracted/work/` came back partial (14046 files, 566398959 bytes; georgia pbf absent). Zip, 9 parts, analysis/ (SHA256SUMS OK), map, ledger queue and boot file were intact.
- Full re-extract: `/workspace/pi5-work-core-2026-11-09/extracted_r2/work/` · 20410 files, 1639216430 bytes, every size matches INVENTORY.tsv · read-only. Use extracted_r2; the partial `extracted/` is left in place, not deleted.

### 9.2 Boot file (appended)

- boot · `/home/box/agent-data/workflows/boot-summary-2026-10-24/SKILL.md` · entry [WORKCORE-2026-11-09] inserted before "## Standing rules"; open item 15 extended "WORKCORE-2026-11-09 makes 21." · pre 6b92d49bbdd9ba92 (archived `/workspace/boot-archive/boot-summary-2026-10-24_SKILL_archived_2026-11-09T2205Z_pre-WORKCORE.md`) → post f49a302c905d8936 (archived `..._2026-11-09T2207Z_post-WORKCORE.md`); both in ARCHIVE_INDEX.sha256 · 2026-11-09
- Final versions of this map go to GitHub (same folder, later commit) and Drive (new file RETRIEVAL_MAP_2026-11-09.final.md; v1 file left in place). Their ids are recorded in STATUS_2026-11-09_append3.md, since a file cannot hold its own hash.

## 12. Addendum 2026-11-09 ~5:15 PM EST — Georgia map pointer + MAP_TEMPLATE (Timothy t782u, t783u, t784u) [GEOMAP-2026-11-09]

Appended after sealed final 6227fbfb96908159; sections above unchanged.

- Georgia pbf pointer (restates section 10 for the follow-up): Pi `~/work/maps/georgia-latest.osm.pbf` · 357057388 bytes · sha256 2ac4c2ef929d4a04ff1280051c62b5791bf062f70eac16cfdabd27e9f9e4a1ce (INVENTORY.tsv row work/maps/georgia-latest.osm.pbf) · dated 2026-10-09 19:06 EDT · deleted on the Pi ~5:00 PM EST for Tesseract 5.5.4.
  - Requested path `extracted/work/maps/georgia-latest.osm.pbf` does NOT exist now: the box restart left extracted/ partial (section 11). Use `/workspace/pi5-work-core-2026-11-09/extracted_r2/work/maps/georgia-latest.osm.pbf` (re-hashed MATCH).
  - Drive: full zip 1l8vN9il7ng5JFCRA7TlUcAbvyZZoLqi6; pieces wc_part00..08 (ids in section 1; the member's bytes sit in wc_part02..06, all 9 needed to rejoin).
  - Public: Geofabrik georgia-latest.osm.pbf; a re-download is a newer snapshot with a different sha.
  - Pi zip + wc_part files: deleted on the Pi after verification. Pi keeps maps/streamlined_20261010_101614 (relayed).
- MAP_TEMPLATE (box `/workspace/pi5-work-core-2026-11-09/map_template/`, read-only):
  - MAP_TEMPLATE_georgia_2026-11-09.md · db9670bccf061756; .txt · 69d99ebbb0857a86; .json · a0727e2d1b9123ed
  - MAP_TEMPLATE_georgia_streamlined_schema_2026-11-09.tsv · 6c2d4a305dac0f62; georgia_pbf_header.json · 9222b852ddcc871a; pbf_header.py · 29b081cb6c17f4f5
  - Header (pure Python, no install; osmium not on box): bbox left -85.606800000 right -80.743130000 top 35.003560000 bottom 30.353650000; osmium/1.16.0; replication 2026-10-09T20:21:04Z seq 4937.
  - Streamlined: addresses.txt 40243482 bytes / 499712 lines / 6a5675d153615f10; road_nodes.txt 334937440 / 9719197 / aed91bc734fa392e; roads.txt 159882942 / 1383997 / 1687eebdb5e8410b.
- Saves of MAP_TEMPLATE:
  - ledger queue · `/workspace/boot-archive/LEDGER_QUEUE.jsonl` line 22 · Gmail only (no Yahoo) · file 8a096dec628c827b · email NOT sent from this seat; goes out via the user's review card (pending)
  - Notion · 413c8669-9c94-810a-a91c-e8124855c29e · "Append 2" at end
  - GitHub · GitTim2Day/Grok-Build-Core `knowledge/pi5-work-core-2026-11-09/map_template/` · commits 1d6b1f77fd891e9384863a4c4e863692641a43f4, 1f6723da9f817166886a9aaa7e55457f2e2411e2 · raw re-read 6/6 MATCH
  - Drive folder 1_Pf8YNWB4eLhaAWVBI59evpBfKVc45TP · md 1OHED7x6IHp6qpR69r2EZPVj6AsqfndP4 (re-download MATCH) · txt 1t6v3YxKgLJwAAb22KM3qMW_omg6RYLUM · json 1mKjkTSsbqY6ggBGJr9SqO8GNazIbPgwG · pbf_header.py 1DCSha10LhaH8Z646p7e5WASjXEu4Y27y · Google Sheet (schema table) 1CGYqQGUv9mnWADKsUD5KXxo6oUxMSHDfjbGcYwzIti0
  - Drive SECRETS.md retry (once, per t784u) · 1vozmPSk9YiFN6cbhUOUEMcDz-e-uDEyy · c7c0c98c3cfa2837
- Rebuild check: osm_streamline.py on the box copy started 17:03 EST into scratch/streamline_check/out_py; result not in yet at this append (pending; will be a later append).

- Boot · `/home/box/agent-data/workflows/boot-summary-2026-10-24/SKILL.md` · [GEOMAP-2026-11-09] entry · pre f49a302c905d8936 → post d2ee1bb24dd9fcf6 (archives …T2215Z_pre-GEOMAP.md, …T2216Z_post-GEOMAP.md in ARCHIVE_INDEX.sha256) · 2026-11-09

## 13. Addendum 2026-11-09 ~5:20 PM EST — rebuild check result [GEOMAP-2026-11-09]

- `python3 -I osm_streamline.py` (box copy of mapbook/osm_streamline.py c3a0db2bd38c0526) on the box copy of georgia-latest.osm.pbf (2ac4c2ef929d4a04) → `/workspace/pi5-work-core-2026-11-09/scratch/streamline_check/out_py/`; 210 seconds.
- addresses.txt 6a5675d153615f10 MATCH; road_nodes.txt aed91bc734fa392e MATCH; roads.txt 1687eebdb5e8410b MATCH (3/3 byte-identical to streamlined_20261010_101614). summary.txt 0c0d691e6eac2773 (extra file the Python twin writes).
- So: the template's restore step 3 is proven for the exact pbf; the Pi's streamlined folder can be rebuilt from any exact copy.

## 14. Addendum 2026-11-09 ~5:20 PM EST — Pi Tesseract 5.5.0 → 5.5.4 update log (Timothy t789u) [TESS554-2026-11-09]

Appended after sealed bde5cc54c46b1275; sections above unchanged. Source: Timothy's photo of the Pi Grok report, 5:16 PM EST, as relayed by the parent session. Pi file hashes were NOT taken (facts live only in the photo).

- Photo: parent gave path `/home/box/agent-data/agents/c367039e-5264-4eb6-8b22-f6edce2f8122/attachments/e6cb9489f6fbeeacecc4596eecfb4c7a5f725696423559c9b83b28026b7a78cd.jpg`. That file is NOT on the box at 5:20 PM EST (newest attachment there is from 16:53 EST), so its sha256 was NOT computed here. The file name looks like a content hash (e6cb9489f6fbeeac…) but that is unverified.
- Pi · `~/work/tess_root` · Tesseract 5.5.0 → 5.5.4, built in /tmp from the official 5.5.4 tarball against the existing leptonica 1.84.1; training tools off. Build folder /tmp/tess554 deleted.
- tessdata eng and osd unchanged · `/home/shepherd/work/tess_root/usr/share/tesseract-ocr/5/tessdata/`.
- Libraries reported: libgif 5.2.2; libjpeg 6b (libjpeg-turbo 2.1.5); libpng 1.6.48; libtiff 4.7.0; zlib 1.3.1; libwebp 1.5.0; libopenjp2 2.5.3. Found: NEON, OpenMP 201511, libarchive 3.7.4.
- Disk after: /dev/mmcblk0p2 29G total, 26G used, 1.7G available, 94% (as printed by df -h).
- Kept on purpose (Timothy's choice): old libtesseract.so.5.0.5 and old training programs in usr/bin. New binary uses libtesseract.so.5.5.
- Not updated: ~/whisper.cpp (absent). Not installed: Valhalla, OSRM, GraphHopper.
- Georgia pbf: already removed before this build (sections 10, 12).
- Note: the zip on the box/Drive holds tess_root? No: tess_root is NOT in the zip (section 5), so there is no off-device copy of the old 5.5.0 tree from this archive.

## 15. Idea entry — camera ladder (DESIGN ONLY, NOT BUILT) (Timothy 2026-11-09 5:11–5:15 PM EST) [CAMLADDER-2026-11-09]

1. Pi: motion detect (frame difference) triggers capture.
2. On device: OCR (Tesseract) or a small vision model turns the capture into text.
3. Only the text leaves the device, to the box or Drive.
4. Escalation: Jetson or A15 for full vision; live video to the iPhone only on trigger.
5. Nothing gets installed without Timothy's OK.

## 16. Append 2026-11-09 17:20 EST: photo hash for section 14 (C61 now active)

The Pi Grok report photo (Tesseract 5.5.4) reached the box at 17:19 EST. It is 4716367 bytes, sha256 b73b98fadd2c8a3863a6b280d9588d1eec925bb521ed3871b50341910e3919f2. The file name e6cb9489... is not its content hash. Path: /home/box/agent-data/agents/c367039e-5264-4eb6-8b22-f6edce2f8122/attachments/e6cb9489f6fbeeacecc4596eecfb4c7a5f725696423559c9b83b28026b7a78cd.jpg

## 17. Addendum 2026-11-09 17:27 EST — Pi memory reading + audit errata (Timothy t790u) [SESSIONAUDIT-2026-11-09]

Appended after sealed 46806abcdb472c08 (section 16 copy in retrieval_map_versions/RETRIEVAL_MAP_2026-11-09.section16.md); sections above unchanged.

### 17.1 Pi memory reading (Timothy photo of the Pi Grok report, 5:22–5:23 PM EST; relayed by the parent)
- available 3.1Gi of total 7.9Gi; unused RAM 1.2Gi; cache reclaimable 2.0Gi; swap 1.4Gi free of 2.0Gi, 630Mi used.
- Recorded exactly as shown. These are display values from the Pi tool (human-readable units); exact byte counts were not given and are UNVERIFIED.
- Photo path given: `/home/box/agent-data/agents/c367039e-5264-4eb6-8b22-f6edce2f8122/attachments/9fe4aa01fde886320eb0742b118aa3f28696b0c4f60c72d6e6892069a113a049.jpg`. NOT on the box at 17:26:46 EST, so its sha256 was NOT computed (status held).

### 17.2 Errata found by the session audit (corrections appended, nothing above edited)
- E1 rounded size labels: "773 MB" (section 3 Pi-side notes) means 773241627 bytes; "357 MB" (MAP_TEMPLATE purpose line, ledger email body) means 357057388 bytes; "100 MB" is the connector's own limit text.
- E2 catalog row C63 is malformed (8 fields; sha256 cut to 16 hex; no bytes; date in the bytes column). Corrective row C64 appended with full sha256 b73b98fadd2c8a3863a6b280d9588d1eec925bb521ed3871b50341910e3919f2 and bytes 4716367 (re-hashed on box).
- E3 section 14 says the photo was "NOT on the box at 5:20 PM EST"; the file mtime is 17:19 EST, so that check ran before 17:19 and the "5:20" heading time is approximate. Section 16 supersedes.
- E4 catalog row C03 carries text in the sha256 column (format deviation; value is still the zip sha).
- E5 Drive root holds `wc_part09` id 1iKVWHnmK7990CHOnQRNvpM1qdZiS5zpE, size 0 bytes, created 2026-11-09T20:35:17Z (3:35:17 PM EST). Not part of the rejoin; NOT deleted; needs Timothy's OK to trash.
- E6 the .txt companion did not receive section 16 when it was added to the .md; a labeled late copy was appended to the .txt after section 17.

## 18. Append 2026-11-09 17:43 EST: external drives on the Pi 5 (pointers only, nothing copied) [DRIVES-2026-11-09]

Source: Timothy's photos of Pi Grok output, 5:27-5:41 PM ET. Display values exactly as shown; exact bytes UNVERIFIED. No hashes of drive contents yet.
- sda1 NTFS "Seagate Expansion Drive" UUID 7C06E34006E2FA52, mounted read-only (udisksctl -o ro, ntfs3) at /media/shepherd/Seagate Expansion Drive. 1.9T size, 400G used (df), 1.5T avail, 22%. Previously only used on the ASUS A15 (Windows).
  Top folders as shown: SVCT_Edge_Vault 232G; WindowsImageBackup 133G; _SVCT_POCKET_BALANCE 23G; SVCT_iPhone_Sorted 5.3G; ollama 3.7G; KBLD_SVCT_Code_Backup 1.9G; need_speech 1.9G; Start_Here_Mac.app 28M; _MAIDEN_BRAIN 4.0M; svct_spines 3.1M; SVCT_Verbal_Tests 2.0M; SVCT_TTT_BUS 1.5M; svct_packs 264K; SVCT_UT_BRIDGE 80K; System Volume Information 36K; SVCT_HIVE_TRAVEL 28K; SVCT_Liability_Hold 12K; Seagate, $RECYCLE.BIN, KBLD_microSD_clones shown as 0 (display only; not stored as zero values). Loose files include UT_GrokBuild_2026-07-31.zip, UT_GrokBuild_KB_Skills_Pathway_2026-07-31.zip, Warranty.pdf, Start_Here_Win.exe, "curl -s httpsapi.x.aiv1responses.txt".
- sdb1 exFAT "_RADIOACTIV" USB stick, remounted read-only at /media/shepherd/_RADIOACTIV. 35G used.
  Top folders as shown: _SVCT_POCKET_PACK 27G; ollama-models 3.8G; ollama-extract 2.2G; .Spotlight-V100 117M; svct_packs 11M; System Volume Information 3.0M; inbox 3.0M; SVCT_Liability_Hold 3.0M; .fseventsd 2.0M. Loose file ollama-linux-arm64.tar.zst 1,600,157,086 bytes, Nov 7 14:38. Also EDGE_DEVICE, nmdsdcid, .cm0013, autorun.inf/.ico.
Retrieval: plug drive into Pi 5, `udisksctl mount -b /dev/sdX1 -o ro`. Next step proposed (awaiting Timothy): read-only file+sha256 listings of the small history folders.

## 19. Append 2026-11-09 18:16 EST: drive survey zip rebuild + analysis [DRIVE-SURVEY-2026-11-09]

How obtained: Pi Grok (shepherd) surveyed Seagate + _RADIOACTIV read-only, wrote `~/drive_survey_2026-11-09.zip` (10578887 bytes, sha256 `734011d832990e5b6cdb8a72bafd892be872343faf5635f4fa277d28483edab9`). Gateway capped ~750KB so Pi split into 700k parents then 179200-byte upload slices `ds_part00_00`..`ds_part14_03` (last slice 6087 bytes) + `ds_SHA256SUMS.txt` + `ds_UPLOAD_SHA256SUMS.txt` (61 Drive uploads). Box pulled via connector `user-Google-drive--[redacted-account]` (owner [redacted-email]) using Drive search (`name contains 'ds_part'` / SHA256), not hand-read photo ids. Concat name-sort order → zip; all 60 slice hashes + 15 parent hashes matched; zip sha matched. `unzip -t` OK. Nothing written to drives. No email. No Drive deletes.

### 19.1 Box paths
- zip: `/workspace/pi5-drive-survey-2026-11-09/original/drive_survey_2026-11-09.zip`
- pieces: `/workspace/pi5-drive-survey-2026-11-09/pieces/` (60 slices + 2 sums + MANIFEST.tsv + rebuilt `ds_part00`..`ds_part14`)
- extracted: `/workspace/pi5-drive-survey-2026-11-09/extracted/drive_survey_2026-11-09/`
- analysis: `/workspace/pi5-drive-survey-2026-11-09/ANALYSIS.md`
- hashes index: `/workspace/pi5-drive-survey-2026-11-09/HASHES.tsv`

### 19.2 Other copies
- Pi: `~/drive_survey_2026-11-09.zip` (source; sha above)
- Drive: 60 `ds_partNN_MM` + `ds_SHA256SUMS.txt` id `1nOzU0vF1FLTYiUBctODP7Ud_M4EhXo3g` (1234 bytes) + `ds_UPLOAD_SHA256SUMS.txt` id `1YDAbl2BCTrtvWiCi1UW8o0c2yB1Mp7Q4` (6516 bytes). Full id list in box `pieces/MANIFEST.tsv` sha256 `1a14edd9b5f1308b`.

### 19.3 Produced file sha256
| path | bytes | sha256 |
|---|---:|---|
| original/drive_survey_2026-11-09.zip | 10578887 | 734011d832990e5b6cdb8a72bafd892be872343faf5635f4fa277d28483edab9 |
| ANALYSIS.md | 85534 | 87d7994df64d1d149d5658b2b652dbe61a49afd6b39987a538654e267f6cc383 |
| pieces/ds_SHA256SUMS.txt | 1234 | bb00e401ff406448f2104740a2e7249480ea54a478dee3117a24ff3ce44a2a47 |
| pieces/ds_UPLOAD_SHA256SUMS.txt | 6516 | 3b570f9c4b1c52200cb4fd6156f112694c503dd9e3a966a6d4cade6c615cca4a |
| pieces/MANIFEST.tsv | 3359 | 1a14edd9b5f1308b1e80fe08019f08b23e06c635cb08f3b6c66a7c2a3bcc2ff4 |
| extracted/.../seagate_files.tsv | 45548996 | 58d7e9bf9bef2b63cfdbcaa08e20aacc13cc45f8adc21bb43963ec4b088f5a4c |
| extracted/.../radioactiv_files.tsv | 3461526 | db74cf793b47c603a5d765788a7b93aeb2ec7e4743e3398c6338dc031e263757 |
| extracted/.../small_sha256.tsv | 84825 | b15ad37224db3fb04915cec62f2932e43cc638545d33f9f257e6b93c5feb34b8 |
| extracted/.../big_folders.tsv | 55022317 | d2a6427ddd6cca9dbea1582778e98e3675aa08f2277d6ac3ccfa437f283c1806 |
| extracted/.../small_text_heads.txt | 523911 | c439c78ae78e03a50b99d8d54b25505d9844b6c09affd2af4177f0fdbca682d1 |
| extracted/.../read_errors.tsv | 11 | ef14f44785d400ed9fb1df5b5ba7af7f7cdd6f31f464b5a45bbb97769e0b798a |

### 19.4 Survey totals (from ANALYSIS; GiB = bytes//1024^3 truncate)
- Seagate Expansion Drive: 226199 files, 427626405067 bytes (398G trunc). Top: SVCT_Edge_Vault 231G; WindowsImageBackup 132G (Tims-PC Backup 2018-02-07); _SVCT_POCKET_BALANCE 22G; SVCT_iPhone_Sorted 5G; ollama 3G; KBLD_SVCT_Code_Backup 1G.
- _RADIOACTIV: 17478 files, 20134452649 bytes (18G trunc). Top: _SVCT_POCKET_PACK 11G; ollama-models 3G; ollama-extract 2G; ollama-linux-arm64.tar.zst 1G.
- Specific sealed filenames NOT on either drive: `kbld9_ocr_enhanced_processor.py`, `test_cms1500_adversarial_v3.py`, `Tims_Tables_Base360_Full_Reference.csv`. CMS1500 path hits 0. Tims Tables family present as `tims_table*` (291 paths). Base360 only as grok meta `Base-360_Earth_Index_Update_meta.json` (87 bytes).
- Cross-drive: 8317 same name+size pairs; 6 small sha256 groups spanning both drives (Liability_Hold + sense_voxel packs).
- read_errors: 0. Mounts remained read-only.

(Map sha256 before this append: `b0288a0df6eaabdb6bfde641ea0cd7c07caefb58a9a61b549824de863f31d031`)

### 19.5 Drive file ids (from search; MANIFEST.tsv authoritative)

| name | id | bytes |
|---|---|---:|
| `ds_part00_00` | `1mdAPvrAY39B3eVpqQI2HmgClhoVtJ9wr` | 179200 |
| `ds_part00_01` | `1zE9COX0PznQHz56lfMj0Q_O1VxWv_xdZ` | 179200 |
| `ds_part00_02` | `1l0tQv-7ObAd3je31qrBTydLGPYDFS8A-` | 179200 |
| `ds_part00_03` | `1nwWOThVRPiqiIwjHcDdg9vKJ2o3yjqod` | 179200 |
| `ds_part01_00` | `10lmWj7gWGreUMyWh5hnW6LSFWsOGsHfb` | 179200 |
| `ds_part01_01` | `1fnodTQ2MTcuYtoMSPFWPe0kTlzhhKopx` | 179200 |
| `ds_part01_02` | `1jj42oQ-8su5NsYJy7mmz3_OZ9nSvQWQ9` | 179200 |
| `ds_part01_03` | `1hw5uEfjqgKJSLLiMcCf5-SX2hT7HWWFH` | 179200 |
| `ds_part02_00` | `124TV1OU1-CWlkt1RW5eMpofZ4sdtHOfG` | 179200 |
| `ds_part02_01` | `1KFSs8LSgZTeaU0FRtD-lmu7gLOQA9aJ6` | 179200 |
| `ds_part02_02` | `1mN65okpd3iAHH12h9959C_VTQwK0bn8Y` | 179200 |
| `ds_part02_03` | `1Vqgd7Qe4DZk8356WaQxg_FRsLeHKfTfg` | 179200 |
| `ds_part03_00` | `1-RqRJBzRA34BdJ8m9M9JRsGTAV8UaJ4h` | 179200 |
| `ds_part03_01` | `1p7vT6gU__P5NWreNK9W8IaGxOgo7vUKc` | 179200 |
| `ds_part03_02` | `1IM6_4ir7wtOF7el1ejOhh98jvl2jP8zK` | 179200 |
| `ds_part03_03` | `1qgLhGM6CnM0wvDXu5HmeglQLsnalu4L5` | 179200 |
| `ds_part04_00` | `10Y7F0JPLGllnLVtBwuR0J_GZ7M5FNtpB` | 179200 |
| `ds_part04_01` | `1qKpe0jvsIfTtWD78AyImnS0OEWslPeSR` | 179200 |
| `ds_part04_02` | `1TP8KJ4-jUgeolOmlduntDf56UcUKoPfT` | 179200 |
| `ds_part04_03` | `14jdQFfeIx2OQsa_VUbOWrQvQzTawARdK` | 179200 |
| `ds_part05_00` | `12QcAZU5bzUe2Ako-Z-iMDsb3-KH0aqA9` | 179200 |
| `ds_part05_01` | `1SRabAGHbWYZH4lgT4XFTLfZtoXtxbiQv` | 179200 |
| `ds_part05_02` | `1aKaxZ_zpxJZlRSI76tsiDtmmcOn0-i-m` | 179200 |
| `ds_part05_03` | `1CynF-3pQCbUzT89V05ldSwGXH7WijtQd` | 179200 |
| `ds_part06_00` | `1kKXviPu-yNMcR-VmV7FNVOqvzCbOo63Q` | 179200 |
| `ds_part06_01` | `1fKpBAX4eYb1lRUhdhaN_kujAyzt9jI5w` | 179200 |
| `ds_part06_02` | `16L3_iFOlr3tvTsZiARSEHwNMcE-7_hh2` | 179200 |
| `ds_part06_03` | `1ApDvzxM0SnouiGzhNeEITbkg8NWqUpdD` | 179200 |
| `ds_part07_00` | `1NLw2kzwwHN_w4c6k48ZwU0MvAPmvA3PX` | 179200 |
| `ds_part07_01` | `1l7OEQTIVu5lU7P5cLRqC24IPmIi6CwDO` | 179200 |
| `ds_part07_02` | `1U2QmMrwWmlENHZU35yJK35pabdkMt9HG` | 179200 |
| `ds_part07_03` | `1OxyNSuNNFJg_5v_Uai3XsVEi6L5gzlZ3` | 179200 |
| `ds_part08_00` | `1VnxNr9TrgG18_Prm7DpIkdW6vfwBqUb7` | 179200 |
| `ds_part08_01` | `1l2DY-AGTtFPH-cA_qBYRLxyFUOokDsno` | 179200 |
| `ds_part08_02` | `1XnoDcAc90geW2nRfEt2spEd26Fy6Ja4q` | 179200 |
| `ds_part08_03` | `1f0gCgtcjz1G-S4fCULMKSXErApazRIwg` | 179200 |
| `ds_part09_00` | `1wJktsxtVEa-4ZbeNGRlAHisTr4fMg8n5` | 179200 |
| `ds_part09_01` | `1IWOlT-ym5pA3UitU3S-5l_p1UpcVX-KV` | 179200 |
| `ds_part09_02` | `12YVaZc5dOx8OhduvmL65CIRKV9hN_Eie` | 179200 |
| `ds_part09_03` | `1LAEri-z20seAFafpqRlO9X-NzZc2_7Fl` | 179200 |
| `ds_part10_00` | `10L2Xd_-pHOqmwRWMoQv7XPir5-jx-xT4` | 179200 |
| `ds_part10_01` | `1nFMVLfL1iysyydzHJvPTrGMGOBA-5Mvm` | 179200 |
| `ds_part10_02` | `1WwNW3WmxgpuIp_7BRErvQHsrH6LEvOE_` | 179200 |
| `ds_part10_03` | `1kTalUUoi6i0hCZN_JiCGCmvWlEmtVzXM` | 179200 |
| `ds_part11_00` | `199iD4PnwdJx5ESpfQSSK0qfkNhV3qkLZ` | 179200 |
| `ds_part11_01` | `1Wm_Onevfex-noUNlueev6IiTCRuxk3LT` | 179200 |
| `ds_part11_02` | `1VothWqB0AkgjHO5aa76KziHEtEuCxrGF` | 179200 |
| `ds_part11_03` | `18sBpmSnqUAmZvQJQLQaDVLsaYwAr5TKG` | 179200 |
| `ds_part12_00` | `1NOh5GGk9JPV9fLh7vemkMyn9mDxJtH5N` | 179200 |
| `ds_part12_01` | `1oBAhctx7-Bi7t1FEpl_lJ1-89YIgzsLL` | 179200 |
| `ds_part12_02` | `1qHIyCTDr53vA4xjFrvxoxnTMj0dsUJgF` | 179200 |
| `ds_part12_03` | `1XHd5V5U9nJBW0Iosjh6PKAm7GLgC-uwB` | 179200 |
| `ds_part13_00` | `1naHVtF1AWGLcLLHxvgamB1u7-ywMSIup` | 179200 |
| `ds_part13_01` | `1Wg12WSCrb2U7pVSIQbnWP6sUw_LQrweb` | 179200 |
| `ds_part13_02` | `1SzND6Clwmh8gmx3ABKUVjs9NeIHJtNio` | 179200 |
| `ds_part13_03` | `1-czZzoscIKF5HRFeg-ln8RjVVuy9DrbN` | 179200 |
| `ds_part14_00` | `1pJweXwHZvN17DiSVOCZipxcIizrw26vV` | 179200 |
| `ds_part14_01` | `12jh_wFidQXUa57VyTmYtrTt9UeSO1wT-` | 179200 |
| `ds_part14_02` | `1MohYJuBH0yXZA8-ZNKFjK_4BoU5P9DGj` | 179200 |
| `ds_part14_03` | `1Z_Rc1EajBj3_qENcyQp6zbh9X8jbYkOD` | 6087 |
| `ds_SHA256SUMS.txt` | `1nOzU0vF1FLTYiUBctODP7Ud_M4EhXo3g` | 1234 |
| `ds_UPLOAD_SHA256SUMS.txt` | `1YDAbl2BCTrtvWiCi1UW8o0c2yB1Mp7Q4` | 6516 |

### 19.6 ANALYSIS.md post-append sha (sections 12–13 added after 19.3 row)
- ANALYSIS.md bytes=86066 sha256 `eb45ee3b474a2a719da548bc88a89b0a8ff79f18d0e1701b28f13201e14b9f01` (supersedes 87d7994d… row in 19.3 for ANALYSIS only; other 19.3 rows unchanged)
- Map sha before this 19.6 note: `d0f0215adc54f8eefafabe720d2179e1a338a039a0161c661e10bbd50eeda9c3`

## 20. Append 2026-11-09 19:57 EST: small_text_heads content digest [SMALL-TEXT-DIGEST-2026-11-09]

Read-only digest of the 361 sections in `small_text_heads.txt` (first ~40 lines of small text files on Seagate / `_RADIOACTIV` from the Pi 5 drive survey).

### 20.1 Box paths
- Digest: `/workspace/pi5-drive-survey-2026-11-09/SMALL_TEXT_HEADS_DIGEST.md`
- Source heads: `/workspace/pi5-drive-survey-2026-11-09/extracted/drive_survey_2026-11-09/small_text_heads.txt` (already extracted; 523911 bytes)
- Companion sha file: `/workspace/pi5-drive-survey-2026-11-09/SMALL_TEXT_HEADS_DIGEST.sha256`

### 20.2 Digest sha256
- SMALL_TEXT_HEADS_DIGEST.md sha256 `7c8013a28f4159c75f2d7ad0fba872dfa4e8c3acde9787f389fd59188496fc39` ([:16]=`7c8013a28f4159c7`)
- Sections parsed: 361 (Seagate 352, _RADIOACTIV 9)

### 20.3 Theme counts (primary assignment)
- KBLD9 / OCR / CMS1500: 7
- Tim's Tables / Base360: 1
- GOSUB: 8
- Device / edge setup: 31
- Boot / ledger / seals: 37
- Ollama / models / TTT bus: 238
- SVCT general: 32
- Possible credentials (paths only): 6
- Personal / other: 1

### 20.4 Flag results (fail-closed)
- Missing sealed targets (`kbld9_ocr_enhanced_processor`, `test_cms1500_adversarial_v3`, `Tims_Tables_Base360_Full_Reference`, sha `a45a3546` / `8d20c24a`, `446 lines` / `154 lines`): **NOT FOUND** in heads or `small_sha256.tsv`.
- `EDGE_TRANSPORT` / matrix: **NOT FOUND**. Pi/USB/Wi-Fi notes exist (`PI5_USB_PORT_POLICY`, room-presence `Wi-Fi Up [redacted-lan-ip]` / `Pi5: PARKED_UNPLUGGED`, hive USB lifecycle) without SSID/password.
- Seal/manifest sha lists checked (spines, flushed_hashes, pharmacy INDEX, STT seals, UT SHA256): **no** missing-file hash hit.
- Credential-looking paths under `_MAIDEN_BRAIN/03_keys/`: listed by path only in digest; values not copied.

### 20.5 Related (not the hunt targets)
- Sealed present: `svct_spines/deploy/kbld_augmented_ollama.py` + `.SEAL.json` (sha256 `6f94daefe21dac97…`, 30993 bytes).
- Tim's Tables CSV head only: `_MAIDEN_BRAIN/00_inbox/desktop_ops_2026-07-27/TIMsTABLeSeq,DotID,Category,Tier,UtilityGrou.txt` (seq 170+; not Base360 Full Reference).

(Map sha256 before this append: `f9079177bc7d2faae41bd77b4bc66c0a840dc639f85bcd27397f6ff30579f8ae`)

## 21. Append 2026-11-09 20:19:00 EST: wc_part09 trash + CMS-1500 laptop mail check + Tim's Tables Drive list [WC09-CMS-TIMS-2026-11-09]

### 21.1 wc_part09 trash (Timothy approved t829u)
- Name: `wc_part09`
- Drive file_id: `1iKVWHnmK7990CHOnQRNvpM1qdZiS5zpE`
- mime: application/octet-stream
- size_bytes before trash: **0** (empty leftover from work_core_2026-11-09.zip slice upload; real pieces wc_part00–08 rebuilt sha efc3307eb84cf5a9)
- modified_time (UTC): 2026-11-09T20:34:21.544Z (= 2026-11-09 15:34:21 EST)
- Action: trash only via user-Google Drive-xai trash_file (recoverable ~30 days). Not permanent delete.
- Post-trash exact_name search: **0 hits** (trashed excluded). Confirmed gone from active Drive.

### 21.2 Gmail CMS-1500 laptop data (read-only, ~17:00 EST onward 2026-11-09)
- Account: user-Gmail-xai / [redacted-email]
- Queries: CMS1500 / CMS-1500 / "CMS 1500" / claim form after:2026/11/09; has:attachment after:2026/11/09; broader CMS/claim/laptop today
- Result: **NOT FOUND** — no CMS-1500 / claim-form messages or attachments in the last few hours (Gmail may lag; Timothy said he will get laptop data over indirectly).
- Download dir created empty: `/workspace/cms1500-laptop-2026-11-09/` (0 files)
- No reply/send/label/delete performed.

### 21.3 Drive Tim's Tables / Base360 / OEIS spreadsheet inventory (list only; no large downloads)
- `Tims_Tables_Base360_Full_Reference.csv`: exact_name search **NOT FOUND**
- Related Base360 archive present: `tims-tables-base360-derived_2026-09-19.tar.gz` id `1lp47SYL68Zi8GYYBGtasVHFBcnZ_cpR1` 45336 B gzip 2026-09-19T04:48:14.657Z
- Spreadsheet/CSV hits (user-Google Drive-xai; duplicates across folders possible; times UTC→ report EST as needed):
  - Google Sheets formulas: TIMS_TABLES_FORMULAS_2026-10-06 (`1CvIe7eosSckyVXz1mknT6jxZuhmkCVQkJKsbFfdesmY`, 1186 B); TIMS_TABLES_FORMULAS_NEWTON_EINSTEIN_2026-10-06 (`1Yr_gpgt7_4v-A9fGUhFaJHeEa0gHjN15v-v8nw4-lDo`, 1714 B)
  - Category9 sheets: TIMS_TABLES_CATEGORY9_*_2026-10-06 (several; ids 1aCeYSzt…, 1tJ_BsuX…, 1sGjaHHf…, 1lVgb3kr…)
  - xlsx: Tims_Tables_Presentation.xlsx (`1Q3L_yufsZyjnI0sQ85momXBDdGZAyaF2` / twin `1b0mdt7U…`, 6114 B); Tims_Tables_SVCT_Edge_Lookup_v1.xlsx (`1RrPpjEj…` / twin `1bHb2JIG…`, 9022 B); Tims_Tables_2_thirds_ADDED_2026-09-01.xlsx (`1E7Osq8_…` / `1A7LHcsg…`, 8319 B)
  - csv: Tims_Tables_Master_Flat.csv, Tims_Tables_Core_Six_Ratios.csv, Tims_Tables_All_Matrix_e6_Long.csv, Tims_Tables_Presentation_e4/e6.csv, tims_tables_equal_leg.csv, TIMS_TABLES_345_UNIT_SCALE_v1.csv
  - OEIS sheets: OEIS_SIZES_2026-10-11 (`1Y13-Vt2x…`), OEIS_THIN_ROW_2026-10-11 (`1EG9l02p…`); OEIS.md text (`1fnPjsoq…`, 17221 B, modified 2026-11-09T21:19:14.818Z)
- create_tims_tables_xlsx.py present (builder script, not the sealed Full Reference).
- No .ods hits in this pass.

(Map sha256 before this append: `413372a58cabefb587092da1cc8db159561f9eb3f1a564ae707f89c33a9abfc0`)
