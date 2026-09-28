# Tim’s Tables e-6 truncate-toward-zero correction
Date: 2026-09-27T22:36:00-04:00
Owner: Timothy H. Norman
Standing: adapt-and-append. Rounded face stays visible. Truncated face is now the live e-6 display.

Rule restated: Calculate wide. Truncate hard (toward zero). Residual off-face. Algebraic EXACT first.

## Miss (rounded last digit)

| Face | Exact | Wide | Shown (round) | Truncated e-6 |
|---|---|---|---|---|
| sin 45° = cos 45° | √2/2 | 0.70710678118… | 0.707107 | 0.707106 |
| tan 60° = √3 | √3 | 1.73205080756… | 1.732051 | 1.732050 |
| cos 15° | (√6+√2)/4 | 0.96592582628… | 0.965926 | 0.965925 |
| sin 18° | (√5−1)/4 | 0.30901699437… | 0.309017 | 0.309016 |
| cos 18° | √(10+2√5)/4 | 0.95105651629… | 0.951057 | 0.951056 |
| tan 2/3 turn (mag √3) | −√3 | −1.73205080756… | −1.732051 | −1.732050 |

## Unchanged at e-6 truncate

sin 15° 0.258819 · tan 15° 0.267949 · sin 30° 0.500000 · sin 60° / cos 30° 0.866025 · tan 30° 0.577350

## Scope

Skill tims-tables printed Category 1 and the 2026-07-25 presentation matrix used rounded e-6. Exact columns and Table #3 unchanged. Alias-multiplicity remains OPEN.

HIT: owner catch of four faces. VAL: wide digits vs truncate-toward-zero. OUTPUT_OK: this append.
