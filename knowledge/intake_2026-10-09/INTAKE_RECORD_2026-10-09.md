# Intake 2026-10-09 — base-360 trial, UDN reference, KBLD9 R3 / R2, 64-cell kernel

Stamp: 2026-10-09T08:15-04:00. Owner: Timothy. Seat: Claude. Append only.
Labels: REPRODUCED = run here this session (x86_64, Python 3.13.16); REPORTED = the other seat's words; ADDED = new file this session.
Nothing ran on a Pi. Every .py here parses under Python 3.11 grammar (Raspberry Pi OS Bookworm). Stdlib only.
Originals are byte-identical to what Timothy uploaded; the two zips are kept whole beside their unpacked folders and every member was compared byte for byte.
Personal and device-identifying items from the same upload were filed in the private archive, not here.

## Files and results

| File | SHA-256 (first 16) | Result |
| --- | --- | --- |
| Base360_Exact_Ratio_Trial.zip → base360_trial/ | a4141e90a911b05c | REPRODUCED: SHA256SUMS.json matches all 6 files; original 11/11 tests pass (also under -O); report.json regenerates byte-identical |
| base360_trial/test_base360_stops_2026_10_09.py | ADDED | 10 tests on how the converter stops: equal accuracy counts as met at that digit; one hair tighter needs the next digit; 41,934-case earliest-stop sweep against independent long division; digit budget stop says accuracy_met False; exact remainder stops; zero budget never loops. Plus 4 zero tests |
| base360_trial/base360_zero_cut_2026_10_09.py | ADDED | Display fix, original not edited (see Defect) |
| KBLD9_SVCT_UDN_reference_v0_1.zip → kbld9_udn_reference/ | 3af718d1a1512eb7 | REPRODUCED: 11/11 tests (also under -O); demo audit regenerates byte-identical, final hash 20a1ee98af56eed2…; identity SIMULATED, keys public demo keys, no C++, no device run (its own words, confirmed) |
| kbld9_validation_r3.py | 095caf9269a90eef | REPRODUCED: PASS 28/28 groups, 10,000 directional cases, 200 concurrent appends (also under -O). Uploaded twice; both copies identical |
| kbld9_adversarial_r2.py | cd1c6a34dcfadaf2 | REPRODUCED: PASS 28/28 (also under -O). Its docstring calls itself kbld9_hardened_candidate.py; the 13 pass / 2 fail suite named in the 2026-10-07 audit is a different file (test_kbld9_adversarial.py), not in hand |
| KBLD9_SVCT_REFERENCE_KERNEL_2026-10-08.txt | 892110f9e520d17a | Python kernel rebuilt from the text: 28 boundary + 36 interior, round trip, 64-thread run and the RECORD line all REPRODUCED. C++ is an excerpt only, so C++ parity and the stdout SHA f68ae592… stay REPORTED |
| Grok_Table_kernel_status_2026-10-08.csv | a555b091c723e084 | REPORTED status table from the other seat; agrees with the kernel text |
| KBLD9_SVCT_PROJECT_ASSESSMENT_2026-10-08.txt | 5e1486b2c3274c62 | REPORTED architecture review from the other seat; no code |

## Mutation check (base-360)

Before: 5 code changes, 4 caught; the change `>` to `>=` in the accuracy stop survived all 11 original tests.
After adding the stop tests: 9 changes, 9 caught (the 5, plus `<` to `<=` on the digit budget, `<=` to `<` on accuracy_met, and two on the zero leaf).
Cross-check: base360.terminating_digits agrees with `gosub_ratio_on_lattice` in kbld/…_DRIVE_D3_restored_2026-10-08.py on all 199,000 ratios p = 1..199, q = 1..1000.

## Defect found: negative zero in base-360 display

`format_digits(encode(-1/720, digits=1))` prints `-0.000`; so does any small negative value cut to few digits.
Timothy's rule: −0 and 0 both become 0. The record itself is right (it keeps sign and the exact error), only the text is wrong.
Fix as a new leaf: `format_digits_no_negative_zero` drops the sign only when the whole part and every shown digit are zero.
base360.py is unchanged. Which one the kit uses is Timothy's call.

## Kernel caution

forward adds a mark and inverse subtracts the same mark, so the round trip can only fail if the two are written inconsistently; at cell 0 the mark is 0.
It proves the bookkeeping, not that 28 + 36 holds information. The other seat says the same about the mask ("reversible mask is still not earned").

## Not done

C++ for base-360 and UDN; any Pi run; vision and face work (private archive, source photos not here); the 64-cell exact mapping.
