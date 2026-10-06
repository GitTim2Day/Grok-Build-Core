"""to_txt.py -- CSVSON text door: convert many file types to UTF-8 .txt (Timothy Norman, 2026-10-05/06).

Main line never dies. Each conflict = detect -> one node -> return (conflict_nodes.bas pattern):
  node 1 QUARANTINE   text-like bytes that are not UTF-8 / listed encodings, mixed encodings, XML entity bombs
  node 2 PARKED       unknown binary: hex wrapper stays parked (magic hex + sha256 + size only)
  node 6 REJECT       archive guard hits: path traversal, links/devices, size/ratio/depth/count caps
  node 7 FAILED       converter error (truncated stream, corrupt container) -- logged, run continues
  node 8 OCR_EMPTY    OCR returned nothing / failed -> metadata only, run continues
Status per result: FULL | PARTIAL | QUARANTINE | PARKED | REJECT | FAILED.
Stdlib + defusedxml + Pillow (box-installed). External tools used only if present on PATH:
  pdftotext / pdftoppm (poppler 25.03.0) and tesseract 5.5.0 (eng+osd) -- BOX ONLY, not on Timothy's devices.
Subprocess calls use argument lists, never a shell. No pip installs.
Output text conventions (read by rcrj.py):
  '%%BLOB-BEGIN <id>' ... '%%BLOB-END <id>'  multiline unit (cell / string with newlines)
  '%%NEST <path> = <compact json>'           nested structure deeper than JSON_FLAT_DEPTH
  '%%ESC'+line                               a source line that itself began with '%%' (escaped)
"""
from __future__ import annotations
import bz2, csv, email, gzip, hashlib, html.parser, io, json, lzma, os, re, shutil, subprocess, tarfile, wave, zipfile
from email import policy

try:
    import defusedxml.ElementTree as DET
    from defusedxml import DefusedXmlException
except Exception:  # pragma: no cover
    DET = None
    DefusedXmlException = None   # FIX 2026-10-06: replaced below by XmlForbidden (was Exception, which made every XML QUARANTINE)
try:
    from PIL import Image, ExifTags
    Image.MAX_IMAGE_PIXELS = 50_000_000   # decompression-bomb guard for pixel data
except Exception:  # pragma: no cover
    Image = None

LIMITS = {
    "max_input": 64 * 2**20,      # top-level file cap
    "max_member": 8 * 2**20,      # per decompressed member / stream
    "max_total": 32 * 2**20,      # per top-level file, all decompressed bytes
    "max_depth": 4,               # archive nesting
    "max_members": 2000,
    "max_ratio": 200,             # declared zip ratio cap (members > 1 MiB)
    "json_flat_depth": 8,
    "ocr_frames": 8,              # OCR frame cap (multi-page TIFF / animated GIF)
    "ocr_pdf_pages": 5,
    "ocr_timeout": 60,
    "max_pixels_ocr": 25_000_000,
}
TEXT_EXT = {".txt", ".md", ".csv", ".tsv", ".json", ".xml", ".html", ".htm", ".yaml", ".yml", ".ini", ".cfg",
            ".conf", ".log", ".bas", ".py", ".c", ".h", ".cpp", ".hpp", ".js", ".ts", ".sh", ".java", ".go",
            ".rs", ".rb", ".pl", ".sql", ".css", ".toml", ".eml", ".mbox", ".rtf", ".svg"}
CODE_EXT = {".bas", ".py", ".c", ".h", ".cpp", ".hpp", ".js", ".ts", ".sh", ".java", ".go", ".rs", ".rb", ".pl",
            ".sql", ".css", ".toml"}
ENCODINGS_TRIED = ["utf-32 (BOM)", "utf-8-sig (BOM)", "utf-16 (BOM)", "utf-8 (strict)", "cp1252 (strict + plausibility)"]
TESSERACT = shutil.which("tesseract")
PDFTOTEXT = shutil.which("pdftotext")
PDFTOPPM = shutil.which("pdftoppm")
try:
    import pytesseract  # only if already installed (it is not on the box as of 2026-10-06)
except Exception:
    pytesseract = None


def tool_versions() -> dict:
    def v(cmd):
        try:
            p = subprocess.run(cmd, capture_output=True, timeout=10, text=True)
            return (p.stdout + p.stderr).strip().splitlines()[0]
        except Exception:
            return "UNDEF (absent)"
    return {"tesseract": v([TESSERACT, "--version"]) if TESSERACT else "UNDEF (absent)",
            "pdftotext": v([PDFTOTEXT, "-v"]) if PDFTOTEXT else "UNDEF (absent)",
            "pytesseract": "present" if pytesseract else "absent (subprocess used)"}


class Budget:
    def __init__(self, limits):
        self.limits, self.total, self.members = limits, 0, 0


class Res(dict):
    """One converted item. Keys: name type status text nodes notes sha256 size encoding converter depth parent."""


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def esc_lines(text: str) -> str:
    return "\n".join(("%%ESC" + ln) if ln.startswith("%%") else ln for ln in text.split("\n"))


# ------------------------------------------------------------------ encodings
UTF8_MB = re.compile(rb"[\xc2-\xdf][\x80-\xbf]|[\xe0-\xef][\x80-\xbf]{2}|[\xf0-\xf4][\x80-\xbf]{3}")
BAD_C0 = re.compile(r"[\x00-\x08\x0b\x0e-\x1f]")


def decode_text(b: bytes):
    """-> (text, encoding, reason). text None = not decodable by the listed encodings (fail closed)."""
    if b.startswith((b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff")):
        try:
            return b.decode("utf-32"), "utf-32-bom", ""
        except UnicodeDecodeError:
            return None, "", "bad_utf32_bom"
    if b.startswith(b"\xef\xbb\xbf"):
        try:
            return b[3:].decode("utf-8"), "utf-8-bom", ""
        except UnicodeDecodeError:
            return None, "", "bad_utf8_after_bom"
    if b.startswith((b"\xff\xfe", b"\xfe\xff")):
        try:
            return b.decode("utf-16"), "utf-16-bom", ""
        except UnicodeDecodeError:
            return None, "", "bad_utf16_bom"
    try:
        return b.decode("utf-8"), "utf-8", ""
    except UnicodeDecodeError as e:
        pos = e.start
    if UTF8_MB.search(b):
        return None, "", f"mixed_encoding (invalid utf-8 @{pos} plus valid utf-8 multibyte sequences)"
    try:
        t = b.decode("cp1252")
    except UnicodeDecodeError:
        return None, "", f"invalid_utf8@{pos}; cp1252 undefined byte"
    if BAD_C0.search(t):
        return None, "", f"invalid_utf8@{pos}; control bytes present (binary-like)"
    return t, "cp1252-detected", ""


def looks_binary(b: bytes) -> bool:
    head = b[:4096]
    if not head:
        return False
    if b"\x00" in head and not head.startswith((b"\xff\xfe", b"\xfe\xff", b"\x00\x00\xfe\xff")):
        return True
    return False


# ------------------------------------------------------------------ type sniffing
def sniff(name: str, b: bytes) -> str:
    ext = os.path.splitext(name.lower())[1]
    if b.startswith(b"PK\x03\x04") or b.startswith(b"PK\x05\x06"):
        try:
            with zipfile.ZipFile(io.BytesIO(b)) as z:
                names = set(z.namelist())
                if "mimetype" in names:
                    mt = z.read("mimetype")[:100]
                    if b"opendocument.text" in mt:
                        return "ODT"
                    if b"opendocument.spreadsheet" in mt:
                        return "ODS"
                if "[Content_Types].xml" in names:
                    if any(n.startswith("word/") for n in names):
                        return "DOCX"
                    if any(n.startswith("xl/") for n in names):
                        return "XLSX"
                    if any(n.startswith("ppt/") for n in names):
                        return "PPTX"
        except Exception:
            pass
        return "ZIP"
    if b.startswith(b"\x1f\x8b"):
        return "GZIP"
    if b.startswith(b"\xfd7zXZ\x00"):
        return "XZ"
    if b.startswith(b"BZh"):
        return "BZIP2"
    if len(b) > 262 and b[257:262] == b"ustar":
        return "TAR"
    if b.startswith(b"%PDF-"):
        return "PDF"
    if b.startswith((b"GIF87a", b"GIF89a")):
        return "GIF"
    if b.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG"
    if b.startswith(b"\xff\xd8\xff"):
        return "JPEG"
    if b.startswith((b"II*\x00", b"MM\x00*")):
        return "TIFF"
    if b.startswith(b"BM") and len(b) > 26:
        return "BMP"
    if b.startswith(b"RIFF") and b[8:12] == b"WAVE":
        return "WAV"
    if b.lstrip()[:5] == b"{\\rtf":
        return "RTF"
    if ext == ".mbox" or (b.startswith(b"From ") and b"\nFrom:" in b[:4096]):
        return "MBOX"
    if ext == ".eml":
        return "EML"
    m = {".md": "MD", ".csv": "CSV", ".tsv": "TSV", ".json": "JSON", ".xml": "XML", ".svg": "XML",
         ".html": "HTML", ".htm": "HTML", ".yaml": "YAML", ".yml": "YAML", ".ini": "INI", ".cfg": "INI",
         ".conf": "INI", ".log": "LOG", ".txt": "TXT", ".bas": "BASIC"}
    if ext in m:
        return m[ext]
    if ext in CODE_EXT:
        return "CODE"
    s = b.lstrip(b"\xef\xbb\xbf \t\r\n")[:64].lower()
    if s.startswith(b"<?xml"):
        return "XML"
    if s.startswith((b"<!doctype html", b"<html")):
        return "HTML"
    if re.match(rb"^(?:[A-Za-z][A-Za-z0-9-]*: .*\r?\n){3,}", b[:2048]):
        return "EML"
    return "UNKNOWN"


# ------------------------------------------------------------------ helpers
class _HTMLText(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.scripts, self.tags = [], 0, 0, 0
    def handle_starttag(self, tag, attrs):
        self.tags += 1
        if tag in ("script", "style"):
            self.skip += 1
            self.scripts += tag == "script"
        if tag in ("br", "p", "div", "li", "tr", "h1", "h2", "h3", "h4", "title"):
            self.out.append("\n")
        for k, v in attrs:
            if k in ("alt", "title") and v:
                self.out.append(f"\n[{k}] {v}\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if tag in ("p", "div", "li", "tr", "td", "th", "title"):
            self.out.append("\n")
    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)


def html_to_text(s: str):
    p = _HTMLText()
    p.feed(s)
    p.close()
    lines = [re.sub(r"[ \t\r\f\v]+", " ", ln).strip() for ln in "".join(p.out).split("\n")]
    return "\n".join(ln for ln in lines if ln), p.scripts


def capped_read(fobj, cap: int):
    """Stream-read at most cap bytes; returns (data, exceeded)."""
    chunks, n = [], 0
    while True:
        c = fobj.read(65536)
        if not c:
            return b"".join(chunks), False
        n += len(c)
        if n > cap:
            return b"", True
        chunks.append(c)


def unsafe_member(name: str) -> str:
    if "\x00" in name:
        return "nul_in_name"
    if name.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", name):
        return "absolute_path"
    if any(p == ".." for p in re.split(r"[\\/]+", name)):
        return "path_traversal"
    return ""


def localname(tag) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else str(tag)


class XmlForbidden(ValueError):
    """FIX 2026-10-06: DTD / entity declaration refused by the stdlib fallback parser."""


if DefusedXmlException is None:
    DefusedXmlException = XmlForbidden
_DTD = re.compile(rb"<!\s*(?:DOCTYPE|ENTITY)|<\x00!\x00|\x00<\x00!", re.I)


def xml_parse(b: bytes):
    if DET is not None:
        return DET.fromstring(b)  # forbids entity expansion / external entities (XXE, billion laughs)
    # FIX 2026-10-06 (ported from edge-canvas-kit vendored copy):
    # defusedxml absent (bare Pi) -> fail closed on ANY DTD/entity declaration, else stdlib ElementTree
    # (with no DTD there is nothing to expand and no external entity to fetch).
    if _DTD.search(b):
        raise XmlForbidden("DTD/entity declaration refused (defusedxml absent; stdlib fallback)")
    import xml.etree.ElementTree as _ET
    return _ET.fromstring(b)


def flatten_json(obj, path="$", depth=0, out=None, maxd=8):
    out = [] if out is None else out
    if isinstance(obj, (dict, list)) and depth >= maxd:
        out.append(f"%%NEST {path} = " + json.dumps(obj, ensure_ascii=False, separators=(",", ":")))
        return out
    if isinstance(obj, dict):
        if not obj:
            out.append(f"{path} = {{}}")
        for k, v in obj.items():
            flatten_json(v, f"{path}.{k}", depth + 1, out, maxd)
    elif isinstance(obj, list):
        if not obj:
            out.append(f"{path} = []")
        for i, v in enumerate(obj):
            flatten_json(v, f"{path}[{i}]", depth + 1, out, maxd)
    else:
        v = obj if isinstance(obj, str) else json.dumps(obj)
        if isinstance(v, str) and ("\n" in v or "\r" in v):
            out.append(f"%%BLOB-BEGIN {path}")
            out.extend(esc_lines(v.replace("\r\n", "\n").replace("\r", "\n")).split("\n"))
            out.append(f"%%BLOB-END {path}")
        else:
            out.append(f"{path} = {v}")
    return out


def e1(s: str) -> str:
    return ("%%ESC" + s) if s.startswith("%%") else s


def cell_line(label: str, v: str) -> list:
    if "\n" in v or "\r" in v:
        return [f"%%BLOB-BEGIN {label}"] + esc_lines(v.replace("\r\n", "\n").replace("\r", "\n")).split("\n") + [f"%%BLOB-END {label}"]
    return [f"{label}: {v}"]


# ------------------------------------------------------------------ OCR node (tesseract, box only)
def ocr_png_bytes(png: bytes, limits) -> tuple[str, str]:
    """-> (text, err). Subprocess with argument list; no shell. pytesseract used only if installed."""
    if pytesseract is not None and Image is not None:
        try:
            return pytesseract.image_to_string(Image.open(io.BytesIO(png)), lang="eng"), ""
        except Exception as e:
            return "", f"pytesseract_error:{type(e).__name__}"
    if not TESSERACT:
        return "", "tesseract_absent"
    try:
        p = subprocess.run([TESSERACT, "stdin", "stdout", "-l", "eng", "--psm", "3"], input=png,
                           capture_output=True, timeout=limits["ocr_timeout"],
                           env=dict(os.environ, OMP_THREAD_LIMIT="1"))   # one thread: no CPU oversubscription
    except subprocess.TimeoutExpired:
        return "", "ocr_timeout"
    except Exception as e:
        return "", f"ocr_exec_error:{type(e).__name__}"
    if p.returncode != 0:
        return "", f"ocr_rc{p.returncode}"
    t, _, why = decode_text(p.stdout)
    return (t or ""), ("" if t is not None else "ocr_output_not_utf8:" + why)


def frame_png(im) -> bytes:
    fr = im.convert("L")
    w, h = fr.size
    if max(w, h) < 1000:   # small images: upscale for tesseract
        k = max(1, min(4, 1000 // max(1, max(w, h))))
        fr = fr.resize((w * k, h * k))
    buf = io.BytesIO()
    fr.save(buf, "PNG")
    return buf.getvalue()


# ------------------------------------------------------------------ converters: return (text, status, notes[], children[])
def c_text(name, b, kind, limits, budget, depth):
    t, enc, why = decode_text(b)
    if t is None:
        return None, "QUARANTINE", [f"node1:{why}"], []
    notes = [f"encoding={enc}"] + (["node1_detected:cp1252 (not utf-8; flagged)"] if enc == "cp1252-detected" else [])
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    if kind == "JSON":
        try:
            obj = json.loads(t)
            return "\n".join(flatten_json(obj, maxd=limits["json_flat_depth"])), "FULL", notes + ["json_flattened"], []
        except (ValueError, RecursionError) as e:
            return esc_lines(t), "PARTIAL", notes + [f"json_invalid:{type(e).__name__} (kept as plain text)"], []
    if kind == "XML":
        try:
            root = xml_parse(t.encode("utf-8"))
        except (DefusedXmlException, XmlForbidden) as e:   # FIX 2026-10-06: fallback refusal is QUARANTINE too
            return None, "QUARANTINE", notes + [f"node1:xml_forbidden:{type(e).__name__}"], []
        except Exception as e:
            return esc_lines(t), "PARTIAL", notes + [f"xml_parse_error:{type(e).__name__} (kept as plain text)"], []
        out = []
        def walk(el, path):
            p = f"{path}/{localname(el.tag)}"
            for k, v in el.attrib.items():
                out.append(f"{p}@{localname(k)} = {v}")
            if el.text and el.text.strip():
                out.extend(cell_line(p, el.text.strip()))
            for ch in el:
                walk(ch, p)
                if ch.tail and ch.tail.strip():
                    out.extend(cell_line(p + "#tail", ch.tail.strip()))
        walk(root, "")
        return "\n".join(out), "FULL", notes + ["defusedxml" if DET is not None else "stdlib-xml (no DTD allowed)"], []
    if kind == "HTML":
        txt, scripts = html_to_text(t)
        return esc_lines(txt), "FULL", notes + [f"html_text_extract; script_blocks_dropped={scripts}"], []
    if kind == "YAML":
        return esc_lines(t), "FULL", notes + ["yaml_as_text; structured parse UNDEF (PyYAML not installed)"], []
    if kind == "RTF":
        return c_rtf(t, notes)
    return esc_lines(t), "FULL", notes, []


RTF_SKIP = {"fonttbl", "colortbl", "stylesheet", "info", "pict", "header", "footer", "object", "themedata",
            "datastore", "latentstyles", "listtable", "listoverridetable", "rsidtbl", "generator", "xmlnstbl"}


def c_rtf(t, notes):
    out, stack, skip, i, n, uc = [], [], False, 0, len(t), 1
    while i < n:
        c = t[i]
        if c == "{":
            stack.append(skip); i += 1
            if t.startswith("{\\*", i - 1):
                skip = True
            continue
        if c == "}":
            skip = stack.pop() if stack else False; i += 1; continue
        if c == "\\":
            m = re.match(r"\\([a-z]+)(-?\d+)? ?|\\'([0-9a-fA-F]{2})|\\(.)", t[i:], re.S)
            if not m:
                i += 1; continue
            i += m.end()
            if m.group(1):
                w, arg = m.group(1), m.group(2)
                if w in RTF_SKIP:
                    skip = True
                elif not skip:
                    if w in ("par", "line", "row"): out.append("\n")
                    elif w in ("tab", "cell"): out.append("\t")
                    elif w == "u" and arg:
                        out.append(chr(int(arg) % 65536)); i += uc
                    elif w == "uc" and arg:
                        uc = int(arg)
            elif m.group(3) and not skip:
                out.append(bytes([int(m.group(3), 16)]).decode("cp1252", "replace"))
            elif m.group(4) and not skip and m.group(4) in "\\{}":
                out.append(m.group(4))
            continue
        if not skip and c not in "\r\n":
            out.append(c)
        i += 1
    txt = "\n".join(ln.rstrip() for ln in "".join(out).split("\n"))
    return esc_lines(txt.strip("\n")), "PARTIAL", notes + ["rtf_simple_strip (formatting, tables layout, embedded objects dropped)"], []


def zip_part(z, name, limits, budget):
    info = z.getinfo(name)
    if info.file_size > limits["max_member"]:
        raise ValueError("part over max_member")
    with z.open(info) as f:
        data, over = capped_read(f, limits["max_member"])
    if over:
        raise ValueError("part over max_member (stream)")
    budget.total += len(data)
    if budget.total > limits["max_total"]:
        raise ValueError("max_total exceeded")
    return data


def c_ooxml(name, b, kind, limits, budget, depth):
    out, notes = [], []
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        names = z.namelist()
        bad = [n for n in names if unsafe_member(n)]
        if bad:
            return None, "REJECT", [f"node6:{unsafe_member(bad[0])}:{bad[0][:60]}"], []
        W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
        S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
        if kind == "DOCX":
            parts = ["word/document.xml"] + sorted(n for n in names if re.match(r"word/(header|footer)\d*\.xml$|word/(footnotes|endnotes|comments)\.xml$", n))
            for part in parts:
                if part not in names:
                    continue
                root = xml_parse(zip_part(z, part, limits, budget))
                out.append(f"## {part}")
                for p in root.iter(W + "p"):
                    buf = []
                    for el in p.iter():
                        if el.tag == W + "t" and el.text:
                            buf.append(el.text)
                        elif el.tag == W + "tab":
                            buf.append("\t")
                        elif el.tag in (W + "br", W + "cr"):
                            buf.append("\n")
                    s = "".join(buf)
                    if s.strip():
                        out.extend(cell_line("p", s) if "\n" in s else [e1(s)])
            notes.append("docx body+headers/footers/notes/comments text; images/formatting dropped")
        elif kind == "XLSX":
            shared = []
            if "xl/sharedStrings.xml" in names:
                for si in xml_parse(zip_part(z, "xl/sharedStrings.xml", limits, budget)).iter(S + "si"):
                    shared.append("".join(t.text or "" for t in si.iter(S + "t")))
            sheetnames = []
            if "xl/workbook.xml" in names:
                sheetnames = [s.get("name") for s in xml_parse(zip_part(z, "xl/workbook.xml", limits, budget)).iter(S + "sheet")]
            sheets = sorted((n for n in names if re.match(r"xl/worksheets/sheet\d+\.xml$", n)), key=lambda s: int(re.findall(r"\d+", s)[-1]))
            for idx, part in enumerate(sheets):
                sn = sheetnames[idx] if idx < len(sheetnames) else part
                for c in xml_parse(zip_part(z, part, limits, budget)).iter(S + "c"):
                    ref, typ = c.get("r", "?"), c.get("t", "")
                    f, v, isel = c.find(S + "f"), c.find(S + "v"), c.find(S + "is")
                    if typ == "s" and v is not None:
                        val = shared[int(v.text)] if v.text and v.text.isdigit() and int(v.text) < len(shared) else ""
                    elif typ == "inlineStr" and isel is not None:
                        val = "".join(t.text or "" for t in isel.iter(S + "t"))
                    else:
                        val = v.text if v is not None and v.text is not None else ""
                    if f is not None and f.text:
                        out.append(f"{sn}!{ref} formula: ={f.text}")
                    if val != "":
                        out.extend(cell_line(f"{sn}!{ref}", val))
            notes.append("xlsx cell values (cached) + formula text; number formats/dates as raw serials; charts dropped")
        elif kind == "PPTX":
            slides = sorted((n for n in names if re.match(r"ppt/(slides/slide|notesSlides/notesSlide)\d+\.xml$", n)),
                            key=lambda s: ("notes" in s, int(re.findall(r"\d+", s)[-1])))
            for part in slides:
                root = xml_parse(zip_part(z, part, limits, budget))
                out.append(f"## {part}")
                for p in root.iter(A + "p"):
                    s = "".join(t.text or "" for t in p.iter(A + "t"))
                    if s.strip():
                        out.append(e1(s))
            notes.append("pptx slide + notes text; images/layout dropped")
        elif kind in ("ODT", "ODS"):
            root = xml_parse(zip_part(z, "content.xml", limits, budget))
            T = "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}"
            TB = "{urn:oasis:names:tc:opendocument:xmlns:table:1.0}"
            def ptext(el):
                buf = []
                def rec(e):
                    if e.text: buf.append(e.text)
                    for ch in e:
                        if ch.tag == T + "s": buf.append(" " * int(ch.get(T + "c", "1")))
                        elif ch.tag == T + "tab": buf.append("\t")
                        elif ch.tag == T + "line-break": buf.append("\n")
                        else: rec(ch)
                        if ch.tail: buf.append(ch.tail)
                rec(el)
                return "".join(buf)
            if kind == "ODT":
                for el in root.iter():
                    if el.tag in (T + "p", T + "h"):
                        s = ptext(el)
                        if s.strip():
                            out.extend(cell_line("p", s) if "\n" in s else [e1(s)])
                notes.append("odt paragraphs/headings text; formatting dropped")
            else:
                for tbl in root.iter(TB + "table"):
                    tn = tbl.get(TB + "name", "Sheet")
                    for r, row in enumerate(tbl.iter(TB + "table-row"), 1):
                        col = 0
                        for cell in row:
                            rep = min(int(cell.get(TB + "number-columns-repeated", "1")), 1024)
                            s = "\n".join(ptext(p) for p in cell.iter(T + "p"))
                            for _ in range(rep):
                                col += 1
                                if s.strip():
                                    out.extend(cell_line(f"{tn}!R{r}C{col}", s))
                            if not s.strip():
                                pass
                notes.append("ods cell text (repeat capped 1024); formulas/styles dropped")
    return "\n".join(out), "FULL", notes, []


def c_pdf(name, b, kind, limits, budget, depth):
    if not PDFTOTEXT:
        return None, "PARKED", ["node2:pdftotext UNDEF (absent)"], []
    try:
        p = subprocess.run([PDFTOTEXT, "-layout", "-enc", "UTF-8", "-", "-"], input=b, capture_output=True, timeout=60)
    except subprocess.TimeoutExpired:
        return None, "FAILED", ["node7:pdftotext_timeout"], []
    if p.returncode != 0:
        return None, "FAILED", [f"node7:pdftotext_rc{p.returncode}"], []
    t, enc, why = decode_text(p.stdout)
    t = (t or "").replace("\f", "\n").replace("\r\n", "\n")
    if t.strip():
        return esc_lines("\n".join(ln.rstrip() for ln in t.split("\n")).strip("\n")), "FULL", ["pdftotext text layer"], []
    # no text layer -> OCR node (box only)
    notes = ["pdftotext returned no text"]
    if not (PDFTOPPM and (TESSERACT or pytesseract)):
        return "", "PARTIAL", notes + ["node8:ocr_unavailable"], []
    pngs = []
    for pg in range(1, limits["ocr_pdf_pages"] + 1):   # one page per call; stdin in, stdout out; writes no files
        try:
            pp = subprocess.run([PDFTOPPM, "-r", "200", "-png", "-gray", "-f", str(pg), "-l", str(pg), "-singlefile", "-"],
                                input=b, capture_output=True, timeout=120)
        except subprocess.TimeoutExpired:
            notes.append(f"node8:pdftoppm_timeout_page{pg}")
            break
        if pp.returncode != 0 or not pp.stdout.startswith(b"\x89PNG"):
            break
        pngs.append(pp.stdout)
    out = []
    for i, png in enumerate(pngs, 1):
        tx, err = ocr_png_bytes(png, limits)
        if err:
            notes.append(f"node8:page{i}:{err}")
        if tx.strip():
            out.append(f"## ocr page {i}")
            out.extend(ln.rstrip() for ln in tx.replace("\f", "").split("\n") if ln.strip())
    if out:
        return esc_lines("\n".join(out)), "PARTIAL", notes + [f"ocr_pages={len(pngs)} (tesseract eng; OCR text is machine-read, not proven)"], []
    return "", "PARTIAL", notes + ["node8:ocr_empty -> metadata only"], []


def c_image(name, b, kind, limits, budget, depth):
    if Image is None:
        return None, "PARKED", ["node2:Pillow absent"], []
    out, notes = [], []
    try:
        im = Image.open(io.BytesIO(b))
        w, h = im.size
        frames = getattr(im, "n_frames", 1)
        out += [f"format: {im.format}", f"width: {w}", f"height: {h}", f"mode: {im.mode}", f"frames: {frames}",
                f"animated: {bool(getattr(im, 'is_animated', False))}"]
        for k, v in sorted(im.info.items(), key=lambda kv: str(kv[0])):
            if isinstance(v, (bytes, bytearray)):
                out.append(f"info.{k}: <{len(v)} bytes>")
            else:
                out.append(f"info.{k}: {str(v)[:200]}")
        try:
            ex = im.getexif()
            for tag, val in ex.items():
                tn = ExifTags.TAGS.get(tag, str(tag))
                out.append(f"exif.{tn}: {str(val)[:200] if not isinstance(val, bytes) else f'<{len(val)} bytes>'}")
        except Exception:
            pass
    except Exception as e:
        return None, "FAILED", [f"node7:image_open:{type(e).__name__}"], []
    status, notes = "PARTIAL", ["image metadata"]
    if w * h > limits["max_pixels_ocr"]:
        notes.append("node8:ocr_skipped_pixel_cap")
        return "\n".join(out), status, notes, []
    if not (TESSERACT or pytesseract):
        notes.append("node8:ocr_unavailable (tesseract absent) -> metadata only")
        return "\n".join(out), status, notes, []
    got = 0
    nfr = min(frames, limits["ocr_frames"])
    if frames > nfr:
        notes.append(f"ocr_frame_cap {nfr}/{frames}")
    for fi in range(nfr):
        try:
            im.seek(fi)
            tx, err = ocr_png_bytes(frame_png(im), limits)
        except Exception as e:
            tx, err = "", f"frame_error:{type(e).__name__}"
        if err:
            notes.append(f"node8:frame{fi}:{err}")
        lines = [ln.rstrip() for ln in tx.replace("\f", "").split("\n") if ln.strip()]
        if lines:
            got += 1
            out.append(f"## ocr frame {fi}")
            out.extend(lines)
    if got:
        notes.append(f"ocr_frames_with_text={got}/{nfr} (tesseract eng; machine-read, not proven)")
    else:
        notes.append("node8:ocr_empty -> metadata only")
    return esc_lines("\n".join(out)), status, notes, []


def c_wav(name, b, kind, limits, budget, depth):
    try:
        with wave.open(io.BytesIO(b)) as w:
            ch, sw, fr, nf = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
            ct = w.getcomptype()
    except Exception as e:
        return None, "FAILED", [f"node7:wav:{type(e).__name__}:{str(e)[:60]}"], []
    out = [f"channels: {ch}", f"sample_width_bytes: {sw}", f"frame_rate: {fr}", f"frames: {nf}",
           f"duration_s: {nf / fr if fr else 0:.3f}", f"compression: {ct}"]
    return "\n".join(out), "PARTIAL", ["wav metadata only; no speech-to-text"], []


def c_email_msg(msg, label, limits, budget, depth, children, parent):
    out = [f"## {label}"]
    for h in ("From", "To", "Cc", "Date", "Subject", "Message-ID"):
        if msg.get(h) is not None:
            out.append(f"{h}: {str(msg.get(h))}")
    for part in msg.walk():
        if part.is_multipart():
            continue
        fn = part.get_filename()
        ctype = part.get_content_type()
        if fn or part.get_content_disposition() == "attachment":
            payload = part.get_payload(decode=True) or b""
            out.append(f"attachment: {fn or '(unnamed)'} ({ctype}, {len(payload)} bytes, sha256 {sha(payload)})")
            children.extend(convert(fn or "attachment.bin", payload, depth + 1, limits, budget, parent))
            continue
        if ctype in ("text/plain", "text/html"):
            try:
                body = part.get_content()
            except Exception:
                raw = part.get_payload(decode=True) or b""
                body, _, _ = decode_text(raw)
                body = body or ""
            if ctype == "text/html":
                body, _ = html_to_text(body)
            out.append(f"-- body {ctype}")
            out.extend(esc_lines(body.replace("\r\n", "\n").strip("\n")).split("\n"))
    return out


def c_email(name, b, kind, limits, budget, depth):
    children, out = [], []
    if kind == "EML":
        msg = email.message_from_bytes(b, policy=policy.default)
        out = c_email_msg(msg, "message 1", limits, budget, depth, children, name)
    else:
        chunks = re.split(rb"(?m)^From [^\n]*\n", b)
        msgs = [c for c in chunks if c.strip()]
        for i, c in enumerate(msgs, 1):
            c = re.sub(rb"(?m)^>(>*From )", rb"\1", c)
            out += c_email_msg(email.message_from_bytes(c, policy=policy.default), f"message {i}", limits, budget, depth, children, name)
    return "\n".join(out), "FULL", [f"email stdlib; attachments recursed={len(children)}"], children


def c_archive(name, b, kind, limits, budget, depth):
    children, notes = [], []
    if depth >= limits["max_depth"]:
        return None, "REJECT", ["node6:depth_cap"], []
    def add(mname, data):
        budget.members += 1
        if budget.members > limits["max_members"]:
            children.append(Res(name=mname, type="?", status="REJECT", text=None, notes=["node6:member_count_cap"], sha256="", size=0, depth=depth + 1, parent=name))
            return
        children.extend(convert(mname, data, depth + 1, limits, budget, name))
    def rej(mname, why, size=0):
        children.append(Res(name=mname, type="?", status="REJECT", text=None, notes=[f"node6:{why}"], sha256="", size=size, depth=depth + 1, parent=name))
    if kind == "ZIP":
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                why = unsafe_member(info.filename)
                if why:
                    rej(info.filename, why); continue
                if info.flag_bits & 0x1:
                    children.append(Res(name=info.filename, type="?", status="PARKED", text=None, notes=["node2:encrypted_member"], sha256="", size=info.file_size, depth=depth + 1, parent=name)); continue
                if info.file_size > 2**20 and info.compress_size and info.file_size / info.compress_size > limits["max_ratio"]:
                    rej(info.filename, f"bomb_ratio declared {info.file_size}/{info.compress_size}", info.file_size); continue
                with z.open(info) as f:
                    data, over = capped_read(f, limits["max_member"])
                if over:
                    rej(info.filename, "bomb_member_cap"); continue
                budget.total += len(data)
                if budget.total > limits["max_total"]:
                    rej(info.filename, "bomb_total_cap"); continue
                add(info.filename, data)
    elif kind == "TAR":
        with tarfile.open(fileobj=io.BytesIO(b), mode="r:") as t:
            for m in t:
                why = unsafe_member(m.name)
                if why:
                    rej(m.name, why); continue
                if m.issym() or m.islnk():
                    rej(m.name, f"link_member->{m.linkname[:60]}"); continue
                if m.isdir():
                    continue
                if not m.isfile():
                    rej(m.name, "device_or_fifo_member"); continue
                if m.size > limits["max_member"]:
                    rej(m.name, "bomb_member_cap", m.size); continue
                data, over = capped_read(t.extractfile(m), limits["max_member"])
                if over:
                    rej(m.name, "bomb_member_cap"); continue
                budget.total += len(data)
                if budget.total > limits["max_total"]:
                    rej(m.name, "bomb_total_cap"); continue
                add(m.name, data)
    else:
        opener = {"GZIP": gzip.GzipFile, "XZ": lzma.LZMAFile, "BZIP2": bz2.BZ2File}[kind]
        inner = re.sub(r"\.(gz|tgz|xz|txz|bz2|tbz2?)$", "", name, flags=re.I)
        if inner == name:
            inner = name + ".out"
        if re.search(r"\.t(gz|xz|bz2?)$", name, re.I):
            inner += ".tar"
        try:
            with opener(fileobj=io.BytesIO(b)) if kind == "GZIP" else opener(io.BytesIO(b)) as f:
                data, over = capped_read(f, limits["max_member"])
        except (EOFError, OSError, lzma.LZMAError) as e:
            return None, "FAILED", [f"node7:stream_error:{type(e).__name__}:{str(e)[:60]}"], []
        if over:
            return None, "REJECT", ["node6:bomb_member_cap (stream)"], []
        budget.total += len(data)
        if budget.total > limits["max_total"]:
            return None, "REJECT", ["node6:bomb_total_cap"], []
        add(inner, data)
    listing = [f"member: {c['name']} status={c['status']}" for c in children if c.get("depth") == depth + 1]
    return "\n".join(listing), "FULL", [f"archive members={len(listing)}"], children


DISPATCH = {
    "TXT": c_text, "MD": c_text, "CSV": c_text, "TSV": c_text, "JSON": c_text, "XML": c_text, "HTML": c_text,
    "YAML": c_text, "INI": c_text, "LOG": c_text, "BASIC": c_text, "CODE": c_text, "RTF": c_text,
    "DOCX": c_ooxml, "XLSX": c_ooxml, "PPTX": c_ooxml, "ODT": c_ooxml, "ODS": c_ooxml,
    "PDF": c_pdf, "GIF": c_image, "BMP": c_image, "TIFF": c_image, "PNG": c_image, "JPEG": c_image,
    "WAV": c_wav, "EML": c_email, "MBOX": c_email,
    "ZIP": c_archive, "TAR": c_archive, "GZIP": c_archive, "XZ": c_archive, "BZIP2": c_archive,
}


def convert(name: str, b: bytes, depth: int = 0, limits=None, budget=None, parent: str = "") -> list:
    """Main line: one item in, list of Res out (item first, then children). Never raises."""
    limits = limits or LIMITS
    budget = budget or Budget(limits)
    r = Res(name=name, parent=parent, depth=depth, size=len(b), sha256=sha(b), magic_hex=b[:8].hex())
    if depth == 0 and len(b) > limits["max_input"]:
        r.update(type="?", status="REJECT", text=None, notes=["node6:max_input"])
        return [r]
    kind = sniff(name, b)
    r["type"] = kind
    if kind == "UNKNOWN":
        if looks_binary(b):
            r.update(status="PARKED", text=None, notes=["node2:hex_wrapper_parked (meta+sha256 only)"])
            return [r]
        t, enc, why = decode_text(b)
        if t is None:
            r.update(status="PARKED", text=None, notes=[f"node2:hex_wrapper_parked ({why})"])
            return [r]
        kind = r["type"] = "TXT"
    elif kind in TEXT_TYPES and looks_binary(b):
        r.update(status="QUARANTINE", text=None, notes=["node1:nul_bytes_in_text_type (no BOM)"])
        return [r]
    try:
        text, status, notes, children = DISPATCH[kind](name, b, kind, limits, budget, depth)
    except Exception as e:  # node 7: converter failed; main line continues
        text, status, notes, children = None, "FAILED", [f"node7:{type(e).__name__}:{str(e)[:80]}"], []
    r.update(text=text, status=status, notes=notes)
    return [r] + list(children)


TEXT_TYPES = {"TXT", "MD", "CSV", "TSV", "JSON", "XML", "HTML", "YAML", "INI", "LOG", "BASIC", "CODE", "RTF", "EML", "MBOX"}


def safe_out_name(r, i: int) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", r["name"])[-80:].lstrip(".") or "item"
    return f"{i:04d}_{base}.txt"


def write_txt(results, outdir: str) -> list:
    """Write each converted text as UTF-8 .txt (header + body). Returns rows for the per-item table."""
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for i, r in enumerate(results, 1):
        fn = ""
        if r.get("text") is not None:
            fn = safe_out_name(r, i)
            hdr = (f"%%CSVSON-TXT source={r['name']} type={r['type']} status={r['status']} sha256={r['sha256']} "
                   f"parent={r.get('parent','')} depth={r.get('depth',0)}")
            body = hdr + "\n" + r["text"] + ("\n" if not r["text"].endswith("\n") else "")
            with open(os.path.join(outdir, fn), "w", encoding="utf-8", newline="\n") as f:
                f.write(body)
        rows.append({"i": i, "name": r["name"], "parent": r.get("parent", ""), "depth": r.get("depth", 0),
                     "type": r["type"], "status": r["status"], "size": r["size"], "sha256": r["sha256"],
                     "txt": fn, "notes": "; ".join(r.get("notes", []))})
    return rows
