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
