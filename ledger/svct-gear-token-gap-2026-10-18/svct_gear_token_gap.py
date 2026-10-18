"""SVCT token-gap view of the golden-spiral gear's straight step.

Timothy H. Norman's model (MODEL, stated by him, not measured):
  * 12-hour clock with modular wrap: the ring position is the motor angle mod 360 deg;
    360 deg becomes 0 deg -- a new starting point, not a break.
  * Teeth are circular tokens on the ring. The toothless straight step is where the ring
    closes and the next token begins: the gap is a MISSING TOKEN, not a broken ratio.
  * In the gap there is no drive: the reader fails closed and HOLDS. When the next token
    arrives the phase re-indexes to that token's lattice position (0 deg on a forward wrap).
  * Corner overlap = the voxel's edge case: two tokens compete for the same shell.

Encoding chosen here (labelled; not physical data):
  * tokens_per_ring N slots of pitch 360/N deg (default N = 12 from the 12-hour clock).
    Physical tooth count is UNKNOWN (video gives none).
  * The missing token is slot N-1, the slot that ends at the closure (360 -> 0).
    Gap width = one pitch. Physical drive-loss width is UNMEASURED.
  * Overlap ("shell competition") zones are the MEASURED sampled hit ranges from
    interference_exact.json (0.25 deg poses, ideal zero-clearance profiles):
    [0.25, 23.25] deg and [356.5, 359.75] deg.
Joint angle outside the gap = the existing SpiralGearTransmission table (spiral_gear.py,
copied byte-for-byte from /workspace/spiral-gear-tendon-2026-10-18/). Stdlib only.
"""
import math
from dataclasses import dataclass

import spiral_gear as sg

TWO_PI = sg.TWO_PI
OVERLAP_ZONES_DEG = ((0.25, 23.25), (356.5, 359.75))   # MEASURED (sampled), see module doc


def ring_position(motor_angle):
    """(turns, ring_rad, ring_deg): motor angle mod 360 deg; 360 -> 0 starts a new turn."""
    turns, frac = sg.SpiralGearTransmission._split(motor_angle)
    return turns, frac, math.degrees(frac)


def token_index(ring_deg, tokens_per_ring=12):
    """Lattice slot of a ring position: floor (truncate) of ring_deg / pitch, mod N."""
    pitch = 360.0 / tokens_per_ring
    i = int(math.floor(ring_deg / pitch))
    return i % tokens_per_ring          # float guard: 360.0 -> slot 0 (the wrap)


def in_overlap(ring_deg):
    return any(lo <= ring_deg <= hi for lo, hi in OVERLAP_ZONES_DEG)


@dataclass(frozen=True)
class TokenState:
    motor_angle: float
    turns: int
    ring_deg: float
    token_index: int        # lattice slot 0..N-1 (N-1 = the missing token)
    in_gap: bool            # slot N-1: no token present -> no drive
    fail_closed: bool       # True in the gap: joint output is a HOLD, not a drive value
    joint_angle: float      # table value outside the gap; held value inside it
    overlap: bool           # shell competition zone (measured sampled ranges)
    resync: bool            # this sample is the first token arrival after the gap


class SVCTGearTokenRing:
    def __init__(self, tokens_per_ring=12, transmission=None, **table_kwargs):
        if not isinstance(tokens_per_ring, int) or tokens_per_ring < 2:
            raise ValueError("tokens_per_ring must be an int >= 2")
        self.N = tokens_per_ring
        self.pitch_deg = 360.0 / tokens_per_ring
        self.gap_slot = tokens_per_ring - 1
        self.tr = transmission or sg.SpiralGearTransmission(**table_kwargs)
        self._held = None
        self._was_gap = None
        self._last_turns = None

    def classify(self, motor_angle):
        """Stateless read: token index, gap flag, overlap flag, table joint angle
        (None in the gap: no token, no drive, fail closed)."""
        turns, _, deg = ring_position(motor_angle)
        idx = token_index(deg, self.N)
        gap = idx == self.gap_slot
        joint = None if gap else self.tr.actuator_to_joint_position(motor_angle)
        return turns, deg, idx, gap, joint, in_overlap(deg)

    def gap_entry_joint(self, turns):
        """Joint angle at the gap's entry edge (last driven position) of turn `turns`."""
        edge = turns * TWO_PI + math.radians(self.gap_slot * self.pitch_deg)
        return self.tr.actuator_to_joint_position(edge)

    def step(self, motor_angle):
        """Stateful read. In the gap: hold the last driven joint angle (fail closed).
        First token after the gap -- or after a sample jump across the closure -- is a
        re-sync: the phase re-indexes to that token's lattice position (table value)."""
        turns, deg, idx, gap, joint, ov = self.classify(motor_angle)
        resync = False
        if gap:
            if self._held is None:          # cold start inside the gap: hold the entry edge
                self._held = self.gap_entry_joint(turns)
            out = self._held
        else:
            crossed = self._last_turns is not None and turns != self._last_turns
            resync = bool(self._was_gap) or crossed
            out = joint
            self._held = joint
        self._was_gap = gap
        self._last_turns = turns
        return TokenState(motor_angle, turns, deg, idx, gap, gap, out, ov, resync)

    def reset(self):
        self._held = None
        self._was_gap = None
        self._last_turns = None
