# Freeze — comparison protocol locked, still appendable

Stamp: 2026-10-08T12:33-04:00
Owner: Timothy. He named the freeze. Append only. Nothing prior overwritten.
Mask first. No identity claim. No engine. No comparison run.

## What is frozen

The protocol specification is closed for this scope until Timothy supersedes it in writing.
Frozen means no new result state, no new reason code, and no confidence percentage.
Appendable means a later correction is a new record. It does not edit these bodies.

## Chain retained

| Record | Ledger | Role |
| --- | --- | --- |
| 12:16 parent | 1a11c4db08df1156 | Map. SHA-256 75a332389ef4a4c2bbdff5dff5b490f77d859160cdcb7af3d336ffe1185dbf99 |
| 12:18 sibling | 1a11c4f6421c5466 | First accumulation append. Mailed size 2547 |
| 12:19 sibling | 1a11c50f0b1e2ffe | Corrected sibling. SHA-256 c46455c066fa6dcdeedebc0396f1b4c1cec72d3260caf6445b5de57fc9098ea6 size 2426 |
| 12:24 audit | 1a11c5502fd792f1 | Custody. SHA-256 5bed7c583ecf5cd8bb28f7528996b1ad7e4c986700240933068bf6c708056c22 size 2623 |
| 12:27 append | 1a11c581ce0e7db7 | Tolerance carries. SHA-256 cea5435fe4e2be6dd3437f1ae181495ee8d600d93b480ff0c3f7b643ae8ebe73 size 1654 |

## Three layers, kept separate

Evidence: what was observed and recorded.
Execution eligibility: whether a comparison may run.
Comparison result: what an executed comparison establishes.

A tolerance is an evidence record. It carries units, modality, and provenance. A bare number is not a tolerance.

Order: prerequisites, then execution status, then result only if executed.
NOT_EXECUTED is an execution status, not a fifth result.
Results remain MATCH, MISMATCH, INDETERMINATE, NOT OBSERVABLE.

Closed reason codes, not expanded: NO_TOLERANCE, TOLERANCE_INAPPLICABLE, UNIT_MISMATCH, NO_REGISTRATION, OBSERVATION_ABSENT.
An examined source whose structure is not visible is NOT OBSERVABLE. The record exists. It is not OBSERVATION_ABSENT.

## Not in the freeze

No fusion engine. No comparison routine. No identity probability.
The next work, only if named, is a test that a minimal routine follows these rules. The rules are not changed to fit the code.
