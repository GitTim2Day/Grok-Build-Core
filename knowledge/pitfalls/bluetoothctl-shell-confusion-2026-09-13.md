# Pitfall: bluetoothctl vs shell confusion (2026-09-13)

## What happened
While pairing the JBL speaker to the Pi 5, `scan on` was typed at the regular bash prompt (`shepherd@raspberrypi:~ $`). Result: `bash: scan: command not found`.

The reader file also failed to install: `python3: can't open file '/home/shepherd/pi_adxl355_link.py'` — the curl pulled the script text to stdout but never wrote it to disk.

## Root cause
`scan`, `pair`, `trust`, `connect` are **bluetoothctl subcommands**, not shell commands. They only work after entering the bluetoothctl interactive prompt (prompt changes to `[bluetooth]#`).

## Corrected sequence (record for future clients/users)
1. Put the JBL in pairing mode (hold Bluetooth button until it flashes).
2. On the Pi: `bluetoothctl`  → prompt becomes `[bluetooth]#`.
3. `power on`
4. `scan on`  — watch for the JBL name + MAC.
5. `pair <MAC>` then `trust <MAC>` then `connect <MAC>`.
6. `exit` to return to shell.
7. Verify: `bluetoothctl info <MAC>` shows Connected: yes.

## Rule to append
Before typing any bluetoothctl subcommand, confirm the prompt shows `[bluetooth]#`. If it shows `shepherd@... $`, you are in the shell — type `bluetoothctl` first.

## Applies to
Any future Bluetooth pairing on Pi or other Linux devices. Same trap for `nmcli`, `wpctl`, and other interactive CLIs.
