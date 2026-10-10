"""runner.py -- capped subprocess runs for BOOT, BASIC and C++ (argument lists, never a shell).

Guard rails (NOT a full sandbox; that is why code runs are localhost-only unless the
server is started with --allow-remote-run):
  * argv lists only, shell=False, stdin closed unless stdin text is given
  * wall-clock timeout, output cap (process killed when the cap is hit)
  * POSIX rlimits when available: CPU seconds, address space, file size, core=0
  * own process group, killed as a group on timeout
  * keyword / header deny-lists refuse source that reaches files, shells, network or the OS
  * run dirs live inside the kit data dir (runs/basic, runs/cpp); nothing is deleted
"""
from __future__ import annotations
import os, re, secrets, signal, subprocess, threading, time

from . import optional

try:
    import resource
except Exception:  # Windows
    resource = None

OUT_CAP = 64 * 1024
SRC_CAP = 256 * 1024
STDIN_CAP = 64 * 1024


def _limits(cpu: int, mem: int, fsize: int):
    if resource is None:
        return None

    def apply():
        for lim, val in ((resource.RLIMIT_CPU, cpu), (resource.RLIMIT_AS, mem), (resource.RLIMIT_FSIZE, fsize),
                         (resource.RLIMIT_CORE, 0)):
            try:
                resource.setrlimit(lim, (val, val))
            except (ValueError, OSError):
                pass
    return apply


def run_capped(argv, cwd, timeout=10, cap=OUT_CAP, stdin_text=None, cpu=10, mem=768 * 2**20, fsize=4 * 2**20,
               env=None) -> dict:
    """Run argv; return {'rc', 'out', 'timed_out', 'capped', 'secs'}. Never raises for child failures."""
    t0 = time.time()
    kw = {}
    if os.name == "posix":
        kw["start_new_session"] = True
        pre = _limits(cpu, mem, fsize)
        if pre:
            kw["preexec_fn"] = pre
    else:
        kw["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    base_env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LANG": "C.UTF-8", "HOME": cwd}
    if os.name == "nt":
        base_env.update({k: os.environ[k] for k in ("SYSTEMROOT", "TEMP", "TMP") if k in os.environ})
    try:
        p = subprocess.Popen(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             stdin=subprocess.PIPE if stdin_text is not None else subprocess.DEVNULL,
                             shell=False, env=env or base_env, **kw)
    except OSError as e:
        return {"rc": None, "out": f"[runner] could not start: {type(e).__name__}", "timed_out": False, "capped": False,
                "secs": 0.0}

    def kill():
        try:
            if os.name == "posix":
                os.killpg(p.pid, signal.SIGKILL)
            else:
                p.kill()
        except Exception:
            pass

    stdin_bytes = stdin_text.encode("utf-8")[:STDIN_CAP] if stdin_text is not None else None
    if os.name == "posix":
        st = _read_posix(p, cap, timeout, t0, stdin_bytes, kill)
    else:
        st = _read_thread(p, cap, timeout, stdin_bytes, kill)
    try:
        p.wait(timeout=5)   # child has exited or was killed; bounded either way
    except Exception:
        pass
    out = st["buf"].decode("utf-8", "replace")
    if st["capped"]:
        out += f"\n[runner] output cap {cap} bytes hit; process stopped"
    if st["timed_out"]:
        out += f"\n[runner] timeout {timeout}s; process stopped"
    if st["held"]:
        out += "\n[runner] output pipe still held by a process outside the run; stopped reading"
    return {"rc": p.returncode, "out": out, "timed_out": st["timed_out"], "capped": st["capped"],
            "secs": round(time.time() - t0, 3), "held": st["held"]}


SLICE = 0.05   # fallback wake only when the kernel cannot report child exit (no pidfd)


def _read_posix(p, cap, timeout, t0, stdin_bytes, kill) -> dict:
    """RUNNER_READ spec v2: wake on need (pipe readable, stdin writable, child exited).
    No thread, no sleep loop. One entry, one exit; every handle closed on the way out."""
    import selectors
    st = {"buf": bytearray(), "capped": False, "timed_out": False, "held": False, "out_done": False}
    out_fd = p.stdout.fileno()
    os.set_blocking(out_fd, False)
    sel = selectors.DefaultSelector()
    sel.register(out_fd, selectors.EVENT_READ, "out")
    in_fd, pos = None, 0
    if stdin_bytes is not None:
        if stdin_bytes:
            in_fd = p.stdin.fileno()
            os.set_blocking(in_fd, False)
            sel.register(in_fd, selectors.EVENT_WRITE, "in")
        else:
            p.stdin.close()
    pidfd = None
    try:
        pidfd = os.pidfd_open(p.pid)
        sel.register(pidfd, selectors.EVENT_READ, "exit")
    except (AttributeError, OSError):
        pidfd = None

    def read_chunk():
        try:
            chunk = os.read(out_fd, 4096)
        except BlockingIOError:
            return "empty"
        except OSError:
            return "eof"
        if not chunk:
            return "eof"
        room = cap - len(st["buf"])
        if room > 0:
            st["buf"].extend(chunk[:room])
        if len(chunk) > room:
            st["capped"] = True
            kill()
            return "cap"
        return "data"

    def drain():
        r = "data"
        while r == "data":
            r = read_chunk()
        if r == "eof":
            st["out_done"] = True
        elif r == "empty":
            st["held"] = True

    deadline = t0 + timeout
    child_done = False
    try:
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                st["timed_out"] = True
                kill()
                if not st["out_done"]:
                    drain()
                break
            events = sel.select(remaining if pidfd is not None else min(remaining, SLICE))
            for key, _ in events:
                if key.data == "out":
                    r = read_chunk()
                    if r == "eof":
                        st["out_done"] = True
                        sel.unregister(out_fd)
                    elif r == "cap":
                        break
                elif key.data == "in":
                    try:
                        pos += os.write(in_fd, stdin_bytes[pos:pos + 65536])
                    except BlockingIOError:
                        pass
                    except OSError:
                        pos = len(stdin_bytes)
                    if pos >= len(stdin_bytes):
                        sel.unregister(in_fd)
                        try:
                            p.stdin.close()
                        except OSError:
                            pass
                        in_fd = None
                else:
                    child_done = True
            if st["capped"]:
                break
            if not child_done and p.poll() is not None:
                child_done = True
            if child_done:
                if not st["out_done"]:
                    drain()
                break
    finally:
        if in_fd is not None:
            try:
                p.stdin.close()
            except OSError:
                pass
        sel.close()
        if pidfd is not None:
            os.close(pidfd)
        p.stdout.close()
    return st


def _read_thread(p, cap, timeout, stdin_bytes, kill) -> dict:
    """Windows: pipes cannot be waited on, so a reader thread stays; an alive thread after
    its bounded join is reported as held instead of being left silent."""
    st = {"buf": bytearray(), "capped": False, "timed_out": False, "held": False}

    def reader():
        while True:
            chunk = p.stdout.read(4096)
            if not chunk:
                break
            room = cap - len(st["buf"])
            if room > 0:
                st["buf"].extend(chunk[:room])
            if len(chunk) > room:
                st["capped"] = True
                kill()
                break

    th = threading.Thread(target=reader, daemon=True)
    th.start()
    if stdin_bytes is not None:
        try:
            p.stdin.write(stdin_bytes)
            p.stdin.close()
        except Exception:
            pass
    try:
        p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        st["timed_out"] = True
        kill()
    th.join(timeout=5)
    if th.is_alive():
        st["held"] = True
    return st


def new_run_dir(data_dir: str, lane: str) -> str:
    d = os.path.join(data_dir, "runs", lane, time.strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(3))
    os.makedirs(d, exist_ok=False)
    return d


# ------------------------------------------------------------------ BOOT
def boot(kit_dir: str) -> dict:
    bas = os.path.join(kit_dir, "basic", "BOOT.bas")
    expect = "0.70710678"
    if not os.path.isfile(bas):
        return {"ok": False, "expect": expect, "out": "", "via": "none", "note": "basic/BOOT.bas absent (fail closed)"}
    bw = optional.need("bwbasic")
    if bw["present"]:
        r = run_capped([bw["path"], bas], cwd=os.path.dirname(bas), timeout=10)
        lines = [ln.strip() for ln in r["out"].splitlines()]
        return {"ok": expect in lines, "expect": expect, "out": r["out"], "via": "bwbasic", "rc": r["rc"]}
    # NEED bwbasic -> absent -> GOSUB python twin (same digit-string cut as BOOT.bas line 500-550)
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("kit_boot_twin", os.path.join(kit_dir, "basic", "boot.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        val = mod.cut_decimal("0.707106781")
        return {"ok": val == expect, "expect": expect, "out": val, "via": "python twin (bwbasic absent)"}
    except Exception as e:
        return {"ok": False, "expect": expect, "out": "", "via": "none", "note": f"bwbasic absent and twin failed: {type(e).__name__}"}


# ------------------------------------------------------------------ BASIC
BASIC_DENY = ["SHELL", "SYSTEM", "KILL", "NAME", "OPEN", "CLOSE", "CHDIR", "MKDIR", "RMDIR", "FILES", "LOAD", "SAVE",
              "MERGE", "CHAIN", "ENVIRON", "ENVIRON$", "EDIT", "NEW", "DELETE", "RENUM", "CALL", "COMMON", "FIELD",
              "LSET", "RSET", "PUT", "GET", "LPRINT", "LOF", "LOC", "EOF", "WRITE", "INPUT#", "PRINT#", "SLEEP",
              "INKEY$", "CLEAR", "DEF SEG", "POKE", "PEEK", "USR", "VARPTR", "OUT", "INP", "WAIT", "BLOAD", "BSAVE",
              "RUN", "TRON", "TROFF", "CMDS", "OPTION"]
_BASIC_WORD = re.compile(r"[A-Za-z][A-Za-z0-9]*\$?")


_WHOLE_REM = re.compile(r"^\s*\d+\s+REM(?:\s.*)?$", re.I)


def basic_screen(code: str):
    """-> '' if allowed, else the refusal reason. Whole-line 'nnn REM ...' comments are skipped;
    everything else (string literals and trailing REMs included) is scanned (fail closed)."""
    if len(code) > SRC_CAP:
        return "source over cap"
    if "\x00" in code:
        return "NUL byte refused"
    scan = "\n".join(ln for ln in code.splitlines() if not _WHOLE_REM.match(ln))
    if "#" in scan:
        return "file-number '#' refused (no file I/O in the editor lane)"
    up = scan.upper()
    words = set(_BASIC_WORD.findall(up))
    for w in BASIC_DENY:
        if " " in w:
            if w in up:
                return f"keyword refused: {w}"
        elif w in words:
            return f"keyword refused: {w}"
    return ""


def run_basic(code: str, data_dir: str, timeout: int = 10) -> dict:
    why = basic_screen(code)
    if why:
        return {"ok": False, "refused": why, "out": ""}
    bw = optional.need("bwbasic")
    if not bw["present"]:
        return {"ok": False, "missing": "bwbasic", "out": "",
                "note": "bwbasic not found on this device (optional). Main line continues; nothing installed."}
    d = new_run_dir(data_dir, "basic")
    src = os.path.join(d, "prog.bas")
    with open(src, "w", encoding="utf-8", newline="\n") as f:
        f.write(code if code.endswith("\n") else code + "\n")
    r = run_capped([bw["path"], "prog.bas"], cwd=d, timeout=timeout, cpu=timeout + 2)
    with open(os.path.join(d, "run.log"), "w", encoding="utf-8") as f:
        f.write(r["out"])
    return {"ok": not r["timed_out"] and not r["capped"], "out": r["out"], "rc": r["rc"], "timed_out": r["timed_out"],
            "capped": r["capped"], "secs": r["secs"], "run_dir": os.path.relpath(d, data_dir)}


# ------------------------------------------------------------------ C++
CPP_HEADERS = {"iostream", "string", "vector", "map", "unordered_map", "set", "unordered_set", "array", "deque", "list",
               "queue", "stack", "algorithm", "numeric", "utility", "tuple", "optional", "variant", "sstream", "iomanip",
               "cmath", "cstdint", "cstddef", "climits", "limits", "stdexcept", "cassert", "functional", "memory",
               "iterator", "bitset", "complex", "ratio", "random", "string_view", "initializer_list", "type_traits",
               "cctype", "cstring", "chrono"}
CPP_DENY = ["system", "popen", "pclose", "fork", "vfork", "clone", "exec", "execl", "execlp", "execle", "execv", "execvp",
            "execve", "execvpe", "posix_spawn", "posix_spawnp", "spawn", "socket", "connect", "bind", "listen", "accept",
            "fopen", "freopen", "fdopen", "open", "openat", "creat", "remove", "rename", "unlink", "unlinkat", "rmdir",
            "mkdir", "chdir", "chmod", "chown", "truncate", "kill", "raise", "signal", "ptrace", "syscall", "dlopen",
            "dlsym", "mmap", "mprotect", "asm", "__asm", "__asm__", "_Pragma", "__attribute__", "getenv", "setenv",
            "putenv", "environ", "extern", "ofstream", "ifstream", "fstream", "filebuf", "filesystem", "thread",
            "jthread", "async", "rdbuf", "FILE", "stdin", "stdout", "stderr", "write", "read", "ioctl", "fcntl",
            "setuid", "setgid", "reinterpret_cast", "volatile"]
_CPP_IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_INCLUDE = re.compile(r"^\s*#\s*include\s*<([a-z_]+)>\s*$")


def _cpp_strip(code: str):
    """Remove comments and string/char literal bodies (they cannot execute once the preprocessor is locked down).
    Returns None when the source cannot be lexed safely (raw strings, unterminated literal/comment)."""
    out, i, n = [], 0, len(code)
    while i < n:
        c = code[i]
        if code.startswith("//", i):
            j = code.find("\n", i)
            i = n if j < 0 else j
        elif code.startswith("/*", i):
            j = code.find("*/", i + 2)
            if j < 0:
                return None
            out.append(" ")
            i = j + 2
        elif c in "\"'":
            if c == '"' and i > 0 and (code[i - 1].isalnum() or code[i - 1] == "_"):
                return None   # prefixed literal (R"..", u8"..", L"..") -- refuse rather than guess
            j = i + 1
            while j < n and code[j] != c:
                if code[j] == "\n":
                    return None
                j += 2 if code[j] == "\\" else 1
            if j >= n:
                return None
            out.append(c + c)
            i = j + 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def cpp_screen(code: str):
    if len(code) > SRC_CAP:
        return "source over cap"
    if "\x00" in code:
        return "NUL byte refused"
    if "\\\n" in code or "\\\r\n" in code:
        return "line continuation refused (token splicing)"
    if "??=" in code or "%:" in code:
        return "trigraph/digraph preprocessor token refused"
    for ln in code.splitlines():
        if ln.lstrip().startswith("#"):
            m = _INCLUDE.match(ln)
            if not m:
                return f"preprocessor line refused (only #include <allowed>): {ln.strip()[:60]}"
            if m.group(1) not in CPP_HEADERS:
                return f"header refused: <{m.group(1)}>"
    stripped = _cpp_strip(code)
    if stripped is None:
        return "source could not be lexed safely (raw/prefixed string or unterminated literal/comment) -- refused"
    idents = set(_CPP_IDENT.findall(stripped))
    for w in CPP_DENY:
        if w in idents:
            return f"identifier refused: {w}"
    for i in idents:
        if i.startswith("__builtin") or i.startswith("exec"):
            return f"identifier refused: {i}"
    return ""


def run_cpp(code: str, data_dir: str, stdin_text=None, compile_timeout: int = 90, run_timeout: int = 10,
            std: str = "c++17", skip_screen: bool = False) -> dict:
    """GOSUB C++ lane. skip_screen is only used by the kit's own self-checks on its shipped twins."""
    why = "" if skip_screen else cpp_screen(code)
    if why:
        return {"ok": False, "refused": why, "out": ""}
    if std not in ("c++17", "c++20"):
        return {"ok": False, "refused": "std must be c++17 or c++20", "out": ""}
    if stdin_text is not None and (not isinstance(stdin_text, str) or len(stdin_text) > STDIN_CAP):
        return {"ok": False, "refused": "stdin over cap", "out": ""}
    cx = optional.need("cxx")
    if not cx["present"]:
        return {"ok": False, "missing": "g++/clang++", "out": "",
                "note": "No C++ compiler found on this device (optional). Main line continues; nothing installed. "
                        "On a Pi 5 you may choose to run: sudo apt install g++"}
    d = new_run_dir(data_dir, "cpp")
    with open(os.path.join(d, "main.cpp"), "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    exe = "main.exe" if os.name == "nt" else "main.bin"
    c = run_capped([cx["path"], f"-std={std}", "-O1", "-pipe", "-o", exe, "main.cpp"], cwd=d, timeout=compile_timeout,
                   cpu=compile_timeout, mem=2048 * 2**20, fsize=256 * 2**20,
                   env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LANG": "C.UTF-8", "HOME": d,
                        "TMPDIR": d, **({k: os.environ[k] for k in ("SYSTEMROOT", "TEMP", "TMP") if k in os.environ})})
    with open(os.path.join(d, "compile.log"), "w", encoding="utf-8") as f:
        f.write(c["out"])
    res = {"compiler": cx.get("name"), "compile_out": c["out"], "compile_rc": c["rc"], "compile_secs": c["secs"],
           "run_dir": os.path.relpath(d, data_dir)}
    if c["rc"] != 0 or not os.path.isfile(os.path.join(d, exe)):
        res.update(ok=False, stage="compile", out="", timed_out=c["timed_out"])
        return res
    # CPU rlimit a little above the wall timeout so the wall clock decides (deterministic 'timed_out')
    r = run_capped([os.path.join(d, exe)], cwd=d, timeout=run_timeout, stdin_text=stdin_text, cpu=run_timeout + 2)
    with open(os.path.join(d, "run.log"), "w", encoding="utf-8") as f:
        f.write(r["out"])
    res.update(ok=(r["rc"] == 0 and not r["timed_out"] and not r["capped"]), stage="run", out=r["out"], rc=r["rc"],
               timed_out=r["timed_out"], capped=r["capped"], secs=r["secs"])
    return res
