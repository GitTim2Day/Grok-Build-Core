#!/usr/bin/env python3
"""
gosub_select_adapter.py — Second shared subroutine (hardened)
Runs AFTER GOSUB_EXACT_DECIDE.
Finite offline capability tables: Whisper.cpp lite/full, Vosk, Piper, Bergamot, Apertium.
Version Clean. Finite. Musical. No infinity. No Zero's.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional, FrozenSet, Tuple
from gosub_exact_decide import ExactDecision, Standing, Verdict

class TaskKind(str, Enum):
    STT = "STT"
    TTS = "TTS"
    MT  = "MT"

class EngineKind(str, Enum):
    NONE = "NONE"
    WHISPER_CPP_LITE = "WHISPER_CPP_LITE"
    WHISPER_CPP = "WHISPER_CPP"
    VOSK = "VOSK"
    PIPER = "PIPER"
    BERGAMOT = "BERGAMOT"
    APERTIUM = "APERTIUM"

WHISPER_CPP_LANGS = frozenset({"en","zh","de","es","ru","ko","fr","ja","pt","tr","pl","ca","nl","ar","sv","it","id","hi","fi","vi","he","uk","el","ms","cs","ro","da","hu","ta","no","th","ur","hr","bg","lt","la","mi","ml","cy","sk","te","fa","lv","bn","sr","az","sl","kn","et","mk","br","eu","is","hy","ne","mn","bs","kk","sq","sw","gl","mr","pa","si","km","sn","yo","so","af","oc","ka","be","tg","sd","gu","am","yi","lo","uz","fo","ht","ps","tk","nn","mt","sa","lb","my","bo","tl","mg","as","tt","haw","ln","ha","ba","jw","su"})
WHISPER_CPP_LITE_EN = frozenset({"en"})
VOSK_LANGS = frozenset({"en","es","fr","de","ru","it","pt","zh","ja","hi","ar","tr","nl","pl","uk","ca","fa","vi","ko","cs","sv","fi","el"})
PIPER_LANGS = frozenset({"ar","ca","cs","cy","da","de","el","en","es","fa","fi","fr","hu","is","it","ka","kk","lb","ne","nl","no","pl","pt","ro","ru","sk","sl","sr","sv","sw","tr","uk","vi","zh"})
BERGAMOT_PAIRS = frozenset({("en","es"),("es","en"),("en","fr"),("fr","en"),("en","de"),("de","en"),("en","ru"),("ru","en"),("en","cs"),("cs","en"),("en","pl"),("pl","en"),("en","et"),("et","en"),("en","bg"),("bg","en"),("es","fr"),("fr","es"),("es","de"),("de","es"),("fr","de"),("de","fr")})
APERTIUM_PAIRS = frozenset({("en","es"),("es","en"),("en","ca"),("ca","en"),("es","ca"),("ca","es"),("en","gl"),("gl","en"),("es","gl"),("gl","es"),("en","pt"),("pt","en"),("es","pt"),("pt","es"),("fr","ca"),("ca","fr"),("oc","ca"),("ca","oc"),("en","eo"),("eo","en"),("es","eo"),("eo","es")})

@dataclass(frozen=True)
class AdapterChoice:
    engine: EngineKind
    task: TaskKind
    source_lang: Optional[str]
    target_lang: Optional[str]
    reason: str
    standing_ok: bool

def GOSUB_SELECT_ADAPTER(decision, task, target_lang=None, prefer_lite=True, prefer_neural_mt=True):
    src = decision.top_lang
    if decision.standing != Standing.EXACT or decision.value_standing != Standing.EXACT:
        return AdapterChoice(EngineKind.NONE, task, src, target_lang, f"standing_blocked:{decision.standing.value}/{decision.value_standing.value}", False)
    if decision.verdict == Verdict.HELD:
        return AdapterChoice(EngineKind.NONE, task, src, target_lang, "verdict_held", True)
    if task == TaskKind.STT:
        if not src: return AdapterChoice(EngineKind.NONE, task, src, None, "no_source_lang", True)
        if prefer_lite and src in WHISPER_CPP_LITE_EN:
            return AdapterChoice(EngineKind.WHISPER_CPP_LITE, task, src, None, "whisper_cpp_lite_en", True)
        if src in WHISPER_CPP_LANGS:
            eng = EngineKind.WHISPER_CPP_LITE if prefer_lite else EngineKind.WHISPER_CPP
            return AdapterChoice(eng, task, src, None, "whisper_cpp", True)
        if src in VOSK_LANGS:
            return AdapterChoice(EngineKind.VOSK, task, src, None, "vosk_fallback", True)
        return AdapterChoice(EngineKind.NONE, task, src, None, "stt_lang_unsupported", True)
    if task == TaskKind.TTS:
        lang = target_lang or src
        if not lang: return AdapterChoice(EngineKind.NONE, task, src, target_lang, "no_tts_lang", True)
        if lang in PIPER_LANGS:
            return AdapterChoice(EngineKind.PIPER, task, src, lang, "piper_offline", True)
        return AdapterChoice(EngineKind.NONE, task, src, lang, "tts_lang_unsupported", True)
    if task == TaskKind.MT:
        if not src or not target_lang: return AdapterChoice(EngineKind.NONE, task, src, target_lang, "mt_missing_lang", True)
        if src == target_lang: return AdapterChoice(EngineKind.NONE, task, src, target_lang, "mt_same_lang", True)
        pair = (src, target_lang)
        if prefer_neural_mt and pair in BERGAMOT_PAIRS:
            return AdapterChoice(EngineKind.BERGAMOT, task, src, target_lang, "bergamot_pair", True)
        if pair in APERTIUM_PAIRS:
            return AdapterChoice(EngineKind.APERTIUM, task, src, target_lang, "apertium_pair", True)
        if pair in BERGAMOT_PAIRS:
            return AdapterChoice(EngineKind.BERGAMOT, task, src, target_lang, "bergamot_pair", True)
        return AdapterChoice(EngineKind.NONE, task, src, target_lang, "mt_pair_unsupported", True)
    return AdapterChoice(EngineKind.NONE, task, src, target_lang, "unknown_task", True)

if __name__ == "__main__":
    from fractions import Fraction
    from gosub_exact_decide import GOSUB_EXACT_DECIDE
    dec = GOSUB_EXACT_DECIDE({"es": Fraction(3), "fr": Fraction(1, 10)})
    print("STT", GOSUB_SELECT_ADAPTER(dec, TaskKind.STT).engine.value)
    print("TTS", GOSUB_SELECT_ADAPTER(dec, TaskKind.TTS, "es").engine.value)
    print("MT ", GOSUB_SELECT_ADAPTER(dec, TaskKind.MT, "en").engine.value)
    print("OK")
