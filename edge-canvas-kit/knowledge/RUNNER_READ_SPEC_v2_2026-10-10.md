# RUNNER_READ spec v2 (2026-10-10, supersedes the thread reader in lib/runner.py)

Author: Timothy (sole author). Claude = tool/validator.
Defect D1 (demonstrated 2026-10-10): a child that hands its stdout to a process outside
the run's group leaves the reader thread blocked forever. Result: one leaked thread per
run, a 5 s stall, and the child's own output lost (`out=''`).

## Trigger rule (Tim, 2026-10-10)
Work on DETECTION OF NEED first; WHEN ASKED second; a timer only where neither exists.
Here need = the kernel saying "pipe readable", "stdin writable" or "child exited".
No thread. No sleep loop.

## Signals (POSIX)
- stdout pipe readable (selectors).
- stdin pipe writable, only while stdin text remains (selectors).
- child exit: pidfd readable (Linux 5.3+, Python 3.9+). FALLBACK when pidfd is not
  available: wake every SLICE = 50 ms and ask the child (p.poll). Fallback only.

## Loop (one GOSUB, one entry, one exit)
```
DEADLINE = t0 + timeout
DO
  WAIT for any signal UNTIL DEADLINE (or SLICE in fallback)
  FOR each signal
    IF stdout readable THEN GOSUB READ_CHUNK      ' EOF -> OUT_DONE; over cap -> CAPPED, KILL, stop
    IF stdin writable  THEN GOSUB WRITE_CHUNK     ' all sent or broken pipe -> close stdin
    IF child exited    THEN CHILD_DONE = 1
  NEXT
  IF NOT CHILD_DONE AND fallback THEN IF p.poll() is not None THEN CHILD_DONE = 1
  IF CAPPED THEN STOP
  IF CHILD_DONE THEN GOSUB DRAIN: STOP           ' read what is waiting now, never wait for EOF
  IF now >= DEADLINE THEN TIMED_OUT = 1: KILL: GOSUB DRAIN: STOP
LOOP
CLEAR: close stdout, stdin, pidfd, selector (every exit path)
```
- DRAIN reads without blocking until "nothing waiting" or EOF or cap. If EOF was not
  reached, HELD = 1 and the output gets the note
  `[runner] output pipe still held by a process outside the run; stopped reading`.
- Child exit with OUT_DONE false is normal for a held pipe; it is not waited on.
- After KILL: wait for the child at most 5 s (as before).
- Return keys unchanged: rc, out, timed_out, capped, secs; one new key: held (bool).

## Windows
Pipes cannot be waited on there; the thread reader stays, but after its bounded join an
alive thread is no longer silent: HELD = 1 and the same note is added.

## Tests (runner_leak_test.py)
T1 escaped grandchild: returns in < 1.5 s, own output kept, threads and fds flat, held.
T2 normal output exact. T3 timeout. T4 output cap. T5 stdin round trip (60,000 bytes).
T6 no deadlock when the child writes 200 KB before reading 60 KB of stdin.
T7 rc passed through with no output. T8 late output (0.5 s) captured.
T9 child closes stdout early and keeps running -> timed out.
T10 30 runs in one process: thread count and open fd count unchanged.
T11 every pipe object closed explicitly on return, not left to garbage collection.
T1 kills its own escaped helper by pid, so the test leaves no stray process.
