# SEAL — KBLD9 core r8a, sealed under THVEA harness v4 (exact boundary oracle)

Sealed: 2026-10-18 13:14:54 EDT (America/New_York), on Timothy H. Norman's order of 2026-10-18 12:56 PM ET ("If r8a gets 16/16: seal r8a").
Condition met: r8a under harness v4 = 16/16 EARNED in 3 of 3 runs (rc 0, VALIDATE OK, identical verdicts).

| Artifact | sha256 |
|---|---|
| core r8a  /workspace/kbld9-r8-2026-10-18/core/kbld9_core_r8a.py | 16934bab2d88a3f7a63a9f16a7c986e296d13dd053c6d441eb05a028545347c6 |
| harness v4  /workspace/kbld9-r8a-seal-2026-10-18/harness/probe_suite_3_thvea_v4.py | 4c20b16f83a3dc283d0119944c360061f563217a0b4d25b464aebbb7a0e865cd |
| sealed suite T1-T4  /workspace/kbld9/probe_suite_3.py | ce0e09f329599dfa511cb036aa9f0c2bbb39d0d84deb46e43c34eb31f4d0096d |
| SHA256SUMS (131 lines)  /workspace/kbld9-r8a-seal-2026-10-18/SHA256SUMS | 427a63428e8b1235b14199a67a68b2131c6e6685239f8543b0ebf285b1e2a6b2 |
| for reference: harness v3 (archived, unchanged) | a656148d2022c9b02698049fee98c63c5e734af06cefb0563acbe196e14c5f38 |
| for reference: core r7 (unchanged, previous production) | 465359bb0339d3acdd1b94282a0d9191fb663b734cd2b552e36baf5e75da31d8 |

Results under v4: r8a 16/16 x3; sealed T1-T4 4/4; r7 13/16 (H4a 12/210, H4b 16/420, H5).
Sanity: 22 audit mutants check level 22/22; audit case-level runner 21/22 (M17, baseline masking, OPEN_GAPS S-G1); r8a-applied 34/34.
Open, not blocking the seal condition: S-G1 (runner masking), S-G2 (skill update needs the parent's UpdateSkill), S-G3 (X12 fence value).
Verify: cd /workspace/kbld9-r8a-seal-2026-10-18 && sha256sum -c SHA256SUMS
