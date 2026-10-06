#!/usr/bin/env python3
"""ui_smoke.py -- headless UI smoke test, ONLY if a Chromium/Chrome is already installed (nothing is installed).

Starts the kit server on a free localhost port (temporary data dir), loads /?smoke=1 in headless
Chromium, and reads the page's own smoke verdict (boot, descend 8647, frames 4x32x32x3, pixel paint,
files, agent citation, JS sandbox = 42, sandbox has no fetch). Optional --screenshot PATH.
No browser found -> prints 'SKIP' and exits 0 (marked as skipped, not passed).
"""
from __future__ import annotations
import argparse, json, os, shutil, signal, subprocess, sys, tempfile, threading, time

KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
BROWSERS = ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome", "msedge"]
FLAGS = ["--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check", "--disable-extensions",
         "--disable-background-networking", "--disable-component-update", "--disable-sync", "--disable-default-apps",
         "--metrics-recording-only", "--disable-domain-reliability", "--disable-client-side-phishing-detection",
         "--safebrowsing-disable-auto-update", "--password-store=basic", "--use-mock-keychain"]


GROUP = {"start_new_session": True} if os.name == "posix" else {}


def kill_group(p):
    """Kill the browser's whole process group (renderers, GPU, zygote), not just the parent."""
    try:
        if os.name == "posix":
            os.killpg(p.pid, signal.SIGKILL)
        elif p.poll() is None:
            p.kill()
    except Exception:
        pass


def find_browser():
    for b in BROWSERS:
        p = shutil.which(b)
        if p:
            return p
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--screenshot", default="")
    a = ap.parse_args(argv)
    br = find_browser()
    if not br:
        print("SKIP: no Chromium/Chrome on this device (UI smoke not run; nothing installed)")
        return 0
    import server
    data = tempfile.mkdtemp(prefix="kit-ui-smoke-")
    srv = server.make_server("127.0.0.1", 0, data)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.port}/?smoke=1"
    prof = tempfile.mkdtemp(prefix="kit-ui-prof-")
    base = [br, *FLAGS, f"--user-data-dir={prof}", "--virtual-time-budget=20000", "--window-size=1280,1100"]
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        base.append("--no-sandbox")
    try:
        # 1) REAL-TIME run with the browser's default process model (sandboxed iframes isolated as in normal use).
        #    The page writes its own verdict to workspace/smoke_result.json in the temp data dir.
        rt = [br, *FLAGS, f"--user-data-dir={prof}", "--window-size=1280,1100"] + base[len(FLAGS) + 4:]
        proc = subprocess.Popen(rt + [url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                                **GROUP)
        res_path = os.path.join(data, "workspace", "smoke_result.json")
        deadline = time.time() + 90
        while time.time() < deadline and not os.path.exists(res_path):
            time.sleep(0.25)
        kill_group(proc)
        proc.wait(timeout=10)
        if not os.path.exists(res_path):
            print("SMOKE (no verdict within 90 s)")
            ok = False
        else:
            time.sleep(0.2)
            res = json.load(open(res_path))
            print("SMOKE", json.dumps(res))
            ok = res.get("verdict") == "PASS"
        if a.screenshot:
            # 2) screenshot uses virtual time; virtual time does not wait for out-of-process iframes, so isolation
            #    is turned off for this capture only (the real-time verdict above keeps the default).
            prof2 = tempfile.mkdtemp(prefix="kit-ui-prof-")
            shot = [br, *FLAGS, "--disable-features=IsolateSandboxedIframes", f"--user-data-dir={prof2}",
                    "--virtual-time-budget=20000", "--window-size=1280,1100"] + base[len(FLAGS) + 4:]
            os.makedirs(os.path.dirname(os.path.abspath(a.screenshot)), exist_ok=True)
            sp = subprocess.Popen(shot + [f"--screenshot={os.path.abspath(a.screenshot)}", url], stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, **GROUP)
            try:
                sp.wait(timeout=120)
            except subprocess.TimeoutExpired:
                pass
            finally:
                kill_group(sp)
                sp.wait(timeout=10)
            print("screenshot:", a.screenshot if os.path.exists(a.screenshot) else "not written")
        print("UI_SMOKE:", "PASS" if ok else "FAIL", f"(browser {os.path.basename(br)}, real-time, default isolation)")
        return 0 if ok else 1
    finally:
        srv.shutdown()
        srv.server_close()


if __name__ == "__main__":
    raise SystemExit(main())
