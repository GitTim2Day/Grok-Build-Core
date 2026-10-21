# Cube turn
Owner: Tim
Stamp: 2026-10-20T20:45-04:00
Kind: brief distraction. Not a boot row. Not a runtime on Shepherd.

## Process
1. The pasted class was run unchanged.
2. Color checks passed, including each face four times and the sexy move six times.
3. Unique sticker ids were then used. F failed. Four F turns reversed each adjacent edge. Same-color edges had hidden it.
4. The other five faces passed unique ids. They were not rewritten.
5. F now copies the four edges, then writes them. A 2 is two turns even when a prime is also present. A bad token stops the sequence.
6. The same IF is in the BASIC file. bwbasic was not on this seat. That file was not run.

## Subroutines
- gosub_parse: IF empty OR the face is outside UDFBLR OR the tail is not empty, prime, 2, or 2-prime, THEN miss. IF the token has 2 THEN two turns. ELSE IF it has a prime THEN three. ELSE one.
- gosub_turn: the face, that many times.
- gosub_inverse: a half turn stays a half turn. A prime becomes one quarter. One quarter becomes a prime.

## Results
- Before the fix: R2 then R2-prime left the cube unsolved. F then F-prime failed on unique ids.
- After the fix: each face, four times and inverse, passed on unique ids. 200 random sequences of 20 turns, then the inverse, passed. Seed 20. Color counts stayed 9. Centers stayed put. A bad token does not move a sticker. R X U stops after R.
- This is the model agreeing with itself. No physical cube was turned.

## Files
- cube_turn.py SHA-256 d0d28a8ca9274dbb42e6d4a8e7e7027b72e2421ecc4f85879616920283a4f8db size 3876
- cube_turn.bas SHA-256 5684988baec62668abaf555401a3078a34981d4b310e6ebab7ade24809695ccc size 785 not executed
