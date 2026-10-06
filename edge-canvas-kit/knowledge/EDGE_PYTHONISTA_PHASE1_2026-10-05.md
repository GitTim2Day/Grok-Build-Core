# EDGE PYTHONISTA PHASE 1: language-per-device stub, Pythonista (iOS) only
Generated: 2026-10-05 ~6:45 PM ET; Cellular transport stub update ~6:48 PM ET
Fail-closed. Docs plus one box-only pure-Python stub. Nothing paired, installed, purchased, flashed, or published. No GitHub push. No sealed primitives.
Nothing was copied to, installed on, or run on Timothy's phone, laptop, Pi, drones, Queen, Hive, or Swarm.
Builds on: `EDGE_MANIFEST_SPEC_2026-10-05.md` (sec 2 fields, sec 2 refuse-to-run steps, sec 5 iOS options A/B/C) - `EDGE_TRANSPORT_MATRIX_2026-10-05.md` - `EDGE_LOCKED_ANSWERS_2026-10-05.md` (A, D, E, F) - `EDGE_DEVICE_PORT_MAP_2026-10-05.md`
Boot continuity this pass: `bwbasic /workspace/hybrid-boot/BOOT.bas </dev/null` PRINT `0.70710678`, exit 0. Math continuity only; not proof that anything here runs on a device.

Source tags: **L** = locked answers A-F - **T** = Timothy's words - **R** = repo notes on box - **P** = public, class-typical, not verified on Timothy's unit - **BOX** = written and tested on the box only - **SUGGESTED** = proposal, not locked - **UNDEF** = not earned.

---

## 1) Scope

- Device: **iOS phone, Pythonista 3 app** (L-A "Both but start with iOS"). Android = later phase, not covered.
- Language for this device: **Python 3, standard library only** (R: existing `targets/pythonista/` is stdlib-only, no pip). Other devices keep their own language rows in the port map (L-D adaptable for all).
- Job of phase 1: **refuse to run** delivered code whose files do not match a sha256 manifest (manifest spec sec 2). Nothing else.
- Code reaches the phone over BT, WiFi, USB, or Cellular (L-F + F'). Which path Timothy uses first: **UNDEF** (manifest spec sec 5 options A/B/C are still QUESTIONS). The check is the same for every path.

## 2) Stdlib-only assumptions

| Module | Used for | Status on Timothy's phone |
|---|---|---|
| `hashlib` | `sha256` of file bytes | P (ships with CPython; Pythonista bundles CPython). **Not verified on his phone** |
| `json` | JSON manifest | P, not verified |
| `os`, `sys` | paths, exit code | P, not verified |
| `tempfile`, `shutil` | self-check only (throwaway copies) | P, not verified |

Not used: `urllib`, `socket`, `ssl`, `cb` (BLE), any network or Bluetooth module, any third-party package, pip.
Python version on the phone: **UNDEF**. The stub avoids new syntax (no `X | None` hints, no match statement) so older Python 3 should parse it; that is a design choice, not a test on the phone.
BOX test: CPython 3.13.5 on the box only.

## 3) How refuse-to-run uses hashlib.sha256 (BOX stub)

`manifest_check.py` follows manifest spec sec 2 steps 1-6:

1. Read the manifest (`.json`, or a lines file `<sha256> <size_bytes> <path>`). Must be ASCII, at most 1 MiB, at most 4096 files, at least 1 file.
2. Each path must be relative, ASCII, no `..`, no `.`, no empty part, no backslash, no colon, no leading `/` or `~`. Duplicates are refused.
3. File must exist, be a regular file, and resolve inside the root (a symlink that points outside is refused). The manifest may not list itself.
4. `size_bytes` must match (cheap gate).
5. `hashlib.sha256()` over the file in 64 KiB chunks; hex digest must equal the manifest value exactly (64 lowercase hex).
6. JSON form also requires `target_device_class` (port-map list or `UNDEF`), `transport_used` (`BT` | `WiFi` | `USB` | `Cellular` | `UNDEF`, exact case), and a non-empty `timestamp_ET`. Optional `hive_unit_id` must be a string.

Any failure prints `FAIL (refuse to run)` and exits **1**. Only a clean run prints `PASS` and exits **0**. The stub only checks; it never runs the payload. What the phone does after PASS: **UNDEF**.
Signing: **UNDEF** (sha256 proves the file matches the list, not who wrote the list).
`manifest_sha256` / receipts for Hive units: **not implemented** (spec sec 3 still SUGGESTED).

## 4) File layout (SUGGESTED, not locked)

On the box (BOX, exists now):

```
tims-edge-math/targets/pythonista/phase1/
  manifest_check.py          stdlib-only check, exit 0/1, PASS/FAIL
  demo/
    manifest.json            JSON form, 2 files, transport_used UNDEF
    manifest.lines           same 2 files, lines form
    payload/hello.py         demo file (not run by the check)
    payload/notes.txt        demo file; has a '-' lead line for the lead_filter demo
```

On the phone (SUGGESTED only; nothing copied):

```
Pythonista Script Library / tims-edge-math / targets / pythonista / phase1 /
  manifest_check.py
  lead_filter.py             OPTIONAL, only if Timothy copies it
  <bundle>/manifest.json     sent with each delivery
  <bundle>/...files...
```

Run (SUGGESTED, Pythonista "Run with Arguments", P, not verified): `manifest_check.py <bundle>/manifest.json` or `--self-check`.

## 5) Bridge to lead_filter.py (optional import)

- `lead_filter.py` lives at `/workspace/github-push-basic-2026-10-05/basic/lead_filter.py` (already in `basic/`, 81/81 PASS earlier). It is **not** copied into `phase1/` this pass.
- `manifest_check.py --self-check` tries `import lead_filter` from its own folder or anything already on `sys.path` (on the box: `PYTHONPATH=/workspace/github-push-basic-2026-10-05/basic`). If present, it runs 3 bridge checks (filter `-` to `CHAR(45)`, restore, fail-closed on missing token). If absent it prints `SKIP` - **absence is not a failure**.
- The manifest check itself never depends on lead_filter. If Timothy wants it on the phone, he copies `lead_filter.py` beside `manifest_check.py` and lists it in the manifest like any other file.

## 6) I/O goals (goals only, NOT implemented)

| Goal | Phone-phase note | Status |
|---|---|---|
| Print (text out) | stub uses plain `print()` to the Pythonista console | BOX only; console on phone UNDEF |
| Speech out | Pythonista `speech` module is class-typical (P) | **UNDEF, not used, not verified** |
| Auditory out (tones / JBL Clip 4 over BT, L-E) | Pythonista `sound` module (P); JBL pairing is an iOS setting | **UNDEF, not paired, not used** |
| Braille | iOS VoiceOver + a braille display (P) would read console text | **UNDEF**: display model and VoiceOver setup unknown |
| Vision / mic (2 camera-mics owned, L-E) | not part of phase 1 | **UNDEF** |

Keep output short plain ASCII lines (`PASS ...`, `FAIL ...`) so speech and braille readers have little to parse. That is a SUGGESTED style, not a tested accessibility claim.

## 7) UNDEF on Timothy's phone (not verified)

1. Pythonista version and bundled Python version.
2. Whether `hashlib`, `json`, `tempfile`, `os.path.realpath`, `os.symlink` behave as on the box.
3. Whether "Run with Arguments" works the same way for him.
4. Script Library paths and whether files arrive there by USB file sharing, Files/iCloud, or LAN download (spec sec 5 A/B/C).
5. `speech`, `sound`, `console`, `cb` modules: present? behavior? (P only).
6. VoiceOver / braille display pairing.
7. What runs after PASS, and who launches it.

## 8) Non-claims

- Stub tested on the box only (see self-check report). Not pushed, copied, AirDropped, or synced to any device.
- No network code, no Bluetooth code, no install step, no pip.
- Not the descending-power sampler / live RGB. Sealed kbld / MinRadius / GOSUB bodies excluded.
- BOOT.bas `0.70710678` = math continuity only.

## 9) Cross-links

- Self-check report: `/workspace/session-scan-2026-10-05/PYTHONISTA_PHASE1_SELFCHECK_2026-10-05.md`
- Manifest spec: `reference-map/EDGE_MANIFEST_SPEC_2026-10-05.md` (full-file `0d92dcc4815c47b107c3f31614ad30f1cf7ed6528671b00b976c0b8b30bbeae7`, not modified)
- Transport matrix: `reference-map/EDGE_TRANSPORT_MATRIX_2026-10-05.md` (full-file `779a085c29645e39c0cb517046f7a1c54270d3354d3460a4b0f41abd08d1f5d1`, not modified)
- Locked answers: `reference-map/EDGE_LOCKED_ANSWERS_2026-10-05.md` (`813d0c20432f079abab16866efedcdeec75914dedeb4bcae54d8a077b4e046f2`, not modified)
- Port map: `reference-map/EDGE_DEVICE_PORT_MAP_2026-10-05.md` (full-file `6b37540f4185c3fc3632863a54903f0093fcbb7f0c3fa895c3aac4e666d4b4a9`, not modified)
- Existing Pythonista math target: `targets/pythonista/main.py` + `README.md` (not modified)

## Footer: hashes (BOX)

| File | sha256 |
|---|---|
| `targets/pythonista/phase1/manifest_check.py` | `f639f973067132aa3a909307c61d6a3ac1260b6dc8c32430358a9cd07cd04b56` |
| `targets/pythonista/phase1/demo/manifest.json` | `e2d048ee792fcf6fac60c25a5278679720c2f9bc8336a60777a6b88317310005` |
| `targets/pythonista/phase1/demo/manifest.lines` | `9764e353f4bdcb43b2559829f3460070d87c5220c09a09d13c558500df0758e2` |
| `targets/pythonista/phase1/demo/payload/hello.py` | `933d02dbf5426732f1f3483fed58602aecea2bc0e48bcc1ef473e6102393f3e7` |
| `targets/pythonista/phase1/demo/payload/notes.txt` | `5cf6a02b4525cb0780b1df188e7929cb8e5bb73414180c096f183151fb212fa3` |
| `basic/lead_filter.py` (optional bridge, not copied) | `6fd51db94ce418178530d39f396376ceb36c1e8c60d65d305852070af11091b3` |

This doc's own hash is reported in MASTER sec 15 (full-file).
GitHub push: **SKIPPED**.
