"""Tests for svct_gear_token_gap.py (stdlib unittest). Prints measured numbers."""
import hashlib, json, math, os, unittest
import spiral_gear as sg
import svct_gear_token_gap as tg

HERE = os.path.dirname(os.path.abspath(__file__))
R = math.radians
PRIOR_SPIRAL_GEAR_SHA = "1ab41e529549fce25cb7e174ee19285cfe0ad21f8afa4055747fba3891a4250b"
PRIOR_TABLE_WORST = 4.223e-06      # truncated value from the prior run; true max < 4.224e-06


def _json():
    with open(os.path.join(HERE, "interference_exact.json")) as f:
        return json.load(f)


class Shared:
    tr = sg.SpiralGearTransmission(table_points=4097, simpson_n=64)   # the existing table


class Provenance(unittest.TestCase):
    def test_spiral_gear_copy_is_byte_identical(self):
        with open(os.path.join(HERE, "spiral_gear.py"), "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, PRIOR_SPIRAL_GEAR_SHA)


class TableOutsideGap(unittest.TestCase):
    """Same 8001-sample motor set as the prior compute.py (-18.8 .. +56.5 rad)."""
    def test_matches_existing_table_and_closed_form(self):
        ring = tg.SVCTGearTokenRing(transmission=Shared.tr)
        n_out = n_gap = 0; max_vs_table = 0.0; max_vs_closed = 0.0
        for i in range(-2000, 6001):
            m = i * 0.0031415926 * 3
            turns, deg, idx, gap, joint, ov = ring.classify(m)
            if gap:
                n_gap += 1; self.assertIsNone(joint); continue
            n_out += 1
            max_vs_table = max(max_vs_table, abs(joint - Shared.tr.actuator_to_joint_position(m)))
            t, frac = Shared.tr._split(m)
            max_vs_closed = max(max_vs_closed, abs(joint - (t * sg.TWO_PI + sg.theta2_closed(frac))))
        print(f"\n  [measured] samples outside gap {n_out}, in gap {n_gap}; "
              f"max |new - existing table| = {sg.trunc_sci(max_vs_table)} rad; "
              f"max |new - closed form| outside gap = {sg.trunc_sci(max_vs_closed)} rad")
        self.assertEqual(max_vs_table, 0.0)
        self.assertLess(max_vs_closed, 4.224e-06)
        self.assertGreater(n_gap, 0)

    def test_full_set_reproduces_prior_worst(self):
        worst = 0.0
        for i in range(-2000, 6001):
            m = i * 0.0031415926 * 3
            t, frac = Shared.tr._split(m)
            worst = max(worst, abs(Shared.tr.actuator_to_joint_position(m) - (t * sg.TWO_PI + sg.theta2_closed(frac))))
        print(f"\n  [measured] full 8001-sample set (gap included), existing table: {sg.trunc_sci(worst)} rad")
        self.assertEqual(sg.trunc_sci(worst), "4.223e-06")


class TokenLattice(unittest.TestCase):
    def test_twelve_slot_index_is_floor(self):
        for d, want in [(0.0, 0), (29.9, 0), (30.1, 1), (179.9, 5), (329.9, 10), (330.1, 11), (359.99, 11)]:
            self.assertEqual(tg.token_index(d, 12), want, d)

    def test_360_is_0(self):
        self.assertEqual(tg.token_index(360.0, 12), 0)
        turns, frac, deg = tg.ring_position(R(360.0))
        self.assertEqual((turns, deg), (1, 0.0))

    def test_negative_angle_wraps(self):
        turns, _, deg = tg.ring_position(R(-10.0))
        self.assertEqual(turns, -1); self.assertAlmostEqual(deg, 350.0, places=9)
        self.assertEqual(tg.token_index(deg, 12), 11)

    def test_other_ring_sizes(self):
        r = tg.SVCTGearTokenRing(tokens_per_ring=360, transmission=Shared.tr)
        self.assertTrue(r.classify(R(359.5))[3]); self.assertFalse(r.classify(R(358.5))[3])
        for bad in (1, 0, 12.0):
            with self.assertRaises(ValueError):
                tg.SVCTGearTokenRing(tokens_per_ring=bad, transmission=Shared.tr)


class GapFailClosed(unittest.TestCase):
    def test_gap_slot_is_last_pitch(self):
        r = tg.SVCTGearTokenRing(transmission=Shared.tr)
        n = 0
        for k in range(1, 3600):
            d = k / 10.0
            g = r.classify(R(d))[3]
            if abs(d - 330.0) > 1e-6:
                self.assertEqual(g, d > 330.0, d)
            n += g
        print(f"\n  [measured] 0.1-deg grid points in the 12-slot gap: {n} of 3599")

    def test_hold_inside_gap_and_flags(self):
        r = tg.SVCTGearTokenRing(transmission=Shared.tr)
        last = r.step(R(329.9))
        self.assertFalse(last.fail_closed)
        for d in (330.5, 340.0, 350.0, 359.9):
            s = r.step(R(d))
            self.assertTrue(s.in_gap and s.fail_closed); self.assertFalse(s.resync)
            self.assertEqual(s.joint_angle, last.joint_angle)
            self.assertEqual(s.token_index, 11)

    def test_cold_start_in_gap_holds_entry_edge(self):
        r = tg.SVCTGearTokenRing(transmission=Shared.tr)
        s = r.step(R(345.0))
        self.assertTrue(s.fail_closed)
        self.assertEqual(s.joint_angle, Shared.tr.actuator_to_joint_position(R(330.0)))

    def test_fail_closed_equals_in_gap_everywhere(self):
        r = tg.SVCTGearTokenRing(transmission=Shared.tr)
        for k in range(-1440, 2881):
            s = r.step(R(k * 0.25))
            self.assertEqual(s.fail_closed, s.in_gap)


class ResyncAtWrap(unittest.TestCase):
    def test_forward_wrap_reindexes_to_phase_zero(self):
        r = tg.SVCTGearTokenRing(transmission=Shared.tr)
        r.step(R(359.9))
        s = r.step(R(360.0))
        self.assertTrue(s.resync); self.assertEqual(s.token_index, 0); self.assertEqual(s.ring_deg, 0.0)
        self.assertEqual(s.turns, 1)
        self.assertAlmostEqual(s.joint_angle, Shared.tr.turn_out, places=12)
        self.assertFalse(r.step(R(360.1)).resync)

    def test_no_resync_while_driven(self):
        r = tg.SVCTGearTokenRing(transmission=Shared.tr)
        flags = [r.step(R(d)).resync for d in range(0, 330)]
        self.assertFalse(any(flags))

    def test_sample_jump_across_closure_still_resyncs(self):
        r = tg.SVCTGearTokenRing(transmission=Shared.tr)
        r.step(R(300.0))
        s = r.step(R(370.0))
        self.assertTrue(s.resync); self.assertEqual(s.turns, 1)

    def test_one_resync_per_turn_over_many_turns(self):
        r = tg.SVCTGearTokenRing(transmission=Shared.tr)
        count = sum(r.step(R(k * 0.5)).resync for k in range(0, 720 * 5 + 1))
        self.assertEqual(count, 5)

    def test_reverse_into_gap_then_forward(self):
        r = tg.SVCTGearTokenRing(transmission=Shared.tr)
        r.step(R(1.0))
        s = r.step(R(-1.0)); self.assertTrue(s.in_gap); self.assertEqual(s.turns, -1)
        s = r.step(R(0.5)); self.assertTrue(s.resync); self.assertEqual(s.token_index, 0)

    def test_back_out_of_gap_without_wrap_resyncs(self):
        r = tg.SVCTGearTokenRing(transmission=Shared.tr)
        r.step(R(329.0)); s = r.step(R(340.0)); self.assertTrue(s.in_gap)
        s = r.step(R(320.0))
        self.assertTrue(s.resync); self.assertEqual((s.turns, s.token_index), (0, 10))
        self.assertEqual(s.joint_angle, Shared.tr.actuator_to_joint_position(R(320.0)))

    def test_resync_jump_equals_ideal_travel_over_gap(self):
        r = tg.SVCTGearTokenRing(transmission=Shared.tr)
        held = r.step(R(330.0)).joint_angle
        jump = r.step(R(360.0)).joint_angle - held
        ideal = sg.theta2_closed(sg.TWO_PI - 1e-15) - sg.theta2_closed(R(330.0))
        print(f"\n  [measured] 12-slot model: held {sg.trunc(held, 9)} rad, "
              f"re-sync jump {sg.trunc(jump, 9)} rad, ideal gear-2 travel over gap {sg.trunc(ideal, 9)} rad")
        self.assertLess(abs(jump - ideal), 1e-5)


class OverlapShellCompetition(unittest.TestCase):
    def test_zones_match_measured_json(self):
        d = _json()
        self.assertEqual([tuple(z) for z in d["hit_theta1_deg_ranges"]], list(tg.OVERLAP_ZONES_DEG))

    def test_flag_counts_107_of_1440(self):
        n = sum(tg.in_overlap(k * 0.25) for k in range(1440))
        self.assertEqual(n, 107)

    def test_flag_equals_measured_depth_on_listed_poses(self):
        d = _json()
        listed = d["depth_by_pose_first_100"] + d["depth_by_pose_last_40"]
        hits = 0
        for deg, depth in listed:
            hit = float(depth) > d["threshold_in_a"]
            hits += hit
            self.assertEqual(tg.in_overlap(deg), hit, deg)
        self.assertEqual(hits, 107)

    def test_overlap_with_gap_and_with_token0(self):
        r = tg.SVCTGearTokenRing(transmission=Shared.tr)
        a = r.classify(R(357.0)); b = r.classify(R(2.25)); c = r.classify(R(23.5))
        self.assertTrue(a[3] and a[5])                  # gap side of the closure
        self.assertTrue((not b[3]) and b[5] and b[2] == 0)   # token 0 driven while competing
        self.assertFalse(c[5])
        self.assertFalse(tg.in_overlap(0.0)); self.assertTrue(tg.in_overlap(0.25))
        self.assertTrue(tg.in_overlap(359.75)); self.assertFalse(tg.in_overlap(356.25))


if __name__ == "__main__":
    unittest.main(verbosity=2)
