"""scan_source_tree_2026-10-08.py -- run an upstream source tree (C/H/Makefile) through the TXT door + RCRJ guard.
Usage: python3 scripts/scan_source_tree_2026-10-08.py <repo-root> <source-dir> <out-dir>
Read-only on the source dir. Flags are kept as data; true rejects are listed."""
import sys, os, json, glob, hashlib, collections
repo, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.join(repo, "csvson", "txt_rcrj"))
import to_txt, rcrj
files = sorted(glob.glob(os.path.join(src, "*.c")) + glob.glob(os.path.join(src, "*.h")) + [p for p in (os.path.join(src, "makefile"), os.path.join(src, "Makefile")) if os.path.exists(p)])
items, recs = [], []
for p in files:
    b = open(p, "rb").read()
    for r in to_txt.convert(os.path.basename(p), b):
        items.append({k: r.get(k) for k in ("name", "type", "status", "size", "sha256", "notes")})
        if r.get("text"):
            recs += rcrj.records_from_txt(r["text"], os.path.basename(p))
env = rcrj.run(recs, out, "SOURCE_SCAN", node="box", db_path=os.path.join(out, "fb.sqlite"))
status = collections.Counter(i["status"] for i in items)
flags = collections.Counter()
for row in env["data"]:
    fl = row.get("flags") or ""
    for f in (fl if isinstance(fl, list) else fl.split("|")):
        if f: flags[f.split(":")[0]] += 1
log = env["meta"].get("reject_log", [])
rej = [r for r in log if r["reason"] != "flagged_kept_as_data"]
print("reject_log entries", len(log), "true rejects", len(rej), "by reason", dict(collections.Counter(r["reason"] for r in log)))
print("sqlite fallback rows", env["meta"].get("sqlite_rows", env["meta"].get("fallback_rows")))
print("files", len(files), "items", len(items), "door status", dict(status))
print("records", len(recs), "rows", len(env["data"]), "rejects", len(rej))
print("flags kept as data:", dict(flags.most_common()))
for r in rej[:10]: print("REJECT", r["reason"], r["context"], repr(r["text"][:60]))
json.dump({"items": items, "flags": dict(flags), "rejects": rej}, open(os.path.join(out, "scan_summary.json"), "w"), indent=1)
