# Edge Canvas Kit (offline-first) — 2026-10-06

One folder that gives you a **Canvas** (RGB frame player + drawing pad), a **browser UI**, a **code editor**
(BASIC, JavaScript, C++), a **file browser**, the **TXT → CSV → JSON converter**, and a **developer agent**,
all running on your own device. It needs only **Python 3 (standard library)** and **a browser**.
No internet, no CDN, no npm, no pip at runtime. Nothing is installed on your devices by the kit.

## Quick start (any device)

    python3 server.py
    # then open http://127.0.0.1:8765

## Raspberry Pi 5 steps

1. Copy the `edge-canvas-kit` folder to the Pi (USB stick, LocalSend, or the home network). No internet is needed after the copy.
2. Open a terminal in the folder and run `python3 server.py` (or `./run.sh`). Raspberry Pi OS ships Python 3.
3. Open **Chromium** at `http://127.0.0.1:8765`.
4. Optional check: `python3 selfcheck.py --quick` (prints `SUMMARY: ALL PASS` when everything works).

### Kiosk mode on the Pi 5 (full screen)

    ./run.sh --kiosk
    # same as: python3 server.py &  then  chromium --kiosk http://127.0.0.1:8765/

Close Chromium (Alt+F4) to leave kiosk mode; `run.sh --kiosk` then stops the server.

### Phone or other devices on the home network (--lan)

    python3 server.py --lan

The server prints a URL like `http://192.168.x.y:8765/#token=...`. Open that exact URL on the phone browser.
The **token is required** for every API call over the home network. BASIC/C++ runs are **off** over the network
unless you start with `--allow-remote-run` (they always work on the Pi itself at 127.0.0.1).

### Windows (ASUS A15)

Double-click `run.bat` (or `py -3 server.py`), then open `http://127.0.0.1:8765`.

## What each tab does

| Tab | What it does |
|---|---|
| Canvas | Plays RGB frames at **32 or 64 fps** (dt = 1/32 s or 1/64 s). Frames come from the **descending sampler** f = m·xⁿ + B (computed, not a camera). A frame is held only while it is built, then **shown or dropped** (counters show both). Drawing pad saves PNGs into `workspace/drawings/`. |
| Code | Textarea with line numbers. **BASIC** runs through the server with `bwbasic` (if present). **JavaScript** runs in a sandboxed iframe (no network). **C++** compiles with `g++`/`clang++` (if present) through `/api/cpp`. Open/Save files in the workspace. |
| Files | Lists/reads/writes files **only inside `workspace/`**. No delete: an overwrite first archives the old copy to `workspace/.archive/`. |
| Converter | Drop a file: TXT door → regex guard → CSV → regex guard → JSON (SQLite fallback). Shows items, flags, TXT, CSV, JSON. Stays on the device. |
| Agent | Offline helper. Answers from the kit docs, `knowledge/` (masked copies of your reference-map docs) and the code, **with citations** (`path:lines`). If the answer is not in those sources it says **"I don't know."** Commands: `/help`, `/tools`, `/reindex`, `/selftest`, `/scaffold <need_gosub|conflict_nodes|lead_filter> <bas|py|cpp> <name>`. |
| Status | Optional extras found on this device, boot result, and a descend calculator (5x³+7, dx 3, 4 steps → **8647**). |

## Optional extras (NEED → GOSUB → RETURN)

The kit looks for these only when a feature needs them. If one is missing, that feature reports it and everything else keeps going.

| Extra | Used for | If missing |
|---|---|---|
| `bwbasic` | Boot check, BASIC runs | Boot uses the Python twin (`basic/boot.py`); BASIC runs report "bwbasic not found" |
| `g++` or `clang++` | C++ runs (`/api/cpp`) | Reports "No C++ compiler found"; nothing installed |
| `tesseract`, `pdftotext` | OCR / PDF text in the converter | Those items report and continue |
| Pillow, defusedxml (Python) | Image details / safe XML parsing | Images PARKED; XML kept as plain text |
| Ollama at 127.0.0.1:11434 | Agent "local model" mode | Agent stays rule-based (cited snippets) |

### Installing g++ on the Pi 5 (your choice; the kit never does this)

Raspberry Pi OS usually ships `g++`. Check with `g++ --version`. If it is missing and **you** want the C++ lane:

    sudo apt install g++

That is optional and done by you; the kit works without it.

## C++ lane

- `cpp/descend.cpp` — C++ twin of the descending update: exact rationals (integer numerator/denominator, gcd-normalized,
  overflow-checked). Prints the final value only (**8647**) then its self-check (`PASS=15 FAIL=0`).
- `cpp/conflict_nodes.cpp` — C++ port of the conflict_nodes dispatcher (detect, call one node, return; BOT never auto-enables). Self-check `PASS=22 FAIL=0`.
- Build by hand: `g++ -std=c++17 -O1 -o descend cpp/descend.cpp && ./descend`
- Through the editor: compile and run use argument lists (no shell), a compile timeout (90 s) and run timeout (10 s),
  a 64 KB output cap, CPU/memory/file-size limits on Linux, and a run folder inside the kit (`runs/cpp/<time>/`).
  Source that reaches files, processes, the network or the preprocessor beyond `#include <allowed header>` is refused.
  These are guard rails, not a full sandbox — which is why code runs are localhost-only by default.

## Security and data rules

- Binds to **127.0.0.1** by default; `--lan` binds the home network and turns the **token** on.
- Every API call needs the `X-Kit-Client` header and a matching Host/Origin (blocks other web pages and DNS rebinding).
- Size caps: JSON 1 MiB, uploads 16 MiB, file writes 2 MiB, URL 4 KB. CSP + nosniff headers on every response.
- No `shell=True` anywhere; nothing is executed from user text except the BASIC/C++ editor runs you start (guarded as above).
- **No outbound network calls** (DM-2). The only client socket is the optional Ollama probe at 127.0.0.1. Personal data is masked in `knowledge/` and in agent snippets (DM-5).
- Append and archive, never delete: no delete endpoint; overwrites archive first; `runs/` keeps every convert/BASIC/C++ run.

## Files

    server.py  agent.py  selfcheck.py  ui_smoke.py  run.sh  run.bat  README.md  ROUNDS_LOG.md
    lib/        descend.py frames.py fsguard.py mask.py optional.py runner.py
    ui/         index.html app.js style.css sandbox.html sandbox.js
    vendor/     txt_rcrj/ (to_txt.py, rcrj.py [kit fix], rcrj_guard.bas) + VENDORED.md
    basic/      BOOT.bas boot.py need_gosub_one_node.bas conflict_nodes.bas/.py lead_filter.bas/.py descending_power_final.bas
    cpp/        descend.cpp conflict_nodes.cpp
    templates/  scaffold templates for the agent
    knowledge/  masked copies of reference-map docs + KNOWLEDGE_MANIFEST.md
    workspace/  your files (Files tab / editor / drawings / scaffolds)

## Tests

    python3 selfcheck.py           # everything (C++ compiles + headless UI smoke if a browser is already installed)
    python3 selfcheck.py --quick   # skips C++ compiles and the UI smoke

Missing optional extras show as **SKIP**, never as PASS. A socket guard fails the run if anything tries to reach a host other than localhost.

`/selftest` (Agent tab) runs `selfcheck.py --quick` **once**: in its own process group, with a 600 s limit, and the whole
group is killed afterwards. The child gets `KIT_SELFTEST_ACTIVE=1`; while that flag is set, `/selftest` refuses instead of
starting another self-check, and `--quick` never calls `/selftest` (added after a runaway on the build box, see ROUNDS_LOG.md).

    python3 mutants.py --list                 # mutation tests (build/maintenance tool; slow on a Pi)
    python3 mutants.py --only <name>          # one mutant at a time; leftovers are counted and killed after each

## Known gaps

- Not yet run on real Raspberry Pi 5 hardware or a real phone (tested on the build box, x86_64, with headless Chrome).
- 64 fps is a named rate, not a measured one; most screens refresh at 60 Hz, so some 64 fps frames are expected to be dropped (the counter shows it).
- The C++/BASIC guards are deny-lists, not an OS sandbox.
