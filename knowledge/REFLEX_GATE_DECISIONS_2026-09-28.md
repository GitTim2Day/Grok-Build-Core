# REFLEX GATE — decisions 2026-09-28
Predecessor: REFLEX_GATE_SPEC_v0.md (PROPOSAL).
Status: DECISIONS LOCKED. Spec v1 may be written from these. No MCU flash. Tests only until Pico 2 is on the bench after 2026-10-01.

Author: Timothy "Rex" Norman. This chair recorded; did not invent.

## Answers

| Q | Decision |
|---|---|
| Q1 | 14 ms hard on life channels. 50 ms hard elsewhere. 9 ms remains the target / soft flag. |
| Q2 | PASS + F_STEP. Real reading, flagged. Never refuse a real danger. |
| Q3 | Never. Life channel is real reading only. GEL_RECOVER stays off on LIFE=1. |
| Q4 | This core first, recovery off. Gel-stack after. |
| Q5 | Hold limited torque. Compliant / back-drivable if contact is life. |
| Q6 | No auto-clear. Resume only when state >= safe AND report submitted AND adjudicated. |
| Q7 | Not yet. Pico 2 purchase after 2026-10-01. Build tests only until then. |
| DSAMP | Defaults stand. Build tests only. |

## Profile numbers from Q1

- DSOFT_US = 9000 on all channels (target / F_SOFT).
- DHARD_US = 14000 when LIFE = 1.
- DHARD_US = 50000 when LIFE = 0.
- Validator: 0 < DSOFT_US <= DHARD_US; life DHARD_US <= 14000; non-life DHARD_US <= 50000.

Hard-limit pin (answer key):
- age > DHARD → REFUSE. Late never passes. Life: > 14000. Non-life: > 50000.
- age == DHARD → still under the "greater than" test → PASS if the rest earned; F_SOFT set because age > DSOFT.
- DSOFT < age <= DHARD → PASS + F_SOFT.
- age <= DSOFT → PASS, no F_SOFT (other flags may still set).

## Safe-state (Q5 + Q6)

PLATFORM 2 (arm / hand): hold limited torque. If contact is life, go compliant / back-drivable. Not a blanket release. Not a pin.

Contact class (Q5 pin, fail-closed):
- CONTACT 1 = life → COMPLIANT
- CONTACT 2 = not-life → HOLD_LIMITED
- CONTACT 0 = unknown → treat as life → COMPLIANT
Cannot-tell is not a third safe pose. It is life until classified.

Clearing SAFE_STATE: forbidden on a single PASS. Requires state >= safe AND report submitted AND adjudicated.

## Recovery

GOSUB 7000 remains refuse until the gel-stack spec is approved. LIFE + RECOV = 1 is still unpublished.
