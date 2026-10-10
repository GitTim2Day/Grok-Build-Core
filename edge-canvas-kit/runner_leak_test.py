#!/usr/bin/env python3
"""runner_leak_test.py -- tests for RUNNER_READ spec v2 (knowledge/RUNNER_READ_SPEC_v2_2026-10-10.md).

Calls lib.runner.run_capped directly with small Python children, so it runs without
bwbasic or a C++ compiler. Prints PASS/FAIL per test and SUMMARY. POSIX only.
"""
import os
import signal
import subprocess
import sys
import threading
import time

KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
from lib import runner  # noqa: E402

PY = sys.executable
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS: " if ok else "FAIL: ") + name + ("" if ok else "  | " + str(detail)))


def fds():
    return len(os.listdir("/proc/self/fd")) if os.path.isdir("/proc/self/fd") else -1


def run(code, timeout=5, cap=runner.OUT_CAP, stdin_text=None):
    return runner.run_capped([PY, "-c", code], cwd=KIT, timeout=timeout, cap=cap, stdin_text=stdin_text)


def main():
    if os.name != "posix":
        print("SKIP: POSIX only")
        return 0
    base_threads, base_fds = threading.active_count(), fds()

    # T1 escaped grandchild keeps the pipe open (it reports its pid so this test kills it: no stray)
    t = time.time()
    r = run("import subprocess,sys; g=subprocess.Popen([sys.executable,'-c','import time; time.sleep(8)'],"
            " start_new_session=True); print('GPID', g.pid); print('child done', flush=True)")
    dt = time.time() - t
    for ln in r["out"].splitlines():
        if ln.startswith("GPID "):
            try:
                os.kill(int(ln.split()[1]), signal.SIGKILL)
            except (ValueError, OSError):
                pass
    check("T1_returns_fast", dt < 1.5, round(dt, 2))
    check("T1_own_output_kept", "child done" in r["out"], repr(r["out"][:80]))
    check("T1_held_flagged", r.get("held") is True and "still held" in r["out"], (r.get("held"), r["out"][-90:]))
    check("T1_threads_flat", threading.active_count() == base_threads, (base_threads, threading.active_count()))
    check("T1_fds_flat", fds() == base_fds, (base_fds, fds()))

    # T2 normal output
    r = run("print('alpha'); print('beta')")
    check("T2_output_exact", r["out"] == "alpha\nbeta\n" and r["rc"] == 0 and not r["timed_out"]
          and not r["capped"] and r.get("held") is False, r)

    # T3 timeout
    t = time.time()
    r = run("import time; time.sleep(30)", timeout=1)
    dt = time.time() - t
    check("T3_timeout", r["timed_out"] and dt < 3, (r["timed_out"], round(dt, 2)))

    # T4 output cap
    r = run("import sys\nwhile True: sys.stdout.write('X'*1000)", cap=50000)
    check("T4_cap", r["capped"] and len(r["out"]) < 50000 + 200 and not r["timed_out"], (r["capped"], len(r["out"])))

    # T5 stdin round trip
    data = ("0123456789" * 6000)
    r = run("import sys; sys.stdout.write(sys.stdin.read())", stdin_text=data, cap=100000)
    check("T5_stdin_roundtrip", r["out"] == data, len(r["out"]))

    # T6 no deadlock: child writes 200 KB before reading stdin
    r = run("import sys; sys.stdout.write('Y'*200000); sys.stdout.flush(); d=sys.stdin.read(); "
            "sys.stdout.write('|%d' % len(d))", stdin_text=data, cap=300000, timeout=10)
    check("T6_no_deadlock", (not r["timed_out"]) and r["out"].endswith("|60000"), (r["timed_out"], r["out"][-20:]))

    # T7 rc pass-through
    r = run("import sys; sys.exit(3)")
    check("T7_rc", r["rc"] == 3 and r["out"] == "", (r["rc"], r["out"]))

    # T8 late output
    r = run("import time; time.sleep(0.5); print('late')")
    check("T8_late_output", r["out"] == "late\n", repr(r["out"]))

    # T9 stdout closed early, child keeps running
    t = time.time()
    r = run("import os,time; os.close(1); time.sleep(30)", timeout=1)
    check("T9_closed_early_times_out", r["timed_out"] and time.time() - t < 3, (r["timed_out"], time.time() - t))

    # T10 many runs: nothing accumulates
    th0, fd0 = threading.active_count(), fds()
    for i in range(30):
        run("print(%d)" % i)
    check("T10_threads_flat_30_runs", threading.active_count() == th0, (th0, threading.active_count()))
    check("T10_fds_flat_30_runs", fds() == fd0, (fd0, fds()))

    # T11 every pipe object explicitly closed on return (CLEAR), not left to garbage collection
    made = []
    real = subprocess.Popen

    class Rec(real):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            made.append(self)
    runner.subprocess.Popen = Rec
    try:
        run("print('x')")
        run("import time; time.sleep(30)", timeout=1)
        run("import sys; sys.stdout.write(sys.stdin.read())", stdin_text="abc")
    finally:
        runner.subprocess.Popen = real
    opened = [(q.stdout, q.stdin) for q in made]
    check("T11_pipes_closed_explicitly", len(made) == 3 and all((o is None or o.closed) and (i is None or i.closed)
                                                               for o, i in opened),
          [(o is not None and o.closed, i is not None and i.closed) for o, i in opened])

    ok = all(results)
    print("TOTAL pass=%d fail=%d" % (sum(results), len(results) - sum(results)))
    print("SUMMARY: " + ("ALL PASS" if ok else "FAILURES"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
