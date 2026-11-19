# SESSION_PATTERN_MAP_2026-11-18_CLAIMS_COMPOUNDING_DEA_NPI
**Sealed:** 2026-11-18T23:48-05:00 America/New_York  
**SHA-256:** 09470277ce108475c31e9adfc8312da7812dc8eea56f2e47e0ca7914ee523839  
**UTC:** 2026-11-19T04:48:27Z  

## Session arc
Started from X12 external code lists and CMS-1500 / 837P structure. Extended through profession flags (physician → NP/PA → pharmacist), DEA vs non-controlled legend, NPI/DEA registrant reference, Neuralink/clinical-trial Part A vs Part B distinction, then compounding product identification (J7999 + narrative vs NCPDP ingredient NDCs) and the partial workaround of listed bases (PCCA/Medisca).

## Pattern match (first pass)
- One professional-claim skeleton (CMS-1500 / 837P) covers physicians, specialists, NPs, PAs, pharmacists when payer recognizes the service.
- Identity: NPI + taxonomy on every claim; DEA (individual + facility) only when Schedule II–V present.
- Remittance and classification: dated external code lists (CARC, RARC, Claim Status, Service Type, NDC, HCPCS Level II).
- Research/trial lines: Z00.6 + Q0/Q1 + IDE category route to Part A, Part B, or neither.
- Compounding: finished product has no NDC; medical benefit uses unclassified HCPCS (J7999 primary) + narrative; pharmacy benefit (NCPDP) requires ingredient-level NDCs when they exist.
- Listed bases (PCCA labeler 51927 and similar) convert the vehicle into a billable NDC, partially restoring pharmacy-claim viability while leaving full patient-specific excipient exclusion outside normal workflow.
- Rebate data: NDC utilization flows to state Medicaid so manufacturers can be invoiced; not paid to pharmacy or office.

## Audit
- Sources: official CMS/X12/NUCC/FDA pages, MAC billing guides, 21 CFR 1301, HIPAA NPI rules, Neuralink trial pages, AMA Category III announcement (effective 2027-01-01).
- No structural claim-form change required for any of the above; flags and narrative fields already exist.
- Gaps left open: CPT (AMA-licensed) and ICD-10-CM full sets not pulled; state-by-state pharmacist protocol matrix not built; live NDC directory not mirrored.
- DEA/NPI reference sealed earlier this sitting (SHA bd9162ee…).
- Time stamps verified America/New_York throughout.

## Remap (second pass)
The durable objects are:
1. Shared professional-claim skeleton with profession/taxonomy flags.
2. DEA gate applied only to controlled-substance lines.
3. Clinical-trial markers that distinguish routine care from investigational.
4. Compounding path: J7999 (or equivalent) + narrative on medical claims; ingredient NDC list on pharmacy claims.
5. Registrant reference (who must hold DEA, who must hold NPI).
6. Explicit note that listed bases are a partial billing workaround, not a restoration of fully custom vehicles.

These sit on the existing indexes (X12 ECLs, NDC, HCPCS Level II, taxonomy) without requiring new code-list formats.

## Pointers
- Prior artifacts this sitting: DEA_and_NPI_Required_Entities_2026-11-18.csv / .md
- Sibling of earlier claims-reference indexes, not a merge.

## Open
- Full CPT/ICD-10 ingest only if later named.
- State pharmacist prescribing matrix only if later named.
