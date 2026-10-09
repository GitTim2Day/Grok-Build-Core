# Base 360 exact-ratio trial

Integer/Fraction arithmetic only. No binary floats, banker rounding or
conversion through rounded floating-point results. Python 3.10+, standard library.

A fractional digit has 360 possible values, 0 through 359. The displayed
three-character tokens are decimal labels for those digit values, separated
by colons; they are not three independent base-10 fractional digits.
The whole part is retained as an integer independent of positional display.

| Ratio | Base-360 fractional representation | Exact? |
|---|---|---|
| 1/2 | 0.180 | Yes |
| 1/3 | 0.120 | Yes |
| 1/4 | 0.090 | Yes |
| 1/5 | 0.072 | Yes |
| 1/8 | 0.045 | Yes |
| 1/9 | 0.040 | Yes |
| 1/12 | 0.030 | Yes |
| 1/7 | 0.051:154:102:308:205:257... | Repeating |

360 = 2^3 * 3^2 * 5. A reduced rational has a terminating base-360
representation exactly when its denominator contains only factors 2, 3 and 5.
This covers many common subdivisions; factors such as 7 or 11 still repeat.
The retained original integer ratio remains exact regardless of display base.

The converter uses long division on integers and stops when the remainder is
zero, the declared absolute accuracy criterion is met, or the digit budget is
exhausted. An unmet criterion is explicit. With no criterion, accuracy_met is
null; finite output is never described as satisfying an unspecified accuracy.
The stopping rule demonstrates the declared-accuracy principle, not a full
EV2 physics implementation or a substitute for device measurement uncertainty.

For 1/7 at tolerance 1/1,000,000, three base-360 fractional digits suffice:
0.051:154:102. The exact absolute representation error is 1/54,432,000.
Two digits fail that criterion. The converter stops at three, with no further
iteration. Arithmetic remains integer ratios throughout.

The extra-digit/string test generates one additional base-360 digit and removes
one complete digit token. Removing one decimal character from a token such as
154 would corrupt the digit; the routine removes the entire token. The resulting
stored measurement string can be parsed back to an exact integer ratio. Its
difference from the original ratio remains recorded, rather than declared zero.

11/11 tests passed, including 20,500 signed-ratio trials (numerators -20 through
20; denominators 1 through 501 exclusive) for error identity/bounds, exact finite
recovery, repeating fractions, sign symmetry, earliest accuracy stop, digit-token
removal and parameter rejection. The report also compares minimum terminating
digit counts in bases 2, 10, 12, 100 and 360 for eighteen representative fractions.

Run:

```sh
python3 -m unittest discover -s . -v
python3 examples.py
```

Files: base360.py (codec), test_base360.py (tests), examples.py (report generator),
report.json (exact results), test_results.txt (execution evidence).
