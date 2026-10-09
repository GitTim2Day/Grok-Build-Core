# Response to the Process-and-Goals handoff — the "obtain, don't guess" items

Stamp: 2026-10-08T23:40-04:00
Owner: Timothy. Seat: Claude. Append only. Labels follow the handoff's PRESERVATION list:
REPRODUCED (independently run here), REPORTED (user-reported), PROPOSED (design), NOT EXECUTED.

## The handoff itself (preserved)

`knowledge/Timothy_Process_and_Goals_AI_Handoff_2026-10-08.md` — byte-identical copy of the chat attachment.
7,137 bytes, UTF-8, SHA-256 7654d06286f06be32b4e804207c0e2929c39e17db00aa3293fa699fb0478b7da. Acquired 2026-10-08 23:31 ET.

## 1. MinRadius_Lp correction — REPRODUCED

Fresh clone of main (d268c5d), 2026-10-08 23:35 ET. Commit 20e81bd is an ancestor of main and adds both leaves.

| Leaf | Bytes | SHA-256 | Run (python3 -I, alone in a folder) |
| --- | --- | --- | --- |
| kbld/kbl_svct_stacks_MinRadius_Lp_2026-08-28_DRIVE_D2_restored_2026-10-08.py | 72694 | 6e91bbc17d4a7d06f81441632f8453d81a2c12a5fc7d831da8091f8e0e3d6600 | 75 passed, 0 failed, exit 0 |
| kbld/kbld_gosub_primitives_MinRadius_Lp_2026-08-28_DRIVE_D3_restored_2026-10-08.py | 44851 | 6c57ae4a86e24e87f4d72455d4d89f6075f504093339f27b76eb9f6fb2f7c073 | ALL GREEN, exit 0 |

Hashes equal the Drive mirrors D2/D3. **New evidence on the bare-assert point:** `python3 -I -O` on the primitives leaf also prints
"ALL GREEN" — with all 79 asserts removed. Under -O that green is vacuous (named pattern: vacuous guard). Which leaf is live: still Timothy's call.

## 2. Self-check baseline messages — REPRODUCED (x86_64 sandbox, not a Pi)

Run: `python3 selfcheck.py` in `edge-canvas-kit/` on main d268c5d, bwbasic 3.20b (pinned build) and Chromium 141.0.7390.37 on PATH.
Environment: Python 3.13.16, gcc 13.3.0, x86_64. Exit code **1**. `TOTAL pass=335 fail=3 skip=0`.
Complete output (568 lines): `logs/SELFCHECK_MAIN_d268c5d_bwbasic320_chromium_2026-10-08.txt`,
SHA-256 12ddeed2fd24d9f8c5c5d116c44178e8f9b0da2a5a788d4c2ad31747c562dd1d.

The three FAIL lines, by name and cause (full text is in the log; run_dir names and seconds change per run):

| Check | What it printed | Cause |
| --- | --- | --- |
| `basic_timeout` | `ERROR in line 10: Syntax error` … `10:GOTO 10`, `timed_out: False` | bwbasic 3.20b refuses a one-line self-loop; the test expects a timeout. A two-line loop still times out. Version difference. |
| `basic_template_runs sweep.bas` | `… FAIL check 3 / FAIL check 4 / FAIL check 7 / PASS= 7  FAIL= 3 / SUMMARY: FAILS` | The original `basic/sweep.bas` builds its 8 places with `STR$`, which bwbasic 3.x prints as `5.44206E+7`. A real defect in that program under 3.x; fixed in the leaf `basic/sweep_cut8_2026-10-08.bas` (10/10). |
| `sweep_crosscheck_basic_vs_python` | `{'Y100': '19.5.44206E+7', 'Y500': '41.7.97703E+7', … 'SAMPLER_FINAL': '19.0005.E+7'}` | Same `STR$` cause as above (the crosscheck reads sweep.bas output). With the leaf swapped in, values match Python; the check then fails only on spacing (`PASS= 10  FAIL= 0` has two spaces under 3.20b). |

Correction to my earlier wording ("three items about 2.20-era expected text"): only `basic_timeout` and the spacing are version text.
The sweep pair is a real `STR$` defect in the original program. On a Pi, expect these same three names; anything else is new and gets investigated.

## 3. Chromium kiosk network — REPRODUCED here; PROPOSED for the Pi

The handoff said: use the exact flags from the screenshot. They were:
`--headless=new --no-sandbox --disable-gpu --user-data-dir=<dir> --disable-background-networking --disable-component-update --disable-sync --no-first-run --virtual-time-budget=8000 --window-size=1100,1300 --hide-scrollbars --screenshot=<file>`

**Measured, they are not enough.** Counting attempts that reached this sandbox's egress proxy while loading the kit page:

| Chromium run | Attempts that tried to leave | Hosts |
| --- | --- | --- |
| no network flags | 3 | accounts.google.com, redirector.gvt1.com, www.google.com |
| the screenshot flags (+ default-apps, domain-reliability, metrics, default-browser) | 2 | accounts.google.com, www.google.com |
| + `--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE 127.0.0.1` | 2 | same (here the sandbox proxy resolves names, so the rule never applies; not a valid test of it) |
| **+ `--proxy-server=http://127.0.0.1:9 --proxy-bypass-list=127.0.0.1;localhost`** (nothing listens on port 9) | **0** | — ; page rendered, boot OK line present, 4 kit API calls served |

What Chromium tried, caught by a refusing logging stub in place of port 9: 6× www.google.com, 1× accounts.google.com,
1× content-autofill.googleapis.com, 1× clients2.google.com/time (plain http). All refused; none reached a network.

PROPOSED kiosk line for the Pi (not yet in `run.sh`; Timothy decides):
`chromium --kiosk --noerrdialogs --disable-infobars --no-first-run --disable-background-networking --disable-component-update --disable-sync --disable-default-apps --disable-domain-reliability --metrics-recording-only --no-default-browser-check --proxy-server=http://127.0.0.1:9 "--proxy-bypass-list=127.0.0.1;localhost" http://127.0.0.1:8765/`
Caveat: with the dead proxy, Chromium cannot reach anything but this device. The kit's Agent dial-out (wip branch) runs in Python, not
in the browser, so it is unaffected. A remote --lan client would browse to the Pi's LAN address; that address must then be added to the
bypass list. NOT EXECUTED on a Pi or in non-headless kiosk mode.

## 4. Questions back to Timothy (the handoff asks to confirm, not guess)

1. "BIS" as an output target: is it BASIC (voice-typed), or something else?
2. EV2 stopping: the measurement/accuracy ratio, its units and the acceptance threshold for each task — not invented here.
3. Which MinRadius_Lp leaf becomes live.
4. Whether `run.sh --kiosk` gets the dead-proxy flags above.

## Not executed / blocked

- Nothing has run on the Pi 5, R1, A15 or Orin from this seat.
- JCJ proper and the KBLD9 core are not in the repo; nothing here claims either ran.
- The Agent ladder with permission-gated dial-out sits on branch `wip/agent-ladder-2026-10-08` (8319387); its last test edit is unrun.
