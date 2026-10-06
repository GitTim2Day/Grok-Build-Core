"""optional.py -- NEED -> GOSUB -> RETURN detection of optional extras.

Nothing here installs anything. Each probe runs only when its feature is needed, caches
the answer, and returns a dict; a missing extra is reported, never fatal.
Ollama is probed ONLY at 127.0.0.1:11434 (hard-coded; never a remote host).
"""
from __future__ import annotations
import json, shutil, subprocess, urllib.request

_cache: dict = {}
OLLAMA_URL = "http://127.0.0.1:11434"


def which(name: str):
    return shutil.which(name)


def _version(argv) -> str:
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=5, stdin=subprocess.DEVNULL)
        lines = (p.stdout + p.stderr).strip().splitlines()
        return lines[0][:120] if lines else "present"
    except Exception as e:
        return f"present (version probe failed: {type(e).__name__})"


def need(feature: str, refresh: bool = False) -> dict:
    """GOSUB: detect one optional extra. RETURN {'present': bool, ...}."""
    if feature in _cache and not refresh:
        return _cache[feature]
    r = {"feature": feature, "present": False}
    if feature == "bwbasic":
        p = which("bwbasic")
        r.update(present=bool(p), path=p or "")
    elif feature == "tesseract":
        p = which("tesseract")
        r.update(present=bool(p), path=p or "", version=_version([p, "--version"]) if p else "")
    elif feature == "pdftotext":
        p = which("pdftotext")
        r.update(present=bool(p), path=p or "")
    elif feature == "cxx":
        for name in ("g++", "clang++", "c++"):
            p = which(name)
            if p:
                r.update(present=True, path=p, name=name, version=_version([p, "--version"]))
                break
    elif feature == "pillow":
        try:
            import PIL  # noqa: F401
            r.update(present=True, version=getattr(PIL, "__version__", "?"))
        except Exception:
            pass
    elif feature == "defusedxml":
        try:
            import defusedxml  # noqa: F401
            r.update(present=True)
        except Exception:
            pass
    elif feature == "ollama":
        try:
            with urllib.request.urlopen(OLLAMA_URL + "/api/tags", timeout=0.8) as resp:
                data = json.loads(resp.read(1_000_000).decode("utf-8", "replace"))
            models = [m.get("name", "") for m in data.get("models", []) if isinstance(m, dict)]
            r.update(present=True, url=OLLAMA_URL, models=models[:20])
        except Exception as e:
            r.update(present=False, url=OLLAMA_URL, why=type(e).__name__)
    else:
        r.update(why="unknown feature (flagged, main line continues)")
    _cache[feature] = r
    return r


def summary(include_ollama: bool = False) -> dict:
    feats = ["bwbasic", "tesseract", "pdftotext", "cxx", "pillow", "defusedxml"] + (["ollama"] if include_ollama else [])
    return {f: need(f) for f in feats}
