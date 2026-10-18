# OPEN_GAPS — kbld9 r8a seal under harness v4 (2026-10-18 ET). Measured only.

| ID | Gap | Evidence | Needs |
|---|---|---|---|
| S-G1 | The audit runner's case-level rule, with the r7 baseline, counts M17 as SURVIVED under v4 (21/22). | r7 itself fails H4b under v4 (16 checks), so M17's 48 H4b failures fall in a case the baseline already fails. Check level 22/22 (M17 +32 checks). The r8a-applied M17 is killed by v4 H4b (34/34). | Timothy: accept check level + r8a baseline as the sanity measure (done here), or ask for a new runner. |
| S-G2 | Skill not updated by this agent. | The UpdateSkill tool is not available to the executor. The full new text is in SKILL_UPDATE_v4.md (existing skill read first, sha c56740f4…a479; only the Run section replaced). | The parent calls UpdateSkill with that text. |
| S-G3 | X12 still fails (r8 R8-G1b): the snapped fence value is r7's float `med + 9.0*mad`, up to 4.663E-15 outside the exact fence. | r8 extra cases on r8a 19/20. v4 does not test this (same compare() as v3, tolerance 1e-9). | Timothy: keep r7 fence value or clamp. |
| S-G4 | v4 oracle with non-finite mad now fails closed (ORACLE UNDEFINED) where v3 classified CLEAN. | No v4 input reaches it (mad finite on every case). | — |
| S-G5 | T4 is box-only (174.3-188.9 ms). No Pi 5 number. | | Pi 5 run by Timothy. |
| S-G6 | Carried over unchanged: r8 R8-G2..G9 and audit G3-G10. | /workspace/kbld9-r8-2026-10-18/OPEN_GAPS.md | — |
