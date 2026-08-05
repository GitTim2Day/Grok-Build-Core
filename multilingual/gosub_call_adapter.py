#!/usr/bin/env python3
"""gosub_call_adapter.py — Third subroutine complete binding layer. Detect / budget / Tim base / sealed refuse."""
from __future__ import annotations
import hashlib, os, shutil, subprocess, time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple
from gosub_select_adapter import AdapterChoice, EngineKind, TaskKind
from tims_base_map import GOSUB_MAP_BINARY_INDEX

DEFAULT_TIMEOUT_MS, DEFAULT_MEMORY_MB, PREFERRED_BASE, INVARIANT_BASE = 8000, 512, 12, 8
ENGINE_CANDIDATES = {
    EngineKind.WHISPER_CPP_LITE: ("whisper-cli", "whisper", "main", "whisper.cpp"),
    EngineKind.WHISPER_CPP: ("whisper-cli", "whisper", "main", "whisper.cpp"),
    EngineKind.VOSK: ("vosk",),
    EngineKind.PIPER: ("piper", "piper-tts"),
    EngineKind.BERGAMOT: ("bergamot", "bergamot-translator"),
    EngineKind.APERTIUM: ("apertium",),
}

@dataclass(frozen=True)
class CallResult:
    ok: bool; engine: EngineKind; task: TaskKind; output: Optional[Any]; elapsed_ms: int
    reason: str; base_used: int; address_digits: Optional[Tuple[int, ...]]; binary_path: Optional[str]; content_hash: str

def GOSUB_CHECK_BUDGET(timeout_ms=DEFAULT_TIMEOUT_MS, memory_mb=DEFAULT_MEMORY_MB):
    if timeout_ms <= 0 or timeout_ms > 60000: return False, "timeout_out_of_range"
    if memory_mb <= 0 or memory_mb > 4096: return False, "memory_out_of_range"
    return True, "budget_ok"

def GOSUB_DETECT_BINARY(engine):
    for name in ENGINE_CANDIDATES.get(engine, ()):
        p = shutil.which(name)
        if p: return p
    return None

def GOSUB_SEAL_RESULT(ok, engine, task, output, elapsed_ms, reason, base_used, address_digits, binary_path):
    payload = f"{ok}|{engine.value}|{task.value}|{output}|{elapsed_ms}|{reason}|{base_used}|{address_digits}|{binary_path}"
    return CallResult(ok, engine, task, output, elapsed_ms, reason, base_used, address_digits, binary_path, hashlib.sha256(payload.encode()).hexdigest()[:16])

def GOSUB_CALL_ADAPTER(choice, payload, timeout_ms=DEFAULT_TIMEOUT_MS, memory_mb=DEFAULT_MEMORY_MB, use_base=PREFERRED_BASE, address_index=None):
    t0 = time.monotonic()
    elapsed = lambda: int((time.monotonic() - t0) * 1000)
    digits = GOSUB_MAP_BINARY_INDEX(address_index, 8, use_base) if address_index is not None else None
    if choice.engine == EngineKind.NONE or not choice.standing_ok:
        return GOSUB_SEAL_RESULT(False, choice.engine, choice.task, None, elapsed(), choice.reason or "engine_none_or_blocked", use_base, digits, None)
    ok_b, reason_b = GOSUB_CHECK_BUDGET(timeout_ms, memory_mb)
    if not ok_b:
        return GOSUB_SEAL_RESULT(False, choice.engine, choice.task, None, elapsed(), reason_b, use_base, digits, None)
    binary = GOSUB_DETECT_BINARY(choice.engine)
    if binary is None:
        return GOSUB_SEAL_RESULT(False, choice.engine, choice.task, None, elapsed(), f"binary_absent:{choice.engine.value}", use_base, digits, None)
    return GOSUB_SEAL_RESULT(False, choice.engine, choice.task, None, elapsed(), f"binary_present_but_model_or_input_required:{choice.engine.value}", use_base, digits, binary)

def GOSUB_PROBE_ALL():
    return {e.value: GOSUB_DETECT_BINARY(e) for e in EngineKind if e != EngineKind.NONE}

if __name__ == "__main__":
    for k, v in GOSUB_PROBE_ALL().items():
        print(k, v or "ABSENT")
