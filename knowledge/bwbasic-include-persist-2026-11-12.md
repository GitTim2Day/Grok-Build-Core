# bwbasic-include-persist-2026-11-12 (hardened 2026-11-12)

Sitting: 2026-11-12

Locked: include BW BASIC so basic/brain_control.bas runs under the interpreter.

## Locomotion placeholder
Separate node / GOSUB for locomotion. Default ABSENT until drivetrain reported able. Branches to drone, hive member, hive, robot, humanoid, or none. Brain stays useful with only eyes/ears/voice.

## Verify on Shepherd (he handles)
which bwbasic
echo 'PRINT 0.70710678' | bwbasic   # exit 0, output matches
bwbasic basic/brain_control.bas     # GOSUB order runs, returns to ALERT

Persist. Archive misses. Pi 5 stays light.

Ledger prior: 1a1d0788c62a9dc5
Unified seal: 1a1d0aa58638d76a
