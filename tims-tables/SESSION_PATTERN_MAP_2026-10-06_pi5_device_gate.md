# Pi 5 device gate — 2026-10-06

Stamp: 2026-10-06T08:56-04:00
Sibling of the nozzle-to-unit-gate map. Not a merge. Pass A written. Pass B re-read.

## Pattern

The Pi 5 finishes the closed row. A device is one kind. Convert on its own floor. It does not guide until it is subscribed to one channel.

## Map

- Camera frame rate is a time. A pixel is a length only after one measured scale.
- Accelerometer is an acceleration. Own noise floor and clip. Outside that, stop. Not a length. Not a Wi-Fi signal.
- Magnetometer is a direction. It does not vote as a range.
- Radio clock or packet time is a time. Missing interval: do not divide. A late packet is not now.
- Signal strength is not a meter. It becomes a range only against a measured length. Until then it stays dark.
- Bluetooth audio is a sample rate. It does not steer. A sleeping speaker is a power fact, not a sensor vote.
- USB power and throughput are ceilings. Past the ceiling, overrun stops or the rate drops.
- A subscribed radio may deliver a reading on one channel. It does not fold a peer's reading back into the Pi's row, and it does not average.
- The closed row still finishes if the radio is down. The peer receives the ratio and the stops.
- An unknown device is logged and does not guide.

## Audit

HIT: one kind, one floor, allow-gate, late packet is not now, RSSI stays dark, closed row survives radio-down.
TIGHTENED: arrival path and closed row stay separate. A subscribed radio may deliver. It may not average.
NOT SEATED: every plugged-in device is running the card.

## Pattern map again

Pass B matches Pass A. The tightened radio line is the one that keeps the gate honest. No new formula. No new spoke.
