"""ingest_gate_ABSENT_STUB.py — shelf stub only.

NOT the live ingest_gate.py.
Live N=10 file absent both chairs 2026-09-16.
Do not treat this as the recovered original.
Recover-not-regenerate standing applies.

Named tenth check: _check_no_float_derived_fraction / FLOAT_DERIVED_FRACTION.
Body not present. Do not infer origin from denom width.
"""
from __future__ import annotations


class IngestGateAbsent(RuntimeError):
    pass


CHECKS_NAMED = [
    "_check_type_tag",
    "_check_no_float_coercion",
    "_check_no_float_derived_fraction",
    "_check_mcu_tag_intact",
    "_check_constant_named",
    "_check_scheme",
    "_check_identity_not_prediction",
    "_check_magnitude",
    "_check_witness",
    "_check_provenance",
]


def check(*_a, **_k):
    raise IngestGateAbsent(
        "live ingest_gate.py N=10 not on this shelf — recover bytes, do not reconstruct"
    )


if __name__ == "__main__":
    print("STUB_ONLY")
    print("N_NAMED", len(CHECKS_NAMED))
    print("ABSENT live body")
