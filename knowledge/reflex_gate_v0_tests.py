#!/usr/bin/env python3
"""Reflex gate answer-key tests. Integer only. TRUNC toward zero.
Decisions 2026-09-28 locked. Not hardware. Not GEL_RECOVER.
"""
from __future__ import annotations


def trunc0_div(m: int, acc: int) -> int:
    if acc <= 0:
        raise ValueError("ACC must be > 0")
    if m < 0 or acc < 0:
        raise ValueError("no negative operands in STEPS")
    return m // acc


def check_life(m, acc, mn, mx, recov, age, dsoft, dhard, prev, sdelta, crc_ok, ts_future):
    V, R, S, F = 2, 0, 0, 8
    A = 1
    if not crc_ok:
        return 2, 6, 8, 0, 1
    if ts_future:
        return 2, 8, 8, 0, 1
    if m == 0:
        return 2, 1, 8, 0, 1
    if m < acc:
        return 2, 2, 8, 0, 1
    if age > dhard:
        return 2, 4, 8, 0, 1
    if m < mn or m > mx:
        return 2, 3, 8, 0, 1
    F = 8
    if abs(m - prev) > sdelta:
        F |= 1
    S = trunc0_div(m, acc) - 1
    if age > dhard:
        return 2, 5, 8, 0, 1
    if age > dsoft:
        F |= 2
    return 1, 0, F, S, 0


def check_nonlife_budget(left, cost):
    if left < cost:
        return 3, 7, 0, 0, 0
    return None


def check_age(age, dsoft, dhard, life):
    fl = 8 if life else 0
    if age > dhard:
        return 2, 4, fl
    if age > dsoft:
        return 1, 0, fl | 2
    return 1, 0, fl


def arm_on_contact(contact):
    if contact == 2:
        return 1
    return 2


def run():
    ACC, MIN, MAX = 5, 20, 800
    SDELTA = 50
    DSOFT, DHARD_LIFE, DHARD_NON = 9000, 14000, 50000
    PREV = 100
    fails = []
    cases = []

    def add(name, got, exp):
        cases.append((name, got, exp))

    add("A1", check_life(100, ACC, MIN, MAX, 0, 2000, DSOFT, DHARD_LIFE, PREV, SDELTA, True, False), (1, 0, 8, 19, 0))
    add("A2", check_life(103, ACC, MIN, MAX, 0, 2000, DSOFT, DHARD_LIFE, PREV, SDELTA, True, False), (1, 0, 8, 19, 0))
    add("A3", check_life(0, ACC, MIN, MAX, 0, 2000, DSOFT, DHARD_LIFE, PREV, SDELTA, True, False), (2, 1, 8, 0, 1))
    add("A4", check_life(4, ACC, MIN, MAX, 0, 2000, DSOFT, DHARD_LIFE, PREV, SDELTA, True, False), (2, 2, 8, 0, 1))
    add("A5", check_life(900, ACC, MIN, MAX, 0, 2000, DSOFT, DHARD_LIFE, PREV, SDELTA, True, False), (2, 3, 8, 0, 1))
    add("A6", check_life(100, ACC, MIN, MAX, 0, 14500, DSOFT, DHARD_LIFE, PREV, SDELTA, True, False), (2, 4, 8, 0, 1))
    add("A8", check_life(100, ACC, MIN, MAX, 0, 9050, DSOFT, DHARD_LIFE, PREV, SDELTA, True, False), (1, 0, 10, 19, 0))
    add("A9", check_life(100, ACC, MIN, MAX, 0, 14000, DSOFT, DHARD_LIFE, PREV, SDELTA, True, False), (1, 0, 10, 19, 0))
    add("A10", check_life(160, ACC, MIN, MAX, 0, 2000, DSOFT, DHARD_LIFE, 100, SDELTA, True, False), (1, 0, 9, 31, 0))
    add("A11", check_life(100, ACC, MIN, MAX, 0, 2000, DSOFT, DHARD_LIFE, PREV, SDELTA, False, False), (2, 6, 8, 0, 1))
    add("A12", check_life(100, ACC, MIN, MAX, 0, 2000, DSOFT, DHARD_LIFE, PREV, SDELTA, True, True), (2, 8, 8, 0, 1))
    add("A13", check_nonlife_budget(300, 400), (3, 7, 0, 0, 0))
    add("Q1-nonlife-hard-room", check_nonlife_budget(20000, 400), None)
    add("Q1-life-eq-hard", check_age(14000, DSOFT, DHARD_LIFE, True), (1, 0, 10))
    add("Q1-life-over-hard", check_age(14001, DSOFT, DHARD_LIFE, True), (2, 4, 8))
    add("Q1-life-soft-band", check_age(9001, DSOFT, DHARD_LIFE, True), (1, 0, 10))
    add("Q1-life-under-soft", check_age(9000, DSOFT, DHARD_LIFE, True), (1, 0, 8))
    add("Q1-non-eq-hard", check_age(50000, DSOFT, DHARD_NON, False), (1, 0, 2))
    add("Q1-non-over-hard", check_age(50001, DSOFT, DHARD_NON, False), (2, 4, 0))
    add("Q1-non-soft-band", check_age(9001, DSOFT, DHARD_NON, False), (1, 0, 2))
    add("Q5-life", arm_on_contact(1), 2)
    add("Q5-not-life", arm_on_contact(2), 1)
    add("Q5-unknown-is-life", arm_on_contact(0), 2)

    ok = 0
    for name, got, exp in cases:
        if got != exp:
            fails.append((name, got, exp))
        else:
            ok += 1
    print("PASS", ok, "of", len(cases))
    for name, got, exp in fails:
        print("FAIL", name, "got", got, "exp", exp)
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(run())
