#!/usr/bin/env python3
"""agent.py -- offline developer helper for the edge-canvas-kit.

Default mode "rules": keyword / TF-IDF search over the kit's docs, knowledge/ (masked copies of
Timothy's reference-map docs) and code; answers with cited snippets (path:lines).
Optional mode "local-model": NEED Ollama -> GOSUB probe 127.0.0.1:11434 -> if present, a local
model rewrites the cited snippets (it is told to answer only from them); if absent, RETURN to
rules.

EXHAUST LADDER (Timothy 2026-10-08: no "I don't know" until every resource has been tried):
  rung 1 exact local match (rules) -> rung 2 widened local match (every passing hit, word forms) ->
  rung 3 Ollama on this device answers from its own knowledge (labelled unverified; nothing leaves) ->
  rung 4 raise the need and ASK Timothy: masked question (DM-5) + his providers (workspace/providers.json:
  web search or a subscribed API, keys in env vars). Nothing dials out until /approve <id> <provider>,
  unless he marked that provider pre_approved. The answer comes back to this device to finish the job.
  Needs log: workspace/needs/agent_needs.jsonl, append-only. Offline stays the default (DM-2).

Commands: /help  /tools  /reindex  /selftest  /scaffold <template> <bas|py|cpp> <name>
          /needs  /approve <id> <provider>  /deny <id>
CLI:      python3 agent.py "how do I run the kit on a Pi 5"
"""
from __future__ import annotations
import hashlib, json, math, os, re, signal, subprocess, sys, time, urllib.parse, urllib.request
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
PROVIDERS_REL = "providers.json"        # Timothy's dial-out list, in the workspace; API keys stay in env vars
WEB_TIMEOUT = 10
WEB_READ_CAP = 1_000_000
WEB_MAX_RESULTS = 5
NEEDS_REL = "needs/agent_needs.jsonl"   # append-only, inside the guarded workspace


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


def stem(t: str) -> str:
    """Word-form fold for rung 2 (formulas->formula, converter->convert, masked->mask). Keeps 'ss' words."""
    if t.endswith("ss"):
        return t
    for suf, rep_ in (("ies", "y"), ("ing", ""), ("ers", ""), ("er", ""), ("ed", ""), ("es", ""), ("s", "")):
        if len(t) > len(suf) + 3 and t.endswith(suf):
            return t[: -len(suf)] + rep_
    return t


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
        self.chunks, self.idf, self.vecs, self.stemsets = [], {}, [], []
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
        self.stemsets = [{stem(t) for t in tset} for _, tset in self.vecs]
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
        hits = [{"score": round(s, 4), "cover": round(cv, 3), "_i": i, **self.chunks[i]} for s, cv, i in scored[:k]]
        return hits, len(known) / len(qset)

    # ---------------------------------------------------------------- answer
    def answer_rules(self, q: str) -> dict:
        hits, vocab_cover = self.search(q)
        top = hits[0] if hits else None
        if not top or top["score"] < MIN_SCORE or top["cover"] < MIN_COVER or vocab_cover < MIN_COVER:
            return {"known": False, "answer": DONT_KNOW, "citations": [], "mode": "rules",
                    "why": {"best_score": top["score"] if top else 0, "best_cover": top["cover"] if top else 0,
                            "vocab_cover": round(vocab_cover, 3)}}
        return self._cite(q, [h for h in hits if h["score"] >= MIN_SCORE and h["cover"] >= MIN_COVER], "rules")

    def _cite(self, q: str, good: list, mode: str) -> dict:
        qset = set(tokens(q)) | {stem(t) for t in tokens(q)}
        cites, lines_out = [], []
        for n, h in enumerate(good, 1):
            rows = h["text"].split("\n")
            pick = [(j, r) for j, r in enumerate(rows) if qset & (set(tokens(r)) | {stem(t) for t in tokens(r)})][:6] or list(enumerate(rows[:6]))
            snippet = mask("\n".join(r for _, r in pick))[0][:1200]
            a = h["a"] + pick[0][0]
            b = h["a"] + pick[-1][0]
            cites.append({"n": n, "path": h["path"], "lines": f"{a}-{b}", "score": h["score"], "snippet": snippet})
            lines_out.append(f"[{n}] {h['path']}:{a}-{b}\n{snippet}")
        return {"known": True, "mode": mode, "citations": cites,
                "answer": "From my sources (quoted, not invented):\n\n" + "\n\n".join(lines_out)}

    # ---------------------------------------------------------------- exhaust ladder (rungs 2, 4, 5)
    def answer_widened(self, q: str) -> dict:
        """Rung 2: same gates (MIN_SCORE, MIN_COVER), but every top-10 hit is eligible, and cover counts word forms."""
        hits, vocab_cover = self.search(q, k=10)
        qs = {stem(t) for t in tokens(q)}
        if not qs:
            return {"known": False, "why": "no words left after stop-list"}
        if not hits:
            return {"known": False, "why": "no source chunk shares a word with the question"}
        known_s = {stem(t) for t in self.idf}
        if len(qs & known_s) / len(qs) < MIN_COVER:
            return {"known": False, "why": "most query words are not in the sources, even as word forms"}
        good = []
        for h in hits:
            cover_s = len(qs & self.stemsets[h["_i"]]) / len(qs)
            if h["score"] >= MIN_SCORE and cover_s >= MIN_COVER:
                good.append(dict(h, cover=round(cover_s, 3)))
        if not good:
            return {"known": False, "why": "no hit passed both gates with word forms"}
        return self._cite(q, good[:3], "rules widened (rung 2: every passing hit, word forms)")

    # -------- rung 3: Ollama on this device answers from its own knowledge (nothing leaves the device)
    def answer_ollama_open(self, q: str) -> dict:
        ol = optional.need("ollama", refresh=True)
        if not ol["present"] or not ol.get("models"):
            return {"known": False, "why": "Ollama not detected at 127.0.0.1:11434"}
        model = os.environ.get("KIT_OLLAMA_MODEL") or ol["models"][0]
        prompt = ("Answer briefly and plainly. If you are not sure, reply exactly: UNSURE.\n\nQUESTION: " + mask(q)[0])
        body = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0}}).encode()
        try:
            req = urllib.request.Request(optional.OLLAMA_URL + "/api/generate", data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                text = json.loads(r.read(2_000_000).decode("utf-8", "replace")).get("response", "").strip()
        except Exception as e:
            return {"known": False, "why": f"Ollama call failed ({type(e).__name__})"}
        if not text or text.upper().startswith("UNSURE"):
            return {"known": False, "why": f"Ollama {model} was not sure"}
        return {"known": True, "mode": f"local model {model} (own knowledge, unverified; not from kit sources)",
                "citations": [], "answer": f"Not in my sources. Your local model {model} answered (unverified):\n\n" + mask(text)[0]}

    # -------- providers Timothy sets up (workspace/providers.json); keys stay in environment variables
    def providers(self) -> list:
        """[{name, kind: web|anthropic|openai, url, model?, key_env?, pre_approved: false}] -- only https; no keys in the file."""
        if self.ws is None:
            return []
        try:
            full = self.ws.resolve(PROVIDERS_REL)
            data = json.load(open(full, encoding="utf-8"))
        except Exception:
            return []
        out = []
        for pv in data if isinstance(data, list) else []:
            if not isinstance(pv, dict) or not re.fullmatch(r"[A-Za-z0-9_-]{1,32}", str(pv.get("name", ""))):
                continue
            if pv.get("kind") not in ("web", "anthropic", "openai") or not str(pv.get("url", "")).startswith("https://"):
                continue
            if pv["kind"] == "web" and "{q}" not in pv["url"]:
                continue
            out.append(pv)
        return out

    # -------- the needs log: append-only; the latest record for an id is its state
    def _needs_path(self) -> str:
        return self.ws.resolve(NEEDS_REL, for_write=True)

    def _append_need(self, rec: dict) -> dict:
        if self.ws is None:
            return dict(rec, saved=False, why="no workspace attached (CLI); need not saved")
        try:
            full = self._needs_path()
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=True) + "\n")
            return dict(rec, saved=True, file="workspace/" + NEEDS_REL)
        except Exception as e:
            return dict(rec, saved=False, why=f"need not saved ({type(e).__name__})")

    def needs(self) -> dict:
        """Latest record per need id, in first-seen order."""
        if self.ws is None:
            return {}
        try:
            rows = open(self._needs_path(), encoding="utf-8").read().splitlines()
        except Exception:
            return {}
        latest = {}
        for ln in rows:
            try:
                r = json.loads(ln)
                latest[r["id"]] = r
            except Exception:
                continue
        return latest

    def raise_need(self, q: str, tried: list) -> dict:
        mq, _ = mask(q)
        ts = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        rec = {"ts": ts, "id": hashlib.sha256((ts + mq).encode()).hexdigest()[:12], "masked_query": mq,
               "tried": tried, "status": "WAITING_PERMISSION"}
        return self._append_need(rec)

    # -------- rung 4: dial out, only after Timothy approves (or a provider he marked pre_approved)
    def _dial(self, pv: dict, mq: str) -> dict:
        try:
            if pv["kind"] == "web":
                req = urllib.request.Request(pv["url"].replace("{q}", urllib.parse.quote(mq)),
                                             headers={"User-Agent": "edge-canvas-kit"})
            else:
                key = os.environ.get(str(pv.get("key_env", "")), "")
                if not key:
                    return {"ok": False, "why": f"key not set (environment variable {pv.get('key_env')!r})"}
                msgs = [{"role": "user", "content": "Answer briefly and plainly; say if unsure.\n\n" + mq}]
                if pv["kind"] == "anthropic":
                    body = {"model": pv.get("model", ""), "max_tokens": 800, "messages": msgs}
                    hdr = {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
                else:
                    body = {"model": pv.get("model", ""), "messages": msgs}
                    hdr = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
                req = urllib.request.Request(pv["url"], data=json.dumps(body).encode(), headers=hdr)
            with urllib.request.urlopen(req, timeout=WEB_TIMEOUT if pv["kind"] == "web" else 120) as r:
                raw = r.read(WEB_READ_CAP).decode("utf-8", "replace")
        except Exception as e:
            return {"ok": False, "why": f"unreachable ({type(e).__name__})"}
        if pv["kind"] == "web":
            host = urllib.parse.urlparse(pv["url"]).hostname or ""
            found, seen = [], set()
            for href, title in re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', raw, re.S | re.I):
                title = re.sub(r"<[^>]+>|\s+", " ", title).strip()
                h2 = urllib.parse.urlparse(href).hostname or ""
                if not title or len(title) < 12 or h2 == host or h2.endswith("." + host) or href in seen:
                    continue
                seen.add(href)
                found.append({"n": len(found) + 1, "path": href, "lines": "web", "score": 0, "snippet": mask(title)[0][:200]})
                if len(found) >= WEB_MAX_RESULTS:
                    break
            if not found:
                return {"ok": False, "why": "web returned no usable results"}
            return {"ok": True, "citations": found,
                    "text": "\n".join(f"[{c['n']}] {c['snippet']}\n    {c['path']}" for c in found)}
        try:
            j = json.loads(raw)
            if pv["kind"] == "anthropic":
                text = "".join(b.get("text", "") for b in j.get("content", []) if b.get("type") == "text")
            else:
                text = j["choices"][0]["message"]["content"]
        except Exception:
            return {"ok": False, "why": "API reply not understood"}
        text = (text or "").strip()
        if not text:
            return {"ok": False, "why": "API returned nothing"}
        return {"ok": True, "citations": [{"n": 1, "path": pv["url"], "lines": "api", "score": 0, "snippet": ""}],
                "text": mask(text)[0]}

    def approve(self, need_id: str, prov: str, by: str = "Timothy") -> dict:
        nd = self.needs().get(need_id)
        if not nd:
            return {"known": False, "citations": [], "answer": f"No need #{need_id}. /needs lists them."}
        if nd["status"] != "WAITING_PERMISSION":
            return {"known": False, "citations": [], "answer": f"Need #{need_id} is {nd['status']}; nothing to approve."}
        pv = next((p for p in self.providers() if p["name"] == prov), None)
        if pv is None:
            names = ", ".join(p["name"] for p in self.providers()) or "none set up"
            return {"known": False, "citations": [], "answer": f"No provider {prov!r}. Providers: {names}."}
        return self._dial_and_finish(nd, pv, approved_by=by)

    def _dial_and_finish(self, nd: dict, pv: dict, approved_by: str) -> dict:
        res = self._dial(pv, nd["masked_query"])
        ts = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        if not res["ok"]:
            self._append_need(dict(nd, ts=ts, status="WAITING_PERMISSION", last_try=f"{pv['name']}: {res['why']}"))
            return {"known": False, "citations": [], "mode": "dial-out failed",
                    "answer": f"Dialled {pv['name']} for need #{nd['id']} (approved by {approved_by}): {res['why']}. Need stays open."}
        self._append_need(dict(nd, ts=ts, status="ANSWERED", provider=pv["name"], approved_by=approved_by,
                               answer_sha256=hashlib.sha256(res["text"].encode()).hexdigest()))
        return {"known": True, "citations": res["citations"], "mode": f"{pv['kind']} {pv['name']} (dialled out, masked, unverified)",
                "answer": f"Need #{nd['id']} answered through {pv['name']} (approved by {approved_by}; masked query "
                          f"{nd['masked_query']!r}; unverified, check before use):\n\n" + res["text"]}

    def deny(self, need_id: str) -> dict:
        nd = self.needs().get(need_id)
        if not nd or nd["status"] != "WAITING_PERMISSION":
            return {"known": False, "citations": [], "answer": f"No open need #{need_id}."}
        self._append_need(dict(nd, ts=time.strftime("%Y-%m-%dT%H:%M:%S%z"), status="DENIED"))
        return {"known": False, "citations": [], "answer": f"Need #{need_id} denied. Nothing left the device."}

    def answer_exhaust(self, q: str, mode: str) -> dict:
        tried = []
        r = self.answer_local_model(q) if mode == "local-model" else self.answer_rules(q)
        tried.append("1 exact local match: " + ("found" if r["known"] else "nothing passed the gates"))
        if r["known"]:
            return dict(r, ladder=tried)
        w = self.answer_widened(q)
        tried.append("2 widened local match: " + ("found" if w["known"] else w["why"]))
        if w["known"]:
            return dict(w, ladder=tried)
        o = self.answer_ollama_open(q)
        tried.append("3 local model (own knowledge): " + ("answered, unverified" if o["known"] else o["why"]))
        if o["known"]:
            return dict(o, ladder=tried)
        need = self.raise_need(q, tried)
        provs = self.providers()
        auto = next((p for p in provs if p.get("pre_approved") is True), None)
        if auto is not None and need.get("saved"):
            out = self._dial_and_finish(need, auto, approved_by="pre-approved provider")
            tried.append(f"4 dial-out via pre-approved {auto['name']}: " + ("answered" if out["known"] else "failed"))
            return dict(out, ladder=tried, need=need)
        names = ", ".join(p["name"] for p in provs) or "none set up yet (workspace/providers.json)"
        tried.append("4 dial-out: waiting for permission")
        steps = "\n".join("  " + t for t in tried)
        ask = (f"\nMay I dial out? Masked question: {need['masked_query']!r}\nProviders: {names}\n"
               f"Reply /approve {need['id']} <provider>  or  /deny {need['id']}") if need.get("saved") else ("\n" + need.get("why", ""))
        return {"known": False, "citations": [], "mode": "permission needed",
                "answer": "Not found on this device yet. Tried:\n" + steps + ask, "ladder": tried, "need": need,
                "why": r.get("why")}

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
        if low.startswith("/needs"):
            open_ = [n for n in self.needs().values() if n["status"] == "WAITING_PERMISSION"]
            body = "\n".join(f"#{n['id']}  {n['masked_query']!r}" + (f"  (last try: {n['last_try']})" if n.get("last_try") else "")
                             for n in open_) or "No open needs."
            return {"known": True, "citations": [], "answer": body}
        if low.startswith("/approve"):
            parts = q.split()
            if len(parts) != 3:
                return {"known": True, "citations": [], "answer": "Usage: /approve <need id> <provider name>"}
            return self.approve(parts[1], parts[2])
        if low.startswith("/deny"):
            parts = q.split()
            if len(parts) != 2:
                return {"known": True, "citations": [], "answer": "Usage: /deny <need id>"}
            return self.deny(parts[1])
        if low.startswith("/scaffold"):
            parts = q.split()
            if len(parts) != 4:
                return {"known": True, "citations": [], "answer": "Usage: /scaffold <need_gosub|conflict_nodes|lead_filter> <bas|py|cpp> <name>"}
            return {"known": True, "citations": [], **self.scaffold(parts[1], parts[2], parts[3])}
        return self.answer_exhaust(q, mode)


if __name__ == "__main__":
    a = Agent()
    q = " ".join(sys.argv[1:]) or "/help"
    print(a.ask(q)["answer"])
