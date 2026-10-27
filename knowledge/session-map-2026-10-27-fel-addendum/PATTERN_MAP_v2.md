# PATTERN_MAP v2 — FEL + UNDEFINED addendum (2026-10-27)
Parent: session-map-2026-10-27-exact-ratio v2 6642fef8200fe1cb8ac9e100c4f1b5cec0747a820320f4dbd053f466fc9b6c14
P1 UNDEFINED, not zero: never denominate a zero; no zero, no infinity (zero only for base ten / possibly binary).
P2 Two filters: KBLD9 and Fixed Exponential Limits (FEL).
P3 FEL: compute e+9 .. e-45; stop past e+9; de-concatenate 1 digit for presentation (e+8 .. e-44). Truncate, never round.
P4 Evidence: v2-undefined SHA256SUMS 4ec2eacfe15c1432b721a1a81cea241e52547f89eb02ff0ba9051528eb5fed71 (-c 66/66 OK); v3-ceiling SHA256SUMS 2ece05f7ff5546a470fde6e2656211d63a0a4370ad1ddc0f3ceed07780f69937 (-c 64/64 OK); engines identical.
P5 Open: no CPU saving measured from the e+9 stop; demo files not updated; interpretation choices pending Timothy.
