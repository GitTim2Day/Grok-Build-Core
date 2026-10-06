"""csvson_ingest_readiness.py -- box-only CSVSON ingest readiness test (2026-10-05).

Scope: synthetic/public samples generated HERE for GIF, BMP, TIFF, XML, HTML, zip,
gzip, xz, bzip2, tar. Nothing from the other Grok sitting is on this box; nothing
here touches Timothy's devices. Nothing is published.

CSVSON short form (Drive [drive-id masked], sha e46bc54b...): file type -> that type's
filter -> CSVSON -> devices or the world.  JCJ proof: JSON, regex, CSV or SQLite,
regex, JSON.  2025-08-03 mail [gmail-id masked]: JSON-to-CSV / CSV-to-JSON, errors
logged in amendable CSVs.
RECORD SHAPE IS UNDEF in the record. The columns below are an ASSUMPTION
(literal reading: one CSV row + one JSON record per file, errors to an append CSV).

Conflicts use conflict_nodes.py (sha 64b186c2...): detect, call one node, return.
  node 1 (NEED=1): text door met non-UTF-8 -> Q=1 QUARANTINE flag; run continues.
  node 2 (NEED=2): binary content would need a hex wrapper -> PARK=1 (not installed);
                   binary types ingest as metadata + sha256 only.
  unknown type    -> UNK flag; run continues.
Stdlib + already-installed Pillow only. Run: python3 csvson_ingest_readiness.py
"""
from __future__ import annotations

import bz2, csv, gzip, hashlib, html.parser, io, json, lzma, os, re, sys, tarfile, zipfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/workspace/conflict-nodes-build")
import conflict_nodes as cn  # noqa: E402

try:
    from PIL import Image
    PIL_VERSION = Image.__version__ if hasattr(Image, "__version__") else __import__("PIL").__version__
except Exception:  # fail closed: no Pillow -> raw-bytes path only
    Image = None
    PIL_VERSION = None

SAMPLES = os.path.join(HERE, "samples")
RT = os.path.join(HERE, "roundtrip")
OUT = os.path.join(HERE, "out")
for d in (SAMPLES, RT, OUT):
    os.makedirs(d, exist_ok=True)

CSV_FIELDS = ["name", "type", "parent", "magic_hex", "magic_ok", "size", "sha256",
              "utf8", "door", "nodes", "q", "park", "unk", "filter",
              "roundtrip", "roundtrip_sha_equal", "status"]

MAGIC = {  # type -> (offset, bytes)
    "GIF": [(0, b"GIF87a"), (0, b"GIF89a")],
    "BMP": [(0, b"BM")],
    "TIFF": [(0, b"II*\x00"), (0, b"MM\x00*")],
    "zip": [(0, b"PK\x03\x04"), (0, b"PK\x05\x06")],
    "gzip": [(0, b"\x1f\x8b")],
    "xz": [(0, b"\xfd7zXZ\x00")],
    "bzip2": [(0, b"BZh")],
    "tar": [(257, b"ustar")],
}
TEXT_TYPES = {"XML", "HTML"}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def write(path: str, b: bytes) -> bytes:
    with open(path, "wb") as f:
        f.write(b)
    with open(path, "rb") as f:
        return f.read()


def magic_ok(typ: str, b: bytes) -> bool | None:
    if typ in TEXT_TYPES:
        head = b.lstrip()[:64].lower()
        if typ == "XML":
            return head.startswith(b"<?xml") or head.startswith(b"<")
        return head.startswith(b"<!doctype html") or head.startswith(b"<html")
    if typ not in MAGIC:
        return None
    return any(b[o:o + len(m)] == m for o, m in MAGIC[typ])


def sniff(b: bytes) -> str:
    """Type filter by content (magic), not by extension."""
    for typ, sigs in MAGIC.items():
        if any(b[o:o + len(m)] == m for o, m in sigs):
            return typ
    head = b.lstrip()[:64].lower()
    if head.startswith(b"<!doctype html") or head.startswith(b"<html"):
        return "HTML"
    if head.startswith(b"<?xml"):
        return "XML"
    return "UNKNOWN"


# ---------------------------------------------------------------- samples (synthetic)
def make_image(mode="RGB", size=(16, 8), seed=0):
    im = Image.new(mode, size)
    px = []
    for y in range(size[1]):
        for x in range(size[0]):
            px.append(((x * 16 + seed * 7) % 256 | 0x80, (y * 32 + 30) % 256, (x * y + 90 + seed) % 256))
    im.putdata(px)
    return im


def gen_samples() -> dict:
    s = {}
    if Image is not None:
        im = make_image()
        bio = io.BytesIO(); im.convert("P", palette=Image.ADAPTIVE, colors=64).save(bio, "GIF"); s["sample.gif"] = bio.getvalue()
        bio = io.BytesIO(); im.save(bio, "BMP"); s["sample.bmp"] = bio.getvalue()
        bio = io.BytesIO(); im.save(bio, "TIFF", compression="raw"); s["sample.tif"] = bio.getvalue()
        bio = io.BytesIO(); im.save(bio, "TIFF", compression="tiff_lzw"); s["sample_lzw.tif"] = bio.getvalue()
        frames = [make_image(seed=k) for k in range(3)]
        bio = io.BytesIO(); frames[0].save(bio, "TIFF", save_all=True, append_images=frames[1:], compression="raw"); s["sample_multipage.tif"] = bio.getvalue()
        gframes = [f.convert("P", palette=Image.ADAPTIVE, colors=32) for f in frames]
        bio = io.BytesIO(); gframes[0].save(bio, "GIF", save_all=True, append_images=gframes[1:], duration=100, loop=0, disposal=1, optimize=False); s["sample_animated.gif"] = bio.getvalue()
    else:  # fail closed: hand-built minimal GIF/BMP/TIFF not attempted; recorded as gap
        pass
    s["sample.xml"] = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                       '<csvson sample="synthetic" date="2026-10-05">\n'
                       '  <row id="1" type="GIF">public demo</row>\n'
                       '  <row id="2" type="TXT">caf\u00e9 \u2014 UTF-8 text door</row>\n'
                       '</csvson>\n').encode("utf-8")
    s["sample.html"] = ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">'
                        '<title>CSVSON demo</title></head>\n<body><!-- synthetic -->'
                        '<p class="a">Leaves are not fruit &amp; roots stay &#8212; demo.</p>'
                        '<br/><img src="x.gif" alt="none"></body></html>\n').encode("utf-8")
    payload = s["sample.xml"]  # stream payload = one well-formed XML doc
    zbio = io.BytesIO()
    with zipfile.ZipFile(zbio, "w", zipfile.ZIP_DEFLATED) as z:
        for n in ("sample.xml", "sample.html") + (("sample.gif",) if "sample.gif" in s else ()):
            zi = zipfile.ZipInfo(n, date_time=(2026, 10, 5, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, s[n])
    s["sample.zip"] = zbio.getvalue()
    s["sample.txt.gz"] = gzip.compress(payload, mtime=0)
    s["sample.txt.xz"] = lzma.compress(payload, format=lzma.FORMAT_XZ)
    s["sample.txt.bz2"] = bz2.compress(payload)
    tbio = io.BytesIO()
    with tarfile.open(fileobj=tbio, mode="w", format=tarfile.USTAR_FORMAT) as t:
        for n in ("sample.xml", "sample.html") + (("sample.bmp",) if "sample.bmp" in s else ()):
            ti = tarfile.TarInfo(n); ti.size = len(s[n]); ti.mtime = 0; ti.mode = 0o644
            t.addfile(ti, io.BytesIO(s[n]))
    s["sample.tar"] = tbio.getvalue()
    s["sample.tar.gz"] = gzip.compress(s["sample.tar"], mtime=0)  # nested: gzip -> tar -> members
    # negative controls (must NOT kill the run)
    s["neg_latin1.xml"] = '<?xml version="1.0"?><r>caf\u00e9</r>\n'.encode("latin-1")  # non-UTF-8 text
    s["neg_unknown.bin"] = bytes([0x00, 0xFF, 0x13, 0x37]) * 8                          # unknown type
    s["neg_truncated.gz"] = gzip.compress(payload, mtime=0)[:20]                          # corrupt container
    return s


# ---------------------------------------------------------------- per-type round-trips
def px_sha(im) -> str:
    return sha(im.mode.encode() + repr(im.size).encode() + im.tobytes())


def rt_image(b: bytes, fmt: str, **save_kw):
    """decode -> re-encode -> decode; compare every frame's pixels."""
    src = Image.open(io.BytesIO(b)); frames_a = []
    n = getattr(src, "n_frames", 1)
    for i in range(n):
        src.seek(i); frames_a.append(src.convert("RGB").copy())
    bio = io.BytesIO()
    if n > 1:
        if fmt == "GIF":
            pf = [f.convert("P", palette=Image.ADAPTIVE, colors=256) for f in frames_a]
            pf[0].save(bio, fmt, save_all=True, append_images=pf[1:], optimize=False, disposal=1)
        else:
            frames_a[0].save(bio, fmt, save_all=True, append_images=frames_a[1:], **save_kw)
    else:
        (frames_a[0].convert("P", palette=Image.ADAPTIVE, colors=256) if fmt == "GIF" else frames_a[0]).save(bio, fmt, **save_kw)
    dst = Image.open(io.BytesIO(bio.getvalue())); frames_b = []
    for i in range(getattr(dst, "n_frames", 1)):
        dst.seek(i); frames_b.append(dst.convert("RGB").copy())
    a = sha("".join(px_sha(f) for f in frames_a).encode()); bb = sha("".join(px_sha(f) for f in frames_b).encode())
    meta = {"width": src.size[0], "height": src.size[1], "mode": src.mode, "frames": n,
            "frames_after": len(frames_b), "pixel_sha_before": a, "pixel_sha_after": bb,
            "reencode_bytes_identical": bio.getvalue() == b}
    return a == bb and n == len(frames_b), f"pixel decode/re-encode/decode ({n} frame{'s' if n > 1 else ''})", meta


def rt_xml(b: bytes):
    root = ET.fromstring(b)
    again = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    c1 = ET.canonicalize(b.decode("utf-8")); c2 = ET.canonicalize(again.decode("utf-8"))
    return sha(c1.encode()) == sha(c2.encode()), "xml.etree parse/serialize/reparse, C14N 2.0 sha", {
        "c14n_sha_before": sha(c1.encode()), "c14n_sha_after": sha(c2.encode()), "elements": sum(1 for _ in root.iter())}


class _Rebuild(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False); self.out = []; self.tags = 0
    def handle_starttag(self, tag, attrs): self.out.append(self.get_starttag_text()); self.tags += 1
    def handle_startendtag(self, tag, attrs): self.out.append(self.get_starttag_text()); self.tags += 1
    def handle_endtag(self, tag): self.out.append(f"</{tag}>")
    def handle_data(self, data): self.out.append(data)
    def handle_comment(self, data): self.out.append(f"<!--{data}-->")
    def handle_decl(self, decl): self.out.append(f"<!{decl}>")
    def handle_entityref(self, name): self.out.append(f"&{name};")
    def handle_charref(self, name): self.out.append(f"&#{name};")
    def handle_pi(self, data): self.out.append(f"<?{data}>")


def rt_html(b: bytes):
    p = _Rebuild(); p.feed(b.decode("utf-8")); p.close()
    rebuilt = "".join(p.out).encode("utf-8")
    return sha(rebuilt) == sha(b), "html.parser token rebuild, byte sha", {"rebuilt_sha": sha(rebuilt), "tags": p.tags}


def rt_zip(b: bytes):
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        bad = z.testzip(); members = {i.filename: z.read(i) for i in z.infolist()}
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED) as z:
        for n, d in members.items():
            zi = zipfile.ZipInfo(n, date_time=(2026, 10, 5, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; z.writestr(zi, d)
    with zipfile.ZipFile(io.BytesIO(bio.getvalue())) as z:
        back = {i.filename: z.read(i) for i in z.infolist()}
    ok = bad is None and {k: sha(v) for k, v in members.items()} == {k: sha(v) for k, v in back.items()}
    return ok, "zipfile read/rewrite/read, member sha", {"members": len(members),
            "archive_bytes_identical": bio.getvalue() == b}, members


def rt_stream(b: bytes, mod, kind):
    payload = mod.decompress(b)
    again = gzip.compress(payload, mtime=0) if kind == "gzip" else (lzma.compress(payload, format=lzma.FORMAT_XZ) if kind == "xz" else mod.compress(payload))
    back = mod.decompress(again)
    return sha(payload) == sha(back), f"{mod.__name__} decompress/compress/decompress, payload sha", {
        "payload_sha": sha(payload), "payload_size": len(payload), "archive_bytes_identical": again == b}, {"payload": payload}


def rt_tar(b: bytes):
    with tarfile.open(fileobj=io.BytesIO(b), mode="r:") as t:
        members = {m.name: t.extractfile(m).read() for m in t.getmembers() if m.isfile()}
    bio = io.BytesIO()
    with tarfile.open(fileobj=bio, mode="w", format=tarfile.USTAR_FORMAT) as t:
        for n, d in members.items():
            ti = tarfile.TarInfo(n); ti.size = len(d); ti.mtime = 0; ti.mode = 0o644; t.addfile(ti, io.BytesIO(d))
    with tarfile.open(fileobj=io.BytesIO(bio.getvalue()), mode="r:") as t:
        back = {m.name: t.extractfile(m).read() for m in t.getmembers() if m.isfile()}
    ok = {k: sha(v) for k, v in members.items()} == {k: sha(v) for k, v in back.items()}
    return ok, "tarfile read/rewrite/read, member sha", {"members": len(members),
            "archive_bytes_identical": bio.getvalue() == b}, members


# ---------------------------------------------------------------- ingest (CSVSON record)
ERRORS = []  # amendable error log (the "liquid"); written append-only
STATES = []  # every conflict_nodes.State used, for the Bot check


def ingest(name: str, b: bytes, parent: str = "", disk_path: str | None = None) -> list:
    st = cn.State()  # boton False; nodes never set it
    STATES.append(st)
    typ = sniff(b)
    rec = {"name": name, "type": typ, "parent": parent, "magic_hex": b[:8].hex(),
           "magic_ok": magic_ok(typ, b), "size": len(b), "sha256": sha(b)}
    # byte-identical raw copy (the plain round-trip every type gets)
    copy_equal = None
    if disk_path:
        cp = write(os.path.join(RT, name.replace("/", "__") + ".copy"), b)
        copy_equal = sha(cp) == sha(b)
    # text door: strict UTF-8
    try:
        b.decode("utf-8", errors="strict"); rec["utf8"] = "valid"; utf8_ok = True
    except UnicodeDecodeError as e:
        rec["utf8"] = f"invalid@{e.start}"; utf8_ok = False
    door = "text" if typ in TEXT_TYPES else ("binary" if typ in MAGIC else "none")
    rec["door"] = door
    if door == "text" and not utf8_ok:
        cn.main_line(st, cn.NEED_NON_UTF8)        # node 1: QUARANTINE flag, no other door
    if door == "binary":
        if not utf8_ok:
            cn.main_line(st, cn.NEED_NON_UTF8)    # text door refused it -> Q flag, run continues
        cn.main_line(st, cn.NEED_HEX)             # content wrapper parked -> metadata + sha only
    if door == "none":
        cn.main_line(st, 99)                       # unknown -> UNK flag, run continues
    cn.main_line(st, cn.NEED_NONE)                 # main line keeps moving
    rec.update({"nodes": st.nodes, "q": st.q, "park": st.park, "unk": st.unk})
    children, extra = [], {"raw_copy_sha_equal": copy_equal}
    ok, how = None, ""
    try:
        if st.q and door == "text":
            ok, how = None, "not run (quarantined at text door)"
        elif typ in ("GIF", "BMP", "TIFF"):
            if Image is None:
                ok, how = copy_equal, "raw byte copy only (Pillow absent)"
            else:
                kw = {"compression": "raw"} if typ == "TIFF" else {}
                ok, how, meta = rt_image(b, typ, **kw); extra.update(meta)
        elif typ == "XML":
            ok, how, meta = rt_xml(b); extra.update(meta)
        elif typ == "HTML":
            ok, how, meta = rt_html(b); extra.update(meta)
        elif typ == "zip":
            ok, how, meta, mem = rt_zip(b); extra.update(meta); children = list(mem.items())
        elif typ == "tar":
            ok, how, meta, mem = rt_tar(b); extra.update(meta); children = list(mem.items())
        elif typ in ("gzip", "xz", "bzip2"):
            mod = {"gzip": gzip, "xz": lzma, "bzip2": bz2}[typ]
            ok, how, meta, mem = rt_stream(b, mod, typ); extra.update(meta)
            children = [(name + ":payload", mem["payload"])]
        else:
            ok, how = None, "no filter for this type"
    except Exception as e:  # filter failure is a conflict, not a crash
        ok, how = False, f"filter error: {type(e).__name__}: {e}"
    rec["filter"] = {"GIF": "Pillow", "BMP": "Pillow", "TIFF": "Pillow", "XML": "xml.etree",
                     "HTML": "html.parser", "zip": "zipfile", "tar": "tarfile", "gzip": "gzip",
                     "xz": "lzma", "bzip2": "bz2"}.get(typ, "none")
    rec["roundtrip"] = how
    rec["roundtrip_sha_equal"] = ok
    if ok is True and (copy_equal in (True, None)):
        rec["status"] = "INGESTED_TEXT" if door == "text" else "INGESTED_META_SHA"
    elif st.q and door == "text":
        rec["status"] = "QUARANTINE"
    elif st.unk:
        rec["status"] = "UNK_FLAGGED"
    else:
        rec["status"] = "ROUNDTRIP_FAIL"
    rec["detail"] = extra
    if rec["status"] not in ("INGESTED_TEXT", "INGESTED_META_SHA") or st.q or st.park or st.unk:
        ERRORS.append({"name": name, "status": rec["status"], "q": st.q, "park": st.park,
                       "unk": st.unk, "note": how})
    out = [rec]
    for cname, cdata in children:
        out += ingest(cname, cdata, parent=name)
    return out


# ---------------------------------------------------------------- JCJ manifest round-trip
FIELD_RX = {"sha256": re.compile(r"^[0-9a-f]{64}$"), "size": re.compile(r"^\d+$"),
            "magic_hex": re.compile(r"^[0-9a-f]{0,16}$"), "q": re.compile(r"^[01]$"),
            "park": re.compile(r"^[01]$"), "unk": re.compile(r"^[01]$"),
            "status": re.compile(r"^(INGESTED_TEXT|INGESTED_META_SHA|QUARANTINE|UNK_FLAGGED|ROUNDTRIP_FAIL)$")}


def row_str(r):
    return {k: ("" if r[k] is None else str(r[k])) for k in CSV_FIELDS}


def jcj_roundtrip(records):
    """JSON -> regex -> CSV -> regex -> JSON; rows must come back equal."""
    j1 = json.loads(json.dumps([row_str(r) for r in records]))
    bad1 = [(r["name"], k) for r in j1 for k, rx in FIELD_RX.items() if not rx.match(r[k])]
    buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=CSV_FIELDS, lineterminator="\n"); w.writeheader(); w.writerows(j1)
    back = list(csv.DictReader(io.StringIO(buf.getvalue())))
    bad2 = [(r["name"], k) for r in back for k, rx in FIELD_RX.items() if not rx.match(r[k])]
    j2 = json.loads(json.dumps(back))
    return j1 == j2 and not bad1 and not bad2, bad1 + bad2, buf.getvalue()


# ---------------------------------------------------------------- main + self-check
def main() -> int:
    samples = gen_samples()
    records = []
    for name in sorted(samples):
        b = write(os.path.join(SAMPLES, name), samples[name])
        records += ingest(name, b, disk_path=os.path.join(SAMPLES, name))   # one bad file never stops the loop
    jcj_ok, jcj_bad, csv_text = jcj_roundtrip(records)
    with open(os.path.join(OUT, "CSVSON_INGEST_MANIFEST.csv"), "w", newline="") as f:
        f.write(csv_text)
    meta = {"generated": "2026-10-05", "box_only": True, "published": False,
            "record_shape": "ASSUMPTION (CSVSON ingest spec UNDEF in record)",
            "csvson_source": "Drive [drive-id masked] sha256 e46bc54b036fef13f602d0207bb7536341b88cebedfbd2b3eb34483ac1938bf9",
            "conflict_nodes_sha256": sha(open(cn.__file__, "rb").read()),
            "pillow": PIL_VERSION, "python": sys.version.split()[0], "records": records}
    with open(os.path.join(OUT, "CSVSON_INGEST_MANIFEST.json"), "w") as f:
        json.dump(meta, f, indent=1, sort_keys=False)
    elog = os.path.join(OUT, "CSVSON_ERROR_LOG.csv")
    new = not os.path.exists(elog)
    with open(elog, "a", newline="") as f:  # append-only; amendable
        w = csv.DictWriter(f, fieldnames=["run", "name", "status", "q", "park", "unk", "note"], lineterminator="\n")
        if new: w.writeheader()
        for e in ERRORS: w.writerow({"run": "2026-10-05", **e})

    by = {r["name"]: r for r in records if not r["parent"]}  # top-level samples only
    kids = [r for r in records if r["parent"]]
    cases = []
    def t(n, ok): cases.append((n, bool(ok)))
    t("pillow_version_recorded", PIL_VERSION is not None and meta["pillow"] == PIL_VERSION)
    expect = {"sample.gif": "GIF", "sample_animated.gif": "GIF", "sample.bmp": "BMP", "sample.tif": "TIFF",
              "sample_lzw.tif": "TIFF", "sample_multipage.tif": "TIFF", "sample.xml": "XML", "sample.html": "HTML",
              "sample.zip": "zip", "sample.txt.gz": "gzip", "sample.txt.xz": "xz", "sample.txt.bz2": "bzip2", "sample.tar": "tar", "sample.tar.gz": "gzip"}
    for n, typ in expect.items():
        r = by.get(n)
        t(f"{n}:sniffed_{typ}", r and r["type"] == typ)
        t(f"{n}:magic_ok", r and r["magic_ok"] is True)
        t(f"{n}:roundtrip_sha_equal", r and r["roundtrip_sha_equal"] is True)
        t(f"{n}:raw_copy_sha_equal", r and r["detail"].get("raw_copy_sha_equal") is True)
        want = "INGESTED_TEXT" if typ in TEXT_TYPES else "INGESTED_META_SHA"
        t(f"{n}:status_{want}", r and r["status"] == want)
        if typ in TEXT_TYPES:
            t(f"{n}:text_door_no_nodes", r and r["q"] == 0 and r["park"] == 0 and r["nodes"] == 0)
        else:
            t(f"{n}:binary_node1_Q_node2_PARK", r and r["q"] == 1 and r["park"] == 1 and r["unk"] == 0)
    t("multipage_tif_3_frames", by["sample_multipage.tif"]["detail"].get("frames") == 3 and by["sample_multipage.tif"]["detail"].get("frames_after") == 3)
    t("animated_gif_3_frames", by["sample_animated.gif"]["detail"].get("frames") == 3)
    t("zip_children_ingested", sum(1 for r in kids if r["parent"] == "sample.zip") == 3)
    t("tar_children_ingested", sum(1 for r in kids if r["parent"] == "sample.tar") == 3)
    member_kids = [r for r in kids if ":payload" not in r["name"] and r["parent"] in ("sample.zip", "sample.tar")]
    t("member_sha_matches_top_sample", len(member_kids) == 6 and all(r["name"] in by and r["sha256"] == by[r["name"]]["sha256"] and r["status"] == by[r["name"]]["status"] for r in member_kids))
    for sp in ("sample.txt.gz", "sample.txt.xz", "sample.txt.bz2"):
        pk = [r for r in kids if r["parent"] == sp]
        t(f"{sp}:payload_reingested_as_XML_text", len(pk) == 1 and pk[0]["type"] == "XML" and pk[0]["status"] == "INGESTED_TEXT" and pk[0]["sha256"] == by["sample.xml"]["sha256"])
    tgz = [r for r in kids if r["parent"] == "sample.tar.gz"]
    t("tar_gz_nested_payload_is_tar", len(tgz) == 1 and tgz[0]["type"] == "tar" and tgz[0]["sha256"] == by["sample.tar"]["sha256"])
    t("tar_gz_grandchildren_3", sum(1 for r in kids if r["parent"] == "sample.tar.gz:payload") == 3)
    t("neg_latin1_xml_QUARANTINE", by["neg_latin1.xml"]["status"] == "QUARANTINE" and by["neg_latin1.xml"]["q"] == 1 and by["neg_latin1.xml"]["park"] == 0)
    t("neg_unknown_UNK_FLAGGED", by["neg_unknown.bin"]["status"] == "UNK_FLAGGED" and by["neg_unknown.bin"]["unk"] == 1)
    t("neg_truncated_gz_ROUNDTRIP_FAIL_not_crash", by["neg_truncated.gz"]["status"] == "ROUNDTRIP_FAIL")
    t("run_continued_after_conflicts", len([n for n in samples]) == len([r for r in records if not r["parent"]]))
    t("bot_never_enabled", len(STATES) == len(records) and all(x.boton is False and x.botskip == 0 for x in STATES))
    t("jcj_json_csv_json_equal_regex_clean", jcj_ok)
    t("error_log_has_q_park_unk", any(e["q"] for e in ERRORS) and any(e["park"] for e in ERRORS) and any(e["unk"] for e in ERRORS))
    lines = [f"{'PASS' if ok else 'FAIL'}  {n}" for n, ok in cases]
    npass = sum(ok for _, ok in cases)
    lines.append(f"SUMMARY: {npass}/{len(cases)} {'ALL PASS' if npass == len(cases) else 'FAIL'}")
    if jcj_bad: lines.append(f"JCJ regex misses: {jcj_bad}")
    txt = "\n".join(lines) + "\n"
    open(os.path.join(OUT, "SELFCHECK_2026-10-05.txt"), "w").write(txt)
    print(txt, end="")
    return 0 if npass == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
