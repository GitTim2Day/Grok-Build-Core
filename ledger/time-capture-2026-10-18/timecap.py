#!/usr/bin/env python3
"""timecap.py - fresh-clock capture (feature id time-capture-auto-2026-10-18).

Commands:
  fetch   read the system clock + monotonic counter, write the stamp file
  status  read the stamp, print ONE status line (never invents a time)
  open    fetch, optional external HTTP Date check, then status (start of reply)
  close   same as open (end of reply)

The stamp's time ALWAYS comes from this code's own clock reads; no command
accepts a time argument.  Stamp path: --stamp PATH, else $TIMECAP_STAMP,
else /workspace/time-capture/last_fetch.json.

Exit codes: 0 fresh; 1 stale; 2 unverified (missing/corrupt/hash);
3 unverified (clock skew / future stamp / different boot / external skew).

Test-only fake clock: if TIMECAP_TEST_NOW="<wall_ns>:<mono_ns>" is set, 'status'
uses it as "now" and every line it prints ends with " [TEST CLOCK]", so a fake
clock can never pass silently as a real time.  fetch/open/close ignore it.
"""
import datetime, hashlib, json, os, socket, sys, time, urllib.request, email.utils
from zoneinfo import ZoneInfo

TZ_NAME = "America/New_York"
DEFAULT_STAMP = "/workspace/time-capture/last_fetch.json"
FRESH_MAX_NS = 60 * 10**9        # fresh iff wall age <= 60 s exactly (ns precision)
SKEW_MAX_NS = 2 * 10**9          # wall age vs monotonic age
EXT_SKEW_MAX_S = 5               # vs HTTP Date header
EXT_URL = os.environ.get("TIMECAP_EXT_URL", "https://www.google.com")  # override is for tests
FIELDS = ("fetch_epoch_ns", "iso_local", "iso_utc", "tz", "monotonic_ns",
          "monotonic_clock", "host", "boot_id", "writer")
LINE_NOFETCH = "Time UNVERIFIED: no fetch available"
LINE_SKEW = "Time UNVERIFIED: clock skew detected"
LINE_BOOT = "Time UNVERIFIED: stamp is from a different boot (monotonic check impossible)"


def boot_id():
    try:
        with open("/proc/sys/kernel/random/boot_id") as f:
            return f.read().strip()
    except OSError:
        return "unknown"


def read_clocks():
    """Real clock reads. Wall = CLOCK_REALTIME, mono = CLOCK_BOOTTIME (same counter as /proc/uptime)."""
    wall = time.time_ns()
    mono = time.clock_gettime_ns(time.CLOCK_BOOTTIME)
    return wall, mono


def iso_from_ns(ns, tz):
    sec, frac = divmod(ns, 10**9)          # floor: truncation, never rounding
    d = datetime.datetime.fromtimestamp(sec, tz)
    off = d.strftime("%z")
    off = off[:3] + ":" + off[3:]
    if tz is datetime.timezone.utc:
        return d.strftime("%Y-%m-%dT%H:%M:%S") + ".%09dZ" % frac
    return d.strftime("%Y-%m-%dT%H:%M:%S") + ".%09d" % frac + off


def canonical(p):
    return "v1|" + "|".join(str(p[k]) for k in FIELDS)


def payload_hash(p):
    return hashlib.sha256(canonical(p).encode()).hexdigest()


def fetch(path):
    wall, mono = read_clocks()
    p = {
        "fetch_epoch_ns": wall,
        "iso_local": iso_from_ns(wall, ZoneInfo(TZ_NAME)),
        "iso_utc": iso_from_ns(wall, datetime.timezone.utc),
        "tz": TZ_NAME,
        "monotonic_ns": mono,
        "monotonic_clock": "CLOCK_BOOTTIME",
        "host": socket.gethostname(),
        "boot_id": boot_id(),
        "writer": "timecap.py",
    }
    p["sha256"] = payload_hash(p)
    d = os.path.dirname(path) or "."
    os.makedirs(d, exist_ok=True)
    tmp = "%s.tmp.%d" % (path, os.getpid())
    with open(tmp, "w") as f:
        json.dump(p, f, indent=1, sort_keys=True)
        f.write("\n")
    os.replace(tmp, path)              # atomic swap; the stamp is a runtime cache
    return p


def load(path):
    """Return a validated stamp dict or None (missing, corrupt, bad types, hash mismatch)."""
    try:
        with open(path) as f:
            p = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(p, dict):
        return None
    for k in FIELDS + ("sha256",):
        if k not in p:
            return None
    for k in ("fetch_epoch_ns", "monotonic_ns"):
        if type(p[k]) is not int:
            return None
    for k in ("iso_local", "iso_utc", "tz", "monotonic_clock", "host", "boot_id", "writer", "sha256"):
        if not isinstance(p[k], str):
            return None
    if p["tz"] != TZ_NAME or payload_hash(p) != p["sha256"]:
        return None
    # derived text must match the hashed epoch (catches consistent re-hash of a wrong iso field)
    if p["iso_local"] != iso_from_ns(p["fetch_epoch_ns"], ZoneInfo(TZ_NAME)):
        return None
    if p["iso_utc"] != iso_from_ns(p["fetch_epoch_ns"], datetime.timezone.utc):
        return None
    return p


def now_clocks():
    t = os.environ.get("TIMECAP_TEST_NOW")
    if t:
        w, m = t.split(":")
        return int(w), int(m), " [TEST CLOCK]"
    w, m = read_clocks()
    return w, m, ""


def hm(p):
    d = datetime.datetime.fromtimestamp(p["fetch_epoch_ns"] // 10**9, ZoneInfo(TZ_NAME))
    return "%d:%s %s" % (int(d.strftime("%I")), d.strftime("%M %p"), d.strftime("%Z")), d.strftime("%H:%M:%S")


def status(path):
    try:
        now_w, now_m, tag = now_clocks()
    except ValueError:
        print(LINE_NOFETCH + " [BAD TEST CLOCK]")
        return 2
    p = load(path)
    if p is None:
        print(LINE_NOFETCH + tag)
        return 2
    if p["boot_id"] != boot_id():
        print(LINE_BOOT + tag)
        return 3
    wall_age = now_w - p["fetch_epoch_ns"]
    mono_age = now_m - p["monotonic_ns"]
    if wall_age < 0 or abs(wall_age - mono_age) > SKEW_MAX_NS:
        print(LINE_SKEW + tag)
        return 3
    t, hms = hm(p)
    if wall_age <= FRESH_MAX_NS:
        print("Time (fresh fetch): %s, fetched %s%s" % (t, hms, tag))
        return 0
    print("Time: %s — STALE, fetched %d s ago%s" % (t, wall_age // 10**9, tag))
    return 1


def external_check():
    """Return (state, delta_s). state in ok|skew|skipped. Never fails on network absence."""
    if os.environ.get("TIMECAP_NO_NET") == "1":
        return "skipped", None
    try:
        req = urllib.request.Request(EXT_URL, method="HEAD")
        with urllib.request.urlopen(req, timeout=3) as r:
            hdr = r.headers.get("Date")
        local = time.time_ns() // 10**9
        remote = int(email.utils.parsedate_to_datetime(hdr).timestamp())
    except Exception:
        return "skipped", None
    delta = local - remote
    return ("skew" if abs(delta) > EXT_SKEW_MAX_S else "ok"), delta


def open_close(path):
    fetch(path)
    state, delta = external_check()
    if state == "skew":
        print("Time UNVERIFIED: external clock skew detected (%+d s vs %s Date header)" % (delta, EXT_URL))
        return 3
    os.environ.pop("TIMECAP_TEST_NOW", None)
    rc = status(path)
    if state == "ok":
        print("External check: ok (%+d s vs %s Date header, limit %d s)" % (delta, EXT_URL, EXT_SKEW_MAX_S))
    else:
        print("External check: skipped (network unavailable or disabled)")
    return rc


def main(argv):
    args = list(argv[1:])
    path = os.environ.get("TIMECAP_STAMP", DEFAULT_STAMP)
    if "--stamp" in args:
        i = args.index("--stamp")
        path = args[i + 1]
        del args[i:i + 2]
    if len(args) != 1 or args[0] not in ("fetch", "status", "open", "close"):
        print("usage: timecap.py [--stamp PATH] fetch|status|open|close", file=sys.stderr)
        return 64
    cmd = args[0]
    if cmd == "fetch":
        p = fetch(path)
        print("fetched %s -> %s" % (p["iso_local"], path))
        return 0
    if cmd == "status":
        return status(path)
    return open_close(path)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
