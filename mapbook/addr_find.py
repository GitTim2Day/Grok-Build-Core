#!/usr/bin/env python3
"""MAPBOOK address finder, Python twin. Built from MAPBOOK_ADDR_SPEC_v1.md.

Usage: python3 -I addr_find.py input.txt > records.txt
Record: R|LINE|STREET|CITY|ST|ZIP  (empty field = one blank). Text only, no floats.
"""
import sys

ML, MS, MT, MR = 200, 12, 12, 500

SUFFIX = set("ST STREET AVE AVENUE RD ROAD DR DRIVE LN LANE BLVD BOULEVARD CT COURT "
             "WAY PKWY PARKWAY HWY HIGHWAY CIR CIRCLE PL PLACE TRL TRAIL TER TERRACE".split())
DIRS = set("N S E W NE NW SE SW".split())
UNITW = set("APT STE SUITE UNIT #".split())
STATES = set(("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE "
              "NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC PR").split())
DIG = "0123456789"
UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def is_digits(t):
    if t == "":
        return False
    for c in t:
        if c not in DIG:
            return False
    return True


def is_house(t):
    return 1 <= len(t) <= 6 and is_digits(t) and t[0] != "0"


def is_alnum(t):
    if t == "":
        return False
    for c in t:
        if c not in UP and c not in DIG:
            return False
    return True


def is_cityword(t):
    has = False
    if t == "":
        return False
    for c in t:
        if c in UP:
            has = True
        elif c not in "-'":
            return False
    return has


def is_zip(t):
    if len(t) == 5:
        return is_digits(t)
    if len(t) == 10:
        return is_digits(t[:5]) and t[5] == "-" and is_digits(t[6:])
    return False


def toks(seg):
    return seg.split(" ") if seg != "" else []


def is_street(seg):
    t = toks(seg)
    n = len(t)
    if n < 3 or n > MT:
        return False
    if not is_house(t[0]):
        return False
    s = n
    if t[n - 1] in DIRS:
        s = n - 1
    if s < 3 or t[s - 1] not in SUFFIX:
        return False
    for k in range(1, s - 1):
        if not is_alnum(t[k]):
            return False
    return True


def is_unit(seg):
    t = toks(seg)
    if len(t) == 2:
        return t[0] in UNITW and is_alnum(t[1])
    if len(t) == 1:
        return len(t[0]) >= 2 and t[0][0] == "#" and is_alnum(t[0][1:])
    return False


def is_city(seg):
    t = toks(seg)
    if len(t) < 1 or len(t) > 4:
        return False
    for w in t:
        if not is_cityword(w):
            return False
    return True


def is_stzip(seg):
    t = toks(seg)
    return len(t) == 2 and t[0] in STATES and is_zip(t[1])


def norm(line):
    out = []
    for c in line:
        if "a" <= c <= "z":
            out.append(chr(ord(c) - 32))
        elif c == ".":
            continue
        else:
            out.append(c)
    segs = []
    for s in "".join(out).split(","):
        segs.append(" ".join(w for w in s.split(" ") if w != ""))
    return segs


def find(lines):
    recs = []
    st = {"ps": "", "pl": 0}

    def emit(r, ln, a, b, c, d):
        if len(recs) >= MR:
            return
        f = [x if x != "" else " " for x in (a, b, c, d)]
        recs.append("%d|%d|%s|%s|%s|%s" % (r, ln, f[0], f[1], f[2], f[3]))
        if len(recs) == MR:
            recs.append("8|0| | | | ")

    def flush():
        if st["ps"] != "":
            emit(1, st["pl"], st["ps"], "", "", "")
            st["ps"] = ""
            st["pl"] = 0

    for i, raw in enumerate(lines):
        if len(recs) > MR:
            break
        L = i + 1
        segs = norm(raw)
        c = len(segs)
        if len(raw) > ML or c > MS:
            flush()
            emit(9, L, "", "", "", "")
            continue
        if c >= 2 and is_stzip(segs[c - 1]) and is_city(segs[c - 2]):
            sv = ""
            if c >= 4 and is_unit(segs[c - 3]) and is_street(segs[c - 4]):
                sv = segs[c - 4] + " " + segs[c - 3]
            elif c >= 3 and is_street(segs[c - 3]):
                sv = segs[c - 3]
            sl = L
            if sv == "" and c == 2 and st["ps"] != "":
                sv, sl = st["ps"], st["pl"]
                st["ps"], st["pl"] = "", 0
            else:
                flush()
            stz = toks(segs[c - 1])
            if sv != "":
                emit(0, sl, sv, segs[c - 2], stz[0], stz[1])
            else:
                emit(2, L, "", segs[c - 2], stz[0], stz[1])
        else:
            flush()
            if c >= 2 and is_unit(segs[c - 1]) and is_street(segs[c - 2]):
                st["ps"], st["pl"] = segs[c - 2] + " " + segs[c - 1], L
            elif c >= 1 and is_street(segs[c - 1]):
                st["ps"], st["pl"] = segs[c - 1], L
    flush()
    return recs


def read_lines(path):
    with open(path, "rb") as fh:
        data = fh.read().decode("utf-8", "replace")
    data = data.replace("\r\n", "\n").replace("\r", "\n")
    lines = data.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


if __name__ == "__main__":
    for r in find(read_lines(sys.argv[1])):
        sys.stdout.write(r + "\n")
