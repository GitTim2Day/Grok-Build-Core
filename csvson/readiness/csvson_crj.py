"""csvson_crj.py -- CSV -> regex extraction -> JSON stage for the CSVSON ingest manifest (2026-10-05).

Order per Timothy (2026-10-05 steer): CSV, then regex extraction, then JSON.
Record support found:
  * Drive EE3F43B4.pdf ([drive-id masked]-) "JCJ Pipeline Core":
      PH1 "Pre-CSV regex reject (bot filter)"; hook_csvson "CSV -> structured node tree -> JSON"
      returns {'data': df.to_dicts(), 'meta': {'source': 'csvson', 'ts': time.time(), 'node': node_id}};
      reject log entries {'ts','reason','text','category','context'}.
  * Gmail [gmail-id masked]: media_parser_hook csvson: {"raw": input, "format": "csv_json_hybrid"}.
The envelope below copies those names. The per-file column set is still an ASSUMPTION (UNDEF in record).
Binary bytes are never carried ("raw" stays a name reference; hex wrapper PARKED, node 2).
Stdlib only. Run after csvson_ingest_readiness.py:  python3 csvson_crj.py
"""
from __future__ import annotations
import csv, io, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FIELDS = ["name", "type", "parent", "magic_hex", "magic_ok", "size", "sha256", "utf8", "door",
          "nodes", "q", "park", "unk", "filter", "roundtrip", "roundtrip_sha_equal", "status"]
CELL = r'(?:"(?:[^"]|"")*"|[^,"\n]*)'
LINE_RX = re.compile("^" + ",".join(f"(?P<{f}>{CELL})" for f in FIELDS) + "$")
FIELD_RX = {
    "type": r"^(GIF|BMP|TIFF|XML|HTML|zip|gzip|xz|bzip2|tar|UNKNOWN)$",
    "magic_hex": r"^[0-9a-f]{0,16}$", "magic_ok": r"^(True|False|)$", "size": r"^\d+$",
    "sha256": r"^[0-9a-f]{64}$", "utf8": r"^(valid|invalid@\d+)$", "door": r"^(text|binary|none)$",
    "nodes": r"^\d+$", "q": r"^[01]$", "park": r"^[01]$", "unk": r"^[01]$",
    "roundtrip_sha_equal": r"^(True|False|)$",
    "status": r"^(INGESTED_TEXT|INGESTED_META_SHA|QUARANTINE|UNK_FLAGGED|ROUNDTRIP_FAIL)$",
}
FIELD_RX = {k: re.compile(v) for k, v in FIELD_RX.items()}


def unq(c: str) -> str:
    return c[1:-1].replace('""', '"') if len(c) >= 2 and c[0] == '"' and c[-1] == '"' else c


def crj(csv_text: str, node: str = "box"):
    """CSV text -> regex extraction (one LINE_RX per row + FIELD_RX per cell) -> JSON envelope."""
    lines = csv_text.splitlines()
    header, body = lines[0], lines[1:]
    rows, rejects = [], []
    if header != ",".join(FIELDS):
        rejects.append({"ts": time.time(), "reason": "header_mismatch", "text": header[:80], "category": "structure", "context": header[:50]})
        return None, rejects
    for i, ln in enumerate(body, 1):
        m = LINE_RX.match(ln)
        if not m:   # conflict -> log, keep moving (detect, call, return)
            rejects.append({"ts": time.time(), "reason": "regex_reject", "text": ln[:80], "category": "line_shape", "context": f"row {i}"})
            continue
        rec = {f: unq(m.group(f)) for f in FIELDS}
        bad = [f for f, rx in FIELD_RX.items() if not rx.match(rec[f])]
        if bad:
            rejects.append({"ts": time.time(), "reason": "regex_reject", "text": ln[:80], "category": "field:" + "|".join(bad), "context": f"row {i}"})
            continue
        rec["csvson"] = {"raw": rec["name"], "format": "csv_json_hybrid"}  # raw = name ref only; bytes not carried
        rows.append(rec)
    env = {"data": rows, "meta": {"source": "csvson", "ts": time.time(), "node": node,
           "order": "CSV -> regex -> JSON", "record_shape": "envelope from record; columns ASSUMPTION",
           "rejects": len(rejects)}}
    return env, rejects


def main() -> int:
    csv_text = open(os.path.join(OUT, "CSVSON_INGEST_MANIFEST.csv"), newline="").read()
    direct = json.load(open(os.path.join(OUT, "CSVSON_INGEST_MANIFEST.json")))["records"]
    env, rej = crj(csv_text)
    json.dump(env, open(os.path.join(OUT, "CSVSON_CRJ.json"), "w"), indent=1)
    cases = []
    def t(n, ok): cases.append((n, bool(ok)))
    t("crj_no_rejects_on_clean_manifest", env is not None and not rej)
    t("crj_row_count_equals_direct", env and len(env["data"]) == len(direct))
    def s(v): return "" if v is None else str(v)
    t("crj_fields_equal_direct_json", env and all(all(r[f] == s(d[f]) for f in FIELDS) for r, d in zip(env["data"], direct)))
    t("crj_envelope_meta_source_csvson", env and env["meta"]["source"] == "csvson" and "node" in env["meta"] and "ts" in env["meta"])
    t("crj_no_binary_bytes_carried", env and all(r["csvson"]["raw"] == r["name"] for r in env["data"]))
    # csv module cross-check: regex extraction agrees with csv.DictReader cell-for-cell
    dr = list(csv.DictReader(io.StringIO(csv_text)))
    t("crj_regex_agrees_with_csv_module", env and all(all(r[f] == d[f] for f in FIELDS) for r, d in zip(env["data"], dr)))
    # negative controls: tampered rows are rejected and logged; run keeps moving
    lines = csv_text.splitlines()
    bad_sha = lines[1].replace(dr[0]["sha256"], dr[0]["sha256"][:-1] + "Z")
    bad_status = lines[2].rsplit(",", 1)[0] + ",INGESTED_ANYWAY"
    bad_shape = lines[3] + ',"extra'
    tampered = "\n".join([lines[0], bad_sha, bad_status, bad_shape] + lines[4:]) + "\n"
    env2, rej2 = crj(tampered)
    t("neg_bad_sha_rejected", any("sha256" in r["category"] for r in rej2))
    t("neg_bad_status_rejected", any("status" in r["category"] for r in rej2))
    t("neg_bad_shape_rejected", any(r["category"] == "line_shape" for r in rej2))
    t("neg_run_continued_rest_ok", env2 and len(env2["data"]) == len(direct) - 3 and len(rej2) == 3)
    t("neg_reject_log_fields_match_pdf", rej2 and all(set(r) == {"ts", "reason", "text", "category", "context"} for r in rej2))
    env3, rej3 = crj("wrong,header\n" + "\n".join(lines[1:]))
    t("neg_header_mismatch_fail_closed", env3 is None and rej3 and rej3[0]["reason"] == "header_mismatch")
    out = [f"{'PASS' if ok else 'FAIL'}  {n}" for n, ok in cases]
    npass = sum(ok for _, ok in cases)
    out.append(f"SUMMARY: {npass}/{len(cases)} {'ALL PASS' if npass == len(cases) else 'FAIL'}")
    txt = "\n".join(out) + "\n"
    open(os.path.join(OUT, "SELFCHECK_CRJ_2026-10-05.txt"), "w").write(txt)
    print(txt, end="")
    return 0 if npass == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
