# time-capture-2026-10-18 — automatic time capture (feature id time-capture-auto-2026-10-18)

For Timothy Norman's Grok Build seat. Purpose: replies never quote a stale or invented time.
STANDING RULE: see RULE.md (verbatim from Timothy, 2026-10-18).

## First capture of this job (recorded as given, not re-measured)
- Box clock: **2026-10-18 12:10:47 EDT**; UTC **2026-10-18T16:10:47.863675037Z** (from `date`, run by the seat).
- Epoch ns of that UTC stamp: 1792339847863675037 (used as a test fixture in t_first_capture_format;
  output `Time (fresh fetch): 12:10 PM EDT, fetched 12:10:47 [TEST CLOCK]`).
- This is the **shared box's clock**, which is set to America/New_York. **Timothy's own PC clock is not
  reachable from the box**; nothing here measures it.

## BOOT STEP
After BOOT.bas 0.70710678 and SOURCES_OF_TRUTH, run `timecap open`
(`/workspace/time-capture-2026-10-18/timecap.sh open`).

## Files
| file | what |
|---|---|
| timecap.py | Python implementation: fetch / status / open / close |
| timecap.sh | bash implementation, same stamp format, hash and lines (stamps interchangeable) |
| test_timecap.py | 25 tests x 2 implementations + 1 cross test; 36 mutants (`--mutants`) |
| TEST_RESULTS.txt | measured results: tests 51/51; mutants pass 1 35/36, pass 2 36/36 |
| SKILL_DRAFT.md | skill `time-capture-auto-2026-10-18` (Timothy installs it) |
| RULE.md | standing rule text + boot step |
| SHA256SUMS | hashes of all files above |

## How it works
- **fetch**: wall clock `time.time_ns()` / `date +%s%N` (CLOCK_REALTIME), monotonic counter
  CLOCK_BOOTTIME (`time.clock_gettime_ns` / `/proc/uptime`, 10 ms resolution in bash), zone
  America/New_York (zoneinfo / `TZ=`). Writes JSON: fetch_epoch_ns, iso_local, iso_utc, tz, monotonic_ns,
  monotonic_clock, host, boot_id, writer, sha256. sha256 = sha256 of
  `v1|epoch|iso_local|iso_utc|tz|mono|mono_clock|host|boot_id|writer`. No command takes a time argument
  (a time argument gives usage error 64). Default stamp `/workspace/time-capture/last_fetch.json`;
  it is replaced atomically on each fetch (it is a runtime cache, the one file that is rewritten by design).
- **status** (one line; checks in this order):
  1. missing / unparsable / wrong types / wrong tz / hash fails / iso fields not equal to the hashed epoch
     → `Time UNVERIFIED: no fetch available` (exit 2)
  2. boot_id differs → `Time UNVERIFIED: stamp is from a different boot (monotonic check impossible)` (exit 3)
  3. wall age < 0, or |wall age − monotonic age| > 2 s → `Time UNVERIFIED: clock skew detected` (exit 3)
  4. wall age ≤ 60.000000000 s → `Time (fresh fetch): 12:10 PM EDT, fetched 12:10:47` (exit 0)
  5. else → `Time: 12:10 PM EDT — STALE, fetched N s ago` (exit 1)
  Seconds are truncated (floor), never rounded. Note: at 60 s + 1 ns the line is STALE and reads
  "fetched 60 s ago" (truncation), which is intended.
- **open / close**: fetch, then optional external check (HEAD https://www.google.com, 3 s timeout,
  HTTP Date header, skew > 5 s → `Time UNVERIFIED: external clock skew detected (...)`, exit 3), then the
  status line, then `External check: ok (...)` or `External check: skipped (...)`. No network = skipped,
  not a failure. `TIMECAP_NO_NET=1` disables it.
- **Test hooks** (honest by construction): `TIMECAP_TEST_NOW=<wall_ns>:<mono_ns>` changes "now" for
  `status` only and tags every line ` [TEST CLOCK]`; fetch/open/close ignore it. `TIMECAP_EXT_URL`
  points the external check at a local test server.

## Measured (see TEST_RESULTS.txt)
- Tests 51/51 pass (py 25/25, sh 25/25, cross-compat 1/1).
- Mutants: pass 1 35/36 (SM18 survived) → added a test → pass 2 36/36 killed (py 18/18, sh 18/18).
- Live external check at test time: `External check: ok (+0 s vs https://www.google.com Date header, limit 5 s)`
  for both implementations.

## Limits
- The hash detects corruption and casual edits; anyone who can write the file can re-hash it. Not a signature.
- Skew check needs the same boot (boot_id); a reboot makes an old stamp UNVERIFIED, which is fail-closed.
- Nothing runs in the background; the tool runs only when called.
- Not touched: BOOT.bas, svct_v20*, /workspace/kbld9/protected/.

## Paths
- Source: `/workspace/time-capture-2026-10-18/`
- Reference-map copy: `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/time-capture-2026-10-18/`
