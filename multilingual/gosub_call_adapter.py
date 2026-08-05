#!/usr/bin/env python3
"""gosub_call_adapter.py — Third subroutine: bounded call + Tim's base addressing."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple, Any
import time
from gosub_select_adapter import AdapterChoice, EngineKind, TaskKind
from tims_base_map import GOSUB_MAP_BINARY_INDEX, GOSUB_RANK_BASES

DEFAULT_TIMEOUT_MS = 8000
DEFAULT_MEMORY_MB = 512
PREFERRED_BASE = 12
INVARIANT_BASE = 8

@dataclass(frozen=True)
class CallResult:
    ok: bool
    engine: EngineKind
    task: TaskKind
    output: Optional[Any]
    elapsed_ms: int
    reason: str
    base_used: int
    address_digits: Optional[Tuple[int, ...]]

def GOSUB_CHECK_BUDGET(timeout_ms=DEFAULT_TIMEOUT_MS, memory_mb=DEFAULT_MEMORY_MB):
    if timeout_ms <= 0 or timeout_ms > 60000: return False, "timeout_out_of_range"
    if memory_mb <= 0 or memory_mb > 4096: return False, "memory_out_of_range"
    return True, "budget_ok"

def GOSUB_CALL_ADAPTER(choice, payload, timeout_ms=DEFAULT_TIMEOUT_MS, memory_mb=DEFAULT_MEMORY_MB, use_base=PREFERRED_BASE, address_index=None):
    t0 = time.monotonic()
    if choice.engine == EngineKind.NONE or not choice.standing_ok:
        return CallResult(False, choice.engine, choice.task, None, int((time.monotonic()-t0)*1000), choice.reason or "engine_none_or_blocked", use_base, None)
    ok_b, reason_b = GOSUB_CHECK_BUDGET(timeout_ms, memory_mb)
    if not ok_b:
        return CallResult(False, choice.engine, choice.task, None, int((time.monotonic()-t0)*1000), reason_b, use_base, None)
    digits = GOSUB_MAP_BINARY_INDEX(address_index, 8, use_base) if address_index is not None else None
    return CallResult(False, choice.engine, choice.task, None, int((time.monotonic()-t0)*1000), f"binary_not_bound:{choice.engine.value}:base{use_base}", use_base, digits)

if __name__ == "__main__":
    from fractions import Fraction
    from gosub_exact_decide import GOSUB_EXACT_DECIDE
    from gosub_select_adapter import GOSUB_SELECT_ADAPTER
    dec = GOSUB_EXACT_DECIDE({"es": Fraction(3), "fr": Fraction(1,10)})
    choice = GOSUB_SELECT_ADAPTER(dec, TaskKind.MT, "en")
    r = GOSUB_CALL_ADAPTER(choice, "hola mundo", address_index=0b10110110)
    print(r.reason, r.address_digits)
