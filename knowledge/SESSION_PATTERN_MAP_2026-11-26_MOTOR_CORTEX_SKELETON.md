# Motor Cortex Skeleton MAM 2026-11-26

## Config Block
- ENVY_IP$ = 192.168.1.12
- MACHINE_ID$ = shepherd-pi-5
- Read by INIT before device map loads

## Trunk (salience 9000 band = 0.9, append-only, Do No Harm first)
- GOSUB 1000 INIT: device map from devices.dat
- GOSUB 2000 QUERY: ON active_leaf GOSUB leaf query blocks
- GOSUB 3000 ACTUATE: ON active_leaf GOSUB leaf actuate blocks
- Default ABSENT until drivetrain exists

## Leaf 1: HP ENVY 4500
- QUERY: OPEN socket, PJL INFO STATUS, read response, print ENVY line
- ACTUATE: OPEN socket, PJL JOB, print test line, close
- Lines 9000-9070 query, 9010-9070 actuate

## Leaf 2: placeholder next device

## Two-Permission Model
- Share-everything: full packet with provenance
- Protect-everything: raw and reasoning stay on-device, redacted skeleton only
- Gate decides per message, not per session

## Redaction at Unit Level
- Content stripped, structure intact
- SVCT provenance name-agnostic: hash, timestamp, pillars survive

## Tree-Channel Model
- Trunk, branches (device class), stems (concrete unit), leaves (actions)
- Mirrors node-channel architecture Nov 7
- Parallel in effect, serial in execution

## Motor Cortex Principle
- Master the controller, own the machine
- Gamepad-to-CAN, drone radio, dashboard operation
- Feedback stream (warning lights, oil, fuel) = input channel

## Language Plan
- Step 1: English local Vosk/Piper on shepherd
- Step 2: Llama 3.2 1B multilingual (8 langs)
- Step 3: UT2

## AirPods Output Selector
- Appended improvement to voice loop, not patch
- PipeWire sink swap, JBL receive-only, AirPods bidirectional

## Hive Ledger
- Units write to nearest shelf when direct comms fail
- Next Shepherd reads all shelves
- Earned-access model for API

## Seal-the-Night Keyword
- Trial confirmed 2026-11-25 22:21
- Midday or midnight, same command, same cycle

## Calendar Sub-Agent
- Authorized 2026-11-26, zero-cost condition
- First new-day step, America/New_York

## Local-Seal Sub-Agent
- Watches artifacts, SHA-256 seal, append manifest
- Human gate before any shelf write

## Drive Gap
- Upload tool absent after three searches
- Box and Notion inline attachment are substitutes
- User-owned to close

## Opens
- ENVY test against printer IP this afternoon
- AirPods selector code
- now_ny placeholder in neural_channel_operators.py