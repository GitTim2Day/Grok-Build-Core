"""Added 2026-10-09: stop-rule and zero tests for base360.py (original not edited).

Why: a mutant that changed the accuracy test from > to >= passed all 11
original tests. These tests pin each way the converter is allowed to stop:
exact remainder, declared accuracy (earliest digit, equality counts as met),
and digit budget (unmet stated explicitly).
"""
from fractions import Fraction as F
import unittest

from base360 import encode, decode
from base360_zero_cut_2026_10_09 import format_digits_no_negative_zero


def errors_by_digit(value, upto, base=360):
    """Exact error after 0..upto digits, by plain long division (independent)."""
    n, d = abs(value.numerator), value.denominator
    r = n % d
    out, scale = [F(r, d)], 1
    for _ in range(upto):
        r = (r * base) % d
        scale *= base
        out.append(F(r, d * scale))
    return out


class StopTests(unittest.TestCase):

    def test_equal_accuracy_stops_at_that_digit(self):
        v = F(1, 7)
        e2 = F(*encode(v, digits=2)['absolute_error'])
        r = encode(v, accuracy=e2)
        self.assertEqual(len(r['digits']), 2)
        self.assertIs(r['accuracy_met'], True)

    def test_just_below_equal_needs_one_more_digit(self):
        v = F(1, 7)
        e2 = F(*encode(v, digits=2)['absolute_error'])
        r = encode(v, accuracy=e2 - F(1, 10**30))
        self.assertEqual(len(r['digits']), 3)
        self.assertIs(r['accuracy_met'], True)

    def test_earliest_stop_sweep(self):
        # For every ratio and every k, accuracy = exact error after k digits.
        # The converter must stop at the first digit whose error <= accuracy.
        checked = 0
        for p in range(-30, 31):
            for q in range(1, 160):
                v = F(p, q)
                errs = errors_by_digit(v, 6)
                for k in range(1, 7):
                    acc = errs[k]
                    if acc == 0:
                        continue
                    want = next(i for i, e in enumerate(errs) if e <= acc)
                    r = encode(v, digits=12, accuracy=acc)
                    self.assertEqual(len(r['digits']), want, (v, k))
                    self.assertIs(r['accuracy_met'], True)
                    self.assertEqual(F(*r['absolute_error']), errs[want])
                    checked += 1
        self.assertEqual(checked, 41934)  # deterministic sweep size

    def test_budget_stop_is_explicit(self):
        r = encode(F(1, 7), digits=2, accuracy=F(1, 10**12))
        self.assertEqual(len(r['digits']), 2)
        self.assertIs(r['accuracy_met'], False)
        self.assertFalse(r['exact'])

    def test_exact_remainder_stops_without_accuracy(self):
        r = encode(F(1, 8), digits=50)
        self.assertEqual(r['digits'], [45])
        self.assertTrue(r['exact'])
        self.assertIsNone(r['accuracy_met'])

    def test_zero_budget_never_loops(self):
        r = encode(F(1, 7), digits=0)
        self.assertEqual(r['digits'], [])
        self.assertEqual(F(*r['absolute_error']), F(1, 7))


class ZeroTests(unittest.TestCase):

    def test_small_negative_cut_shows_plain_zero(self):
        for v, n in [(F(-1, 10**9), 1), (F(-1, 10**9), 2), (F(-1, 720), 1)]:
            text = format_digits_no_negative_zero(encode(v, digits=n))
            self.assertFalse(text.startswith('-'), (v, n, text))
            self.assertEqual(set(text.replace('.', '').replace(':', '')), {'0'})

    def test_record_still_keeps_sign_and_error(self):
        r = encode(F(-1, 720), digits=1)
        self.assertEqual(r['sign'], -1)
        self.assertEqual(F(*r['absolute_error']), F(1, 720))
        self.assertEqual(decode(r), 0)

    def test_nonzero_negative_keeps_sign(self):
        self.assertEqual(format_digits_no_negative_zero(encode(F(-1, 2))), '-0.180')
        self.assertEqual(format_digits_no_negative_zero(encode(F(-3, 2))), '-1.180')

    def test_zero_is_zero(self):
        self.assertEqual(format_digits_no_negative_zero(encode(F(0), digits=3)), '0')


if __name__ == '__main__':
    unittest.main()
