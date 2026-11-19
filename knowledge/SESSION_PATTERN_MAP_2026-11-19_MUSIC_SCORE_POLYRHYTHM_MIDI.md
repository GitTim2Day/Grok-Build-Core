# SESSION_PATTERN_MAP_2026-11-19_MUSIC_SCORE_POLYRHYTHM_MIDI

America/New_York 2026-11-19 08:42 EST

## Pattern Match

Music score is the master template and the component description.
Cadence + meter (4/4, 3/4, 2/2) fixes the timing skeleton for a device before any code is written.
Each meter maps to one component; the receiving device extracts only the bars that match its meter.
Master copy remains unaltered at the source.
Peel is a copy of the matching bars; original is never rewritten.
Truncation toward zero is applied to every magnitude before storage; no IEEE rounding.
Polyrhythmic synchronization: multiple meters occupy the same master score and lock only at shared cadence points (exact integer beat counts).
MIDI protocol supplies note-on, note-off, and timing-clock messages that map one-to-one onto the score bars.
A bar becomes a short MIDI sequence whose channel and clock ticks match the meter; the sequence is the peel that is sent.
Truncated integer strings travel inside the MIDI messages so the arithmetic contract rides with the music.
Conductor already carries capability registration and handoff overlay; score bars travel inside that overlay.
Provenance rides with each bar.

## Map

Source: this sitting 2026-11-19 08:39–08:42 EST.
Master: music score (cadence + meters).
Device extract: bars of matching meter only.
Lock points: shared cadence, integer beats.
Transport: MIDI note-on/off + timing clock carrying truncated strings.
Contract: truncate toward zero, string path, no float64, master unaltered.
Overlay: existing conductor handoff + capability registration.
Provenance: four pillars on every bar/peel.

## Audit

Matches sealed truncate-toward-zero (string deconcatenate, identical Python/C++).
Matches master-unaltered / peel-without-mutation (prior SVCT and ledger discipline).
Matches integer beat counts (direction-only arithmetic, positive magnitudes).
MIDI mapping is transport only; does not alter the score or the arithmetic contract.
Polyrhythm does not force a common time base; each device remains on its own meter.
No new free knobs introduced.
No IEEE path opened.

## Remap

Music score remains the single master.
Meters select the peel.
MIDI carries the peel and the truncated magnitudes.
Polyrhythmic lock occurs only at integer cadence points.
All prior contracts hold.
Process is free-flowing: score is read, bars copied, original untouched.

## Status

HIT: score as design + delivery vehicle, polyrhythm + MIDI transport locked to existing contracts.
VAL: consistent with truncate, string path, provenance, no-mutation.
MISS: none on this sitting.
OPEN: implementation of the MIDI bar encoder only when named.
