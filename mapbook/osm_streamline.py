#!/usr/bin/env python3
"""OSM streamline v1, Python twin. Built from OSM_STREAMLINE_SPEC_v1.md.

Usage: python3 -I osm_streamline.py georgia-latest.osm.pbf OUTDIR
Keeps addresses (offline geocoder) and roads (routing feed); drops the rest.
Stdlib only (zlib + hand protobuf reader). Integer coordinates, text chop output.
"""
import hashlib
import os
import struct
import sys
import time
import zlib

MH, MB = 65536, 33554432
FEATURES = {"OsmSchema-V0.6", "DenseNodes"}
ROADSET = set(("motorway trunk primary secondary tertiary unclassified residential service "
               "motorway_link trunk_link primary_link secondary_link tertiary_link "
               "living_street road").split())
ADDR_KEYS = ("addr:housenumber", "addr:street", "addr:city", "addr:state", "addr:postcode")


class Refuse(Exception):
    pass


# ---------- protobuf reader (GOSUB-style small routines) ----------
def rd_varint(buf, i):
    shift = 0
    val = 0
    while True:
        if i >= len(buf):
            raise Refuse("truncated varint")
        b = buf[i]
        i += 1
        val |= (b & 0x7F) << shift
        if b < 0x80:
            return val, i
        shift += 7
        if shift > 63:
            raise Refuse("varint too long")


def fields(buf):
    i = 0
    n = len(buf)
    while i < n:
        key, i = rd_varint(buf, i)
        fno, wt = key >> 3, key & 7
        if wt == 0:
            v, i = rd_varint(buf, i)
        elif wt == 2:
            ln, i = rd_varint(buf, i)
            if i + ln > n:
                raise Refuse("truncated field")
            v = buf[i:i + ln]
            i += ln
        elif wt == 1:
            if i + 8 > n:
                raise Refuse("truncated field")
            v = buf[i:i + 8]
            i += 8
        elif wt == 5:
            if i + 4 > n:
                raise Refuse("truncated field")
            v = buf[i:i + 4]
            i += 4
        else:
            raise Refuse("bad wire type %d" % wt)
        yield fno, wt, v


def unzz(n):
    return (n >> 1) ^ -(n & 1)


def s64(n):
    return n - (1 << 64) if n >= (1 << 63) else n


def packed(buf):
    out = []
    i = 0
    while i < len(buf):
        v, i = rd_varint(buf, i)
        out.append(v)
    return out


def undelta(vals):
    out = []
    acc = 0
    for v in vals:
        acc += unzz(v)
        out.append(acc)
    return out


# ---------- coordinates: integer nanodegrees -> text, chop not round ----------
def coord_text(nano, pos_letter, neg_letter):
    mag = nano if nano >= 0 else -nano
    whole = mag // 1000000000
    frac = "%09d" % (mag - whole * 1000000000)
    frac7 = frac[:7]                      # text chop: drop last 2 digits
    letter = neg_letter if nano < 0 else pos_letter
    if whole == 0 and frac7 == "0000000":
        letter = pos_letter               # no negative zero
    return "%s%d.%s" % (letter, whole, frac7)


def lat_t(n):
    return coord_text(n, "N", "S")


def lon_t(n):
    return coord_text(n, "E", "W")


def blank(s):
    return s if s != "" else " "


# ---------- capped inflate (spec v1.3) ----------
def inflate_capped(comp):
    d = zlib.decompressobj()
    try:
        out = d.decompress(comp, MB + 1)
    except zlib.error:
        raise Refuse("zlib error")
    if len(out) > MB:
        raise Refuse("blob size out of range")
    if not d.eof:
        raise Refuse("zlib error")
    return out


# ---------- block stream ----------
def blocks(path):
    with open(path, "rb") as fh:
        while True:
            hl = fh.read(4)
            if len(hl) == 0:
                return
            if len(hl) < 4:
                raise Refuse("truncated header length")
            (hlen,) = struct.unpack(">I", hl)
            if hlen == 0 or hlen > MH:
                raise Refuse("header size out of range")
            hdr = fh.read(hlen)
            if len(hdr) != hlen:
                raise Refuse("truncated header")
            kind, dsize = "", -1
            for fno, wt, v in fields(hdr):
                if fno == 1 and wt == 2:
                    kind = bytes(v).decode("utf-8", "surrogateescape")
                elif fno == 3 and wt == 0:
                    dsize = v
            if dsize <= 0 or dsize > MB:
                raise Refuse("blob size out of range")
            raw = fh.read(dsize)
            if len(raw) != dsize:
                raise Refuse("truncated blob")
            data, rsize, have, comp = None, -1, False, None
            for fno, wt, v in fields(raw):
                if fno == 1 and wt == 2:
                    data, have = bytes(v), True
                elif fno == 2 and wt == 0:
                    rsize = v
                elif fno == 3 and wt == 2:
                    comp = bytes(v)
                elif fno in (4, 5, 6, 7):
                    raise Refuse("unsupported blob compression field %d" % fno)
            if comp is not None:
                if rsize < 0 or rsize > MB:
                    raise Refuse("raw_size out of range")
                data, have = inflate_capped(comp), True
                if len(data) != rsize:
                    raise Refuse("raw_size mismatch")
            elif have and rsize >= 0 and len(data) != rsize:
                raise Refuse("raw_size mismatch")
            if not have:
                raise Refuse("empty blob")
            yield kind, data


def check_header(data):
    for fno, wt, v in fields(data):
        if fno == 4 and wt == 2:
            feat = bytes(v).decode("utf-8", "surrogateescape")
            if feat not in FEATURES:
                raise Refuse("unsupported required feature: " + feat)


def primitive(data):
    """Return (strings, granularity, lat_off, lon_off, groups) for one block."""
    strings, groups = [], []
    gran, lato, lono = 100, 0, 0
    for fno, wt, v in fields(data):
        if fno == 1 and wt == 2:
            for f2, w2, s in fields(v):
                if f2 == 1 and w2 == 2:
                    strings.append(bytes(s).decode("utf-8", "surrogateescape"))
        elif fno == 2 and wt == 2:
            groups.append(v)
        elif fno == 17 and wt == 0:
            gran = v
        elif fno == 19 and wt == 0:
            lato = s64(v)
        elif fno == 20 and wt == 0:
            lono = s64(v)
    if gran <= 0:
        raise Refuse("granularity must be > 0")
    return strings, gran, lato, lono, groups


def each_node(strings, gran, lato, lono, group):
    """Yield (id, nanolat, nanolon, tags dict) for plain and dense nodes."""
    for fno, wt, v in fields(group):
        if fno == 1 and wt == 2:
            nid, lat, lon, keys, vals = 0, 0, 0, [], []
            for f2, w2, x in fields(v):
                if f2 == 1 and w2 == 0:
                    nid = unzz(x)
                elif f2 == 2 and w2 == 2:
                    keys = packed(x)
                elif f2 == 3 and w2 == 2:
                    vals = packed(x)
                elif f2 == 8 and w2 == 0:
                    lat = unzz(x)
                elif f2 == 9 and w2 == 0:
                    lon = unzz(x)
            if len(keys) != len(vals):
                raise Refuse("node keys/vals length mismatch")
            tags = {sidx(strings, k): sidx(strings, vv) for k, vv in zip(keys, vals)}
            yield nid, lato + gran * lat, lono + gran * lon, tags
        elif fno == 2 and wt == 2:
            ids, lats, lons, kv = [], [], [], []
            for f2, w2, x in fields(v):
                if f2 == 1 and w2 == 2:
                    ids = undelta(packed(x))
                elif f2 == 8 and w2 == 2:
                    lats = undelta(packed(x))
                elif f2 == 9 and w2 == 2:
                    lons = undelta(packed(x))
                elif f2 == 10 and w2 == 2:
                    kv = packed(x)
            if not (len(ids) == len(lats) == len(lons)):
                raise Refuse("dense arrays length mismatch")
            p = 0
            for j in range(len(ids)):
                tags = {}
                if kv:
                    while True:
                        if p >= len(kv):
                            raise Refuse("dense keys_vals truncated")
                        k = kv[p]
                        p += 1
                        if k == 0:
                            break
                        if p >= len(kv):
                            raise Refuse("dense keys_vals truncated")
                        tags[sidx(strings, k)] = sidx(strings, kv[p])
                        p += 1
                yield ids[j], lato + gran * lats[j], lono + gran * lons[j], tags


def each_way(strings, group):
    for fno, wt, v in fields(group):
        if fno == 3 and wt == 2:
            wid, keys, vals, refs = 0, [], [], []
            for f2, w2, x in fields(v):
                if f2 == 1 and w2 == 0:
                    wid = s64(x)
                elif f2 == 2 and w2 == 2:
                    keys = packed(x)
                elif f2 == 3 and w2 == 2:
                    vals = packed(x)
                elif f2 == 8 and w2 == 2:
                    refs = undelta(packed(x))
            if len(keys) != len(vals):
                raise Refuse("way keys/vals length mismatch")
            yield wid, {sidx(strings, k): sidx(strings, vv) for k, vv in zip(keys, vals)}, refs


def count_relations(group):
    n = 0
    for fno, wt, v in fields(group):
        if fno == 4 and wt == 2:
            n += 1
    return n


def sidx(strings, k):
    if k >= len(strings):
        raise Refuse("string index out of range")
    return strings[k]


def addr_fields(tags):
    return [tags.get(k, "") for k in ADDR_KEYS]


def run(src, outdir):
    t0 = time.time()
    os.makedirs(outdir, exist_ok=True)
    stats = {"blocks": 0, "nodes": 0, "ways": 0, "relations": 0}
    addrs = []          # [kind, id, house, street, city, state, zip, lat, lon, pos, firstref]
    roads = []          # (wid, class, name, refs)
    need = set()

    # ---- pass 1: READ -> RECORD -> CLEAR per block ----
    for kind, data in blocks(src):
        stats["blocks"] += 1
        if stats["blocks"] == 1 and kind != "OSMHeader":
            raise Refuse("first block is not OSMHeader")
        if kind == "OSMHeader":
            check_header(data)
            continue
        if kind != "OSMData":
            continue                       # unknown block types are skippable by spec
        strings, gran, lato, lono, groups = primitive(data)
        for g in groups:
            for nid, la, lo, tags in each_node(strings, gran, lato, lono, g):
                stats["nodes"] += 1
                if "addr:housenumber" in tags:
                    a = addr_fields(tags)
                    addrs.append(["N", nid] + a + [lat_t(la), lon_t(lo), "NODE", 0])
            for wid, tags, refs in each_way(strings, g):
                stats["ways"] += 1
                if "addr:housenumber" in tags:
                    first = refs[0] if refs else 0
                    addrs.append(["W", wid] + addr_fields(tags) + ["", "", "", first])
                    if first:
                        need.add(first)
                if tags.get("highway", "") in ROADSET:
                    roads.append((wid, tags["highway"], tags.get("name", ""), refs))
                    need.update(refs)
            stats["relations"] += count_relations(g)
        strings = groups = data = None     # CLEAR

    if stats["blocks"] == 0:
        raise Refuse("empty input file")

    # ---- pass 2: coordinates for needed nodes only ----
    found = {}
    if need:
        for kind, data in blocks(src):
            if kind != "OSMData":
                continue
            strings, gran, lato, lono, groups = primitive(data)
            for g in groups:
                for nid, la, lo, tags in each_node(strings, gran, lato, lono, g):
                    if nid in need:
                        found[nid] = (la, lo)
            strings = groups = data = None

    missing = need - set(found)
    for a in addrs:
        if a[0] == "W":
            f = a[10]
            if f in found:
                a[7], a[8], a[9] = lat_t(found[f][0]), lon_t(found[f][1]), "FIRSTREF"
            else:
                a[9] = "MISSINGREF"

    road_ids = set()
    for r in roads:
        road_ids.update(r[3])

    with open(os.path.join(outdir, "addresses.txt"), "w", encoding="utf-8", errors="surrogateescape", newline="\n") as fo:
        for a in addrs:
            row = [a[0], str(a[1])] + [blank(x) for x in a[2:10]]
            fo.write("|".join(row) + "\n")
    with open(os.path.join(outdir, "roads.txt"), "w", encoding="utf-8", errors="surrogateescape", newline="\n") as fo:
        for wid, cls, name, refs in roads:
            fo.write("%d|%s|%s|%d|%s\n" % (wid, cls, blank(name), len(refs),
                                            blank(" ".join(str(x) for x in refs))))
    with open(os.path.join(outdir, "road_nodes.txt"), "w", encoding="utf-8", errors="surrogateescape", newline="\n") as fo:
        for nid in sorted(road_ids):
            if nid in found:
                fo.write("%d|%s|%s\n" % (nid, lat_t(found[nid][0]), lon_t(found[nid][1])))

    h = hashlib.sha256()
    with open(src, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    lines = [
        "input=%s" % os.path.basename(src),
        "input_bytes=%d" % os.path.getsize(src),
        "input_sha256=%s" % h.hexdigest(),
        "blocks=%d nodes=%d ways=%d relations=%d" % (stats["blocks"], stats["nodes"],
                                                     stats["ways"], stats["relations"]),
        "kept_addresses=%d kept_roads=%d road_nodes=%d" % (len(addrs), len(roads),
                                                         len(road_ids & set(found))),
        "missing_refs=%d" % len(missing),
    ]
    for fn in ("addresses.txt", "roads.txt", "road_nodes.txt"):
        lines.append("%s_bytes=%d" % (fn, os.path.getsize(os.path.join(outdir, fn))))
    lines.append("seconds=%d" % int(time.time() - t0))
    with open(os.path.join(outdir, "summary.txt"), "w", encoding="utf-8", errors="surrogateescape", newline="\n") as fo:
        fo.write("\n".join(lines) + "\n")
    return lines


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("usage: osm_streamline.py INPUT.osm.pbf OUTDIR\n")
        sys.exit(2)
    try:
        for ln in run(sys.argv[1], sys.argv[2]):
            print(ln)
    except Refuse as e:
        sys.stderr.buffer.write(("REFUSED: %s\n" % e).encode("utf-8", "surrogateescape"))
        sys.exit(1)
