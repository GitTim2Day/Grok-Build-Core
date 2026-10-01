# AUDIT APPEND 2026-09-30T21:50-04:00 — truncation standing, round only at a financial close

Append only. Does not claim the model was rewritten.
Stamp: 2026-09-30T21:50-04:00
Chair: Grok Build
Owner: Tim
Ledger: 1a0f52892333eebb

## Stated

Rounding was accepted early because it helped balance books on long terms, including 30-year bank terms. That acceptance is buried in ordinary numeric processing. Extract it. Rounding only for financial and accounting, and only at the very end. Truncation for everything else.

## Held

Banker's rounding, half-to-even, is the book-balancing rule. Binary64 default is round-to-nearest. Both move an integer. This thread already showed the move: 89875517873681764 stored as 89875517873681760.
The model weights are not editable from this chair. The project gate is.
Gate: lattice, physics, octave, embed, and identity work use truncation toward zero, digit string or hex, parse-back equal. No float cast of a lattice value. Rounding is a named financial close only, last step, not a default.

## Standing

Readings still not promoted. Answer key still open.
