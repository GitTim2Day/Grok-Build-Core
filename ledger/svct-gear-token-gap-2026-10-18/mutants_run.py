"""Mutation check: one fault at a time in a temp copy of svct_gear_token_gap.py;
test_svct_gear_token_gap.py must fail. Originals untouched."""
import os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, "svct_gear_token_gap.py")).read()
MUTANTS = [
    ("gap slot N-2", "self.gap_slot = tokens_per_ring - 1", "self.gap_slot = tokens_per_ring - 2"),
    ("token index rounds", "i = int(math.floor(ring_deg / pitch))", "i = int(round(ring_deg / pitch))"),
    ("no mod-N wrap", "return i % tokens_per_ring", "return i"),
    ("overlap upper edge 23.0", "((0.25, 23.25), (356.5, 359.75))", "((0.25, 23.0), (356.5, 359.75))"),
    ("overlap lower edge 357.0", "((0.25, 23.25), (356.5, 359.75))", "((0.25, 23.25), (357.0, 359.75))"),
    ("overlap open interval", "lo <= ring_deg <= hi", "lo < ring_deg < hi"),
    ("no hold in gap (drives through)", "            out = self._held\n", "            out = self.tr.actuator_to_joint_position(motor_angle)\n"),
    ("resync ignores gap", "resync = bool(self._was_gap) or crossed", "resync = crossed"),
    ("resync ignores closure crossing", "resync = bool(self._was_gap) or crossed", "resync = bool(self._was_gap)"),
    ("fail_closed never set", "TokenState(motor_angle, turns, deg, idx, gap, gap, out, ov, resync)", "TokenState(motor_angle, turns, deg, idx, gap, False, out, ov, resync)"),
    ("cold start holds phase 0", "self._held = self.gap_entry_joint(turns)", "self._held = turns * TWO_PI"),
    ("gap reports a joint value", "joint = None if gap else self.tr.actuator_to_joint_position(motor_angle)", "joint = self.tr.actuator_to_joint_position(motor_angle)"),
]
killed = 0
for name, old, new in MUTANTS:
    assert SRC.count(old) >= 1, name
    d = tempfile.mkdtemp(prefix="tg_mut_")
    with open(os.path.join(d, "svct_gear_token_gap.py"), "w") as f:
        f.write(SRC.replace(old, new, 1))
    for fn in ("test_svct_gear_token_gap.py", "spiral_gear.py", "interference_exact.json"):
        shutil.copy(os.path.join(HERE, fn), d)
    p = subprocess.run([sys.executable, "-B", "test_svct_gear_token_gap.py"], cwd=d, capture_output=True, text=True, timeout=300)
    k = p.returncode != 0
    killed += k
    print(f"{'KILLED' if k else 'SURVIVED'}: {name}")
    shutil.rmtree(d)
print(f"mutants killed {killed}/{len(MUTANTS)}")
