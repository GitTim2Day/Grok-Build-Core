#!/usr/bin/env python3
"""server.py -- edge-canvas-kit local server (Python 3 standard library only).

    python3 server.py                  # http://127.0.0.1:8765  (this device only)
    python3 server.py --lan            # home network; prints a token URL; token required on every API call
    python3 server.py --port 9000 --data-dir /media/usb/kit-data

Offline-first (DM-1..DM-7): no outbound network calls. The only client socket the kit can
open is the optional Ollama probe at 127.0.0.1:11434 (agent "local model" mode).
Main line keeps moving: every optional extra is NEED -> GOSUB -> RETURN (see lib/optional.py).
Security: localhost by default; --lan needs a token; per-endpoint size caps; Host/Origin checks;
required X-Kit-Client header (blocks cross-site form posts); CSP + nosniff headers; argv lists,
never a shell. BASIC/C++ runs are the only code execution and are localhost-only unless
--allow-remote-run is given (guard rails in lib/runner.py, not a full sandbox).
"""
from __future__ import annotations
import argparse, hmac, json, os, re, secrets, sys, threading, time, traceback, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

KIT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT_DIR)
sys.path.insert(0, os.path.join(KIT_DIR, "vendor", "txt_rcrj"))

from lib import descend, frames, fsguard, optional, runner  # noqa: E402
from lib.mask import mask  # noqa: E402
import agent as agent_mod  # noqa: E402

VERSION = "edge-canvas-kit 2026-10-06"
DEFAULT_PORT = 8765
CAP_JSON = 1 * 2**20
CAP_CONVERT = 16 * 2**20
CAP_WRITE = fsguard.MAX_WRITE * 2 + 4096   # base64 headroom
STATIC = {"index.html": "text/html; charset=utf-8", "app.js": "text/javascript; charset=utf-8",
          "style.css": "text/css; charset=utf-8", "sandbox.html": "text/html; charset=utf-8",
          "sandbox.js": "text/javascript; charset=utf-8"}
CSP_MAIN = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: blob:; connect-src 'self'; "
            "frame-src 'self'; worker-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; "
            "frame-ancestors 'none'")
CSP_SANDBOX = ("default-src 'none'; script-src 'self' 'unsafe-eval' blob:; worker-src blob:; style-src 'self'; "
               "connect-src 'none'; img-src 'none'; form-action 'none'; base-uri 'none'; frame-ancestors 'self'; "
               "sandbox allow-scripts")


class ApiError(Exception):
    def __init__(self, status, msg):
        super().__init__(msg)
        self.status, self.msg = status, msg


class KitServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, addr, data_dir, require_token=False, token="", allow_remote_run=False, lan=False):
        super().__init__(addr, Handler)
        self.kit_dir = KIT_DIR
        self.data_dir = os.path.realpath(data_dir)
        os.makedirs(self.data_dir, exist_ok=True)
        self.ws = fsguard.Workspace(os.path.join(self.data_dir, "workspace"))
        self.require_token = require_token
        self.token = token
        self.lan = lan
        self.allow_remote_run = allow_remote_run
        self.heavy = threading.BoundedSemaphore(1)
        self.agent = agent_mod.Agent(KIT_DIR, workspace=self.ws)
        self.started = time.time()

    @property
    def port(self):
        return self.server_address[1]


def _qs1(q, k, default=None):
    v = q.get(k)
    return v[0] if v else default


class Handler(BaseHTTPRequestHandler):
    server_version = "edge-canvas-kit"
    sys_version = ""
    protocol_version = "HTTP/1.1"

    # ---------------------------------------------------------------- plumbing
    def log_message(self, fmt, *args):  # no query strings (tokens) in logs
        path = self.path.split("?", 1)[0] if hasattr(self, "path") else "-"
        sys.stderr.write(f"[{time.strftime('%H:%M:%S')}] {self.command} {path} {args[1] if len(args) > 1 else ''}\n")

    def _headers(self, status, ctype, length, csp=CSP_MAIN, extra=None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(length))
        self.send_header("Content-Security-Policy", csp)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        # sandbox.js/html are fetched by the opaque-origin JS sandbox iframe, so they cannot be same-origin-only
        self.send_header("Cross-Origin-Resource-Policy", "cross-origin" if csp == CSP_SANDBOX else "same-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=(), usb=(), serial=()")
        self.send_header("Cache-Control", "no-store")
        if csp == CSP_MAIN:
            self.send_header("X-Frame-Options", "DENY")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()

    def _send_json(self, status, obj):
        b = json.dumps(obj, ensure_ascii=True).encode("utf-8")
        extra = None
        if status >= 400:   # an unread request body must never be parsed as a next request: close after errors
            self.close_connection = True
            extra = {"Connection": "close"}
        self._headers(status, "application/json; charset=utf-8", len(b), extra=extra)
        self.wfile.write(b)

    def _host_ok(self):
        host = (self.headers.get("Host") or "").strip().lower()
        if self.server.lan:
            return bool(host) and len(host) < 256
        p = self.server.port
        return host in {f"127.0.0.1:{p}", f"localhost:{p}", f"[::1]:{p}"}

    def _api_gate(self):
        if not self._host_ok():
            raise ApiError(403, "Host header refused (DNS-rebinding guard)")
        origin = self.headers.get("Origin")
        if origin is not None and origin != "null":
            if origin.lower() != "http://" + (self.headers.get("Host") or "").lower():
                raise ApiError(403, "cross-origin request refused")
        elif origin == "null":
            raise ApiError(403, "opaque-origin request refused")
        if self.headers.get("X-Kit-Client") != "1":
            raise ApiError(403, "X-Kit-Client header required")
        if self.server.require_token:
            got = self.headers.get("X-Kit-Token") or ""
            if not got or not hmac.compare_digest(got.encode(), self.server.token.encode()):
                raise ApiError(401, "token required (start screen of the server prints it)")

    def _body(self, cap):
        if self.headers.get("Transfer-Encoding"):
            raise ApiError(411, "chunked bodies refused; send Content-Length")
        cl = self.headers.get("Content-Length")
        if cl is None or not cl.isdigit():
            raise ApiError(411, "Content-Length required")
        n = int(cl)
        if n > cap:
            raise ApiError(413, f"body over cap ({cap} bytes)")
        data = b""
        while len(data) < n:
            chunk = self.rfile.read(n - len(data))
            if not chunk:
                raise ApiError(400, "short body")
            data += chunk
        return data

    def _json_body(self, cap=CAP_JSON):
        raw = self._body(cap)
        try:
            obj = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            raise ApiError(400, "body must be UTF-8 JSON")
        if not isinstance(obj, dict):
            raise ApiError(400, "JSON object required")
        return obj

    def _run_allowed(self):
        if self.server.lan and not self.server.allow_remote_run:
            raise ApiError(403, "code runs are off over the home network; restart with --allow-remote-run to enable")

    def _heavy(self, fn):
        if not self.server.heavy.acquire(blocking=False):
            raise ApiError(429, "busy with another heavy job; try again")
        try:
            return fn()
        finally:
            self.server.heavy.release()

    # ---------------------------------------------------------------- verbs
    def do_GET(self):
        self._dispatch("GET")

    def do_POST(self):
        self._dispatch("POST")

    def do_HEAD(self):
        self._send_json(405, {"error": "method not allowed"})

    def do_PUT(self):
        self._send_json(405, {"error": "method not allowed"})

    do_DELETE = do_PATCH = do_OPTIONS = do_PUT

    def _dispatch(self, method):
        try:
            if len(self.path) > 4096:
                raise ApiError(414, "URL too long")
            u = urllib.parse.urlsplit(self.path)
            path, q = u.path, urllib.parse.parse_qs(u.query, max_num_fields=32)
            if not path.startswith("/api/"):
                if method != "GET":
                    raise ApiError(405, "method not allowed")
                return self._static(path)
            self._api_gate()
            route = ROUTES.get((method, path))
            if route is None:
                known = any(p == path for (_, p) in ROUTES)
                raise ApiError(405 if known else 404, "method not allowed" if known else "no such endpoint")
            out = route(self, q)
            self._send_json(200, out)
        except ApiError as e:
            self._send_json(e.status, {"error": e.msg})
        except fsguard.GuardError as e:
            self._send_json(e.status, {"error": str(e)})
        except (descend.DescendError, frames.FramesError) as e:
            self._send_json(400, {"error": str(e)})
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as e:  # node 7: log, answer, keep serving
            traceback.print_exc()
            try:
                self._send_json(500, {"error": f"server node error: {type(e).__name__}"})
            except Exception:
                pass

    def _static(self, path):
        if path in ("/", "/index.html"):
            name = "index.html"
        elif path.startswith("/ui/"):
            name = path[4:]
        else:
            raise ApiError(404, "not found")
        if name not in STATIC:
            raise ApiError(404, "not found")
        b = open(os.path.join(KIT_DIR, "ui", name), "rb").read()
        csp = CSP_SANDBOX if name.startswith("sandbox") else CSP_MAIN
        self._headers(200, STATIC[name], len(b), csp=csp)
        self.wfile.write(b)

    # ---------------------------------------------------------------- endpoints
    def api_status(self, q):
        s = self.server
        return {"version": VERSION, "mode": "lan" if s.lan else "local", "token_required": s.require_token,
                "code_runs": (not s.lan) or s.allow_remote_run, "outbound_network": "off (no outbound calls)",
                "optional": optional.summary(include_ollama=False),
                "ollama": "probed only when the agent's local-model mode is used (127.0.0.1:11434)",
                "uptime_s": int(time.time() - s.started)}

    def api_boot(self, q):
        return runner.boot(KIT_DIR)

    def api_descend(self, q):
        b = self._json_body()
        v = descend.final_value(b.get("m", 5), b.get("n", 3), b.get("B", 7), b.get("x0", 0), b.get("dx", 3),
                                b.get("steps", 4))
        return {"final": descend.fmt(v)}

    def api_frames(self, q):
        args = {k: _qs1(q, k) for k in ("fps", "frames", "w", "h", "m", "n", "B", "x0", "dx") if _qs1(q, k) is not None}
        return frames.generate(**args)

    def api_files_list(self, q):
        return self.server.ws.list(_qs1(q, "path", ""))

    def api_files_read(self, q):
        return self.server.ws.read(_qs1(q, "path", ""))

    def api_files_write(self, q):
        b = self._json_body(CAP_WRITE)
        return self.server.ws.write(b.get("path", ""), b.get("content", ""), b.get("encoding", "utf-8"))

    def _examples(self):
        out = []
        for sub, ext in (("basic", ".bas"), ("cpp", ".cpp")):
            d = os.path.join(KIT_DIR, sub)
            out += [f"{sub}/{n}" for n in sorted(os.listdir(d)) if n.endswith(ext)] if os.path.isdir(d) else []
        return out

    def api_examples(self, q):
        return {"examples": self._examples()}

    def api_examples_read(self, q):
        name = _qs1(q, "name", "")
        if name not in self._examples():   # fixed allow-list of shipped kit files; no path input reaches the disk
            raise ApiError(404, "not an example")
        return {"name": name, "content": open(os.path.join(KIT_DIR, *name.split("/")), encoding="utf-8").read()}

    def api_convert(self, q):
        raw_name = urllib.parse.unquote(self.headers.get("X-Filename") or "upload.bin")[:200]
        name = re.sub(r"[^A-Za-z0-9._-]+", "_", os.path.basename(raw_name.replace("\\", "/"))).lstrip(".") or "upload.bin"
        data = self._body(CAP_CONVERT)
        return self._heavy(lambda: convert_upload(self.server.data_dir, name, data))

    def api_agent(self, q):
        b = self._json_body()
        text = b.get("q", "")
        if not isinstance(text, str) or len(text) > 4000:
            raise ApiError(400, "q must be a string of at most 4000 chars")
        mode = b.get("mode", "rules")
        if text.strip().lower().startswith("/selftest"):
            self._run_allowed()
            return self._heavy(lambda: self.server.agent.ask(text, mode=mode))
        return self.server.agent.ask(text, mode=mode)

    def api_basic(self, q):
        self._run_allowed()
        b = self._json_body()
        code = b.get("code", "")
        if not isinstance(code, str):
            raise ApiError(400, "code must be a string")
        return self._heavy(lambda: runner.run_basic(code, self.server.data_dir))

    def api_cpp(self, q):
        self._run_allowed()
        b = self._json_body()
        code, stdin = b.get("code", ""), b.get("stdin")
        if not isinstance(code, str):
            raise ApiError(400, "code must be a string")
        return self._heavy(lambda: runner.run_cpp(code, self.server.data_dir, stdin_text=stdin, std=b.get("std", "c++17")))


ROUTES = {
    ("GET", "/api/status"): Handler.api_status,
    ("GET", "/api/boot"): Handler.api_boot,
    ("POST", "/api/descend"): Handler.api_descend,
    ("GET", "/api/frames"): Handler.api_frames,
    ("GET", "/api/files"): Handler.api_files_list,
    ("GET", "/api/files/read"): Handler.api_files_read,
    ("POST", "/api/files/write"): Handler.api_files_write,
    ("GET", "/api/examples"): Handler.api_examples,
    ("GET", "/api/examples/read"): Handler.api_examples_read,
    ("POST", "/api/convert"): Handler.api_convert,
    ("POST", "/api/agent"): Handler.api_agent,
    ("POST", "/api/basic"): Handler.api_basic,
    ("POST", "/api/cpp"): Handler.api_cpp,
}


# -------------------------------------------------------------------- converter integration
def convert_upload(data_dir: str, name: str, data: bytes) -> dict:
    """Text door (to_txt) + RCRJ (regex -> CSV -> regex -> JSON, SQLite fallback), vendored unchanged."""
    import to_txt, rcrj  # vendored from /workspace/csvson-ingest-2026-10-05/txt_rcrj
    run_dir = runner.new_run_dir(data_dir, "convert")
    os.makedirs(os.path.join(run_dir, "input"))
    with open(os.path.join(run_dir, "input", name), "wb") as f:
        f.write(data)
    results = to_txt.convert(name, data)
    rows = to_txt.write_txt(results, os.path.join(run_dir, "txt"))
    records, txt_preview, budget = [], [], 24_000
    for row in rows:
        if not row["txt"]:
            continue
        t = open(os.path.join(run_dir, "txt", row["txt"]), encoding="utf-8").read()
        records.extend(rcrj.records_from_txt(t, default_source=row["name"]))
        if budget > 0:
            txt_preview.append({"txt": row["txt"], "text": t[:budget]})
            budget -= min(len(t), budget)
    env = rcrj.run(records, os.path.join(run_dir, "rcrj"), "CSVSON_RCRJ", node="edge-canvas-kit")
    csv_text = open(env["_paths"]["csv"], encoding="utf-8").read()
    meta = env["meta"]
    flags = sorted({f for d in env["data"] for f in d.get("flags", "").split("|") if f}
                   | {r["category"] for r in meta["reject_log"] if r["reason"] == "flagged_kept_as_data"})
    return {"run_dir": os.path.relpath(run_dir, data_dir), "items": rows, "txt_preview": txt_preview,
            "csv_preview": "\n".join(csv_text.split("\n")[:101])[:24_000],
            "json_preview": {"data": env["data"][:50], "meta": {k: meta[k] for k in ("source", "node", "run_id", "order", "counts")}},
            "flags": flags, "reject_log": meta["reject_log"][:100], "sqlite_rows": meta["sqlite_rows"][:50],
            "json_roundtrip_equal": env["_json_roundtrip_equal"],
            "tools": {"tesseract": bool(to_txt.TESSERACT), "pdftotext": bool(to_txt.PDFTOTEXT),
                      "pillow": to_txt.Image is not None, "defusedxml": to_txt.DET is not None}}


# -------------------------------------------------------------------- main
def lan_addresses():
    """This device's home-network addresses, found WITHOUT any network traffic or DNS lookup:
    Linux/Pi: `hostname -I` (argv list, reads local interfaces). Elsewhere: none (print a template)."""
    import shutil, subprocess
    exe = shutil.which("hostname") if sys.platform.startswith("linux") else None
    if not exe:
        return []
    try:
        p = subprocess.run([exe, "-I"], capture_output=True, text=True, timeout=3, stdin=subprocess.DEVNULL)
        return [a for a in p.stdout.split() if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", a) and not a.startswith("127.")]
    except Exception:
        return []


def make_server(host="127.0.0.1", port=DEFAULT_PORT, data_dir=None, lan=False, token=None, allow_remote_run=False,
                require_token=None):
    data_dir = data_dir or KIT_DIR
    if require_token is None:
        require_token = lan
    if require_token and not token:
        token = secrets.token_urlsafe(18)
    return KitServer((host, port), data_dir, require_token=require_token, token=token or "",
                     allow_remote_run=allow_remote_run, lan=lan)


def main(argv=None):
    ap = argparse.ArgumentParser(description="edge-canvas-kit local server (offline)")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--lan", action="store_true", help="listen on the home network (token required)")
    ap.add_argument("--bind", default=None, help="explicit bind address (default 127.0.0.1, or 0.0.0.0 with --lan)")
    ap.add_argument("--token", default=None, help="set the --lan token yourself (default: random each start)")
    ap.add_argument("--allow-remote-run", action="store_true", help="allow BASIC/C++ runs from other devices (--lan)")
    ap.add_argument("--data-dir", default=None, help="where workspace/ and runs/ live (default: the kit folder)")
    a = ap.parse_args(argv)
    host = a.bind or ("0.0.0.0" if a.lan else "127.0.0.1")
    if not a.lan and host not in ("127.0.0.1", "localhost", "::1"):
        ap.error("binding beyond localhost needs --lan (which turns the token on)")
    srv = make_server(host, a.port, a.data_dir, lan=a.lan, token=a.token, allow_remote_run=a.allow_remote_run)
    print(f"{VERSION}  data: {srv.data_dir}")
    print(f"  open  http://127.0.0.1:{srv.port}/" + (f"#token={srv.token}" if srv.require_token else ""))
    if a.lan:
        ips = lan_addresses()
        for ip in ips:
            print(f"  phone http://{ip}:{srv.port}/#token={srv.token}")
        if not ips:
            print(f"  phone http://<this-device-address>:{srv.port}/#token={srv.token}   (find the address in your router or OS settings)")
        print("  token is required on the home network; code runs:", "ON" if a.allow_remote_run else "OFF (localhost only)")
    print("  offline: no outbound network calls. Ctrl+C stops.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()
