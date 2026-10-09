# KBLD9 / SVCT / UDN minimal Python reference

October 8, 2026. Source requirements: the OPERATOR's supplied continuation handoff.
This is a new isolated milestone prototype, not an edit of an existing KBLD9 release.

## Run

Requires Python 3.10 or later; no third-party packages.

    python3 -m unittest discover -s kbld9_udn_reference -v
    python3 kbld9_udn_reference/reference.py > audit.jsonl

The sample processes 9 records: permanent OPERATOR root, two provisional
contributors, two simulated identity events, one authorization, one exact
result, one unauthorized rejection, and convergence. The exact calculation
is (2/3)*(3/2)^2 + (-1/4) = 5/4.

## Demonstrated

- Stable OPERATOR and CONTRIBUTOR_1 / CONTRIBUTOR_2 identifiers.
- Immutable event snapshots, appended identity evidence, multiple parents.
- Authorization bound to the complete request digest, actor and validity window.
- Explicit exact path and allowlisted POLYNOMIAL routine, with strict rational validation.
- Exact recomputation before accepting the result.
- SHA-256 parent references and separate sequential audit linkage.
- Deterministic canonical JSON bytes and graph replay.
- HMAC authentication using public demonstration keys.
- Unauthorized and unavailable execution paths produce rejection records.

## Boundaries and remaining work

This is not the complete KBLD9 filter or the 64-cell SVCT representation.
The input validator is a small boundary stub. UDN has one exact routine and
explicit rejection for unsupported paths; numerical and AI paths are not implemented.
External transport is unavailable even if a request is authorized.

Identity verification is simulated. No voice or facial recognition occurs.
The demonstration keys are public and provide no deployment security.
HMAC provides shared-key authentication, not digital signatures or independent
proof of which shared-key holder acted. Key enrollment, custody, revocation,
passkeys and signed authorizations remain unimplemented.

Authorization here represents an authenticated participant permitting their
own exact request; a production policy for operator grants and delegation has
not been defined. It must be explicit before expansion.

Events are immutable through the public interface but held in process memory.
Export produces a snapshot, not durable append-only enforcement. Crash recovery,
concurrent writers, fsync and protected storage are not implemented. A trusted
external final hash is required to detect truncated tails. Recomputing hashes
cannot establish authenticity without trusted credentials and checkpoints.
Replay verifies graph structure and authentication; it is not a second independent
semantic policy engine. Logical ticks demonstrate validity intervals, not trusted
wall-clock timestamps. Resource exhaustion limits beyond the exponent bound
are not implemented.

C++ implementation, shared cross-language vectors and byte parity remain pending.
No Raspberry Pi, Jetson or A15 execution or performance benchmark was performed.

## Frozen evidence-comparison protocol

Separate and unchanged: MATCH, MISMATCH, INDETERMINATE, NOT OBSERVABLE.
NOT_EXECUTED remains an execution status.
Reason codes remain NO_TOLERANCE, TOLERANCE_INAPPLICABLE, UNIT_MISMATCH,
NO_REGISTRATION, OBSERVATION_ABSENT.
Prototype execution diagnostics are separate and never comparison reason codes.

The canonical event format is a prototype detail, not a frozen new protocol.
Established architectural decisions remain those of the supplied handoff.
