SESSION_PATTERN_MAP_2026-11-19_DIGIT_BY_DIGIT_STRING_BUILD
Stamp: 2026-11-19T09:38-05:00 America/New_York
Status: SEALED

HIT
Digit-by-digit left-to-right string construction is the standing truncation method.
Source text is read one character at a time.
Sign (if present) is kept first.
Digits after the decimal are appended one by one until the named place count is reached, then growth stops.
The finished string is never converted back to a number.
No float64 intermediate.
Python and C++ adapters produce identical results from the same source text.
Places is the parameter. Current test contract is six places.

VAL
Matches the sealed truncate-toward-zero contract (2026-11-12).
Supersedes any intermediate float capture.
Compatible with direction-only arithmetic (sign is direction).
BW BASIC remains the emitter; the adapter or a later pure-BASIC string loop performs the cut.

MISS
None on the method.

OPEN
Wire the method into the existing Python and C++ adapters when next named.
Pure-BASIC string loop only if later directed.

Sibling of session-map-2026-11-12-truncate-toward-zero and session-map-2026-11-12-svct-string-token. Not a merge.
Pointer only. Body is this map.
