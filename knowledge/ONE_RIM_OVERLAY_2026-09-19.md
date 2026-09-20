# ONE_RIM_OVERLAY — 2026-09-19

Standing: HIT owner text + VAL mapping. ASSERTED DERIVED. Not Full Reference (still ABSENT). Sibling of Base-360 DERIVED SAVE 2026-09-19. Do not merge. Do not promote.

Owner: Timothy H. Norman
Stamp: 2026-09-19T23:39:00-04:00
Trigger: “Very good, now save that to the project.”
Source sitting: one-rim / many-bases overlay statement + chair confirmation.

## Owner text (HIT — do not paraphrase away)

You can put every base on the same circle. The base is how many equal spokes you draw. The start mark is the start mark. A finished turn is labeled with the base, then (2×) base, (3×) base, and so on. You never have to write “from (0) to (B).” You write start (→ B → 2B → ⋯).

Hands (the old hardware).
Ten fingers (→) base (10). Twelve finger-bones on four fingers of one hand, thumb as pointer (→) base (12). Egypt ran a decimal administration and a 12 / 24 / 360 time-and-circle stack like the rest of the ancient Near East. That is enough to say the picture is old, not a gimmick. Monument stone is a separate engineering story; the counting bones are the part that maps cleanly.

Binary on that same circle.
Base (2) has two spokes. One turn (→) two hemispheres. That is the whole refinement of one digit: left / right, off / on. Good for codes, gates, and cheap storage. Bad for a rim you wanted to navigate. To get nuance back you do not invent a new infinity. You stack turns of two, which is the same thing as more bits:

[ 2, 4, 8, 16, …, 2^n ]

Those are more spokes. They are still only powers of two. A (360^n) rim and a (2^n) rim can sit on the same disk. Where a tick exists on both, you can convert. Where a (360^n) tick falls between two binary ticks, binary has to snap, and that is the nuance you lose.

Overlay.
On one circle you can mark:
- base (2) hemispheres
- base (10) decades
- base (12) hours
- base (360) degrees
- finer (360^2, 360^3)
- fractions in ((0,1]) of a turn (start is the excluded (0); a full turn is (1) or (B))
- sine / cosine / tangent as heights and slopes read off the same radii — not as a second universe

Sine of a tick is then “opposite over hypotenuse at that spoke,” and if the spoke is a (360^n) fraction you already own, the angle is exact in your domain. The length of a chord may still need a finer tick if you refuse (√) as a primitive. That is resolution, not a fight.

Refinement gap, stated as a ratio of ticks per turn.

ticks(360^n) / ticks(2^m) = 360^n / 2^m = (2^3 · 3^2 · 5)^n / 2^m

Base (360) already contains (2), (3), and (5). Binary contains only (2). For the same “budget” of marks, (360^n) hits thirds and fifths that (2^m) can only approximate. That is the weakness: not that binary cannot compute, but that its circle is coarse in every prime but (2).

Use with current machines.
Keep binary as the transport (bits, hex, tokens). Keep (360^n) fractions as the quantity. Convert at the edge: tick index (→) bit pattern for storage; bit pattern (→) fraction before you add. Add in the fraction / circular base. Do not let the two-hemisphere snap become the arithmetic.

That is the whole overlay: one rim, many bases, start (≠) “nothing,” full cycle (=) the base, binary for codes, (360^n) for measured nuance.

## Chair confirmation (VAL — mapping only)

- Start is a mark. Start ≠ stored zero. Finished turn = the base.
- Aligns with locked refusal of k=0 on the Base-360 derived face and “no true zero stored as value.”
- Hands map: 10 fingers → base 10; 12 phalanges + thumb pointer → base 12. Egypt decimal admin beside 12/24/360 circle = same overlay, old.
- Monument stone remains a separate engineering file.
- Binary on the rim = two hemispheres. Stacked 2^m = more spokes of one prime. Snap when a 360^n tick falls between binary ticks = resolution, not a new infinity.
- Tick-ratio algebra:

  360^n / 2^m = (2^3 · 3^2 · 5)^n / 2^m = 2^(3n−m) · 3^(2n) · 5^n

- GOSUB_RATIO_CLASS_A remains two-sided on {2,3,5}.
- Constant cells-per-shell stays. Radius is a weight, not r² cell growth.
- Trig read off the same radii. Angle exact in-domain when the spoke is an owned 360^n fraction. Chord that refuses √ as primitive → finer tick / pole cell.
- Machine rule unchanged: bits/hex/tokens = transport; 360^n or reduced {2,3,5}-smooth fraction = quantity. Convert at the edge. Add on the circular face.
- Fraction-airlock still applies: do not build a tagged FRACTION from an already-rounded float (FLOAT_DERIVED_FRACTION).
- Last Ledger Base-360 row is ASSERTED DERIVED. Full Reference remains ABSENT. This overlay does not fill that hole.

## Status flags

HIT: owner overlay text
VAL: algebra + mapping to sealed faces
OUTPUT_OK: this file
PROMOTION: refused (not Full Reference)
SIBLING: Base360 DERIVED SAVE 2026-09-19 — not a merge

## Next rung (not executed)

Discrete overlay table: ticks that exist on both rims vs ticks that must snap. Requires explicit GOSUB_TO_NEXT.
