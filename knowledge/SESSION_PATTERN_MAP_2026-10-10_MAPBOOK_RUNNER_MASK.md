# Session pattern map — 2026-10-10 (08:15–09:50 ET)

Owner: Timothy Norman. Seat: Claude (chat). Append only.
Each row: the pattern, where it showed up, the rule it leaves behind. Labels: EARNED (run and
checked this session), PROPOSED (needs Tim's yes).

## 1. Patterns

| # | Pattern | Where it showed up | Rule left behind | Label |
| --- | --- | --- | --- | --- |
| 1 | One name, many apps | "Mapper" = Safari redirect, Contact Mapper, PinMapper, Google screenshot lists | List every candidate, dedupe features to fundamentals, show Tim before building | EARNED (15 fundamentals) |
| 2 | Edge first, key last | MAPBOOK features | 12 of 15 run offline on the Pi; Google only through key-free Maps URLs | EARNED (sources fetched) |
| 3 | Defects found by the second twin | OSM streamline S1-S6 (empty file, UTF-8, zlib crash, check order, bounds, NUL cut) | Fix the spec first, then both twins; fuzz until 0 mismatches | EARNED (2,200 cases) |
| 4 | Key gaps found by mutants | no primary road, already-sorted ids, no header-missing file; mask prefix and front-of-word cases | A surviving mutant means a missing test, not a lucky pass | EARNED (31/31, 8/8) |
| 5 | Daemon that leans on time | runner reader thread, accelerometer sleep loop, camera loop | Trigger order: need detected -> asked -> scheduled -> asleep | EARNED (runner), PROPOSED (rest) |
| 6 | Leak proven before the fix | runner: 5 s stall, lost output, +1 thread, +1 fd per run | Demonstrate, then fix; tests run on the old code must fail | EARNED |
| 7 | My own test leaked | T1 helper process counted as STRAY by the kit's mutant tool | Every test kills what it starts, by pid | EARNED |
| 8 | My own test was wrong | "Ashlee" contains lowercase lee, so the word-boundary mutant lived | When a mutant survives a new test, check the test's data first | EARNED |
| 9 | Gate rule protects one person only | mask v1 NAME rule = the author's surname | Known-names list + bogus placeholders (John Q. Public...), same set for demos and test forms | EARNED (327 pass) |
| 10 | Old rule outlived its reason | "Tim pastes URL" fetch gate on ~50 register rows | Fetch every URL directly; Pi script for the rest; never ask Tim to paste | EARNED (28 EARNED, 21 Pi) |
| 11 | Block is not geography | robots.txt, JavaScript pages, a legal block | No VPN or workaround; the Pi reading a public API is ordinary use | EARNED |
| 12 | Planted or honest errors caught | `wget https://google.com` for Chrome; Chrome thought needed for bwbasic; America.gov unknown | Check every claim against the source before acting | EARNED |
| 13 | AI front doors are not sources | America.gov runs on Gemini and Grok | Its answers stay ASSERTED until the agency page confirms | EARNED |
| 14 | Stop hook vs gate rule | hook demanded a push before mutants ran | Push unverified work only to a wip/ checkpoint branch; main only after the gate | EARNED |
| 15 | Long waits get interrupted | 5 interrupts during blocking test waits | Run long gates in the background, report when done | PROPOSED |
| 16 | Scheduled tasks hit the limit | weekly source watch and monthly review failed (usage limit) | Budget scheduled work; lean prompts with search caps | PROPOSED |

## 2. Where the updates happened (search path: GitHub log, Notion register, task list)

| Store | What | ID / location |
| --- | --- | --- |
| GitHub main | MAPBOOK finder + OSM streamline | a689f48 `mapbook/` |
| GitHub wip | runner checkpoint (merged later) | 3aa87aa `wip/runner-read-v2` |
| GitHub main | runner reader v2 | bfe139a `edge-canvas-kit/lib/runner.py` + tests + spec |
| GitHub main | mask v2 + route script | 8416e57 `edge-canvas-kit/lib/mask.py`, `routes/route_check_pi.sh` |
| GitHub main | Pi handoff | c5afad1 `HANDOFF_2026-10-10_PI.md` |
| Notion register | 6 new GOV-FIRST rows | collection 29c9fd18…; GSA GitHub, USA.gov, GSA.gov, data.gov CKAN (now SUPERSEDED), code.gov, America.gov |
| Notion register | 28 rows -> EARNED, 21 -> BLOCKED (Pi), 3 notes | same collection; Last Check 2026-10-10 |
| Notion register | Data.gov v4 row retitled GOV-FIRST, EARNED with DEMO_KEY | 3e9c86699c9481958f41e050d4c80d74 |
| Scheduled tasks | Daily BOLO 07:49 ET, auto mode | trig_013BfAzbABrohdQrgTPpqPUX |
| Sandbox only | fuzz/mutant logs, big.pbf | not kept |

## 3. Repeating processes, grouped (each is now one subroutine)

- **GATE_SHIP** (ran 4 times: finder, streamline, runner, mask): spec -> twins -> answer key -> fuzz -> mutants -> fix spec first -> commit -> fresh-clone verify.
- **FETCH_RECORD** (ran ~55 times): fetch URL -> one-line fact -> register Status / Last Check / Last Result / Next Action.
- **CHECKPOINT** (ran 2 times): wip branch while unverified; handoff file at the end.
- **CLAIM_CHECK** (ran 4 times): search or fetch the source before acting on a claim.

## 4. Not done
Pi run of MAPBOOK, route check, daemon census, BASIC/UI mutants; address finder BASIC twin;
CMS-1500 field masking; daemon fixes #2-#4.
