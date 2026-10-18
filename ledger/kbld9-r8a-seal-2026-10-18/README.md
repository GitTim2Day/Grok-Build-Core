# kbld9-r8a-seal-2026-10-18 — KBLD9 core r8a SEALED under THVEA harness v4 (exact boundary oracle)

Ordered by Timothy H. Norman 2026-10-18 12:56 PM ET. Box only. New files only. Not edited: r7 (`465359bb…31d8`), harness v3 (`a656148d…5f38`, archived), the sealed suite (`ce0e09f3…096d`), r8a itself, BOOT.bas, svct_v20*, `/workspace/kbld9/protected/` (not opened). Hashes re-checked before and after: unchanged.

## Headline (measured)
- **Harness v4** `4c20b16f…65cd`: v3 with one logic change — the oracle decides 3/6/9-sigma membership exactly, `|x-med| <= t*mad` on exact values (Fraction == exact Decimal digit strings). No float division, no rounding. Everything else as v3 (logs/diff_v3_v4.patch). v4 oracle vs independent exact Decimal reference: 0/210.
- **r8a under v4: 16/16 EARNED, three runs** (identical verdicts). Sealed T1-T4 4/4.
- **r7 under v4: 13/16** (FAIL H4a 12/210, H4b 16/420, H5 ERROR on [1e308,-1e308,0.0]).
- **Sanity, 22 audit mutants:** check level 22/22 killed; audit case-level runner 21/22 (M17 masked because r7 baseline itself fails H4b under exact math, OPEN_GAPS S-G1); same 22 patterns on r8a + 12 r8-specific: 34/34 killed, each M01-M22 by a v4 case.
- **Seal:** SEAL.md. Skill text for UpdateSkill: SKILL_UPDATE_v4.md (not applied by this agent).

## Files
| Path | What |
|---|---|
| SEAL.md | seal record: r8a, harness v4, sealed suite, SHA256SUMS hashes (written after SHA256SUMS) |
| TEST_RESULTS.txt | every count |
| OPEN_GAPS.md | S-G1..S-G6 |
| SKILL_UPDATE_v4.md | full new kbld9-probe-suite-3 SKILL.md text (Run section only changed) |
| harness/probe_suite_3_thvea_v4.py | harness v4 (LOCAL ONLY) |
| harness/make_v4_from_v3.py | builder v3 -> v4 (hash-checked, anchored, no overwrite) |
| harness/xcheck_v4_oracle.py | v4 oracle vs exact Decimal reference and v3 oracle |
| harness/checklevel_mutants_v4.py, checklevel_driver_v4.py | check-level mutant sanity |
| harness/run_mutants_r8_v4.py | r8 mutant runner pointed at v4 |
| harness/SKILL_v4_NEW.md | the new SKILL.md body alone |
| logs/, results/ | every run log and result JSON |
| SHA256SUMS | sha256 of every file above plus the 4 external artifacts (absolute paths) |

## Shelf policy
GitHub `GitTim2Day/Grok-Build-Core` is PUBLIC: docs and hashes only (README, SEAL, TEST_RESULTS, OPEN_GAPS, SKILL_UPDATE_v4, SHA256SUMS). No `.py`, no results JSON, no core or harness code. Drive: one combined markdown + SHA256SUMS. Email: summary, hashes, links; no attachments.
