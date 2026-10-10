#!/usr/bin/env python3
"""mutants.py -- mutation tests for the edge-canvas-kit self-checks (box build tool; also shipped for re-runs).

Each mutant copies the kit to a temp dir, applies ONE deliberate bug (exact-once string replace),
and runs the matching test (selfcheck --quick, selfcheck full for C++, or ui_smoke for UI).
CAUGHT = the test failed (non-zero exit or timeout). A baseline (no mutation) must PASS first.

Safety (R6, after the runaway incident): mutants run ONE AT A TIME; each test runs in its own process
group with KIT_SELFTEST_ACTIVE=1 and a hard timeout, and the whole group is killed on teardown. After each
mutant, any process still living under the mutants temp dir is counted and killed; more than STRAY_ABORT
of them stops the run (exit 3). Use --only NAME to run a single mutant (the box runs them that way).
"""
from __future__ import annotations
import argparse, os, shutil, signal, subprocess, sys, tempfile, time

KIT = os.path.dirname(os.path.abspath(__file__))
Q, FULL, UI = "quick", "full", "ui"
MUTANTS = [
    ("descend_walk_wrong_add", "lib/descend.py", "d[k] += d[k + 1]", "d[k] += d[k]", Q),
    ("descend_walk_short_range", "lib/descend.py", "        for k in range(n):\n            d[k] += d[k + 1]", "        for k in range(n - 1):\n            d[k] += d[k + 1]", Q),
    ("descend_zero_den_unguarded", "lib/descend.py", "    except ZeroDivisionError:\n        raise DescendError", "    except KeyError:\n        raise DescendError", Q),
    ("frames_fps_30_allowed", "lib/frames.py", "FPS_ALLOWED = (32, 64)", "FPS_ALLOWED = (30, 32, 64)", Q),
    ("frames_green_from_d2", "lib/frames.py", "buf[j + 1] = (di[1] // D) % 256", "buf[j + 1] = (di[2] // D) % 256", Q),
    ("fsguard_realpath_escape_off", "lib/fsguard.py", "        if full != self.root and not full.startswith(self.root + os.sep):\n            raise GuardError(\"path escapes", "        if False:\n            raise GuardError(\"path escapes", Q),
    ("fsguard_dotdot_and_hidden_off", "lib/fsguard.py", "            if s == \"..\":\n                raise GuardError(\"path traversal refused\", 403)", "            if s == \"..\" and False:\n                raise GuardError(\"path traversal refused\", 403)\n            if s == \"..\":\n                continue", Q),
    ("fsguard_dotdot_check_off", "lib/fsguard.py", "            if s == \"..\":\n                raise GuardError(\"path traversal refused\", 403)", "            if s == \"..\" and False:\n                raise GuardError(\"path traversal refused\", 403)", Q),
    ("fsguard_no_archive_on_overwrite", "lib/fsguard.py", "            shutil.copy2(full, dest)\n            archived = self.rel(dest)", "            archived = \"\"", Q),
    ("fsguard_archive_writable", "lib/fsguard.py", "not (i == 0 and s == ARCHIVE and not for_write)", "not (i == 0 and s == ARCHIVE)", Q),
    ("server_token_ignored", "server.py", "        if self.server.require_token:\n            got", "        if False:\n            got", Q),
    ("server_host_check_off", "server.py", "        if not self._host_ok():\n            raise ApiError(403", "        if False:\n            raise ApiError(403", Q),
    ("server_client_header_off", "server.py", "        if self.headers.get(\"X-Kit-Client\") != \"1\":", "        if False:", Q),
    ("server_json_cap_1GiB", "server.py", "CAP_JSON = 1 * 2**20", "CAP_JSON = 1 * 2**30", Q),
    ("server_lan_runs_allowed", "server.py", "        if self.server.lan and not self.server.allow_remote_run:", "        if False:", Q),
    ("server_csp_wildcard", "server.py", "CSP_MAIN = (\"default-src 'self'; script-src 'self';", "CSP_MAIN = (\"default-src *; script-src * 'unsafe-inline';", Q),
    ("server_filename_unsanitized", "server.py", "name = re.sub(r\"[^A-Za-z0-9._-]+\", \"_\", os.path.basename(raw_name.replace(\"\\\\\", \"/\"))).lstrip(\".\") or \"upload.bin\"", "name = raw_name", Q),
    ("server_keepalive_after_error", "server.py", "        if status >= 400:   # an unread", "        if False:   # an unread", Q),
    ("runner_cpu_limit_equals_wall", "lib/runner.py", "stdin_text=stdin_text, cpu=run_timeout + 2)", "stdin_text=stdin_text, cpu=1)", FULL),
    ("server_origin_check_off", "server.py", "            if origin.lower() != \"http://\" + (self.headers.get(\"Host\") or \"\").lower():", "            if False:", Q),
    ("runner_basic_shell_allowed", "lib/runner.py", "BASIC_DENY = [\"SHELL\", ", "BASIC_DENY = [", Q),
    ("runner_cpp_system_allowed", "lib/runner.py", "CPP_DENY = [\"system\", ", "CPP_DENY = [", Q),
    ("runner_cpp_header_allowlist_off", "lib/runner.py", "            if m.group(1) not in CPP_HEADERS:", "            if False:", Q),
    ("runner_output_cap_off", "lib/runner.py", "        if len(chunk) > room:\n            st[\"capped\"] = True\n            kill()\n            return \"cap\"", "        if False:\n            st[\"capped\"] = True\n            kill()\n            return \"cap\"", Q),
    ("runner_v2_drain_skipped", "lib/runner.py", "            if child_done:\n                if not st[\"out_done\"]:\n                    drain()", "            if child_done:\n                if False:\n                    drain()", Q),
    ("runner_v2_held_not_flagged", "lib/runner.py", "        elif r == \"empty\":\n            st[\"held\"] = True", "        elif r == \"empty\":\n            pass", Q),
    ("runner_v2_waits_for_eof", "lib/runner.py", "            if child_done:\n                if not st[\"out_done\"]:", "            if child_done and st[\"out_done\"]:\n                if not st[\"out_done\"]:", Q),
    ("runner_v2_stdin_never_closed", "lib/runner.py", "                    if pos >= len(stdin_bytes):\n                        sel.unregister(in_fd)\n                        try:\n                            p.stdin.close()", "                    if pos >= len(stdin_bytes):\n                        sel.unregister(in_fd)\n                        try:\n                            pass", Q),
    ("runner_v2_pipe_not_closed", "lib/runner.py", "            os.close(pidfd)\n        p.stdout.close()", "            os.close(pidfd)", Q),
    ("runner_v2_pidfd_not_closed", "lib/runner.py", "        if pidfd is not None:\n            os.close(pidfd)", "        if pidfd is not None:\n            pass", Q),
    ("runner_v2_timeout_off", "lib/runner.py", "            if remaining <= 0:\n                st[\"timed_out\"] = True", "            if remaining <= -3600:\n                st[\"timed_out\"] = True", Q),
    ("runner_boot_expect_wrong", "lib/runner.py", "    expect = \"0.70710678\"", "    expect = \"0.7071067\"", Q),
    ("agent_cover_gate_off", "agent.py", "MIN_COVER = 0.5", "MIN_COVER = 0.0", Q),
    ("agent_citation_off_by_one", "agent.py", "            a = h[\"a\"] + pick[0][0]", "            a = h[\"a\"] + pick[0][0] + 1", Q),
    ("agent_indexes_tests", "agent.py", "EXCLUDE = {\"selfcheck.py\", \"ui_smoke.py\"}", "EXCLUDE = set()", Q),
    ("mask_email_rule_off", "lib/mask.py", "[A-Za-z0-9._%+\\-]+@[A-Za-z0-9\\-]+", "[A-Za-z0-9._%+\\-]+@@[A-Za-z0-9\\-]+", Q),
    ("optional_ollama_remote", "lib/optional.py", "OLLAMA_URL = \"http://127.0.0.1:11434\"", "OLLAMA_URL = \"http://ollama.example.net:11434\"", Q),
    ("rcrj_fix_reverted", "vendor/txt_rcrj/rcrj.py", "        if not isinstance(rec, dict):   # malformed record: reject node, continue\n            rejects.append(reject_entry(\"bad_record\", repr(rec)[:80], \"structure\", f\"record#{n}\"))\n            continue\n        ctx = f\"{rec.get('source','')}:{rec.get('line_no','')}\"", "        ctx = f\"{rec.get('source','')}:{rec.get('line_no','')}\"\n        if not isinstance(rec, dict):\n            rejects.append(reject_entry(\"bad_record\", repr(rec)[:80], \"structure\", ctx))\n            continue", Q),
    ("to_txt_dtd_check_off", "vendor/txt_rcrj/to_txt.py", "    if _DTD.search(b):\n        raise XmlForbidden", "    if False:\n        raise XmlForbidden", Q),
    ("to_txt_fallback_exception_wide", "vendor/txt_rcrj/to_txt.py", "    DefusedXmlException = XmlForbidden", "    DefusedXmlException = Exception", Q),
    ("cpp_descend_wrong_walk", "cpp/descend.cpp", "d[k] = add(d[k], d[k + 1]);", "d[k] = add(d[k], d[k]);", FULL),
    ("cpp_conflict_bot_autoenable", "cpp/conflict_nodes.cpp", "        case 5: if (!s.boton) s.botskip = 1; return;", "        case 5: s.boton = true; return;", FULL),
    ("cpp_overflow_check_off", "cpp/descend.cpp", "    if (aa > LLONG_MAX / bb) throw std::overflow_error(\"mul\");", "", FULL),
    ("agent_selftest_guard_off", "agent.py", "        if os.environ.get(SELFTEST_FLAG) == \"1\":", "        if False:", Q),
    ("agent_selftest_child_flag_off", "agent.py", "        env[SELFTEST_FLAG] = \"1\"\n", "        env.pop(SELFTEST_FLAG, None)\n", Q),
    ("agent_selftest_same_group", "agent.py", "        kw = {\"start_new_session\": True}", "        kw = {\"start_new_session\": False}", Q),
    ("selfcheck_quick_calls_selftest", "selfcheck.py", "    if not a.quick:\n        st, j, _, _ = req(lan.port, \"POST\", \"/api/agent\", body={\"q\": \"/selftest\"}", "    if True:\n        st, j, _, _ = req(lan.port, \"POST\", \"/api/agent\", body={\"q\": \"/selftest\"}", Q),
    ("server_lan_runs_allowed_full", "server.py", "        if self.server.lan and not self.server.allow_remote_run:", "        if False:", FULL),
    ("ui_frame_channel_swap", "ui/app.js", "px[i * 4] = bin.charCodeAt(j); px[i * 4 + 1] = bin.charCodeAt(j + 1);", "px[i * 4] = bin.charCodeAt(j + 1); px[i * 4 + 1] = bin.charCodeAt(j);", UI),
    ("ui_sandbox_fetch_left_on", "ui/sandbox.js", "self.fetch=undefined;", "", UI),
    ("ui_sandbox_origin_check_off", "ui/app.js", "    if (ev.source !== $(\"jsbox\").contentWindow) return;   // only our sandbox\n", "", None),
    # ---- R8: Spectrum Sweep
    ("sweep_axis_order_flipped", "lib/sweep.py", "AXIS_EXPS = tuple(range(7, 17))", "AXIS_EXPS = tuple(range(16, 6, -1))", Q),
    ("sweep_redshift_multiply", "lib/sweep.py", "    return f_emit / one_plus_z", "    return f_emit * one_plus_z", Q),
    ("sweep_label_microondas", "lib/sweep.py", "(\"Undae minimae\", 10**9", "(\"Microondas\", 10**9", Q),
    ("sweep_decay_sign_flipped", "lib/sweep.py", "e = math.exp(-kf * xf)", "e = math.exp(kf * xf)", Q),
    ("sweep_samples_cap_off", "lib/sweep.py", "    if N > MAX_SAMPLES:\n        raise SweepError", "    if False:\n        raise SweepError", Q),
    ("sweep_z_cap_off", "lib/sweep.py", "if Z < 0 or Z > MAX_Z:", "if Z < 0:", Q),
    ("sweep_visible_band_800THz", "lib/sweep.py", "VIS_HI_HZ = 790 * 10**12", "VIS_HI_HZ = 800 * 10**12", Q),
    ("sweep_trunc_rounds", "lib/sweep.py", "t = format(d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_DOWN), \"f\")", "t = format(d.quantize(Decimal(1).scaleb(-places), rounding=\"ROUND_HALF_UP\"), \"f\")", Q),
    ("sweep_overlay_newline_allowed", "lib/sweep.py", "    if _CTRL.search(text):", "    if False:", Q),
    ("sweep_rgb_blue_green_swap", "lib/sweep.py", "r, g, b = 0.0, (lam - 440) / (490 - 440), 1.0", "r, g, b = 0.0, 1.0, (lam - 440) / (490 - 440)", Q),
    ("sweep_pow2_not_exact", "lib/sweep.py", "    if k is not None:\n        return f\"{k}.00000000\"", "    if False:\n        return f\"{k}.00000000\"", Q),
    ("server_sweep_unknown_params_allowed", "server.py", "        if unknown:\n            raise ApiError(400, f\"unknown sweep", "        if False:\n            raise ApiError(400, f\"unknown sweep", Q),
    ("ui_sweep_audio_on_by_default", "ui/index.html", "<input id=\"swaudio\" type=\"checkbox\">", "<input id=\"swaudio\" type=\"checkbox\" checked>", Q),
    ("basic_sweep_multiply_redshift", "basic/sweep.bas", "390 FO = 500000000000000 / (1 + 1)", "390 FO = 500000000000000 * (1 + 1)", Q),
    ("cpp_sweep_trunc_rounds", "cpp/sweep.cpp", "long long fp = (long long)std::floor((v - (long double)ip) * 100000000.0L);", "long long fp = (long long)std::round((v - (long double)ip) * 100000000.0L);", FULL),
    ("sweep_cut_scientific", "lib/sweep.py", "rounding=ROUND_DOWN), \"f\")", "rounding=ROUND_DOWN), \"\")", Q),
    ("server_query_fields_500", "server.py", "            except ValueError:\n                raise ApiError(400, \"too many query fields\")", "            except KeyError:\n                raise ApiError(400, \"too many query fields\")", Q),
    ("ui_sweep_axis_flip", "ui/app.js", "return AX.T + (AX.hi - L) / (AX.hi - AX.lo)", "return AX.T + (L - AX.lo) / (AX.hi - AX.lo)", UI),
    ("ui_sweep_overlay_multiline", "ui/app.js", ".replace(/[\\u0000-\\u001f\\u007f\\u2028\\u2029]+/g, \" \").replace(/\\s+/g, \" \")", "", UI),
]


def copy_kit(dst):
    shutil.copytree(KIT, dst, ignore=shutil.ignore_patterns("runs", ".tmp", "__pycache__", "*.pyc", "workspace"))
    os.makedirs(os.path.join(dst, "workspace"), exist_ok=True)


STRAY_ABORT = 50
TMP_PREFIX = os.path.join(tempfile.gettempdir(), "kit-mutants-")


def kill_group(p):
    try:
        if os.name == "posix":
            os.killpg(p.pid, signal.SIGKILL)
        elif p.poll() is None:
            p.kill()
    except Exception:
        pass


def strays():
    """PIDs (not us) whose command line or cwd is under a kit-mutants temp dir (Linux /proc; else empty)."""
    me, found = os.getpid(), []
    if not os.path.isdir("/proc"):
        return found
    for d in os.listdir("/proc"):
        if not d.isdigit() or int(d) == me:
            continue
        try:
            cmd = open(f"/proc/{d}/cmdline", "rb").read().replace(b"\0", b" ").decode("utf-8", "replace")
            try:
                cwd = os.readlink(f"/proc/{d}/cwd")
            except OSError:
                cwd = ""
            if TMP_PREFIX in cmd or cwd.startswith(TMP_PREFIX):
                found.append(int(d))
        except OSError:
            continue
    return found


def sweep(label):
    """Kill leftovers after a mutant. Returns how many were found; aborts the run if too many."""
    pids = strays()
    for pid in pids:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
    if pids:
        print(f"STRAYS: {len(pids)} process(es) left after {label}; killed")
    if len(pids) > STRAY_ABORT:
        print(f"ABORT: more than {STRAY_ABORT} stray processes after {label}; stopping")
        raise SystemExit(3)
    return len(pids)


def run_test(kit, mode, timeout=240):
    cmd = {Q: [sys.executable, "selfcheck.py", "--quick"], FULL: [sys.executable, "selfcheck.py"],
           UI: [sys.executable, "ui_smoke.py"]}[mode]
    env = dict(os.environ)
    env["KIT_SELFTEST_ACTIVE"] = "1"
    kw = {"start_new_session": True} if os.name == "posix" else {}
    p = subprocess.Popen(cmd, cwd=kit, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                         stdin=subprocess.DEVNULL, env=env, **kw)
    try:
        out, _ = p.communicate(timeout=timeout)
        tail = [ln for ln in (out or "").splitlines() if ln.startswith(("FAIL", "SUMMARY", "UI_SMOKE", "SKIP: ui"))][:4]
        return p.returncode, " / ".join(tail)[:300]
    except subprocess.TimeoutExpired:
        return "timeout", "test timed out (counts as caught)"
    finally:
        kill_group(p)
        try:
            p.communicate(timeout=10)
        except Exception:
            pass


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append", default=[], help="run just this mutant (repeatable)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--no-baseline", action="store_true")
    a = ap.parse_args(argv)
    if a.list:
        for m in MUTANTS:
            print(m[0], m[4] or "UNTESTED")
        return 0
    unknown = set(a.only) - {m[0] for m in MUTANTS}
    if unknown:
        print(f"ERROR: unknown mutant(s) {sorted(unknown)}")
        return 2
    sweep("start")
    tmp = tempfile.mkdtemp(prefix="kit-mutants-")
    if not a.no_baseline:
        base = os.path.join(tmp, "baseline")
        copy_kit(base)
        rc, tail = run_test(base, Q)
        sweep("baseline")
        print(f"BASELINE quick: rc={rc} {tail}")
        if rc != 0:
            print("SUMMARY: BASELINE FAILED -- mutants not meaningful")
            return 2
    caught = total = 0
    rows = []
    for name, fn, old, new, mode in MUTANTS:
        if a.only and name not in a.only:
            continue
        if mode is None:
            print(f"NOTE: {name} -- not runnable headless (equivalent under smoke test); listed as UNTESTED")
            rows.append((name, "UNTESTED", ""))
            continue
        total += 1
        d = os.path.join(tmp, name)
        copy_kit(d)
        p = os.path.join(d, fn)
        s = open(p, encoding="utf-8").read()
        n = s.count(old)
        if n != 1:
            print(f"ERROR: {name}: pattern found {n} times (mutant not applied)")
            rows.append((name, "NOT_APPLIED", f"count={n}"))
            continue
        open(p, "w", encoding="utf-8").write(s.replace(old, new))
        t = time.time()
        rc, tail = run_test(d, mode)
        sweep(name)
        ok = rc != 0
        caught += ok
        rows.append((name, "CAUGHT" if ok else "SURVIVED", tail))
        print(f"{'CAUGHT' if ok else 'SURVIVED'}: {name} [{mode}] rc={rc} {time.time() - t:.1f}s | {tail}")
    print(f"MUTANTS caught={caught}/{total}")
    print("SUMMARY: ALL MUTANTS CAUGHT" if caught == total else f"SUMMARY: SURVIVORS={total - caught}")
    return 0 if caught == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
