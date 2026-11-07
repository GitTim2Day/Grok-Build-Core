# SESSION PATTERN MAP — 2026-11-07 Build Backup 2026-11-06 Identify & Restore Path

**Stamp:** 2026-11-07T17:53-05:00 America/New_York  
**Sitting:** Backup email screenshot → Drive remainder folder pull → capability confirmation  
**Source:** Grok conversation thread (photo of Yahoo Mail “Build backup 2026-11-06 part 1/3 meta”, then “What changed”, “Pull the Drive”, “What can I accomplish with this”)

## Pattern Match

- Screenshot of Yahoo Mail on ASUS laptop showing self-sent email “Build backup 2026-11-06 part 1/3 meta” (Fri Nov 6 11:40 PM).
- Body is plain-text bundle (Gmail connector could not attach); contains restore notes, checksums, held-back list, and full source of `split_bundle.py`.
- Explicit: changes since 2026-11-05 backup, cutoff 2026-11-06T04:28:00Z; full tarball on private Drive.
- Drive search located folder “Build backup 2026-11-06 remainder” (id 1_oKQYF-CLmr2V2Mix1SaAhS_pCud4HER).
- Contents: 22-part split tarball (total 16,121,828 bytes, SHA-256 7f8643f45c6ca383df0124ff0a23ea8cb2072f083cf0a36bac01e436abc8f003), RESTORE.md, SHA256SUMS, CONTENTS_SHA256SUMS (2842 files), HELD_BACK.tsv, BIG_over5MB.tsv, DRIVE_NAMES.tsv, PARTS_SHA256SUMS, BUNDLE_SHA256SUMS, split_bundle.py, plus blocked-type files (catalog.sqlite, tok.sh).
- RESTORE.md details: incremental + full post-office / crosswalk-fixes / ratio-bas / truncation-corrections / reference-map top-level + 2026-11-06 items (process-ledger, session-map-night, gosub-proposal, MASTER_REFERENCE_MAP.pre-*).
- Held-back: private billing timeline, lock files, old crosswalk copy, prior nightly backup run folder, undated top-level outside scope; 8 large files unchanged since 2026-10-25 left in prior remainder folder.
- Capability: full restore (cat parts → verify → tar → sha256sum -c), individual file recovery via split_bundle.py from email bodies, integrity confirmation, known-good sealed snapshot.

## Map

| Item | Value |
|------|-------|
| Drive folder | Build backup 2026-11-06 remainder |
| Folder ID | 1_oKQYF-CLmr2V2Mix1SaAhS_pCud4HER |
| Tarball size | 16,121,828 bytes |
| Tarball SHA-256 | 7f8643f45c6ca383df0124ff0a23ea8cb2072f083cf0a36bac01e436abc8f003 |
| Parts | 22 (part-00 … part-21) |
| Files in tarball | 2842 |
| Cutoff | 2026-11-06T04:28:00Z |
| Prior backup | 2026-11-05 |
| Key new items | process-ledger-2026-11-06, session-map-2026-11-06-night, gosub-proposal-2026-11-06, MASTER_REFERENCE_MAP.pre-* |

## Audit

- HIT: Drive folder located and listed; RESTORE.md, SHA256SUMS, BIG_over5MB.tsv, DRIVE_NAMES.tsv, HELD_BACK.tsv (partial) read; restore path and held-back rules confirmed.
- VAL: Tarball SHA matches email note; part count and size consistent with 750 KB upload limit; 2842-file claim present in RESTORE.md; private items correctly excluded.
- miss: full CONTENTS_SHA256SUMS not expanded in this sitting; email part 2/3 and 3/3 not fetched; no independent re-extraction test performed here.
- open: none on the identification and capability statement.

## Remap

Sitting produces a verified pointer to the sealed 2026-11-06 Build backup remainder on Drive and the matching email bundles. Restore is cat-parts → sha256 → tar → sha256sum -c; individual recovery via split_bundle.py. Held-back list and large-file pointer are explicit. This is the latest known-good off-box snapshot for that cutoff.

Pointer skill: session-map-2026-11-07-backup-identify  
Sibling of prior backup maps, not a merge.
