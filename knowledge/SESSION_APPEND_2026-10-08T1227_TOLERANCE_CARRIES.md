# Append — tolerance carries its own record

Stamp: 2026-10-08T12:27-04:00
Parent map 75a332389ef4a4c2bbdff5dff5b490f77d859160cdcb7af3d336ffe1185dbf99 ledger 1a11c4db08df1156
12:18 sibling ledger 1a11c4f6421c5466
12:19 seat ledger 1a11c50f0b1e2ffe
Audit ledger 1a11c5502fd792f1 SHA-256 5bed7c583ecf5cd8bb28f7528996b1ad7e4c986700240933068bf6c708056c22 size 2623
Append only. None of those overwritten. Not a merge.
Mask first. No identity claim. No engine.

## Added

A tolerance is not a bare number. It carries units, modality, and provenance.
A numerical tolerance from one modality does not apply to another structure or another imaging method.
A photograph pixel tolerance does not apply to a dental radiograph.

NOT_EXECUTED is the name of the execution status already required. It is not a fifth comparison result.

Order:
1. Prerequisites. Both observations present. Units compatible. Geometry comparable, or a declared registration present. Declared tolerance applicable to this measurement and this modality.
2. Execution status. Prerequisite fails, or tolerance missing or inapplicable: NOT_EXECUTED, with a reason code. Nothing was compared.
3. Result, only if executed: MATCH, MISMATCH, INDETERMINATE, NOT OBSERVABLE.

Reason codes are a closed list. Free text is not a reason.
Named now, not expanded: NO_TOLERANCE, TOLERANCE_INAPPLICABLE, UNIT_MISMATCH, NO_REGISTRATION, OBSERVATION_ABSENT.
NOT OBSERVABLE remains a result: the source was examined and the structure is not in it.
OBSERVATION_ABSENT is NOT_EXECUTED: there is no second observation record to compare.

No confidence percentage. No fusion engine. No comparison routine run.
