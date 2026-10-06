#!/usr/bin/env python3
"""agent.py -- offline developer helper for the edge-canvas-kit.

Default mode "rules": keyword / TF-IDF search over the kit's docs, knowledge/ (masked copies of
Timothy's reference-map docs) and code; answers with cited snippets (path:lines).
Fail closed: when the query's words are not in the sources, it says it does not know.
Optional mode "local-model": NEED Ollama -> GOSUB probe 127.0.0.1:11434 -> if present, a local
model rewrites the cited snippets (it is told to answer only from them); if absent, RETURN to
rules. Never sends anything off the device; no other host is ever contacted.

Commands: /help  /tools  /reindex  /selftest  /scaffold <template> <bas|py|cpp> <name>
CLI:      python3 agent.py "how do I run the kit on a Pi 5"
"""
from __future__ import annotations
import json, math, os, re, signal, subprocess, sys, time, urllib.request
from collections import Counter

KIT_DIR = os.path.dirname(os.path.abspath(__file__))
if KIT_DIR not in sys.path:
    sys.path.insert(0, KIT_DIR)
from lib import optional  # noqa: E402
from lib.mask import mask  # noqa: E402

SELFTEST_FLAG = "KIT_SELFTEST_ACTIVE"
SELFTEST_TIMEOUT = 600


def _kill_group(p):
    """Kill the child's whole process group (POSIX) or the child (Windows). Never raises."""
    try:
        if os.name == "posix":
            os.killpg(p.pid, signal.SIGKILL)
        elif p.poll() is None:
            p.kill()
    except Exception:
        pass

EXCLUDE = {"selfcheck.py", "ui_smoke.py"}   # test files hold adversarial / fake queries; never answer from them
SOURCE_GLOBS = [("knowledge", (".md", ".txt")), ("docs", (".md", ".txt")), ("", (".md", ".py", ".sh", ".bat")),
                ("lib", (".py",)), ("basic", (".bas", ".py")), ("cpp", (".cpp",)), ("ui", (".js", ".html", ".css")),
                ("templates", (".tmpl",))]
STOP = set("""a an the and or of to in on for is are was were be been it its this that these those with as at by from
what which who whom how why when where do does did can could should would will i you he she we they me my your our
their there here about into over under than then so if not no yes up down out all any some such only own same too very
just also please tell show give explain me us one two get got use using used have has had kit""".split())
TEMPLATES = {("need_gosub", "bas"), ("need_gosub", "py"), ("conflict_nodes", "bas"), ("conflict_nodes", "py"),
             ("conflict_nodes", "cpp"), ("lead_filter", "bas"), ("lead_filter", "py")}
MIN_SCORE = 0.10
MIN_COVER = 0.5
DONT_KNOW = "I don't know. That is not in my sources (kit docs, knowledge/ copies, code)."


def tokens(text: str) -> list:
    out = []
    for w in re.findall(r"[a-z0-9]+(?:[-_.][a-z0-9]+)*", text.lower()):
        w = w.strip(".")
        if not w:
            continue
        parts = re.split(r"[-_.]", w)
        cand = [w] + (parts if len(parts) > 1 else [])
        for t in cand:
            if len(t) >= 2 and t not in STOP:
                out.append(t)
    return out


def chunk_file(rel: str, text: str) -> list:
    lines = text.split("\n")
    chunks, start = [], 0
    is_md = rel.endswith((".md", ".txt"))
    size = 40 if is_md else 30
    i = 0
    while i < len(lines):
        if is_md and i > start and lines[i].startswith("#"):
            chunks.append((start, i))
            start = i
        elif i - start >= size:
            chunks.append((start, i))
            start = i
        i += 1
    if start < len(lines):
        chunks.append((start, len(lines)))
    return [{"path": rel, "a": a + 1, "b": b, "text": "\n".join(lines[a:b])} for a, b in chunks if "\n".join(lines[a:b]).strip()]


class Agent:
    def __init__(self, kit_dir: str = KIT_DIR, workspace=None):
        self.kit_dir = kit_dir
        self.ws = workspace
        self.chunks, self.idf, self.vecs = [], {}, []
        self.built = 0.0

    # ---------------------------------------------------------------- index
    def sources(self) -> list:
        out = []
        for sub, exts in SOURCE_GLOBS:
            d = os.path.join(self.kit_dir, sub)
            if not os.path.isdir(d):
                continue
            for name in sorted(os.listdir(d)):
                p = os.path.join(d, name)
                if name in EXCLUDE or name.startswith("."):
                    continue
                if os.path.isfile(p) and name.endswith(exts) and os.path.getsize(p) < 1_500_000:
                    out.append(os.path.relpath(p, self.kit_dir).replace(os.sep, "/"))
        return out

    def build(self):
        chunks = []
        for rel in self.sources():
            try:
                t = open(os.path.join(self.kit_dir, rel), encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue  # non-UTF-8 source: skipped (quarantine node), index continues
            chunks.extend(chunk_file(rel, t))
        df = Counter()
        tfs = []
        for c in chunks:
            tf = Counter(tokens(c["text"]) + tokens(c["path"]))
            tfs.append(tf)
            df.update(tf.keys())
        n = max(len(chunks), 1)
        self.idf = {t: math.log((n + 1) / (d + 0.5)) for t, d in df.items()}
        self.vecs = []
        for tf in tfs:
            v = {t: (1 + math.log(c)) * self.idf[t] for t, c in tf.items()}
            norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
            self.vecs.append(({t: x / norm for t, x in v.items()}, set(tf)))
        self.chunks = chunks
        self.built = time.time()

    def search(self, q: str, k: int = 3) -> tuple:
        if not self.chunks:
            self.build()
        qt = [t for t in tokens(q)]
        qset = set(qt)
        known = [t for t in qset if t in self.idf]
        if not qset:
            return [], 0.0
        qv = Counter(t for t in qt if t in self.idf)
        qvec = {t: (1 + math.log(c)) * self.idf[t] for t, c in qv.items()}
        qn = math.sqrt(sum(x * x for x in qvec.values())) or 1.0
        scored = []
        for i, (v, tset) in enumerate(self.vecs):
            s = sum(qvec[t] / qn * v.get(t, 0.0) for t in qvec)
            if s > 0:
                cover = len(qset & tset) / len(qset)
                scored.append((s, cover, i))
        scored.sort(reverse=True)
        hits = [{"score": round(s, 4), "cover": round(cv, 3), **self.chunks[i]} for s, cv, i in scored[:k]]
        return hits, len(known) / len(qset)

    # ---------------------------------------------------------------- answer
    def answer_rules(self, q: str) -> dict:
        hits, vocab_cover = self.search(q)
        top = hits[0] if hits else None
        if not top or top["score"] < MIN_SCORE or top["cover"] < MIN_COVER or vocab_cover < MIN_COVER:
            return {"known": False, "answer": DONT_KNOW, "citations": [], "mode": "rules",
                    "why": {"best_score": top["score"] if top else 0, "best_cover": top["cover"] if top else 0,
                            "vocab_cover": round(vocab_cover, 3)}}
        qset = set(tokens(q))
        cites, lines_out = [], []
        for n, h in enumerate([h for h in hits if h["score"] >= MIN_SCORE and h["cover"] >= MIN_COVER], 1):
            rows = h["text"].split("\n")
            pick = [(j, r) for j, r in enumerate(rows) if qset & set(tokens(r))][:6] or list(enumerate(rows[:6]))
            snippet = mask("\n".join(r for _, r in pick))[0][:1200]
            a = h["a"] + pick[0][0]
            b = h["a"] + pick[-1][0]
            cites.append({"n": n, "path": h["path"], "lines": f"{a}-{b}", "score": h["score"], "snippet": snippet})
            lines_out.append(f"[{n}] {h['path']}:{a}-{b}\n{snippet}")
        return {"known": True, "mode": "rules", "citations": cites,
                "answer": "From my sources (quoted, not invented):\n\n" + "\n\n".join(lines_out)}

    def answer_local_model(self, q: str) -> dict:
        base = self.answer_rules(q)
        if not base["known"]:
            base["mode"] = "local-model (not called: nothing in sources)"
            return base
        ol = optional.need("ollama", refresh=True)
        if not ol["present"] or not ol.get("models"):
            base["mode"] = "rules (Ollama not detected at 127.0.0.1:11434; returned to rules)"
            return base
        model = os.environ.get("KIT_OLLAMA_MODEL") or ol["models"][0]
        ctx = "\n\n".join(f"[{c['n']}] {c['path']}:{c['lines']}\n{c['snippet']}" for c in base["citations"])
        prompt = ("Answer the question using ONLY the numbered sources below. Cite them like [1]. If the sources do not "
                  "contain the answer, reply exactly: I don't know.\n\nSOURCES:\n" + ctx + "\n\nQUESTION: " + mask(q)[0])
        body = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0}}).encode()
        try:
            req = urllib.request.Request(optional.OLLAMA_URL + "/api/generate", data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                text = json.loads(r.read(2_000_000).decode("utf-8", "replace")).get("response", "").strip()
        except Exception as e:
            base["mode"] = f"rules (local model call failed: {type(e).__name__})"
            return base
        if not text:
            base["mode"] = "rules (local model returned nothing)"
            return base
        base.update(mode=f"local-model {model} (draft from cited sources)", answer=mask(text)[0] + "\n\n---\n" + base["answer"])
        return base

    # ---------------------------------------------------------------- commands
    def scaffold(self, template: str, lang: str, name: str) -> dict:
        if (template, lang) not in TEMPLATES:
            return {"ok": False, "answer": "Unknown template. Have: " + ", ".join(f"{t} {l}" for t, l in sorted(TEMPLATES))}
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,40}", name or ""):
            return {"ok": False, "answer": "Name must be letters/digits/_ (start with a letter, max 41)."}
        if self.ws is None:
            return {"ok": False, "answer": "No workspace attached (run through server.py)."}
        src = open(os.path.join(self.kit_dir, "templates", f"{template}.{lang}.tmpl"), encoding="utf-8").read()
        body = src.replace("{{NAME}}", name).replace("{{DATE}}", time.strftime("%Y-%m-%d"))
        res = self.ws.write(f"{name}.{lang}", body)
        return {"ok": True, "answer": f"Scaffolded workspace/{res['path']} from {template}.{lang}.tmpl"
                + (f" (previous version archived to {res['archived']})" if res.get("archived") else ""), "file": res}

    def selftest(self) -> dict:
        """Run `selfcheck.py --quick` once, in its own process group, with a hard timeout.

        Recursion guard (R6, after the runaway incident): the child gets KIT_SELFTEST_ACTIVE=1, and any
        /selftest asked while that flag is set is refused without starting anything. selfcheck.py also
        sets the flag for itself, and --quick never calls /selftest.
        """
        if os.environ.get(SELFTEST_FLAG) == "1":
            return {"ok": False, "refused": True,
                    "answer": "refused: a self-check is already running (KIT_SELFTEST_ACTIVE=1); not starting another"}
        env = dict(os.environ)
        env[SELFTEST_FLAG] = "1"
        if os.name == "posix":
            kw = {"start_new_session": True}
        else:
            kw = {"creationflags": getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)}
        try:
            p = subprocess.Popen([sys.executable, os.path.join(self.kit_dir, "selfcheck.py"), "--quick"],
                                 cwd=self.kit_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 stdin=subprocess.DEVNULL, text=True, env=env, **kw)
        except Exception as e:
            return {"ok": False, "answer": f"self-check could not run: {type(e).__name__}"}
        try:
            out, _ = p.communicate(timeout=SELFTEST_TIMEOUT)
            rc = p.returncode
        except subprocess.TimeoutExpired:
            _kill_group(p)
            try:
                out = (p.communicate(timeout=10)[0] or "")
            except Exception:
                out = ""
            out += "\n[self-check timed out; its process group was killed]"
            rc = None
        finally:
            _kill_group(p)   # reap stragglers left in the child's group
        out = (out or "")[-6000:]
        summary = [ln for ln in out.splitlines() if ln.startswith(("SUMMARY", "TOTAL"))]
        return {"ok": rc == 0, "answer": "\n".join(summary) or out[-800:], "log_tail": out[-3000:]}

    def ask(self, q: str, mode: str = "rules") -> dict:
        q = (q or "").strip()
        if not q:
            return {"known": False, "answer": "Ask a question or type /help.", "citations": []}
        low = q.lower()
        if low.startswith("/help"):
            return {"known": True, "citations": [], "answer": __doc__.split("Commands:")[1].strip()}
        if low.startswith("/tools"):
            return {"known": True, "citations": [], "answer": json.dumps(optional.summary(include_ollama=True), indent=1)}
        if low.startswith("/reindex"):
            self.build()
            return {"known": True, "citations": [], "answer": f"Indexed {len(self.chunks)} chunks from {len(self.sources())} files."}
        if low.startswith("/selftest"):
            return {"known": True, "citations": [], **self.selftest()}
        if low.startswith("/scaffold"):
            parts = q.split()
            if len(parts) != 4:
                return {"known": True, "citations": [], "answer": "Usage: /scaffold <need_gosub|conflict_nodes|lead_filter> <bas|py|cpp> <name>"}
            return {"known": True, "citations": [], **self.scaffold(parts[1], parts[2], parts[3])}
        if mode == "local-model":
            return self.answer_local_model(q)
        return self.answer_rules(q)


if __name__ == "__main__":
    a = Agent()
    q = " ".join(sys.argv[1:]) or "/help"
    print(a.ask(q)["answer"])
