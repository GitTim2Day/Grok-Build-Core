"""mutants.py -- break each guard on purpose; the self-check must FAIL for every mutant (caught).
Usage: python3 mutants.py <round_label>. Mutant trees are kept under mutants_txt/<round>/ (never deleted)."""
from __future__ import annotations
import concurrent.futures as cf, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
M = [  # (name, file, old, new)
    ("formula_prefix_off", "rcrj.py", 'LEAD_SAFE = re.compile(r"^(?:\\s*[=+\\-@\\t\\r]|\')")', 'LEAD_SAFE = re.compile(r"^(?!x)x")'),
    ("formula_detect_off", "rcrj.py", '"formula_lead": re.compile(r"^\\s*[=+\\-@\\t\\r]"),', '"formula_lead": re.compile(r"^(?!x)x"),'),
    ("formula_embedded_off", "rcrj.py", '"formula_embedded": re.compile(', '"formula_embedded": re.compile(r"^(?!x)x") or re.compile('),
    ("sql_regex_off", "rcrj.py", '"sql_pattern": re.compile(', '"sql_pattern": re.compile(r"^(?!x)x") or re.compile('),
    ("nul_check_off", "rcrj.py", '    if "\\x00" in text:\n        return', '    if False:\n        return'),
    ("control_strip_off", "rcrj.py", '        clean = RX["control"].sub("", clean)\n', '        pass\n'),
    ("prompt_regex_off", "rcrj.py", '"prompt_injection": re.compile(', '"prompt_injection": re.compile(r"^(?!x)x") or re.compile('),
    ("html_regex_off", "rcrj.py", '"html_tag": re.compile(', '"html_tag": re.compile(r"^(?!x)x") or re.compile('),
    ("guard_post_always_ok", "rcrj.py", '    """Re-validate a parsed CSV row. \'\' = ok, else mismatch reason."""\n', '    """Re-validate a parsed CSV row. \'\' = ok, else mismatch reason."""\n    return ""\n'),
    ("sqlite_string_built", "rcrj.py", "        cur = self.db.execute(INS, params)", "        cur = self.db.execute(f\"INSERT INTO csvson_fallback (run_id, ts, text) VALUES ('{self.run_id}', 0, '{clean}')\")"),
    ("csv_fit_always_fits", "rcrj.py", '    """\'\' if it fits a CSV row, else the fallback reason."""\n', '    """\'\' if it fits a CSV row, else the fallback reason."""\n    return ""\n'),
    ("max_record_off", "rcrj.py", "    if len(text) > MAX_RECORD:", "    if False:"),
    ("quote_minimal", "rcrj.py", "quoting=csv.QUOTE_ALL, lineterminator", "quoting=csv.QUOTE_MINIMAL, lineterminator"),
    ("reject_field_renamed", "rcrj.py", '"category": category, "context": context}', '"cat": category, "context": context}'),
    ("wrapper_source_changed", "rcrj.py", 'env = {"data": data, "meta": {"source": "csvson"', 'env = {"data": data, "meta": {"source": "csv"'),
    ("esc_unescape_off", "rcrj.py", '        elif ln.startswith("%%ESC"):\n            recs.append({"line_no": no, "kind": "line", "text": ln[5:]})', '        elif ln.startswith("%%ESC"):\n            recs.append({"line_no": no, "kind": "line", "text": ln})'),
    ("traversal_guard_off", "to_txt.py", '    if any(p == ".." for p in re.split(r"[\\\\/]+", name)):\n        return "path_traversal"', '    if False:\n        return "path_traversal"'),
    ("absolute_guard_off", "to_txt.py", '    if name.startswith(("/", "\\\\")) or re.match(r"^[A-Za-z]:", name):', '    if False:'),
    ("stream_cap_off", "to_txt.py", "        if n > cap:\n            return b\"\", True", "        if False:\n            return b\"\", True"),
    ("ratio_check_off", "to_txt.py", 'info.file_size / info.compress_size > limits["max_ratio"]', 'False'),
    ("total_cap_off", "to_txt.py", '                budget.total += len(data)\n                if budget.total > limits["max_total"]:\n                    rej(info.filename, "bomb_total_cap"); continue', '                budget.total += len(data)'),
    ("depth_cap_off", "to_txt.py", '    if depth >= limits["max_depth"]:', '    if False:'),
    ("tar_link_guard_off", "to_txt.py", "                if m.issym() or m.islnk():", "                if False:"),
    ("defusedxml_swapped_unsafe", "to_txt.py", "        return DET.fromstring(b)  # forbids", "        import xml.etree.ElementTree as UNSAFE\n        return UNSAFE.fromstring(b)  # forbids"),
    ("mixed_encoding_off", "to_txt.py", "    if UTF8_MB.search(b):", "    if False:"),
    ("bom_utf16_off", "to_txt.py", '    if b.startswith((b"\\xff\\xfe", b"\\xfe\\xff")):\n        try:\n            return b.decode("utf-16")', '    if False:\n        try:\n            return b.decode("utf-16")'),
    ("nul_text_quarantine_off", "to_txt.py", "    elif kind in TEXT_TYPES and looks_binary(b):", "    elif False:"),
    ("marker_escape_off", "to_txt.py", '    return "\\n".join(("%%ESC" + ln) if ln.startswith("%%") else ln for ln in text.split("\\n"))', '    return text'),
    ("ocr_frame_cap_off", "to_txt.py", '    nfr = min(frames, limits["ocr_frames"])', '    nfr = frames'),
    ("ocr_node_off", "to_txt.py", "    if not (TESSERACT or pytesseract):\n        notes.append(\"node8:ocr_unavailable", "    if True:\n        notes.append(\"node8:ocr_unavailable"),
    ("ocr_fail_crashes", "to_txt.py", '        if err:\n            notes.append(f"node8:frame{fi}:{err}")', '        if err:\n            raise RuntimeError(err)'),
    ("pdf_ocr_fallback_off", "to_txt.py", '    if not (PDFTOPPM and (TESSERACT or pytesseract)):', '    if True:'),
    ("pdftoppm_writes_cwd", "to_txt.py", '"-f", str(pg), "-l", str(pg), "-singlefile", "-"]', '"-f", str(pg), "-l", str(pg), "-", "-"]'),
    ("pixel_cap_off", "to_txt.py", "    Image.MAX_IMAGE_PIXELS = 50_000_000", "    Image.MAX_IMAGE_PIXELS = None"),
    ("bas_formula_prefix_off", "rcrj_guard.bas", '2530 P$ = C$: IF SP = 1 THEN P$ = "\'" + C$', "2530 P$ = C$"),
    ("bas_sql_off", "rcrj_guard.bas", '2160 IF INSTR(U$, "DROP TABLE")', '2160 IF 0 AND INSTR(U$, "DROP TABLE")'),
    ("bas_post_always_ok", "rcrj_guard.bas", '3010 M = 0: X$ = ""', '3010 M = 0: X$ = "": RETURN'),
    ("bas_nul_off", "rcrj_guard.bas", "2020 IF N0 = 1 THEN F7 = 1: V = 1: RETURN", "2020 REM nul node removed"),
    ("bas_control_off", "rcrj_guard.bas", "2070 IF SGN(32 - A) = 1 THEN KEEP = 0", "2070 REM control strip removed"),
    # round-2 additions
    ("traversal_backslash_off", "to_txt.py", 'for p in re.split(r"[\\\\/]+", name)', 'for p in name.split("/")'),
    ("bad_record_guard_off", "rcrj.py", '        if not isinstance(rec.get("text"), str):', '        if False:'),
    # round-4 additions (ported fixes A + B, 2026-10-06)
    ("non_dict_guard_off", "rcrj.py", "        if not isinstance(rec, dict):   # malformed record", "        if False:   # malformed record"),
    ("dtd_fallback_check_off", "to_txt.py", "    if _DTD.search(b):\n        raise XmlForbidden", "    if False:\n        raise XmlForbidden"),
    ("fallback_exception_wide", "to_txt.py", "    DefusedXmlException = XmlForbidden", "    DefusedXmlException = Exception"),
    ("fallback_refusal_uncaught", "to_txt.py", "        except (DefusedXmlException, XmlForbidden) as e:", "        except DefusedXmlException as e:"),
    ("sqlite_fail_raises", "rcrj.py", '            self.errors.append(f"sqlite_error:{type(e).__name__}")\n            return None', '            raise'),
    ("csv_field_limit_off", "rcrj.py", "    csv.field_size_limit(max(csv.field_size_limit(), 4 * MAX_RECORD))\n", ""),
    ("rtf_skip_off", "to_txt.py", "                if w in RTF_SKIP:", "                if False:"),
    ("html_script_skip_off", "to_txt.py", "        if not self.skip:\n            self.out.append(d)", "        if True:\n            self.out.append(d)"),
    ("json_nest_off", "to_txt.py", '            return "\\n".join(flatten_json(obj, maxd=limits["json_flat_depth"]))', '            return "\\n".join(flatten_json(obj, maxd=10**6))'),
    ("xxe_external_allowed", "to_txt.py", "        return DET.fromstring(b)  # forbids", "        return DET.fromstring(b, forbid_entities=False, forbid_external=False)  # forbids"),
    ("member_count_cap_off", "to_txt.py", '        if budget.members > limits["max_members"]:', '        if False:'),
]


def run_one(label, m):
    name, fn, old, new = m
    d = os.path.join(HERE, "mutants_txt", label, name)
    if os.path.exists(d):
        os.replace(d, d + ".prev")
    os.makedirs(d)
    for f in ("to_txt.py", "rcrj.py", "rcrj_guard.bas"):
        shutil.copy(os.path.join(HERE, f), d)
    src = open(os.path.join(d, fn)).read()
    if src.count(old) != 1:
        return name, "BAD_MUTANT", f"pattern count {src.count(old)}"
    open(os.path.join(d, fn), "w").write(src.replace(old, new))
    env = dict(os.environ, CSVSON_MOD_DIR=d, CSVSON_OUT=os.path.join(d, "out"))
    try:
        p = subprocess.Popen([sys.executable, os.path.join(HERE, "selfcheck.py")], cwd=d, env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, text=True, start_new_session=True)
        try:
            out = p.communicate(timeout=600)[0]
        finally:
            try:
                os.killpg(p.pid, 9)   # whole group, never leave children behind
            except OSError:
                pass
    except subprocess.TimeoutExpired:
        return name, "CAUGHT", "timeout"
    open(os.path.join(d, "selfcheck_output.txt"), "w").write(out)
    summ = [ln for ln in out.splitlines() if ln.startswith("SUMMARY")]
    fails = [ln.split()[1] for ln in out.splitlines() if ln.startswith("FAIL")]
    if summ and "ALL PASS" in summ[-1]:
        return name, "SURVIVED", summ[-1]
    return name, "CAUGHT", (summ[-1] if summ else "crash: " + out.strip().splitlines()[-1][:100]) + " | " + ",".join(fails[:4])


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "r1"
    with cf.ThreadPoolExecutor(int(os.environ.get("MUTANT_WORKERS", "1"))) as ex:   # serial by default (2026-10-06)
        res = list(ex.map(lambda m: run_one(label, m), M))
    lines = [f"{st:9} {n:28} {det}" for n, st, det in res]
    caught = sum(st == "CAUGHT" for _, st, _ in res)
    lines.append(f"MUTANTS: {caught}/{len(M)} caught {'ALL CAUGHT' if caught == len(M) else 'GAPS'}")
    txt = "\n".join(lines) + "\n"
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    open(os.path.join(HERE, "out", f"MUTANTS_TXT_RCRJ_{label}.txt"), "w").write(txt)
    print(txt, end="")


if __name__ == "__main__":
    main()
