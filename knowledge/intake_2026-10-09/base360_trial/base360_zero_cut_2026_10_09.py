"""Additive leaf, 2026-10-09. base360.py is not edited.

Tim's rule: -0 and 0 both become 0. base360.format_digits keeps the sign of
the source even when every shown digit is zero, so a small negative value cut
to few digits prints "-0.000". This display drops the sign only in that case.
The encode record is untouched: it still carries sign, source ratio and the
exact absolute error, so nothing is lost.
"""
from base360 import format_digits


def format_digits_no_negative_zero(record):
    shown_zero = record['whole'] == 0 and all(d == 0 for d in record['digits'])
    if shown_zero and record['sign'] < 0:
        record = dict(record, sign=1)
    return format_digits(record)
