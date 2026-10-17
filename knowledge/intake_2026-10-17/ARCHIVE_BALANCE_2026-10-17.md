# Archive balance — 2026-10-17

What was not added. The miss stays here. Nothing below was deleted from a shelf; it was never the leaf.

## From the conformance paste

Not adopted:

- The in-memory Chain. A disk neighbor already exists: knowledge/intake_2026-10-09/kbld9_validation_r3.py Ledger. Different canon. That one rejects floats, locks canonical bytes, uses previous_hash None at the start, and sequence starting at 1. The paste uses prev = 64 zeros and does not check parent_ts except inside the hash.
- Shallow copy. forward() shares the nested data dict. Mutating data["v"] on a read copy changed the live record and verify went false. The paste's own copy test only writes the top-level content field, so it passed.
- Geometry spokes^2. Already held. Octave check E4: 8 bands x 8 sectors = 64 cells of 1/64. Tim's Tables: N=360 gives 129600 cells. Not re-sealed.
- Reserved-cell contents. Still C2. The count 8 + 56 = 64 was not turned into an allocator.

The number face of that paste was kept. It is exact_text.frac_trunc_sig. 1/10^20 at 4 significant digits stays positional: 0.00000000000000000001000. That value is outside the BASIC band.

## From gen_bas.py

Not adopted, as pasted:

- DATA written as nD+00. Bywater 3.20b says Bad DATA. The 2026-10-08 vetting already recorded that. The runnable file uses long integer literals.
- Source literal 1D+14. Same reason. The runnable file uses 100000000000000#.
- The remark "UNRUN: no BASIC interpreter". Bywater 3.20b ran this leaf on this seat. Source identity of that interpreter remains the pinned tar, not this seat's binary hash.
- The header comment says the generator writes EXACT_CUT_SPEC.txt. The pasted generator does not write that file. bas_mirror.py is named in a remark and was not in the paste.
- cut8 was not touched. cut8 rounds at 10 places and then cuts to 8. This leaf does not round. Different rule.
- Original line 1400 always prefixes "-" when NG%=1. On a zero result that is "-0". The runnable file returns 0. One added line. Case 21 locks it.

## BASIC band, kept as a shutoff, not a bug

Denominator 1 through 100000000000000. Significant digits 1 through 40. Numerator is a digit string, length 1 through 254. Walk budget 70 steps. Outside that, UNKNOWN.

10^14 is inside the exact integer range of binary64 for this long division: the widest intermediate is 10^15 - 1, and that is below 2^53. 10^20 is not in the band. Python still cuts it. BASIC returns UNKNOWN. Both are right.

## Original generator, kept so the D+00 form stays visible

The pasted gen_bas.py body is not repeated here in full. Its DATA shape was:

    DATA "<numerator>",<denom>D+00,<sig>,<sign>,"<expected>"

That shape is the archived one. Do not put it back on the runnable file.

## Drive burst 2026-10-17 18:30 EDT

Read from Drive. Originals left where they were. Not moved. Not deleted.

Kept: `exact_text.cpp` only. SHA-256 ebbdd3486905358b1b3a199a4db6a33963b06ee2e87f3fd08b1d9dc49163b738, 1761 bytes. Integer port of the cut. Contract remains `exact_text.py`. If the two ever disagree, the Python leaf is right and the C++ is wrong.

Checked this seat, g++ -std=c++17, 11 lines in main, all matched `frac_trunc_sig`:

- 980665/(100000*299792458^2) at 12 digits, and the same ratio times 10, 100, and 1000
- 1999999/1000000 at 3 digits, both signs: 1.99 and -1.99
- 1/3 at 12: 0.333333333333
- 2/3 at 4: 0.6666
- 0 at 5: 0
- 1/10^20 at 4: 0.00000000000000000001000
- 156525121/1210320000 at 12: 0.129325402372

The Drive `exact_text.py` (a962da585920c71eb471b60ef31e6de7a5218f9a9b665015b29b1aa0d2d36503) matched the sealed leaf on 819 Fraction cases, including those 11. It is not the leaf. `Fraction(1.999999)` is accepted there and returns "1.99". The sealed leaf refuses a float. That file was not copied in.

### Not adopted

- `svct_conformance.py` (4c53db58..., 27/27 on its own tests, head 3bb0bb3c93c26b6b4d5bdacc8afdd15cf9ac19334c7fc3bba7cc6eb80dad2194). Same chain as this morning. Nested `data` is still shared. Mutating `data["v"]` on a read copy wrote "evil" into the live record and verify went false. Its own copy test still only replaces top-level content.
- Geometry in that file. spokes^2 and 360^2 = 129600 already held. Reserved-cell contents still C2.
- `udn_demo.py` (20e2819f..., 16/16). The file says proposal, not a sealed spec. Two closed forms checked out as arithmetic: df/f = g*dh/c^2 with g = 980665/100000 and c = 299792458, and lambda = mH^2/(2 v^2) with the supplied mH = 12511/100 and v = 246, ratio 156525121/1210320000. Those inputs were supplied, not measured here. The name UDN was not assigned a job.
- `ev2_ratio_check.py`. Not EV2. No energy formula. Adding float 0.1, 100000 times: Fraction and Decimal('0.1') reach 10000/1; float64 prints 10000.000000018848; 99995 of 100000 steps differ; final signed error about 1.8848368199542165e-8. Directional ratio left as 100000/10. The checkpoint is ROUND_DOWN to 1e-7, not a significant-digit cut. The same quantize on 1.999999 returns 1.9999990, not 1.99.
- `ev2_ratio_check_v2.py` (20/20 on its own tests). Same accumulation, directional ratio now reduced, and its Decimal cut matched its own cases. Still not EV2. Not a second cut rule.
- `claims_check.py`. Prints FAILS=0. Fourteen of those lines compare a value. W4b and H5 through H9 and the four redshift lines set the flag true and do not compare. Exact lines that did compare: interference 4, 2, 0, 16/5; density 1, 1/16, 1/81, 1/256, 1/10000; lambda 156525121/1210320000. H2, H3, and H4 are tolerance or rounded-float checks. The Planck length printed from G, hbar, and c is not the sealed L_p = c*t_p.
- `SVCT_gel_v14_draft.xlsx` (13328 bytes, SHA-256 4ccdd674716e974d28e6771eeb94edb7dea3abaee2bd9b43a58b610f9070c7ec). Formula grid, cached values empty. s = 4, so 64 cells means 4^3, not spokes^2. Index complement is the spatial antipode on that grid (64/64). No coordinate is zero. Cap marks one face, 16 cells, not 8 reserved. Angles are Excel ATAN2 cut with TRUNC to 8 decimal degrees. Boot cell is labeled SYNTHETIC. delta_ms is empty.
- `text 41.txt`. Roles, part names, and prices for Pi 5, Jetson, and the A15. Speeds are labeled estimates. Nothing was timed here. Not a purchase.
- `svct_audit_2026-10-17.zip`. Two Drive copies, same bytes, SHA-256 65afee429454ddc445e350f6fa9b2e1f3684d1ac978b367eb2afcc43a8561308. Holds FINDINGS.md and audit.py. The scanner keeps files by name keywords. That is filename identity, so the scanner was not adopted. The boundary arithmetic was run here, on an empty directory, output outside it: pass, and the old 1e-30 floor rejects L_p. t_p = 539/10^46, L_p = 80794067431/5000000000000000000000000000000000000000000000. This does not re-seal MinRadius. The 2026-08-28 seal already states it. The audit's claim that GitHub was inaccessible was their seat, not this one.
- `MinRadius_L_p_seal_2026-08-28_AUDIT_COPY_2026-10-17.md`. A copy of the existing seal. Not a new seal. The counts 9/9, 39/39, 75/75, 87/87, 48/48 were not rerun.
- `SHA256SUMS.txt`. Matches the four files that were both listed and uploaded: exact_text.cpp, exact_text.py, svct_conformance.py, udn_demo.py. Lists cpp.out, py.out, and mutate_udn.py, which are not on Drive. mutate.py on Drive is older (2026-10-01 and 2026-09-28), not this burst. The sums file does not cover the ev2 files, claims_check.py, text 41.txt, the xlsx, or the zip.

