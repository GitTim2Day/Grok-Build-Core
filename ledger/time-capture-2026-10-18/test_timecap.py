#!/usr/bin/env python3
"""Error tests + mutants for timecap.py and timecap.sh (time-capture-auto-2026-10-18).

  python3 test_timecap.py            run the suite on both implementations
  python3 test_timecap.py --mutants  also run every mutant; a mutant is KILLED if >=1 test fails

Fixture stamps are always derived from a REAL fetch by the implementation under test,
then edited (and re-hashed where the case needs a valid hash) to simulate stale, future
or skewed stamps.  "Now" is faked only through TIMECAP_TEST_NOW, whose output always
carries the " [TEST CLOCK]" tag.  All network checks use a local 127.0.0.1 server or
TIMECAP_NO_NET=1, except one optional live check that is reported but never fails.
"""
import datetime, hashlib, http.server, json, os, re, shutil, socket, subprocess, sys, tempfile, threading, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timecap as ref                     # reference helpers for fixtures only
from zoneinfo import ZoneInfo

S = 10**9
FRESH_RE = re.compile(r"^Time \(fresh fetch\): (1[0-2]|[1-9]):[0-5]\d [AP]M E[DS]T, fetched ([01]\d|2[0-3]):[0-5]\d:[0-5]\d( \[TEST CLOCK\])?$")
STALE_RE = re.compile(r"^Time: (1[0-2]|[1-9]):[0-5]\d [AP]M E[DS]T — STALE, fetched (\d+) s ago( \[TEST CLOCK\])?$")
CLOCKISH = re.compile(r"\d{1,2}:\d\d")
NOFETCH = "Time UNVERIFIED: no fetch available"
SKEW = "Time UNVERIFIED: clock skew detected"
BOOT = "Time UNVERIFIED: stamp is from a different boot (monotonic check impossible)"


class Impl:
    def __init__(self, name, cmd):
        self.name, self.cmd = name, cmd
    def run(self, stamp, *args, env=None):
        e = dict(os.environ); e.pop("TIMECAP_TEST_NOW", None); e.pop("TIMECAP_STAMP", None)
        e.setdefault("TIMECAP_NO_NET", "1")
        if env: e.update(env)
        e = {k: v for k, v in e.items() if v is not None}
        r = subprocess.run(self.cmd + ["--stamp", stamp] + list(args), capture_output=True, text=True, env=e, timeout=20)
        return r.returncode, r.stdout.rstrip("\n").split("\n") if r.stdout else [""]


def rehash(p):
    p = dict(p)
    p["iso_local"] = ref.iso_from_ns(p["fetch_epoch_ns"], ZoneInfo(ref.TZ_NAME))
    p["iso_utc"] = ref.iso_from_ns(p["fetch_epoch_ns"], datetime.timezone.utc)
    p["sha256"] = ref.payload_hash(p)
    return p

def write(path, p):
    with open(path, "w") as f:
        json.dump(p, f)

def fetched(impl, d):
    path = os.path.join(d, "s.json")
    rc, _ = impl.run(path, "fetch")
    assert rc == 0, "fetch rc %d" % rc
    with open(path) as f:
        return path, json.load(f)

def now_env(wall, mono):
    return {"TIMECAP_TEST_NOW": "%d:%d" % (wall, mono)}

def check_failure_line(line):
    """A failure case must say UNVERIFIED (with no clock-like text) or STALE."""
    if "UNVERIFIED" in line:
        assert not CLOCKISH.search(line), "UNVERIFIED line contains a time: %r" % line
        return
    assert "STALE" in line and STALE_RE.match(line), "failure printed something else: %r" % line


# ---------------- tests: each takes (impl, tmpdir) ----------------
def t_fresh(impl, d):
    path, p = fetched(impl, d)
    rc, out = impl.run(path, "status")
    assert rc == 0 and FRESH_RE.match(out[0]) and "[TEST CLOCK]" not in out[0], (rc, out)
    assert out[0].endswith("fetched " + p["iso_local"][11:19]), out   # HH:MM:SS truncated from stamp
    return out[0]

def _stale_fake(impl, d, secs):
    path, p = fetched(impl, d)
    rc, out = impl.run(path, "status", env=now_env(p["fetch_epoch_ns"] + secs * S, p["monotonic_ns"] + secs * S))
    m = STALE_RE.match(out[0])
    assert rc == 1 and m and m.group(2) == str(secs) and out[0].endswith("[TEST CLOCK]"), (rc, out)
    check_failure_line(out[0])
    return out[0]

def t_stale_61(impl, d): return _stale_fake(impl, d, 61)
def t_stale_3600(impl, d): return _stale_fake(impl, d, 3600)

def t_stale_3600_real_clock(impl, d):
    path, p = fetched(impl, d)
    p["fetch_epoch_ns"] -= 3600 * S; p["monotonic_ns"] -= 3600 * S
    write(path, rehash(p))
    rc, out = impl.run(path, "status")
    m = STALE_RE.match(out[0])
    assert rc == 1 and m and 3600 <= int(m.group(2)) <= 3602 and "[TEST CLOCK]" not in out[0], (rc, out)
    check_failure_line(out[0])
    return out[0]

def t_boundary_60_fresh(impl, d):
    path, p = fetched(impl, d)
    rc, out = impl.run(path, "status", env=now_env(p["fetch_epoch_ns"] + 60 * S, p["monotonic_ns"] + 60 * S))
    assert rc == 0 and FRESH_RE.match(out[0]), (rc, out)
    return out[0]

def t_boundary_60s_plus_1ns_stale(impl, d):
    path, p = fetched(impl, d)
    rc, out = impl.run(path, "status", env=now_env(p["fetch_epoch_ns"] + 60 * S + 1, p["monotonic_ns"] + 60 * S + 1))
    m = STALE_RE.match(out[0])
    assert rc == 1 and m and m.group(2) == "60", (rc, out)      # truncated, not rounded
    return out[0]

def t_boundary_61_stale(impl, d):
    return _stale_fake(impl, d, 61)

def t_truncate_not_round(impl, d):
    path, p = fetched(impl, d)
    # 61.999999999 s old must print "61 s ago", never 62
    rc, out = impl.run(path, "status", env=now_env(p["fetch_epoch_ns"] + 62 * S - 1, p["monotonic_ns"] + 62 * S - 1))
    assert rc == 1 and STALE_RE.match(out[0]).group(2) == "61", (rc, out)
    # stamp at hh:mm:59.999999999 must display that minute and :59
    base = p["fetch_epoch_ns"] // (60 * S) * (60 * S) + 60 * S - 1
    shift = base - p["fetch_epoch_ns"]
    p["fetch_epoch_ns"] = base; p["monotonic_ns"] += shift
    write(path, rehash(p))
    rc, out = impl.run(path, "status", env=now_env(base + S // 2, p["monotonic_ns"] + S // 2))
    dt = datetime.datetime.fromtimestamp(base // S, ZoneInfo(ref.TZ_NAME))
    exp = "Time (fresh fetch): %d:%s, fetched %s [TEST CLOCK]" % (int(dt.strftime("%I")), dt.strftime("%M %p %Z"), dt.strftime("%H:%M:59"))
    assert rc == 0 and out[0] == exp, (rc, out, exp)
    return out[0]

def t_first_capture_format(impl, d):
    """Fixture built from Timothy's first capture epoch, 2026-10-18T16:10:47.863675037Z (test only)."""
    path, p = fetched(impl, d)
    e = 1792339847863675037
    shift = e - p["fetch_epoch_ns"]
    p["fetch_epoch_ns"] = e; p["monotonic_ns"] += shift
    write(path, rehash(p))
    rc, out = impl.run(path, "status", env=now_env(e + 5 * S, p["monotonic_ns"] + 5 * S))
    assert rc == 0 and out[0] == "Time (fresh fetch): 12:10 PM EDT, fetched 12:10:47 [TEST CLOCK]", (rc, out)
    assert ref.iso_from_ns(e, datetime.timezone.utc) == "2026-10-18T16:10:47.863675037Z"
    return out[0]

def t_missing(impl, d):
    rc, out = impl.run(os.path.join(d, "nope.json"), "status")
    assert rc == 2 and out[0] == NOFETCH, (rc, out); check_failure_line(out[0])
    return out[0]

def t_corrupt(impl, d):
    path, p = fetched(impl, d)
    good = open(path).read()
    variants = {"truncated": good[: len(good) // 2], "garbage": "not json at all {", "empty": "",
                "array": "[1,2,3]", "null": "null", "number": "42"}
    for k in ("sha256", "fetch_epoch_ns", "monotonic_ns", "boot_id", "iso_local"):
        q = dict(p); q.pop(k); variants["missing_" + k] = json.dumps(q)
    q = dict(p); q["fetch_epoch_ns"] = str(q["fetch_epoch_ns"]); variants["epoch_as_string"] = json.dumps(q)
    q = dict(p); q["monotonic_ns"] = float(q["monotonic_ns"]); variants["mono_as_float"] = json.dumps(q)
    q = dict(p); q["tz"] = "UTC"; variants["wrong_tz"] = json.dumps(rehash(q))
    q = dict(p); q["monotonic_ns"] = float(q["monotonic_ns"]); q["sha256"] = ref.payload_hash(q)
    variants["mono_as_float_rehashed"] = json.dumps(q)       # valid hash, wrong type
    for name, txt in variants.items():
        with open(path, "w") as f: f.write(txt)
        rc, out = impl.run(path, "status")
        assert rc == 2 and out[0] == NOFETCH, (name, rc, out)
    return "%d corrupt variants -> %s" % (len(variants), NOFETCH)

def t_hash_tamper(impl, d):
    path, p = fetched(impl, d)
    cases = {}
    q = dict(p); q["fetch_epoch_ns"] += 3600 * S; cases["epoch_no_rehash"] = q
    q = dict(p); q["monotonic_ns"] += 1; cases["mono_no_rehash"] = q
    q = dict(p); q["host"] = "evil"; cases["host_no_rehash"] = q
    q = dict(p); q["sha256"] = "0" * 64; cases["sha_zeroed"] = q
    q = dict(p); q["sha256"] = q["sha256"].upper(); cases["sha_upper"] = q
    q = dict(p); q["iso_local"] = "2026-10-18T09:00:00.000000000-04:00"; q["sha256"] = ref.payload_hash(q); cases["iso_local_rehashed_but_wrong"] = q
    q = dict(p); q["iso_utc"] = "2026-10-18T13:00:00.000000000Z"; q["sha256"] = ref.payload_hash(q); cases["iso_utc_rehashed_but_wrong"] = q
    for name, q in cases.items():
        write(path, q)
        rc, out = impl.run(path, "status")
        assert rc == 2 and out[0] == NOFETCH, (name, rc, out)
    return "%d tamper variants -> %s" % (len(cases), NOFETCH)

def t_future_stamp_rehashed(impl, d):
    path, p = fetched(impl, d)
    p["fetch_epoch_ns"] += 3600 * S          # wall says the fetch is an hour in the future
    write(path, rehash(p))
    rc, out = impl.run(path, "status")
    assert rc == 3 and out[0] == SKEW, (rc, out); check_failure_line(out[0])
    return out[0]

def t_future_small_fake(impl, d):
    path, p = fetched(impl, d)
    # wall age -1 s, mono age 0 s: diff 1 s (<2 s) so only the negative-age rule catches it
    rc, out = impl.run(path, "status", env=now_env(p["fetch_epoch_ns"] - S, p["monotonic_ns"]))
    assert rc == 3 and out[0] == SKEW + " [TEST CLOCK]", (rc, out); check_failure_line(out[0])
    return out[0]

def t_skew_mono_ahead(impl, d):
    path, p = fetched(impl, d)
    p["monotonic_ns"] -= 10 * S              # mono age 10 s, wall age ~0 s
    write(path, rehash(p))
    rc, out = impl.run(path, "status")
    assert rc == 3 and out[0] == SKEW, (rc, out); check_failure_line(out[0])
    return out[0]

def t_skew_wall_jump_fake(impl, d):
    path, p = fetched(impl, d)
    rc, out = impl.run(path, "status", env=now_env(p["fetch_epoch_ns"] + 30 * S, p["monotonic_ns"] + 10 * S))
    assert rc == 3 and out[0] == SKEW + " [TEST CLOCK]", (rc, out); check_failure_line(out[0])
    return out[0]

def t_skew_boundary(impl, d):
    path, p = fetched(impl, d)
    rc, out = impl.run(path, "status", env=now_env(p["fetch_epoch_ns"] + 12 * S, p["monotonic_ns"] + 10 * S))
    assert rc == 0 and FRESH_RE.match(out[0]), ("2 s exactly is allowed", rc, out)
    rc, out = impl.run(path, "status", env=now_env(p["fetch_epoch_ns"] + 12 * S + 1, p["monotonic_ns"] + 10 * S))
    assert rc == 3 and out[0].startswith(SKEW), ("2 s + 1 ns is skew", rc, out)
    return "2 s fresh / 2 s+1 ns skew"

def t_skew_beats_stale(impl, d):
    path, p = fetched(impl, d)
    rc, out = impl.run(path, "status", env=now_env(p["fetch_epoch_ns"] + 3600 * S, p["monotonic_ns"] + 100 * S))
    assert rc == 3 and out[0].startswith(SKEW), (rc, out)
    return out[0]

def t_other_boot(impl, d):
    path, p = fetched(impl, d)
    p["boot_id"] = "00000000-0000-0000-0000-000000000000"
    write(path, rehash(p))
    rc, out = impl.run(path, "status")
    assert rc == 3 and out[0] == BOOT, (rc, out); check_failure_line(out[0])
    return out[0]

def t_bad_test_clock(impl, d):
    path, p = fetched(impl, d)
    rc, out = impl.run(path, "status", env={"TIMECAP_TEST_NOW": "abc:def"})
    assert rc == 2 and "UNVERIFIED" in out[0], (rc, out); check_failure_line(out[0])
    return out[0]

def t_fetch_takes_no_time_args(impl, d):
    path = os.path.join(d, "s.json")
    rc, out = impl.run(path, "fetch", "2020-01-01T00:00:00Z")
    assert rc == 64 and not os.path.exists(path), (rc, out)
    # a fake 'now' must not leak into fetch
    rc, _ = impl.run(path, "fetch", env=now_env(10**18, 1))
    p = json.load(open(path))
    assert rc == 0 and abs(p["fetch_epoch_ns"] - time.time_ns()) < 5 * S, p
    return "fetch rejects time args; ignores TIMECAP_TEST_NOW"

def t_open_close_no_net(impl, d):
    path = os.path.join(d, "s.json")
    for cmd in ("open", "close"):
        rc, out = impl.run(path, cmd, env={"TIMECAP_TEST_NOW": "1:1"})   # must be ignored
        assert rc == 0 and FRESH_RE.match(out[0]) and "[TEST CLOCK]" not in out[0], (cmd, rc, out)
        assert out[1] == "External check: skipped (network unavailable or disabled)", out
    return out[0] + " / " + out[1]

class _H(http.server.BaseHTTPRequestHandler):
    offset = 0
    def do_HEAD(self):
        self.send_response_only(200)
        self.send_header("Date", self.date_time_string(time.time() + self.offset))
        self.end_headers()
    def log_message(self, *a): pass

def _server(offset):
    H = type("H", (_H,), {"offset": offset})
    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

def t_external_skew_local(impl, d):
    path = os.path.join(d, "s.json")
    srv = _server(3600)
    try:
        rc, out = impl.run(path, "open", env={"TIMECAP_NO_NET": None, "TIMECAP_EXT_URL": "http://127.0.0.1:%d/" % srv.server_port})
    finally:
        srv.shutdown()
    assert rc == 3 and out[0].startswith("Time UNVERIFIED: external clock skew detected"), (rc, out)
    assert len(out) == 1, out
    return out[0]

def t_external_ok_local(impl, d):
    path = os.path.join(d, "s.json")
    srv = _server(0)
    try:
        rc, out = impl.run(path, "close", env={"TIMECAP_NO_NET": None, "TIMECAP_EXT_URL": "http://127.0.0.1:%d/" % srv.server_port})
    finally:
        srv.shutdown()
    assert rc == 0 and FRESH_RE.match(out[0]) and out[1].startswith("External check: ok"), (rc, out)
    return out[1]

def t_external_down_skipped(impl, d):
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    path = os.path.join(d, "s.json")
    rc, out = impl.run(path, "open", env={"TIMECAP_NO_NET": None, "TIMECAP_EXT_URL": "http://127.0.0.1:%d/" % port})
    assert rc == 0 and FRESH_RE.match(out[0]) and out[1].startswith("External check: skipped"), (rc, out)
    return out[1]

TESTS = [t_fresh, t_stale_61, t_stale_3600, t_stale_3600_real_clock, t_boundary_60_fresh,
         t_boundary_60s_plus_1ns_stale, t_boundary_61_stale, t_truncate_not_round, t_first_capture_format,
         t_missing, t_corrupt, t_hash_tamper, t_future_stamp_rehashed, t_future_small_fake,
         t_skew_mono_ahead, t_skew_wall_jump_fake, t_skew_boundary, t_skew_beats_stale, t_other_boot,
         t_bad_test_clock, t_fetch_takes_no_time_args, t_open_close_no_net, t_external_skew_local,
         t_external_ok_local, t_external_down_skipped]

def t_cross(impls, d):
    a, b = impls
    for w, r in ((a, b), (b, a)):
        path, _ = fetched(w, d)
        rc, out = r.run(path, "status")
        assert rc == 0 and FRESH_RE.match(out[0]), (w.name, r.name, rc, out)
    return "py stamp read by sh and sh stamp read by py: fresh"


def run_suite(impls, verbose=True):
    res = []
    for impl in impls:
        for t in TESTS:
            d = tempfile.mkdtemp(prefix="tc_")
            try:
                msg = t(impl, d); ok = True
            except Exception as ex:
                msg = "FAIL %r" % (ex,); ok = False
            finally:
                shutil.rmtree(d, ignore_errors=True)
            res.append((impl.name, t.__name__, ok, msg))
    d = tempfile.mkdtemp(prefix="tc_")
    try:
        msg = t_cross(impls, d); ok = True
    except Exception as ex:
        msg = "FAIL %r" % (ex,); ok = False
    shutil.rmtree(d, ignore_errors=True)
    res.append(("py+sh", "t_cross_compat", ok, msg))
    if verbose:
        for r in res:
            print("%-5s %-32s %s  %s" % (r[0], r[1], "PASS" if r[2] else "FAIL", r[3]))
    return res

PY_MUTANTS = [
    ("PM01 staleness check removed", "if wall_age <= FRESH_MAX_NS:", "if True:"),
    ("PM02 skew check removed", "if wall_age < 0 or abs(wall_age - mono_age) > SKEW_MAX_NS:", "if False:"),
    ("PM03 future (negative age) check removed", "if wall_age < 0 or abs(", "if abs("),
    ("PM04 hash check removed", ' or payload_hash(p) != p["sha256"]', ""),
    ("PM05 boundary <= -> <", "if wall_age <= FRESH_MAX_NS:", "if wall_age < FRESH_MAX_NS:"),
    ("PM06 fresh limit 61 s", "FRESH_MAX_NS = 60 * 10**9", "FRESH_MAX_NS = 61 * 10**9"),
    ("PM07 stale seconds rounded", "wall_age // 10**9, tag", "round(wall_age / 10**9), tag"),
    ("PM08 missing stamp prints a plausible time", "        print(LINE_NOFETCH + tag)\n        return 2",
     '        print("Time (fresh fetch): 12:00 PM EDT, fetched 12:00:00")\n        return 0'),
    ("PM09 skew tolerance 20 s", "SKEW_MAX_NS = 2 * 10**9", "SKEW_MAX_NS = 20 * 10**9"),
    ("PM10 abs() dropped from skew", "abs(wall_age - mono_age)", "(wall_age - mono_age)"),
    ("PM11 boot check removed", 'if p["boot_id"] != boot_id():', "if False:"),
    ("PM12 iso_local consistency check removed", 'if p["iso_local"] != iso_from_ns(p["fetch_epoch_ns"], ZoneInfo(TZ_NAME)):', "if False:"),
    ("PM13 display seconds rounded", 'fromtimestamp(p["fetch_epoch_ns"] // 10**9,', 'fromtimestamp(round(p["fetch_epoch_ns"] / 10**9),'),
    ("PM14 external skew ignored", 'return ("skew" if abs(delta) > EXT_SKEW_MAX_S else "ok"), delta', 'return "ok", delta'),
    ("PM15 open honours fake clock", '    os.environ.pop("TIMECAP_TEST_NOW", None)\n', ""),
    ("PM16 fetch accepts a time argument", 'if len(args) != 1 or', 'if len(args) not in (1, 2) or'),
    ("PM17 TEST CLOCK tag dropped", 'return int(w), int(m), " [TEST CLOCK]"', 'return int(w), int(m), ""'),
    ("PM18 type check removed", "if type(p[k]) is not int:", "if False:"),
]
SH_MUTANTS = [
    ("SM01 staleness check removed", "if [ $wa -le $FRESH_MAX_NS ]; then", "if true; then"),
    ("SM02 skew check removed", "if [ $wa -lt 0 ] || [ $d -gt $SKEW_MAX_NS ]; then", "if false; then"),
    ("SM03 future (negative age) check removed", "if [ $wa -lt 0 ] || [ $d -gt", "if [ $d -gt"),
    ("SM04 hash check removed", '[ "$(canon_hash "$S_E" "$S_IL" "$S_IU" "$S_TZ" "$S_M" "$S_MC" "$S_HOST" "$S_BID" "$S_W")" = "$S_H" ] || return 1', "true"),
    ("SM05 boundary -le -> -lt", "if [ $wa -le $FRESH_MAX_NS ]; then", "if [ $wa -lt $FRESH_MAX_NS ]; then"),
    ("SM06 fresh limit 61 s", "FRESH_MAX_NS=60000000000", "FRESH_MAX_NS=61000000000"),
    ("SM07 stale seconds rounded", "$(( wa / 1000000000 )) s ago", "$(( (wa + 500000000) / 1000000000 )) s ago"),
    ("SM08 missing stamp prints a plausible time", 'if ! load "$path"; then echo "$LINE_NOFETCH$tag"; return 2; fi',
     'if ! load "$path"; then echo "Time (fresh fetch): 12:00 PM EDT, fetched 12:00:00"; return 0; fi'),
    ("SM09 skew tolerance 20 s", "SKEW_MAX_NS=2000000000", "SKEW_MAX_NS=20000000000"),
    ("SM10 abs dropped from skew", "d=$(( wa - ma )); [ $d -lt 0 ] && d=$(( -d ))", "d=$(( wa - ma ))"),
    ("SM11 boot check removed", 'if [ "$S_BID" != "$(boot_id)" ]; then', "if false; then"),
    ("SM12 iso_local consistency check removed", '[ "$S_IL" = "$(iso_local "$S_E")" ] || return 1', "true"),
    ("SM13 display seconds rounded", "local s=$(( S_E / 1000000000 )) t hms", "local s=$(( (S_E + 500000000) / 1000000000 )) t hms"),
    ("SM14 external skew ignored", "if [ $a -gt $EXT_SKEW_MAX_S ]; then EXT_STATE=skew; else EXT_STATE=ok; fi", "EXT_STATE=ok"),
    ("SM15 open honours fake clock", "  unset TIMECAP_TEST_NOW\n", ""),
    ("SM16 fetch accepts a time argument", '[ ${#args[@]} -eq 1 ] ||', '[ ${#args[@]} -ge 1 ] ||'),
    ("SM17 TEST CLOCK tag dropped", 'tag=" [TEST CLOCK]"', 'tag=""'),
    ("SM18 type check removed", '($n | all(test("^-?[0-9]+$")))', 'true'),
]

def make_impls(py_src, sh_src):
    return [Impl("py", ["python3", py_src]), Impl("sh", ["bash", sh_src])]

def run_mutants():
    rows = []
    for lang, muts, src_name in (("py", PY_MUTANTS, "timecap.py"), ("sh", SH_MUTANTS, "timecap.sh")):
        src = open(os.path.join(HERE, src_name)).read()
        for name, old, new in muts:
            assert src.count(old) >= 1, "mutant pattern not found: " + name
            d = tempfile.mkdtemp(prefix="mut_")
            mp = os.path.join(d, src_name)
            with open(mp, "w") as f: f.write(src.replace(old, new, 1))
            py = mp if lang == "py" else os.path.join(HERE, "timecap.py")
            sh = mp if lang == "sh" else os.path.join(HERE, "timecap.sh")
            impls = [i for i in make_impls(py, sh) if i.name == lang]
            res = [r for r in run_suite(impls, verbose=False) if r[0] == lang]
            failed = [r[1] for r in res if not r[2]]
            rows.append((name, bool(failed), failed))
            shutil.rmtree(d, ignore_errors=True)
    for name, killed, failed in rows:
        print("%-48s %s  by %s" % (name, "KILLED" if killed else "SURVIVED", ",".join(failed) if failed else "-"))
    k = sum(1 for r in rows if r[1])
    print("MUTANTS: %d/%d killed (py %d/%d, sh %d/%d)" % (k, len(rows),
          sum(1 for r in rows if r[1] and r[0].startswith("PM")), len(PY_MUTANTS),
          sum(1 for r in rows if r[1] and r[0].startswith("SM")), len(SH_MUTANTS)))
    return k == len(rows)

def live_external():
    """Optional real-network check; reported, never fails the suite."""
    out = {}
    for impl in make_impls(os.path.join(HERE, "timecap.py"), os.path.join(HERE, "timecap.sh")):
        d = tempfile.mkdtemp(prefix="tc_")
        rc, lines = impl.run(os.path.join(d, "s.json"), "open", env={"TIMECAP_NO_NET": None})
        shutil.rmtree(d, ignore_errors=True)
        out[impl.name] = (rc, lines)
        print("LIVE %s open rc=%d: %s" % (impl.name, rc, " | ".join(lines)))
    return out

if __name__ == "__main__":
    impls = make_impls(os.path.join(HERE, "timecap.py"), os.path.join(HERE, "timecap.sh"))
    res = run_suite(impls)
    n_ok = sum(1 for r in res if r[2])
    print("TESTS: %d/%d passed (py %d/%d, sh %d/%d, cross %d/1)" % (n_ok, len(res),
          sum(1 for r in res if r[0] == "py" and r[2]), sum(1 for r in res if r[0] == "py"),
          sum(1 for r in res if r[0] == "sh" and r[2]), sum(1 for r in res if r[0] == "sh"),
          sum(1 for r in res if r[0] == "py+sh" and r[2])))
    live_external()
    ok = n_ok == len(res)
    if "--mutants" in sys.argv:
        ok = run_mutants() and ok
    sys.exit(0 if ok else 1)
