#!/usr/bin/env python3
"""Build osm_fixture.pbf byte by byte (answer key input for OSM streamline v1).
Hand-written protobuf encoder; stdlib only. Independent of osm_streamline.py."""
import struct
import sys
import zlib


def varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def zz(n):  # zigzag for sint64
    return (n << 1) ^ (n >> 63)


def f_varint(field, n):
    return varint(field << 3 | 0) + varint(n)


def f_bytes(field, b):
    return varint(field << 3 | 2) + varint(len(b)) + b


def packed(field, nums):
    return f_bytes(field, b"".join(varint(x) for x in nums))


def packed_s(field, nums):
    return packed(field, [zz(x) for x in nums])


def delta(xs):
    out, prev = [], 0
    for x in xs:
        out.append(x - prev)
        prev = x
    return out


def blob(kind, payload, compress):
    if compress:
        b = f_varint(2, len(payload)) + f_bytes(3, zlib.compress(payload))
    else:
        b = f_bytes(1, payload)
    hdr = f_bytes(1, kind.encode()) + f_varint(3, len(b))
    return struct.pack(">I", len(hdr)) + hdr + b


def strtab(strs):
    return f_bytes(1, b"".join(f_bytes(1, s.encode()) for s in strs))


# Header block
header = f_bytes(4, b"OsmSchema-V0.6") + f_bytes(4, b"DenseNodes")

# Data block 1: dense nodes + plain nodes; lat_offset 99, lon_offset -99
S1 = ["", "addr:housenumber", "75", "addr:street", "Langley Drive", "addr:city",
      "Lawrenceville", "addr:postcode", "30046", "highway", "residential", "name",
      "building", "yes", "addr:state", "GA", "100", "power", "line"]
ids = [101, 102, 103]
lats = [339562149, 339565000, 339570123]
lons = [-839879625, -839875000, -839870456]
kv = [1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 0, 0, 0]
dense = packed_s(1, delta(ids)) + packed_s(8, delta(lats)) + packed_s(9, delta(lons)) + packed(10, kv)
g1 = f_bytes(2, dense)


def node(i, lat, lon, keys, vals):
    b = f_varint(1, zz(i))
    if keys:
        b += packed(2, keys) + packed(3, vals)
    return b + f_varint(8, zz(lat)) + f_varint(9, zz(lon))


g2 = (f_bytes(1, node(201, 339000000, -840000000, [17], [18]))
      + f_bytes(1, node(202, 0, 0, [1], [16]))
      + f_bytes(1, node(203, -10, 5, [1], [16]))
      + f_bytes(1, node(3, 1, 1, [], []))
      + f_bytes(1, node(1024, 2, 2, [], [])))
# lat_offset/lon_offset (fields 19/20) are int64, not sint64: two's complement varint
blk1 = strtab(S1) + f_bytes(2, g1) + f_bytes(2, g2) + f_varint(19, 99) + f_varint(20, (-99) & 0xFFFFFFFFFFFFFFFF)

# Data block 2: ways + relation, different string table
S2 = ["", "highway", "residential", "name", "Langley Drive", "building", "yes",
      "addr:housenumber", "100", "addr:street", "footway", "primary"]


def way(i, keys, vals, refs):
    return f_varint(1, i) + packed(2, keys) + packed(3, vals) + packed_s(8, delta(refs))


g3 = (f_bytes(3, way(301, [1, 3], [2, 4], [101, 102, 103]))
      + f_bytes(3, way(302, [5, 7, 9], [6, 8, 4], [103, 999]))
      + f_bytes(3, way(303, [1], [2], [102, 888]))
      + f_bytes(3, way(304, [1], [10], [101]))
      + f_bytes(3, way(305, [7], [8], [777]))
      + f_bytes(3, way(306, [1], [11], [1024, 3, 101])))
g4 = f_bytes(4, f_varint(1, 401))
blk2 = strtab(S2) + f_bytes(2, g3) + f_bytes(2, g4)

data = blob("OSMHeader", header, False) + blob("OSMData", blk1, False) + blob("OSMData", blk2, True)
open(sys.argv[1] if len(sys.argv) > 1 else "osm_fixture.pbf", "wb").write(data)
# fault file: data block with no header in front (must REFUSE)
open("faults/noheader.pbf", "wb").write(blob("OSMData", blk2, False))
