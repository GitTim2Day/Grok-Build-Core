# OEIS MATCHING — integer lists in work_core_2026-11-09.zip

OEIS data: /workspace/oeis_public/stripped.gz (401172 sequences) and names.gz, downloaded from oeis.org (OEIS End-User License / CC BY-SA 4.0, attribution: The OEIS Foundation).

## Method

- Scope: every UTF-8/text file under `work/` except `venv_*/`, `third_party/`, `maps/` (OSM coordinates), `rruff/data785|broad785/` (Raman spectra, decimal data), `.git/`, `__pycache__/`, files > 4000000 bytes, and `oeis_earn/run/*.jsonl` (8 files that are themselves OEIS extracts; matching them would only rediscover OEIS).
- Extracted lists (scripts/numlists.py): bracketed integer arrays `[..]`, `{..}`, `(..)` incl. multi-line; runs of ≥6 integers on one line (comma/space/semicolon/bar separated, floats excluded); integer-only CSV/TSV columns (≥6 cells); integer JSON arrays. Raw lists 133294 → unique 13083.
- Matching (scripts/oeismatch.py): every 6-term window of each list with ≥3 distinct values is looked up against every 6-term window of every OEIS sequence; each hit is extended both ways to the longest exact common run. Exact integers only. A run of ≥6 consecutive terms counts as a match. "Leading" = the run starts at the first stored term of the OEIS entry.
- Lists with a hit: 31 of 13083. Each was then read in context and classed as **meaningful** (the file is clearly storing that sequence) or **coincidental** (row ids, test inputs, measurement rows that happen to occur in some OEIS entry).

## A. Meaningful matches

| file:line (copies) | A-number | OEIS name | terms matched | where in OEIS | stored terms |
|---|---|---|--:|---|---|
| work/oeis_earn/drive_orig/gp_selftest.py:11<br>work/oeis_earn/run/gp_selftest.py:11 | A000040 | The prime numbers. | 10 of 10 stored | from OEIS term index 0 (of 58 listed); leading | 2,3,5,7,11,13,17,19,23,29 |
| work/oeis_earn/drive_orig/gp_selftest.py:8<br>work/oeis_earn/run/gp_selftest.py:8 | A000041 | a(n) is the number of partitions of n (the partition numbers). | 16 of 16 stored | from OEIS term index 0 (of 50 listed); leading | 1,1,2,3,5,7,11,15,22,30,42,56,77,101,135,176 |
| work/oeis_earn/drive_orig/gp_selftest.py:9<br>work/oeis_earn/run/gp_selftest.py:9 | A000110 | Bell or exponential numbers: number of ways to partition a set of n labeled elements. | 12 of 12 stored | from OEIS term index 0 (of 27 listed); leading | 1,1,2,5,15,52,203,877,4140,21147,115975,678570 |
| work/oeis_earn/drive_orig/gp_selftest.py:30<br>work/oeis_earn/run/gp_selftest.py:30 | A000142 | Factorial numbers: n! = 1*2*3*4*...*n (order of symmetric group S_n, number of permutations of n letters). | 12 of 12 stored | from OEIS term index 0 (of 23 listed); leading | 1,1,2,6,24,120,720,5040,40320,362880,3628800,39916800 |
| work/oeis_earn/drive_orig/gp_selftest.py:17<br>work/oeis_earn/run/gp_selftest.py:17 | A000203 | a(n) = sigma(n), the sum of the divisors of n. Also called sigma_1(n). | 12 of 12 stored | from OEIS term index 0 (of 70 listed); leading | 1,3,4,7,6,12,8,15,13,18,12,28 |
| work/oeis_earn/drive_orig/gp_selftest.py:24<br>work/oeis_earn/drive_orig/gp_selftest.py:29<br>work/oeis_earn/run/gp_selftest.py:24<br>work/oeis_earn/run/gp_selftest.py:29 | A000720 | pi(n), the number of primes <= n. Sometimes called PrimePi(n) to distinguish it from the number 3.14159... | 12 of 12 stored | from OEIS term index 0 (of 78 listed); leading | 0,1,2,2,3,3,4,4,4,4,5,5 |
| work/oeis_earn/drive_orig/gp_selftest.py:33<br>work/oeis_earn/run/gp_selftest.py:33 | A001065 | Sum of proper divisors (or aliquot parts) of n: sum of divisors of n that are less than n. | 12 of 12 stored | from OEIS term index 0 (of 80 listed); leading | 0,1,1,3,1,6,1,7,4,8,1,16 |
| work/oeis_earn/drive_orig/gp_selftest.py:26<br>work/oeis_earn/run/gp_selftest.py:26 | A001222 | Number of prime divisors of n counted with multiplicity (also called big omega of n, bigomega(n) or Omega(n)). | 12 of 12 stored | from OEIS term index 1 (of 111 listed); offset 1 | 1,1,2,1,2,1,3,2,2,1,3,1 |
| work/oeis_earn/drive_orig/gp_selftest.py:10<br>work/oeis_earn/run/gp_selftest.py:10 | A010815 | From Euler's Pentagonal Theorem: coefficient of q^n in Product_{m>=1} (1 - q^m). | 16 of 16 stored | from OEIS term index 0 (of 93 listed); leading | 1,-1,-1,0,0,1,0,1,0,0,0,0,-1,0,0,-1 |
| work/Grok-Build-Core/kbld/kbl_svct_stacks_MinRadius_Lp_2026-08-28_DRIVE_D2_restored_2026-10-08.py:640<br>work/Grok-Build-Core/kbld/kbl_svct_stacks_MinRadius_Lp_2026-08-28_DRIVE_D2_restored_2026-10-08.py:658<br>work/Grok-Build-Core/kbld/kbld_gosub_primitives_MinRadius_Lp_2026-08-28.py:23<br>work/Grok-Build-Core/kbld/kbld_gosub_primitives_MinRadius_Lp_2026-08-28_DRIVE_D3_restored_2026-10-08.py:22<br>work/jcj/vendor/kbl_svct_stacks_D2.py:640<br>work/jcj/vendor/kbl_svct_stacks_D2.py:658 | A018226 | Magic numbers of nucleons: nuclei with one of these numbers of either protons or neutrons are more stable agai | 7 of 7 stored | from OEIS term index 0 (of 7 listed); leading | 2,8,20,28,50,82,126 |
| work/Grok-Build-Core/knowledge/intake_2026-10-09/base360_trial/test_base360.py:7 | A018412 | Divisors of 360. | 23 of 23 stored | from OEIS term index 1 (of 24 listed); offset 1 | 2,3,4,5,6,8,9,10,12,15,18,20,24,30,36,40,45,60,72,90,120,180,360 |

Note: `oeis_earn/run/gp_selftest.py` and `oeis_earn/drive_orig/gp_selftest.py` are byte-identical (same sha256); both carry these lists. For A001222 the file starts at n=2 (`a(n)=vecsum(factor(n)[,2])`, offset 2), so the run starts at OEIS index 1. For A018412 the test list omits the divisor 1 (it tests 1/d for d>1); 23 of the 24 divisors are present. A018226 is a finite sequence (7 terms) and all 7 match; A162626 (a(n) = n(n^2+5)/3 for n ≥ 4, and n(n+1)(n+2)/3 for n ≤ 3) also reproduces these 7 terms from index 1.

## B. Decision per meaningful match: formula or stored table?

Cost figures are exact operation or byte counts, not timings (no Pi 5 timing was measured). All candidates below are exact in integer arithmetic; none needs floats or rounding.

| list | formula / generator (integer-only) | stored bytes now | compute cost | **pick** | why |
|---|---|--:|---|---|---|
| partitions p(0..15) (A000041), gp_selftest.py:8 | Euler pentagonal recurrence p(n)=Σ(-1)^(k+1)[p(n-k(3k-1)/2)+p(n-k(3k+1)/2)] | 69 (line incl. newline) | < 16×8 additions | **table** | It is the answer key that tests gp_mini; generating the key with code in the same harness weakens the test. Now verified against OEIS term-for-term. |
| Bell B(0..11) (A000110), :9 | Bell triangle (row sums by additions) | 67 | 66 additions | **table** | same reason: independent oracle; verified exact. |
| Euler pentagonal coeffs (A010815), :10 | a(n)=(-1)^k if n=k(3k±1)/2 else 0 | 60 | ≤ 16 checks | **table** | oracle; verified. |
| primes 1..10 (A000040), :11 | sieve to 29 | 46 | ≤ 29 marks | **table** | oracle; verified. |
| σ(n), π(n) (2 copies), Ω(n), n!, σ(n)−n (A000203, A000720, A001222, A000142, A001065), :17,:24,:26,:29,:30,:33 | trial-division / running product | 42, 36, 36, 36, 66, 37 (list-literal text, lines 17/24/29/26/30/33) | ≤ 12×12 divisions each | **table** | oracle role; the file already computes the easy ones (Fibonacci, n²+1, Catalan) by formula, and keeps literals where the formula would be the thing under test. |
| divisors of 360 except 1 (A018412), base360_trial/test_base360.py:7 | `[d for d in range(2,361) if 360 % d == 0]` | 66 (tuple text) | 359 modulo operations | **formula** | The test asserts a property for *every* proper divisor >1; generating the set guarantees completeness (no silent omission), is exact, and costs a few hundred integer ops. |
| nuclear magic numbers (A018226), kbl_svct_stacks_D2.py:640/658 and 4 other copies | A162626 polynomial n(n²+5)/3 (n≥4), n(n+1)(n+2)/3 (n≤3) | 27 per copy (`(2, 8, 20, 28, 50, 82, 126)`) | 7 cubic evaluations | **table** | Physical constants established by experiment; the polynomial is an approximation that happens to fit these 7 and predicts 184 beyond 126, which the code does not need. Table is smaller than the formula code and cannot drift. Source comments already say the use as a token grid is "NOT derived". |

## C. Coincidental matches (listed for completeness; not evidence of a stored OEIS sequence)

| file:location | stored terms (first 12) | n terms | best OEIS run | why coincidental |
|---|---|--:|---|---|
| work/CHECKPOINT_v8_part11_2026-10-10.md:12 (+0 copies) | 2,3,4,7,8,9,10,11 | 8 | A121405, 8 terms (Numbers that are not the sum of distinct pentagonal numbers ) | hand-picked values / ids |
| work/Grok-Build-Core/edge-canvas-kit/lib/descend.py:89 (+0 copies) | 5,3,7,0,3,4 | 6 | A029684, 6 terms (n-th digit after decimal point of 4th root of n.) | hand-picked test inputs |
| work/Grok-Build-Core/knowledge/intake_2026-10-09/KBLD9_SVCT_REFERENCE_KERNEL_2026-10-08.txt:37 (+0 copies) | -40,-23,-6,11,28,45,62,79,96,113,130,147 | 64 | A365316, 9 terms (a(n) = number of visible diamonds (squares rotated by 45 deg) | arithmetic progression (row ids / ranges); matches 4 sequences |
| work/Grok-Build-Core/knowledge/intake_2026-10-09/base360_trial/examples.py:6 (+0 copies) | 2,3,4,5,6,7,8,9,10,11,12,16 | 18 | A293715, 12 terms (Numbers k such that A007755(k) is prime.) | hand-picked values / ids |
| work/Grok-Build-Core/mapbook/make_osm_fixture.py:72 (+0 copies) | 1,2,3,4,5,6,7,8,14,15,0,0 | 13 | A032870, 10 terms (Numbers whose base-7 representation Sum_{i=0..m} d(i)*7^i ha) | hand-picked values / ids |
| work/Grok-Build-Core/tims-tables/Tims_Tables_Core_Six_Ratios.csv:col3(Degrees) (+0 copies) | 45,60,90,120,180,240,270,360 | 8 | A359410, 6 terms (Integers d such that the longest possible arithmetic progres) | hand-picked values / ids |
| work/escalations/tests/deid_v6.py.before_stamp_epoch_2026-10-15:209 (+30 copies) | 0,1,2,3,5,6,8,9,11,12,14,15 | 12 | A061723, 12 terms (Floor of arithmetic-geometric mean of n and 2*n - 1.) | hand-picked values / ids |
| work/jcj/runs/out_spec_csv/STORE_ITEMS.csv:col1(id) (+1 copies) | 0,1,2,3,4,5,6,7,8,9,10,11 | 56 | A001477, 56 terms (The nonnegative integers.) | arithmetic progression (row ids / ranges); matches 11362 sequences |
| work/jcj/selfcheck_numeric.py:310 (+0 copies) | 350,355,358,359,0,1,2,4,5,10,180 | 11 | A109511, 6 terms (Number of subsets of the first n numbers having a common div) | hand-picked test inputs |
| work/jcj/selfcheck_numeric.py.before_circular_2026-10-14:119 (+1 copies) | 1,2,3,4,5,6,7,8,9,10,20 | 11 | A032571, 11 terms (Numbers k whose decimal representation, read as a base-20 va) | hand-picked test inputs |
| work/jcj/selfcheck_numeric.py.before_circular_2026-10-14:130 (+7 copies) | 10,11,9,10,12,10,11,9,10,10,1000 | 11 | A172005, 6 terms (Shortest SNUSP representation of a number using only + and @) | hand-picked test inputs |
| work/jcj/selfcheck_runctl.py:206 (+1 copies) | 1,2,3,4,5,6,7,8 | 8 | A000027, 8 terms (The positive integers. Also called the natural numbers, the ) | arithmetic progression (row ids / ranges); matches 6805 sequences |
| work/jcj/vendor/conflict_nodes.py:12 (+3 copies) | 0,1,2,3,4,5 | 6 | A000030, 6 terms (Initial digit of n.) | arithmetic progression (row ids / ranges); matches 2732 sequences |
| work/jcj_cpp/uni_tables.h:12 (+0 copies) | 0,1,3,4,6,7,8,10,11,13,14,15 | 4929 | A098670, 51 terms (Start with a(1) = 5. Construct slowest growing sequence such) | Unicode property ranges generated by gen_tables.py |
| work/kbld9_shadow_runs/2026-10-15_ndbc41008/stage1_csvson/csvson.csv:col1(rid) (+5 copies) | 1,2,3,4,5,6,7,8,9,10,11,12 | 6398 | A262530, 110 terms (Numbers such that digits occur at most twice in decimal repr) | arithmetic progression (row ids / ranges); matches 13220 sequences |
| work/kbld9_shadow_runs/2026-10-15_ndbc41008/stage1_csvson/csvson.csv:col5(line_no) (+2 copies) | 2,3,4,5,6,7,8,9,10,11,12,13 | 6398 | A262530, 109 terms (Numbers such that digits occur at most twice in decimal repr) | arithmetic progression (row ids / ranges); matches 12284 sequences |
| work/kbld9_shadow_runs/2026-10-15_ndbc41008/stage2_jcj/ndbc_41008_realtime.txt.csv:col1(id) (+2 copies) | 0,1,2,3,4,5,6,7,8,9,10,11 | 6398 | A262530, 110 terms (Numbers such that digits occur at most twice in decimal repr) | arithmetic progression (row ids / ranges); matches 13588 sequences |
| work/kbld9_shadow_runs/2026-10-15_usgs_all_day/stage1_csvson/csvson.csv:col1(rid) (+1 copies) | 1,2,3,4,5,6,7,8,9,10,11,12 | 250 | A262530, 110 terms (Numbers such that digits occur at most twice in decimal repr) | arithmetic progression (row ids / ranges); matches 12797 sequences |
| work/kbld9_shadow_runs/2026-10-15_usgs_all_day/stage1_csvson/csvson.csv:col5(line_no) (+0 copies) | 2,3,4,5,6,7,8,9,10,11,12,13 | 250 | A262530, 109 terms (Numbers such that digits occur at most twice in decimal repr) | arithmetic progression (row ids / ranges); matches 11853 sequences |
| work/kbld9_shadow_runs/2026-10-15_usgs_all_day/stage2_jcj/usgs_all_day.csv.csv:col1(id) (+0 copies) | 0,1,2,3,4,5,6,7,8,9,10,11 | 250 | A262530, 110 terms (Numbers such that digits occur at most twice in decimal repr) | arithmetic progression (row ids / ranges); matches 13164 sequences |

## D. Numeric lists with no meaningful OEIS match that look formula-derivable

| file:location | what it is | formula | stored bytes | **pick** | why |
|---|---|---|--:|---|---|
| Grok-Build-Core/knowledge/intake_2026-10-09/KBLD9_SVCT_REFERENCE_KERNEL_2026-10-08.txt:37 | `RECORD` line, 64 terms −40, −23, …, 1031 | a(n) = 17n − 40, n = 0..63 | 258 | **formula for regeneration; keep the RECORD line as evidence** | It is a captured run output; the formula verifies it exactly in 64 integer multiply-adds. |
| Grok-Build-Core/tims-tables/Tims_Tables_Core_Six_Ratios.csv col 3 `Degrees` | 45,60,90,120,180,240,270,360 | Degrees = 360·p/q from the `Fraction` column (always an exact integer here) | 8 cells | **formula (derive from Fraction)** | The column duplicates the exact ratio. Note the same file stores `Radians (e-15)` and `Exact_Decimal` as rounded decimals (e.g. "1/6 ≈ 0.1666667"), which conflicts with the no-float rule; store p/q only and render 2π·p/q symbolically. Only a coincidental 6-term OEIS run (A359410). |
| Grok-Build-Core/tims-tables/TIMS_TABLES_CATEGORY9_*.csv (4 files) col 2 `category` | constant 9 | a(n)=9 | 7+8+15+19 cells | **formula / drop column** | Constant column; the file name already says CATEGORY9. |
| escalations/**/deid_v3..v6 (.py/.cpp, 31 copies) `is_datetime` digit positions | 0,1,2,3,5,6,8,9,11,12,14,15 | {0..15} minus {4,7,10,13} | 40 per copy (list literal) | **table** | Fixed ISO-8601 layout; the literal is clearer and cannot be mis-derived. No meaningful OEIS match (A061723 run is accidental). |
| kbld9_shadow_runs/**/csvson.csv `rid`, `line_no`; stage2 `.csv` `id`; jcj/runs/out_spec_csv/STORE_ITEMS.csv `id` (and the circular_demo/old + new copies) | 1..6398, 2..6399, 0..6397, 1..250, 0..55 | row index (+0/+1) | 30883 + 30886 + 30880 + 892 + 894 + 890 + 158 = 95483 per set | **table** | They are explicit join keys in append-only audit records; records must stand alone. The id columns are 95483 of the 3055246 bytes of those 5 files (exact ratio 95483/3055246). |
| svct_model/out_{py,cpp,bas}.txt, act_{py,cpp,bas}.txt | cumulative state-time columns | prefix sums of the duration column; whole file = svct_model.py / active_model.* run on events.txt (248 bytes) / turns.txt (2121 bytes) | 1340×3 + 8384×3 | **table (keep as cross-language evidence)** | These are the 3-way differential outputs (Python/C++/BASIC); they are the proof, not data. |
| jcj_cpp/uni_tables.h | 4929-term Unicode range array and others, "generated by gen_tables.py; Python 3.13.5, unicodedata 15.1.0" | gen_tables.py (1754 bytes) from Python `unicodedata` | 115138 | **table** | C++ has no unicodedata; the generated header pins the Unicode version; the generator is kept for re-derivation. |
| escalations/**/deid_v3..v6.bas `RL$` (21 copies) | 036,059,063,102,203,556,692,790,821,…,893 | none found | 75 per copy (`RL$="…"`) | **table** | Looks like a code list (zero-padded 3-digit codes), not a sequence. |

Not formula-derivable (data, kept as data): measurement rows in `kbld9_shadow_runs/` and `circular_demo/` (NOAA NDBC buoy 41008 and USGS feeds), run logs in `runs/`, byte-size columns (`archive/DEDUPE_INDEX.tsv`, `escalations/hostile/RUN_OUTPUT_MANIFEST_2026-10-15.tsv`, `Grok-Build-Core/knowledge/FILE_MAP_PUBLIC_2026-10-09.tsv`), HTTP status columns (`route_check_20261010_101907.tsv`), epoch timestamps.

Tim's Tables (`Grok-Build-Core/tims-tables/`, 29 files): the CSVs hold fractions, ratios, units and decimal renderings; the only integer runs of ≥6 are the Degrees column and the constant category column above. No Tim's Tables list matches an OEIS sequence meaningfully.

## E. OEIS material already in the archive

- `oeis_earn/` (26 files, 129218225 bytes): the 2026-10-16 EARN re-run on a full OEIS checkout (`EARN_RESULTS_2026-10-16.md`: 400,361 entries; earn_pari on 6802 table entries: EARNED 2747). `run/PARI_BLOCKS.jsonl` (76935374 bytes) and `run/inventory.jsonl` (48792824 bytes) are derived from OEIS and can be regenerated from the public data plus `pari_extract.py` / `inventory.py`.
