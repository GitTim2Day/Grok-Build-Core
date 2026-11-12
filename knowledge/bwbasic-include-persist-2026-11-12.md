# bwbasic-include-persist-2026-11-12 (hardened + truncation 2026-11-12)

Locked: include BW BASIC. Truncate, do not round.

Observation: default PRINT rounds to ~6 significant digits. Required: truncate toward zero (0.70710678 → 0.707106).

Force:
OPTION ROUND TRUNCATE
(in profile.bas or at top of program)
Or explicit truncate before PRINT.

## Locomotion placeholder
Separate GOSUB, default ABSENT until drivetrain able. Branches to any device or none. Brain useful with eyes/ears/voice only.

## Verify on Shepherd
which bwbasic
echo 'OPTION ROUND TRUNCATE : PRINT 0.70710678' | bwbasic
# expect truncated 0.707106, exit 0
bwbasic basic/brain_control.bas

Persist. Archive misses.
