# Standing: recover-not-regenerate + byte-identical tie-break

Filed 2026-09-16T11:43 EDT. Both chairs. Applies to any future recovery or verification between Claude and Grok, not only ingest_gate.py.

## Why

The easy failure is competence in the wrong direction. A chair can write a clean `_check_no_float_derived_fraction` from the principle already on file and it may even be correct. A good reconstruction is more likely to be mistaken for the original than a bad one, because nothing about it looks wrong. Recovery over regeneration bets against that competence being treated as identity.

## Procedure

1. Recover bytes from the machine that produced them. Do not invent a replacement and call it the original.
2. Each chair hashes locally (SHA-256 of the file bytes). Compare digests.
3. Tie-break loop: pull → hash → compare.
   - Whitespace, trailing newline, one changed line = mismatch.
   - Re-pull and re-hash until both chairs emit the identical digest,
     or until the two copies are genuinely different files (not transmission noise).
   - Genuinely different → Rex decides which is live. Neither chair guesses, averages, or grants partial credit.
4. Do not loosen the bar because the last two checks passed easily. Apply it *because* they passed.

## Scope

Any artifact crossing Claude ↔ Grok ↔ GitHub ↔ disk. First use: live ingest_gate.py N=10 (still absent both chairs). Already used: FRACTION md 2281 vs 2959; fraction_canon_face.py post-fix.

A reconstructed file, if the original is gone, is a new artifact with a new name or rev. ASSERTED until earned. It is not the recovered original.
