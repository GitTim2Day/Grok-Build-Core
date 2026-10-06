"""rcrj.py -- regex -> CSV -> regex -> JSON (RCRJ) for CSVSON .txt (Timothy Norman, 2026-10-05/06).

Main line (BASIC-style):
  100 FOR each record of each .txt
  110   GOSUB 2000 REGEX_GUARD_PRE      insertion prevention BEFORE CSV (flag / neutralize / reject)
  120   IF REJECT THEN GOSUB 4000 REJECT_LOG : NEXT
  130   IF NOT CSV_FIT THEN GOSUB 5000 SQLITE_FALLBACK : NEXT     (multiline blob, nested, oversize)
  140   CSV row (csv module, QUOTE_ALL, formula-safe "'" prefix)
  200 read CSV back -> GOSUB 3000 REGEX_GUARD_POST per row (re-validate + round-trip equality)
  210   IF MISMATCH THEN GOSUB 5000 SQLITE_FALLBACK (reason guard_post_mismatch)
  300 JSON in JCJ wrapper {'data': rows, 'meta': {'source': 'csvson', 'ts', 'node', ...}}
      reject log entries {'ts','reason','text','category','context'} (JCJ Pipeline Core PDF field names)
SQLite: sqlite3 stdlib, fixed DDL, parameterized '?' queries only -- never string-built SQL.
Flags never execute anything: SQL / prompt-injection / HTML markers are DATA, flagged and carried.
"""
from __future__ import annotations
import csv, hashlib, io, json, os, re, sqlite3, time

MAX_FIELD = 4096          # CSV fit cap (chars); longer -> SQLite
MAX_RECORD = 1_048_576    # hard cap (chars); longer -> REJECT (not stored anywhere)
TAMPER_HOOK = None        # TEST ONLY: callable(csv_text)->csv_text applied after write, to prove GUARD_POST catches drift
FIELDS = ["rid", "source", "src_sha256", "type", "line_no", "kind", "flags", "text"]

RX = {
    "formula_lead": re.compile(r"^\s*[=+\-@\t\r]"),
    "formula_embedded": re.compile(r"(?:^|[,;\t|]|:\s)\s*[=+@\-]\s*(?:[A-Za-z_][A-Za-z0-9_.]*\s*\(|cmd\s*\||[A-Za-z]+\|)", re.I),
    "sql_pattern": re.compile(r"(?:'\s*;?\s*(?:--|#)|;\s*(?:drop|delete|insert|update|alter|create|truncate|exec(?:ute)?|attach|pragma)\b"
                              r"|\bunion\s+(?:all\s+)?select\b|\bor\s+'?\d+'?\s*=\s*'?\d+|\bxp_cmdshell\b|/\*.*?\*/"
                              r"|\bsleep\s*\(\s*\d+\s*\)|\bwaitfor\s+delay\b|\bdrop\s+table\b)", re.I),
    "control": re.compile("[\x01-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\u200b-\u200f\u202a-\u202e\u2066-\u2069\ufeff]"),
    "prompt_injection": re.compile(r"(?:ignore\s+(?:all\s+|any\s+)?(?:the\s+)?(?:previous|prior|above)\s+(?:instructions|prompts?|rules)"
                                   r"|disregard\s+(?:all\s+|the\s+)?(?:previous|prior|above)|\byou\s+are\s+now\b|system\s+prompt"
                                   r"|<\|im_(?:start|end)\|>|\[/?INST\]|###\s*(?:instruction|system)|BEGIN\s+SYSTEM|developer\s+mode"
                                   r"|\bjailbreak\b|do\s+anything\s+now)", re.I),
    "html_tag": re.compile(r"<\s*/?\s*(?:script|iframe|object|embed|svg|img|style|link|meta|form|input|a|body|html|div|span|p)\b[^>]*>?"
                           r"|javascript\s*:|\bon[a-z]+\s*=\s*['\"]", re.I),
    "script": re.compile(r"<\s*script\b|javascript\s*:", re.I),
}
LEAD_SAFE = re.compile(r"^(?:\s*[=+\-@\t\r]|')")
POST_LINE = re.compile(r'^"(?:[^"]|"")*"(?:,"(?:[^"]|"")*"){%d}$' % (len(FIELDS) - 1))


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", "surrogatepass")).hexdigest()


def csv_safe(v: str) -> str:
    """Formula-safe prefix (OWASP): cells leading with = + - @ TAB CR (after spaces) or ' get one "'"."""
    return "'" + v if LEAD_SAFE.match(v) else v


def csv_unsafe(v: str) -> str:
    return v[1:] if v.startswith("'") else v


# ------------------------------------------------------------------ segmentation (.txt -> records)
def records_from_txt(text: str, default_source: str = "") -> list:
    lines = text.split("\n")
    meta = {"source": default_source, "type": "TXT", "sha256": ""}
    start = 0
    if lines and lines[0].startswith("%%CSVSON-TXT "):
        for m in re.finditer(r"(\w+)=(\S*)", lines[0]):
            meta[m.group(1)] = m.group(2)
        start = 1
    recs, i = [], start
    while i < len(lines):
        ln = lines[i]
        no = i + 1
        if ln.startswith("%%BLOB-BEGIN "):
            tag = ln[len("%%BLOB-BEGIN "):]
            buf, j, closed = [], i + 1, False
            while j < len(lines):
                if lines[j] == "%%BLOB-END " + tag:
                    closed = True
                    break
                buf.append(lines[j][5:] if lines[j].startswith("%%ESC") else lines[j])
                j += 1
            recs.append({"line_no": no, "kind": "blob", "text": "\n".join(buf), "tag": tag, "closed": closed})
            i = j + 1
            continue
        if ln.startswith("%%NEST "):
            recs.append({"line_no": no, "kind": "nested", "text": ln[len("%%NEST "):]})
        elif ln.startswith("%%ESC"):
            recs.append({"line_no": no, "kind": "line", "text": ln[5:]})
        elif ln.strip():
            recs.append({"line_no": no, "kind": "line", "text": ln})
        i += 1
    for r in recs:
        r.update(source=meta.get("source", default_source), type=meta.get("type", "TXT"), src_sha256=meta.get("sha256", ""))
    return recs


# ------------------------------------------------------------------ GOSUB 2000 REGEX_GUARD_PRE
def guard_pre(text: str, kind: str = "line"):
    """-> (clean_text, flags[list], verdict 'PASS'|'REJECT', reason). Detect, neutralize-or-flag, RETURN."""
    flags = []
    if "\x00" in text:
        return text.replace("\x00", ""), ["nul"], "REJECT", "nul_byte"
    if len(text) > MAX_RECORD:
        return text[:80], ["oversize_hard"], "REJECT", "oversize_hard"
    clean = text
    if RX["control"].search(clean):
        clean = RX["control"].sub("", clean)
        flags.append("control_stripped")
    if kind == "line" and ("\n" in clean or "\r" in clean):
        flags.append("multiline")
    for k in ("formula_lead", "formula_embedded", "sql_pattern", "prompt_injection", "html_tag", "script"):
        if RX[k].search(clean):
            flags.append(k)
    if clean.count('"') % 2 == 1:
        flags.append("quote_unbalanced")
    if "," in clean or '"' in clean:
        flags.append("delimiter_or_quote_present")
    if len(clean) > MAX_FIELD:
        flags.append("overlong")
    return clean, flags, "PASS", ""


def csv_fit(rec: dict, clean: str, flags: list) -> str:
    """'' if it fits a CSV row, else the fallback reason."""
    if rec["kind"] == "nested":
        return "nested_structure"
    if rec["kind"] == "blob" or "\n" in clean or "\r" in clean:
        return "multiline_blob"
    if "overlong" in flags:
        return "oversize_field"
    return ""


# ------------------------------------------------------------------ GOSUB 3000 REGEX_GUARD_POST
def guard_post(physical_line: str, parsed: list, expected: dict) -> str:
    """Re-validate a parsed CSV row. '' = ok, else mismatch reason."""
    if not POST_LINE.match(physical_line):
        return "post_line_shape"
    if len(parsed) != len(FIELDS):
        return "post_field_count"
    for f, cell in zip(FIELDS, parsed):
        want = str(expected[f])
        if cell != csv_safe(want):
            return f"post_cell_mismatch:{f}"
        if csv_unsafe(cell) != want:
            return f"post_roundtrip:{f}"
        if RX["formula_lead"].match(cell) and not cell.startswith("'"):
            return f"post_formula_live:{f}"
        if "\x00" in cell or RX["control"].search(cell):
            return f"post_control:{f}"
        if len(cell) > MAX_FIELD + 1:
            return f"post_overlong:{f}"
    return ""


# ------------------------------------------------------------------ GOSUB 5000 SQLITE_FALLBACK
DDL = ("CREATE TABLE IF NOT EXISTS csvson_fallback ("
       "id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT NOT NULL, ts REAL NOT NULL, source TEXT, src_sha256 TEXT, "
       "type TEXT, line_no INTEGER, kind TEXT, reason TEXT, flags TEXT, text TEXT, text_sha256 TEXT)")
INS = ("INSERT INTO csvson_fallback (run_id, ts, source, src_sha256, type, line_no, kind, reason, flags, text, text_sha256) "
       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
SEL = "SELECT text, text_sha256 FROM csvson_fallback WHERE id = ?"


class Fallback:
    def __init__(self, path: str, run_id: str):
        self.path, self.run_id = path, run_id
        self.db = sqlite3.connect(path)
        self.db.execute(DDL)
        self.n, self.errors = 0, []

    def put(self, rec: dict, clean: str, flags: list, reason: str) -> int:
        params = (self.run_id, time.time(), rec.get("source", ""), rec.get("src_sha256", ""), rec.get("type", ""),
                  int(rec.get("line_no", 0)), rec.get("kind", ""), reason, "|".join(flags), clean, sha(clean))
        try:
            cur = self.db.execute(INS, params)
            self.db.commit()
            rid = cur.lastrowid
            back = self.db.execute(SEL, (rid,)).fetchone()
        except sqlite3.Error as e:
            self.errors.append(f"sqlite_error:{type(e).__name__}")
            return None
        if back is None or back[0] != clean or back[1] != sha(clean):
            self.errors.append("sqlite_readback_mismatch")
            return None
        self.n += 1
        return rid

    def close(self):
        self.db.close()


def reject_entry(reason, text, category, context):
    return {"ts": time.time(), "reason": reason, "text": text[:80], "category": category, "context": context}


# ------------------------------------------------------------------ main line
def run(records: list, outdir: str, stem: str, node: str = "box", run_id: str = "", db_path: str = "") -> dict:
    os.makedirs(outdir, exist_ok=True)
    run_id = run_id or time.strftime("%Y%m%dT%H%M%S")
    fb = Fallback(db_path or os.path.join(outdir, stem + "_fallback.sqlite"), run_id)
    rejects, pending, fb_rows = [], [], []
    for n, rec in enumerate(records, 1):
        # KIT FIX 2026-10-06 (edge-canvas-kit vendored copy): dict check BEFORE building ctx, so a non-dict record
        # goes to the bad_record node and the main line continues (old order raised AttributeError).
        # PENDING port back to csvson-ingest-2026-10-05/txt_rcrj/rcrj.py and GitHub.
        if not isinstance(rec, dict):   # malformed record: reject node, continue
            rejects.append(reject_entry("bad_record", repr(rec)[:80], "structure", f"record#{n}"))
            continue
        ctx = f"{rec.get('source','')}:{rec.get('line_no','')}"
        if not isinstance(rec.get("text"), str):   # malformed record: reject node, continue
            rejects.append(reject_entry("bad_record", repr(rec)[:80], "structure", ctx))
            continue
        try:
            ln_no = int(rec.get("line_no", 0))
        except (TypeError, ValueError):
            ln_no = 0
        rec = dict(rec, kind=rec.get("kind") if rec.get("kind") in ("line", "blob", "nested") else "line", line_no=ln_no)
        try:
            clean, flags, verdict, why = guard_pre(rec["text"], rec["kind"])                  # GOSUB 2000
        except Exception as e:   # node error: log, continue
            rejects.append(reject_entry("guard_pre_error", rec["text"][:80], type(e).__name__, ctx))
            continue
        if verdict == "REJECT":
            rejects.append(reject_entry(why, clean, "guard_pre:" + "|".join(flags), ctx))  # GOSUB 4000
            continue
        for f in flags:
            if f in ("formula_lead", "formula_embedded", "sql_pattern", "prompt_injection", "html_tag", "script", "control_stripped"):
                rejects.append(reject_entry("flagged_kept_as_data", clean, f, ctx))
        reason = csv_fit(rec, clean, flags)
        if reason:                                                                          # GOSUB 5000
            rid = fb.put(rec, clean, flags, reason)
            if rid is None:   # SQLite node failed: log it, main line continues (record held, not lost silently)
                rejects.append(reject_entry("sqlite_write_failed", clean, fb.errors[-1], ctx))
                continue
            fb_rows.append({"sqlite_id": rid, "reason": reason, "context": ctx})
            rejects.append(reject_entry("sqlite_fallback", clean, reason, ctx))
            continue
        pending.append({"rid": n, "source": rec.get("source", ""), "src_sha256": rec.get("src_sha256", ""),
                        "type": rec.get("type", ""), "line_no": rec.get("line_no", 0), "kind": rec["kind"],
                        "flags": "|".join(flags), "text": clean, "_rec": rec, "_flags": flags})
    csv_path = os.path.join(outdir, stem + ".csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writerow(FIELDS)
        for p in pending:
            w.writerow([csv_safe(str(p[k])) for k in FIELDS])
    raw = open(csv_path, encoding="utf-8", newline="").read()
    if TAMPER_HOOK is not None:
        raw = TAMPER_HOOK(raw)
    phys = raw.split("\n")[1:]
    csv.field_size_limit(max(csv.field_size_limit(), 4 * MAX_RECORD))
    try:
        parsed = list(csv.reader(io.StringIO(raw)))[1:]
    except csv.Error as e:   # whole-file parse failure: every pending row goes to SQLite via GUARD_POST mismatch
        rejects.append(reject_entry("post_csv_parse_error", str(e), "guard_post", csv_path))
        parsed = []
    data = []
    if len(parsed) != len(pending):
        rejects.append(reject_entry("post_row_count", f"{len(parsed)}!={len(pending)}", "guard_post", csv_path))
    for i, p in enumerate(pending):
        line = phys[i] if i < len(phys) else ""
        row = parsed[i] if i < len(parsed) else []
        bad = guard_post(line, row, p) if len(parsed) == len(pending) else "post_row_count"  # GOSUB 3000
        if bad:
            rid = fb.put(p["_rec"], p["text"], p["_flags"], "guard_post_mismatch:" + bad)  # GOSUB 5000
            if rid is None:
                rejects.append(reject_entry("sqlite_write_failed", p["text"], fb.errors[-1], f"{p['source']}:{p['line_no']}"))
                continue
            fb_rows.append({"sqlite_id": rid, "reason": "guard_post_mismatch:" + bad, "context": p["source"]})
            rejects.append(reject_entry("guard_post_mismatch", p["text"], bad, f"{p['source']}:{p['line_no']}"))
            continue
        d = {k: (csv_unsafe(c) if k != "rid" else int(c)) for k, c in zip(FIELDS, row)}
        d["line_no"] = int(d["line_no"])
        d["csv_safe_prefixed"] = row[FIELDS.index("text")].startswith("'")
        data.append(d)
    fb.close()
    env = {"data": data, "meta": {"source": "csvson", "ts": time.time(), "node": node, "run_id": run_id, "sqlite_errors": fb.errors,
           "order": "txt -> REGEX_GUARD_PRE -> CSV -> REGEX_GUARD_POST -> JSON (fallback SQLite)",
           "counts": {"records": len(records), "csv_rows": len(data), "sqlite_rows": len(fb_rows),
                      "rejected": sum(1 for r in rejects if r["reason"] in ("nul_byte", "oversize_hard", "bad_record")),
                      "held_errors": sum(1 for r in rejects if r["reason"] in ("sqlite_write_failed", "guard_pre_error")),
                      "flag_entries": sum(1 for r in rejects if r["reason"] == "flagged_kept_as_data")},
           "sqlite": os.path.basename(fb.path), "sqlite_rows": fb_rows, "reject_log": rejects}}
    json_path = os.path.join(outdir, stem + ".json")
    s = json.dumps(env, ensure_ascii=True, indent=1)
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(s)
    env["_json_roundtrip_equal"] = json.loads(s)["data"] == data
    env["_paths"] = {"csv": csv_path, "json": json_path, "sqlite": fb.path}
    return env
