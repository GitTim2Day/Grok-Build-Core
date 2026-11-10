# PATTERN_MAP_v3 — 2026-11-09 drives · hunt · Base360 (Research seat)

Built 2026-11-09 20:45 EST (file mtime; 2026-11-10T01:45Z) as v2 + pass-2 fixes D17-D19 (AUDIT_pass2.md). Sources: EVIDENCE.md (E1-E69, T1-T20, M1-M7, A1-A10) + EVIDENCE_ADDENDUM_pass1.md (E70-E83), with AUDIT.md fixes D1-D16. v1 left unchanged. Principles P1-P8 from E59 (full sha checked). Only T items are Timothy's claims; M = memory summaries; A = assistant claims.

## Patterns (10)

### PAT-1 Fail-closed hunt: the three sealed bodies are still missing — P5, P3
- Sealed claims: OCR 446 lines `a45a3546…`, v3 154 lines `8d20c24a…` (E31); Base360 Full Reference claim-only (E60, E61).
- Searched: 428 + 28 share pages, Gmail, Outlook, AgentMail, both drives (E20, E8 §5/§12, E10 flag 1); Yahoo stopped, no connector (E30).
- Near copies only: airlock OCR 520 lines `426879847a0b4a3c` in 3 identical places (E22, E23, E62; L2); airlock set 10/10 OK (E24, E25); v1/v2 tests (E27, E28).
- Unchanged by audit.

### PAT-2 Chunked transfer + hash rebuild — P3, P4, P6
- Drive survey: Pi zip 10578887 B → 15 parents (14 × 716800 + 543687) → 60 slices of 179200 B (last 6087) → Drive → box rebuild, sha `734011d832990e5b` MATCH (E4, E6, E7; L3).
- **Fixed (D1):** Drive holds **62** survey files (60 slices + 2 sum files), not 61 (E5). No parent piece was uploaded.
- Survey contents checked: E11 (361 sections), E12, E13, E14, E15 (0 read errors); digest E10.
- Lock-loop bundle: 48/48 array hashes (E16, E19; L12).
- Drive pieces still present per E1 §19.2 (E68, live UNVERIFIED).

### PAT-3 Truncate, never round; no stored zero; no ±∞ — P4, P1
- Tim's Tables multi builder (Timothy asked for Sheets/ODS, T12): 0.707106 not 0.707107 (E45); UNDEFINED for 0/∞; 8^(1/4) = 1.681792, original hard-coded 2 (E42 line 172, E46, A5 ✓).
- **Fixed (D2):** the original wrote 0-like values in 13 cells and ∞ in 4 (17), not "216 cells" (A2). 216 = all data-sheet diffs vs original (E44, E47; L8).
- Lock-loop: exact ratios, offset 1/4, mag + dir, zero → L_p rule, none found (E17, E18).
- Survey GiB truncated 398 / 18 (E12, E13).

### PAT-4 Base360 geometry chain — P1, P4, P3
- Timothy verbatim: 1:1:√2 and 1:1:2, "Two different ways of saying it" (T1); waves "behave in a manner similar to that, don't they?" (T2, a question the assistant affirmed, A8 ✓); "That's the connection at Tim's tables" (T3); SVCT voxel → 360 squared, "maps of a globe and navigation" (T4, A7 ✓); spherical voxel flattened into a circle = token (T5); full provenance on reconstruction (T6); rules like the four → ten pillars; "you anchor the original timestamp" (T7).
- Memory summaries only (D12): star at top, R=1, four 90° triangles, hemisphere isosceles, two stacked = square (M1, M2, M3).
- **Fixed (D10):** the permanent anchor form is Zulu (M6): 8:10 PM EST = 2026-11-10T01:10Z (minute only); A3 gave ET only.
- Physics pointers shelf for related maps: E77.

### PAT-5 Lead vs anchor (gel vs permanent) — P5, P3
- Timothy: unanchored SVCs generate matching content / data / timestamps / context (T8, his word "SVCs" kept, D13); "to lead, it's an imagination … creative imagination … work on a edge device" (T9); gel SVCT thought style (T18). Memory entry M4; five-pillar gel/permanent rule M7.
- 60 / 61 observation (T17) stays an **UNANCHORED LEAD**. The 60 = 15 parents × 4 slices from the 179200-byte gateway limit (E6, A9 ✓). **Fixed (D1):** the "61 files on Drive" support (A1) was wrong; the real Drive count is 62 (L14).
- Airlock 520-line OCR is a near copy, never the seal (E22, E23).

### PAT-6 Edge-first placeholders, not builds — P6, P8, P2
- Sensor / COMM / HIVE list: 54 slots, all PLACEHOLDER, 9 UNDEF, pulse/EKG/EEG non-diagnostic + isolation (E48-E51; T13, T14, T15; A10 ✓).
- Transport order SUGGESTED, not locked; Cellular rank UNDEF (E52; L5). GPIO sources E53, E54 (L6).
- Memory/RAM overflow to Seagate, _RADIOACTIV, microSD; drives read-only until Timothy OKs a writable mount (M5, memory summary).
- Device side: earlier-today CLI-devices map (E58), device menu (E75; A15 brand unconfirmed, D17), Pi update sheet (E76).
- Camera within a foot; OCR step above 1080p, target UNDEF (T11, A6 advice, D14). Pi-stdlib formats for Tim's Tables (E40).

### PAT-7 Append-only maps, twins and checksums — P3
- Retrieval map appended §18-21 with before-shas (E1, E64; L9). **Recorded (D6):** live E1 sha `eb048c78fce6f977`.
- **Open (D3):** E2 .txt twin and E83 GitHub-stage copy lag (no §18-21).
- **Recorded (D4, D5, D16):** E21 fails on the appended HUNT_REPORT; E9 ANALYSIS row superseded; E65 sums are root-relative.
- **Recorded (D7):** ledger lines 21/24/25 point at files that grew; line 25 versions are exact prefixes (E55, E56, E57, E74; L10).
- Earlier maps today: E56, E57, E58. Boot archive index 32/32 OK (E80, E81); consolidation log (E82).
- Caveat: restore mtimes (E69). This cycle was requested in T20.

### PAT-8 Timothy-gated actions — P5, P2
- wc_part09 trashed on his words "Naturally, we need to trash the WC underscore part oh nine" (T11; E1 §21.1; E67 live UNVERIFIED).
- "Word. Save it." → 8 memory items (T19, A10). Project save of today's work still awaits his OK (E40 "Not done").
- **Fixed (D11):** keeping the ds_part pieces is the assistant's advice (A4) to his question (T16), pending his OK, not his decision (E68).
- Yahoo one-time exception used read-only and stopped (E30).

### PAT-9 Official sources only (CMS-1500) — P5, P7, P3
- cms.gov / nucc.org / payer PDFs, 110/110 OK; field map 61, payer 17, PA 57 rows, UNDEF where the source is silent (E35-E39).
- Airlock throwaway tests: v1 5 PASS / 1 FAIL then crash at line 808; v2 14 PASS / 1 FAIL on T9 (E26-E29, E32-E34).
- Laptop CMS-1500 data not yet in Gmail (E66, T11).

### PAT-10 Mail watch / post-office rhythm — P5, P3 (new in v2)
- Post-office runs 18:09 light, 19:07 full, 20:05 light: no urgent, no billing charge (E70, E71, E63). Gmail writes: none at 18:09 and 20:05; one Code label on 1a1c0d631f365c6e at 19:07 (**fixed, D18**). Message pulls (E73, E79).
- Billing-timeline entry (written 17:06:47 EST by an earlier run, D19) is a support reply with no charge (E72) → no billing stop.
- Morning inbox zip is an X data export containing auth/billing JSON names; not opened this pass (E78).

## Checked vs UNVERIFIED
- **Checked on disk this pass:** E1-E66, E69-E83 hashes; all folder manifests listed in AUDIT §A; survey totals; digest counts; lock-loop 48/48; test outputs; Tim's Tables values; sensor counts; ledger attachments; retrieval-map sha chain; P1-P8 source sha.
- **UNVERIFIED:** live Drive state (E67, E68, Drive ids in E40/E1 §21.3) — not re-queried; ledger lines 21 and 24 prefix status (D7); Timothy verbatim before t819u (M1-M7 are summaries); exact second of the 8:10 PM anchor; OCR "next step up" target; OEIS "three or four thousand" formulas (Timothy's count, T11, not recounted); the three sealed bodies (NOT FOUND).

## Nothing from v1 dropped
Every item cited in v1 and v2 is cited here (checked by script in AUDIT_pass2.md and AUDIT_pass3.md), plus the 41 pass-1 recoveries in DROPPED.tsv.

## Executable SVCT map (IF-THEN / GOSUB routes for a future seat)
Each route: read the file, apply the check, RETURN with OK / MISMATCH / UNVERIFIED. Never open kbld9/protected, BOOT.bas or svct_v20*.

```
10 REM PAT-1 sealed bodies
20 IF asked for OCR 446 / v3 154 / Base360 Full Reference THEN GOSUB 1000
1000 READ E31 (jul9_seals_raw.txt) -> take full sha a45a3546… / 8d20c24a…
1010 SEARCH box + drives lists E12,E13 + E20 table by exact name
1020 IF found AND full sha == seal THEN label SEALED ELSE label NEAR or NOT FOUND (E22 = NEAR, never SEALED)
1030 RETURN

30 REM PAT-2 chunk rebuild
40 IF a zip arrives in pieces THEN GOSUB 2000
2000 READ piece MANIFEST (E5 style) + Pi sums (E6/E7)
2010 sha256 each slice; cat in name order per parent; sha256 parent; cat parents; sha256 zip
2020 IF any mismatch THEN stop, report the piece name ELSE unzip -t, record count = rows in MANIFEST (not memory)
2030 RETURN

50 REM PAT-3 exact values
60 IF writing any table value THEN GOSUB 3000
3000 keep ratio as value; render by string-cut (truncate) with >= 2 extra digits computed
3010 IF value would be 0 or ±inf THEN write UNDEFINED (or L_p marker per E17) ; sign -> Direction column
3020 cross-check formats (E44 style): diffs must be 0
3030 RETURN

70 REM PAT-4 Base360 rules
80 IF a Base360 / token / globe question THEN GOSUB 4000
4000 READ T1-T7 (verbatim) first, M1-M3 second (summary; say so)
4010 one right triangle -> all four sections; 1:1:√2 <-> 1:1:2; 360x360 contacts; flatten = token with rule name+version, radius bounds, truncation depth, original sha256
4020 anchor = original timestamp in Zulu (M6), ET display only
4030 RETURN

90 REM PAT-5 lead vs anchor
100 IF a match is found without an anchor THEN GOSUB 5000
5000 label UNANCHORED LEAD (gel); keep it
5010 IF original timestamp AND full hash AND disk count all check THEN promote to permanent ELSE stay lead
5020 RETURN

110 REM PAT-6 edge placeholders
120 IF a sensor / comm / hive item is named THEN GOSUB 6000
6000 READ E49 (TSV); IF slot exists THEN cite slot_id ELSE add row status PLACEHOLDER, match UNDEF unless an earned source (E52-E54) names it
6010 medical signals: non-diagnostic, isolation required; no install / pairing without Timothy
6020 RETURN

130 REM PAT-7 append-only maps
140 IF updating a map THEN GOSUB 7000
7000 sha256 before; append section; sha256 after; write both; never edit above
7010 IF a twin (.txt / gh_stage / Drive) exists THEN mark it stale until re-copied (D3)
7020 IF a sums file predates an append THEN leave it; record the new hash in the new map (done-check rule 8)
7030 RETURN

150 REM PAT-8 gated actions
160 IF action = trash / save-to-project / send / writable mount THEN GOSUB 8000
8000 find Timothy's verbatim go (T-class) for that exact action; assistant advice (A-class) is not a go
8010 IF none THEN draft + stop ELSE act once, then verify (search count after)
8020 RETURN

170 REM PAT-9 official sources
180 IF CMS-1500 field / payer / PA rule needed THEN GOSUB 9000
9000 READ E37/E38/E39; IF cell UNDEF THEN answer UNDEF (no guess); cite E36 sha for the PDF
9010 tests: run v2 (E28) on extractor E26; expect T9 FAIL until fixed; any v3 rebuild = NEW label unless sha == 8d20c24a…
9020 RETURN

190 REM PAT-10 mail watch
200 IF post-office run THEN GOSUB 9500
9500 read newest RUN_NOTE; IF billing line has an amount or charge THEN STOP and ask Timothy ELSE log only
9510 RETURN
```

## Open items
1. Three sealed bodies still missing (PAT-1); Yahoo Sent around Jul 9 only by Timothy's own hand.
2. CMS-1500 v3 rebuild label rule + T9 taint fix (PAT-9); laptop CMS-1500 data (E66).
3. Project save of today's work (survey, map §18-21, CMS-1500 set, Base360 rules, Tim's Tables builder, placeholder list, this map) awaits Timothy's OK (PAT-8).
4. ds_part pieces: keep or trash after the save — needs Timothy's word (D11).
5. Re-copy E2 .txt twin and the GitHub/Drive copies of the retrieval map after the save (D3).
6. Wi-Fi link not locked (PAT-6); OCR step above 1080p + camera stand (T11, D14).
7. A15 brand: ASUS in E1 §18 and memory vs "Timothy said Acer" in E75 — unconfirmed, ask Timothy (D17).
8. 60/61 lead stays unanchored (PAT-5).
