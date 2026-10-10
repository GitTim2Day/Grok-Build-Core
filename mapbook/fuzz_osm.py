#!/usr/bin/env python3
"""Differential fuzz: random valid PBFs + byte-mutated PBFs through both twins."""
import os, random, struct, subprocess, sys, zlib, filecmp
R = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
def varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F; n >>= 7
        if n: out.append(b | 0x80)
        else: out.append(b); return bytes(out)
zz = lambda n: ((n << 1) ^ (n >> 63)) & 0xFFFFFFFFFFFFFFFF
fv = lambda f, n: varint(f << 3) + varint(n & 0xFFFFFFFFFFFFFFFF)
fb = lambda f, b: varint(f << 3 | 2) + varint(len(b)) + b
pk = lambda f, ns: fb(f, b"".join(varint(x) for x in ns))
pks = lambda f, ns: pk(f, [zz(x) for x in ns])
def delta(xs):
    o, p = [], 0
    for x in xs: o.append(x - p); p = x
    return o
def blob(kind, payload, comp):
    b = fv(2, len(payload)) + fb(3, zlib.compress(payload)) if comp else fb(1, payload)
    h = fb(1, kind.encode()) + fv(3, len(b))
    return struct.pack(">I", len(h)) + h + b
KEYS = ["addr:housenumber","addr:street","addr:city","addr:state","addr:postcode","highway","name","building","x"]
VALS = ["12","Main St","Atlanta","GA","30303","residential","service","footway","primary","yes","","Ünïcode Rd"]
def tags():
    t = {}
    for _ in range(R.randint(0, 4)):
        t[R.choice(KEYS)] = R.choice(VALS)
    return t
def gen():
    strs = [""] + KEYS + VALS
    idx = {s: i for i, s in enumerate(strs)}
    st = fb(1, b"".join(fb(1, s.encode()) for s in strs))
    ids = list(range(1, R.randint(2, 60)))
    blocks = []
    nodeids = []
    for _ in range(R.randint(1, 4)):
        n = R.randint(0, 15); chunk = [ids.pop(0) for _ in range(min(n, len(ids)))]
        nodeids += chunk
        gran = R.choice([100, 100, 1, 1000])
        lato = R.randint(-10**9, 10**9) if R.random() < .5 else 0
        lono = R.randint(-10**9, 10**9) if R.random() < .5 else 0
        groups = b""
        if chunk:
            if R.random() < .5:
                lats = [R.randint(-9*10**8, 9*10**8) // gran for _ in chunk]
                lons = [R.randint(-18*10**8, 18*10**8) // gran for _ in chunk]
                kv = []
                for _ in chunk:
                    for k, v in tags().items(): kv += [idx[k], idx[v]]
                    kv.append(0)
                d = pks(1, delta(chunk)) + pks(8, delta(lats)) + pks(9, delta(lons)) + pk(10, kv)
                groups += fb(2, fb(2, d))
            else:
                g = b""
                for i in chunk:
                    t = tags(); b = fv(1, zz(i))
                    if t: b += pk(2, [idx[k] for k in t]) + pk(3, [idx[v] for v in t.values()])
                    b += fv(8, zz(R.randint(-9*10**8, 9*10**8)//gran)) + fv(9, zz(R.randint(-18*10**8, 18*10**8)//gran))
                    g += fb(1, b)
                groups += fb(2, g)
        g = b""
        for w in range(R.randint(0, 6)):
            refs = [R.randint(1, 70) for _ in range(R.randint(0, 5))]
            t = tags()
            g += fb(3, fv(1, 1000 + len(blocks) * 100 + w) + pk(2, [idx[k] for k in t]) + pk(3, [idx[v] for v in t.values()]) + pks(8, delta(refs)))
        if g: groups += fb(2, g)
        if R.random() < .3: groups += fb(2, fb(4, fv(1, 5)))
        blk = st + groups
        if gran != 100: blk += fv(17, gran)
        if lato: blk += fv(19, lato)
        if lono: blk += fv(20, lono)
        blocks.append(blob("OSMData", blk, R.random() < .5))
    hdr = blob("OSMHeader", fb(4, b"OsmSchema-V0.6") + fb(4, b"DenseNodes"), False)
    return hdr + b"".join(blocks)
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, errors="surrogateescape")
    return r.returncode, r.stderr.strip()
mism = crash = valid = refused = 0
N = int(sys.argv[2]) if len(sys.argv) > 2 else 300
for case in range(N):
    data = gen()
    if case % 2 == 1:                      # byte-mutate half of them
        b = bytearray(data)
        for _ in range(R.randint(1, 4)):
            b[R.randrange(len(b))] = R.randrange(256)
        if R.random() < .2: b = b[:R.randrange(len(b))]
        data = bytes(b)
    p = "fuzz/c.pbf"; open(p, "wb").write(data)
    for d in ("fuzz/py", "fuzz/cpp"):
        for f in ("addresses.txt", "roads.txt", "road_nodes.txt"):
            try: os.remove(os.path.join(d, f))
            except FileNotFoundError: pass
    a = run(["python3", "-I", "osm_streamline.py", p, "fuzz/py"])
    b = run(["./osm_streamline_san", p, "fuzz/cpp"])
    if "Traceback" in a[1] or (b[0] not in (0, 1)) or "runtime error" in b[1] or "AddressSanitizer" in b[1]:
        crash += 1; open("fuzz/crash_%d.pbf" % case, "wb").write(data); print("CRASH", case, a[1][-200:], b[1][-200:]); continue
    same = a[0] == b[0]
    if same and a[0] == 0:
        valid += 1
        for f in ("addresses.txt", "roads.txt", "road_nodes.txt"):
            if not filecmp.cmp("fuzz/py/" + f, "fuzz/cpp/" + f, shallow=False): same = False
    elif same:
        refused += 1
        if a[1] != b[1]: same = False
    if not same:
        mism += 1; open("fuzz/mism_%d.pbf" % case, "wb").write(data); print("MISMATCH", case, a, b)
print("cases=%d valid_agree=%d refused_agree=%d mismatches=%d crashes=%d" % (N, valid, refused, mism, crash))
