# Session pattern map v2 — 2026-10-27 exact-ratio FOR loop (scope=session)
Built 2026-10-27 ~14:25 ET. Never invent: anything not checked on disk is UNVERIFIED.

## Evidence items
| E | Fact | Source | sha256 (file) |
|---|---|---|---|
| E1 | Float STEP 0.1: 11th value 0.99999999999999988898, 1.0 missed (Python=C) | exponent-step-probe-2026-10-27/RESULTS.md | c2e334f2cde91c8574060d72c22fb24385af60ef3742580670fd2041337d9e35 |
| E2 | bwbasic 2.20: any fractional STEP runs body once and quits | same | same |
| E3 | bwbasic FOR I=1 TO 0 runs once; x^0 gives 2 without guard; guard IF N>=1 fixes | same | same |
| E4 | Fractional exponent as exact integer q-th root, 45 dp truncated; 2^(-1/2)=1/sqrt2 | same | same |
| E5 | Integer counter + X=I/q hits all values, ends exactly on 1 | exponent-step-probe README.md | 2f8f4894fefc2b3ae174dde7605e040064d3927a362c6a08c3614ae8da7da8fc |
| E6 | Exact-ratio FOR/TO/NEXT routines: Python, C, bwbasic GOSUB 5000/5500/5700/5800 (+4000 runner, 6000/6100/6300 helpers) | exact-for-loop-2026-10-27/README.md | 35de93f997e92f4fc84c233ad5a9043bc995fc913e7a4ee9fa7666e30f47520c |
| E7 | Loop main 440 vectors: Python=C byte-identical (1,063,181 lines); bwbasic 439/439 (63,180 lines, V029 skipped); 419 ref-equal, 21 E3 prefix, 0 mismatch | RESULTS.md, out_compare.txt | 770cb628…8bbd, eca28696…f197 |
| E8 | Hardening 24 vectors: 3 engines byte-identical, 66 lines | RESULTS.md | 770cb628…8bbd |
| E9 | Pythagorean GOSUB 7000-7755: 254+H45, 255 lines, identical, = Fraction reference | RESULTS.md | same |
| E10 | 45-degree tests: squared check, deferred-scale rotation (8 steps = 16x, K=8 -> 1/16), near-isosceles series to 27304197-27304196-38613965; 69/69 checks | RESULTS.md | same |
| E11 | 3 rounds: R1 V029 too slow + double interpreter; R2 80-col wrap fixed with WIDTH 255; R3 all byte-identical, tri45 N$ clobber fixed | ROUNDS.md | 0099f028dcb2f79e251b1ce77345d054976f4262341c14f5f54ead35e9187014 |
| E12 | Limits: 2^53-1 all engines; E4 cap 1e6 is a design choice, not in spec; E6 untested; zero printed 0/1 (pending Timothy's ruling) | RESULTS.md | same |
| E13 | 1/sqrt2 45dp truncated 0.707106781186547524400844362104849039284835937 (= isqrt(5*10^89)) | RESULTS.md | same |
| E14 | Timothy: exact ratio steps restore FOR/TO/NEXT utility like GOSUB and IF-THEN | chat (parent brief) | UNVERIFIED on disk |
| E15 | Timothy: avoid decimals, use fractions (1 1/3 = 4/3) | chat | UNVERIFIED on disk |
| E16 | Timothy: 3-4-5 triangle in place of roots/squaring; sin^2 = sin*sin; circumvent 1/sqrt2 | chat | UNVERIFIED on disk |
| E17 | Timothy [pt1046u]: "Two 90 degree angles is a semicircle. That leaves 3/4 and 4/4. It's hiding there somewhere. It may even already be on Tim's Tables in a different BaseNNN. Maybe a function of a sphere or geodesics." -> OPEN idea, not a claim | owner message pt1046u | n/a |
| E18 | Queued email 4 (boot file S6): queue sha 96c13e22…d50f; live skill now 099897c5…; archived copy 96c13e22 exists -> needs re-seal before release | boot-archive/LEDGER_QUEUE.jsonl; GOSUB_PROPOSAL_2026-10-27.md:12 | 919ab0c0…bbc; 896c845a…5245 |
| E19 | Equation audit: solve_seq.py lines 98-99 pre-write FAIL for A000040 before solving; recommendation per no-value rule | equation-scratch-pad/solve_seq.py | c62c828a9d6d0f2ed9f6168ce691e88220a60e4227f8aa7ced64893c6fa26e22 |
| E20 | Rubik summary answered today | chat only | UNVERIFIED (no new file today) |
| E21 | Timothy 2:17 PM ET: "1:1:(2^(1/2)) could be modified"; approved squared-sides form 1:1:2 (1+1=2, root only on display) | parent steering message | n/a |
| E22 | squared-sides test: 13/13 OK (1:1:2, 9:16:25, 25:144:169, NI01-NI10 squared, max C2 1491038293021225 < 2^53-1); Python=C=bwbasic byte-identical 0759d79f…1289 | exact-for-loop-2026-10-27/squared-sides/ | SHA256SUMS fa799f2fd1e11ad36e6e82b84c566d9a071ddb8538ccd420955f89799d5a5b9c |
| E23 | Tim's Tables: 45° entries are 1/8 turn, sin=cos=√2/2, tan 1; isosceles right u:u:u√2 (2026-10-02); no exact/base-N substitute for sqrt2 found; sphere octant files are DERIVED from circle token | tims-tables/TIMS_TABLE_ADD_ISOSCELES_RIGHT_2026-10-02.md; TIMS_TABLES_TO_1_12_2026-09-22.md:16; BASE360_DERIVED_LOCK_2026-09-19.md:64 | 2fda92f0…566a; b0817c30…bcf; d0430471…a71b |

## Patterns
- P1 Exact ratio over float drift (E1, E2, E4, E5, E6, E7, E13, E15).
- P2 Empty loop / empty product guard; engine quirks fixed by routine, not trust (E3, E11).
- P3 Three-engine byte-identical as proof (E7, E8, E9, E10, E22).
- P4 Root-free geometry: squared domain, 3-4-5, deferred scale, 1:1:2 (E10, E16, E21, E22, E23).
- P5 Declared limits, fail closed (E3 code, E4 cap, E6 untested) (E7, E12).
- P6 Open questions held for Timothy (E12 zero ruling, E17, E18, E19).

## Fixes from AUDIT
- D1: squared-sides/ sealed by its own SHA256SUMS fa799f2f…5b9c; parent SUMS untouched.
- D2: queue email 4 needs re-seal (point at archived 96c13e22 copy or re-hash live 099897c5); held for Timothy, queue not touched, nothing sent.
- D4: v2 copied to the live master's reference-map (session-scan-2026-10-05/.../reference-map/session-map-2026-10-27-exact-ratio/).
- D8: E23 now carries paths and hashes.

## Checked vs UNVERIFIED
Checked: E1-E13, E18, E19, E22, E23 (sha256sum -c 14/14, 55/55, 9/9; line counts; output shas; Tim's Tables lines).
UNVERIFIED: E14-E16, E20 (chat only); bwbasic V029; E6 path; bwbasic overflow monotone for every build; zero 0/1 and E4 cap await Timothy.
OPEN (not a claim): E17 — 3/4 and 4/4 substitute for 1/sqrt2, maybe on Tim's Tables in another BaseNNN, sphere or geodesics. Search today: NOT FOUND (Tim's Tables gives 45° only as √2/2 and u:u:u√2; the root-free form now in use is squared sides 1:1:2, E21/E22).

## v1 -> v2 drop check
All 23 evidence items and 6 patterns from v1 are present in v2 (0 dropped).
