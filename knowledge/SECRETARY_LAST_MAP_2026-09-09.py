#!/usr/bin/env python3
"""SECRETARY_LAST_MAP_2026-09-09.py -- the Secretary last map + duty as runnable Python.

Converted 2026-10-03 from the live Secretary PDFs (all copies live, Tim 2026-10-03T13:14-04:00).
Words are frozen in TEXT and checked by hash. The ladder and the save gate are code.
Run:  python3 SECRETARY_LAST_MAP_2026-09-09.py          (self-test)
      python3 SECRETARY_LAST_MAP_2026-09-09.py FILE.pdf  (identify a copy + compare words)
Do not invent a new Secretary. Cite a copy by size + hash, not by letter.
"""
import hashlib
import os
import re
import sys

SOURCES = (
    {"where": "Drive 1WQ6TfjmbommC0SUd9pxUHXT5HMe8q3oI", "size": 3292,
     "sha256": "9ce237c42694200da17814c921125442c5eec9a1d431b692c07da35b85d8e97a",
     "note": "renders with text off-page; words extract whole"},
    {"where": "Drive 1CqNgVuGNnuHaQFB4h76F7_Bq6gAwIlpC (HYBRID)", "size": 4465,
     "sha256": "b3eb1645bb4c1f038971af9f4bc72cd863ba2e3c453b5b5f50b47170943a4f36", "note": ""},
    {"where": "attachment 2026-10-03", "size": 4381,
     "sha256": "6bbef94cdeb0926a292b4e323312a442fc1137462b56fbf7ef1e1354ded85e13",
     "note": "recorded same words; not opened by this chair"},
    {"where": "other chair (automations-only)", "size": 20318,
     "sha256": "e03c769a844bf0cd24a4b2b67a5592b3848c5707550f319d86d98d54936849b8",
     "note": "not opened by this chair"},
)

LADDER = (
    (0, "Secretary: last map + duty file + PDF"),
    (1, "Gmail To timnorman730@gmail.com + CC Yahoo (THE PING; verify To/CC before speak)"),
    (2, "Notion living index + convert to skill"),
    (3, "GitHub Grok-Build-Core/knowledge"),
    (4, "Google Sheets appendable row"),
    (5, "Drive Grok_Build_Archives"),
    (6, "Disk artifacts/writer-card-RIDER"),
)
STATUSES = ("HIT", "CONTINUE", "EXHAUSTED")
BODY_WORD_COUNT = 280
BODY_WORDS_SHA256 = "e6f0984e18f9aee92d7b3f8704ab583795edd1e96d0acd963544a36b50ea180f"
_FURNITURE = re.compile(r"^(SECRETARY  \|  last map|Timothy H\. Norman  \||Page \d of 2)")

TEXT = """SECRETARY  |  last map + duty  |  2026-09-09
Timothy H. Norman  |  Grok-Build-Ledger  |  not a transfer  |  no Class B
Page 1 of 2   secretary -> local -> email shelf -> folders

Hop-skip failure / mitigation / boot priority
Same class, months running. Expected from X. Not from this chair.

The failure
Claiming the book is saved while skipping the hop he actually watches. Tonight: Notion/GitHub/Drive out, Gmail+Yahoo skipped. Secretary ladder (30 Aug) already put email shelf as rung 3. That rung was skipped.
Kin of ledger Row 3B (claiming done before verified). Tonight is Row 3D.

Save order when he says everything
0  Secretary: last map + duty file + PDF
1  Gmail To timnorman730@gmail.com + CC Yahoo  (THE PING; verify To/CC before speak)
2  Notion living index + convert to skill
3  GitHub Grok-Build-Core/knowledge
4  Google Sheets appendable row
5  Drive Grok_Build_Archives
6  Disk artifacts/writer-card-RIDER
Do not declare saved until Pri 1 is verified.

SECRETARY  |  last map + duty  |  2026-09-09
Timothy H. Norman  |  Grok-Build-Ledger  |  not a transfer  |  no Class B
Page 2 of 2   secretary -> local -> email shelf -> folders

SECRETARY duty  |  2026-09-09
Duty officer. Index, not a speechwriter. Successor of SECRETARY_2026-08-30 (Gmail 1a0515e2dff308d5).

Ladder (do not skip a rung)
secretary -> local disk -> EMAIL SHELF (To Gmail + CC Yahoo) -> photo library if a face exists -> folders (Notion, GitHub, Drive, Sheets).

HIT / CONTINUE / EXHAUSTED
HIT = file it. CONTINUE = hop now. EXHAUSTED = looked, gone, do not make it up.

Last map this sitting
MAC hive: category -> subcategory -> hive/swarm -> node = one MAC. Parties: company, owner, operator, appointed user. Ancestral Merkle. Dual identity MAC + voice + SVCT.

Reshare
These PDFs and the full retrieve suite are his and this chair's. He will reshare when this chair is allowed to receive and use them routinely. Until then: this copy, the 30 Aug shelf, and the ladder. Do not invent a new Secretary.
No Class B. No two hundred. No government-ID. Thin layer. Share, not withhold.
"""


def body_words(text):
    """Words of the map with page furniture (running head, byline, page footer) removed."""
    out = []
    for line in text.splitlines():
        if _FURNITURE.match(line.strip()):
            continue
        out.extend(line.split())
    return out


def words_sha256(words):
    return hashlib.sha256(" ".join(words).encode("utf-8")).hexdigest()


def identify_copy(data):
    """Return the SOURCES entry whose bytes match, or None. Size and hash must both match."""
    digest = hashlib.sha256(data).hexdigest()
    for src in SOURCES:
        if src["sha256"] == digest and src["size"] == len(data):
            return src
    return None


def pdf_body_words(path):
    """Body words of a Secretary PDF (needs pypdf). Returns None when pypdf is absent."""
    try:
        import pypdf
    except ImportError:
        return None
    text = "\n".join(page.extract_text() or "" for page in pypdf.PdfReader(path).pages)
    return body_words(text)


def secretary_gate(results, rung1_readback_ok):
    """Ladder gate. results maps rung -> HIT/CONTINUE/EXHAUSTED.
    Returns (saved, reason). Never 'saved' unless rung 1 is read back and no rung is skipped."""
    for rung, _ in LADDER:
        if rung not in results:
            return False, "NOT SAVED: rung %d skipped" % rung
        if results[rung] not in STATUSES:
            return False, "NOT SAVED: rung %d has unknown status %r" % (rung, results[rung])
    extra = sorted(set(results) - {r for r, _ in LADDER})
    if extra:
        return False, "NOT SAVED: unknown rung %r" % extra[0]
    if not rung1_readback_ok:
        return False, "NOT SAVED: Pri 1 (Gmail To/CC) not verified"
    if results[1] != "HIT":
        return False, "NOT SAVED: Pri 1 is %s, not HIT" % results[1]
    return True, "saved"


def self_test():
    fails = []

    def check(name, cond):
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            fails.append(name)

    w = body_words(TEXT)
    check("body word count = %d" % BODY_WORD_COUNT, len(w) == BODY_WORD_COUNT)
    check("body words hash frozen", words_sha256(w) == BODY_WORDS_SHA256)
    check("ladder rungs 0..6 in order", [r for r, _ in LADDER] == list(range(7)))
    check("four live copies, distinct hashes", len({s["sha256"] for s in SOURCES}) == 4)
    check("every copy hash is 64 hex", all(re.fullmatch(r"[0-9a-f]{64}", s["sha256"]) for s in SOURCES))
    check("TEXT names 'Do not invent a new Secretary'", "Do not invent a new Secretary." in TEXT)

    allhit = {r: "HIT" for r, _ in LADDER}
    check("gate: all HIT + readback -> saved", secretary_gate(allhit, True) == (True, "saved"))
    check("gate: no readback -> NOT SAVED", secretary_gate(allhit, False)[0] is False)
    skip = dict(allhit)
    del skip[1]
    check("gate: rung 1 skipped -> NOT SAVED (Row 3D)", secretary_gate(skip, True)[0] is False)
    gap = dict(allhit)
    del gap[4]
    check("gate: middle rung skipped -> NOT SAVED", secretary_gate(gap, True)[0] is False)
    ex = dict(allhit)
    ex[6] = "EXHAUSTED"
    check("gate: EXHAUSTED rung still files -> saved", secretary_gate(ex, True)[0] is True)
    cont = dict(allhit)
    cont[1] = "CONTINUE"
    check("gate: Pri 1 CONTINUE -> NOT SAVED", secretary_gate(cont, True)[0] is False)
    bad = dict(allhit)
    bad[3] = "DONE"
    check("gate: unknown status -> NOT SAVED", secretary_gate(bad, True)[0] is False)
    more = dict(allhit)
    more[7] = "HIT"
    check("gate: unknown rung -> NOT SAVED", secretary_gate(more, True)[0] is False)
    check("identify: wrong bytes -> None", identify_copy(b"not a secretary") is None)

    here = os.path.dirname(os.path.abspath(__file__))
    stem = "SECRETARY_LAST_MAP_2026-09-09"
    txt = os.path.join(here, stem + ".txt")
    if os.path.exists(txt):
        with open(txt, encoding="utf-8") as fh:
            check(".txt twin equals TEXT", fh.read() == TEXT)
    md = os.path.join(here, stem + ".md")
    if os.path.exists(md):
        with open(md, encoding="utf-8") as fh:
            m = fh.read()
        check(".md twin carries all 7 rungs", all(desc.split(" (")[0] in m for _, desc in LADDER))
    for name in (stem + ".pdf", stem + "_HYBRID.pdf"):
        p = os.path.join(here, name)
        if os.path.exists(p):
            with open(p, "rb") as fh:
                check(name + " is a known live copy", identify_copy(fh.read()) is not None)
            pw = pdf_body_words(p)
            if pw is not None:
                check(name + " words == TEXT words", words_sha256(pw) == BODY_WORDS_SHA256)

    print("n_fail=%d" % len(fails))
    return 0 if not fails else 1


def main(argv):
    if len(argv) < 2:
        return self_test()
    rc = 0
    for path in argv[1:]:
        with open(path, "rb") as fh:
            data = fh.read()
        src = identify_copy(data)
        pw = pdf_body_words(path)
        same = None if pw is None else (words_sha256(pw) == BODY_WORDS_SHA256)
        print("%s size=%d sha256=%s copy=%s words_match=%s" % (
            path, len(data), hashlib.sha256(data).hexdigest(),
            src["where"] if src else "UNKNOWN", same))
        if src is None or same is False:
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
