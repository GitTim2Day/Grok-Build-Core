from collections import deque
import math

from sealed_truncate import to_count as sealed_to_count, sealed_truncate, UNKNOWN


class SlidingWindowFilter:
    BOOTSTRAP_MIN = 4
    MAD_SCALE = 1.4826
    MAD_FLOOR = 0.05
    STD_FLOOR = 0.1
    STEP_CONFIRM = 8
    STEP_SPAN = 3.0
    PLACES = 3
    SCALE = 1000

    def __init__(self, window_size=48, max_dev=3.0, value_ceiling=None):
        self.window_size = window_size
        self.max_dev = max_dev
        self.value_ceiling = value_ceiling
        self.cluster = deque(maxlen=window_size)
        self.pending = deque(maxlen=max(20, window_size))
        self.last_good = None
        self.last_good_count = None
        self.stuck_flag = False
        self.total_samples = 0
        self.outlier_count = 0

    @classmethod
    def to_count(cls, x):
        return sealed_to_count(x, places=cls.PLACES)

    @classmethod
    def from_count(cls, count):
        if count is None:
            return None
        return count / float(cls.SCALE)

    @classmethod
    def _truncate_3(cls, x):
        t = sealed_truncate(x, places=cls.PLACES)
        if t == UNKNOWN:
            return None
        return cls.from_count(cls.to_count(x))

    @staticmethod
    def _is_poison(raw):
        return sealed_to_count(raw, places=3) is None

    @staticmethod
    def _median_of(seq):
        if not seq:
            return None
        s = sorted(seq)
        n = len(s)
        if n % 2 == 0:
            return (s[n // 2 - 1] + s[n // 2]) / 2.0
        return s[n // 2]

    def _median_count(self):
        return self._median_of(self.cluster)

    def _median(self):
        mc = self._median_count()
        if mc is None:
            return None
        return mc / float(self.SCALE)

    def _mad_count(self):
        if len(self.cluster) < 3:
            return self.STD_FLOOR * self.SCALE
        med = self._median_count()
        devs = [abs(x - med) for x in self.cluster]
        raw = self._median_of(devs)
        scaled = raw * self.MAD_SCALE
        if scaled <= 0.0:
            return self.MAD_FLOOR * self.SCALE
        return scaled

    def _mad(self):
        return self._mad_count() / float(self.SCALE)

    def _pending_is_new_level(self):
        if len(self.pending) < self.STEP_CONFIRM:
            return False
        pmed = self._median_of(self.pending)
        if pmed is None:
            return False
        pdevs = [abs(x - pmed) for x in self.pending]
        pmad = self._median_of(pdevs) * self.MAD_SCALE
        span = max(
            self.STEP_SPAN * self.SCALE,
            3.0 * max(pmad, 1.0),
            self.STEP_SPAN * abs(pmed) / 100.0,
        )
        return all(abs(x - pmed) <= span for x in self.pending)

    def _commit_pending(self):
        self.stuck_flag = len(set(self.pending)) == 1
        self.cluster.clear()
        for c in self.pending:
            self.cluster.append(c)
        self.last_good_count = self.pending[-1]
        self.last_good = self.from_count(self.last_good_count)
        self.pending.clear()

    def filter(self, raw):
        self.total_samples += 1
        if self._is_poison(raw):
            return self.last_good if self.last_good is not None else 0.0

        raw_f = float(raw)
        count = self.to_count(raw_f)

        if self.value_ceiling is not None and raw_f > self.value_ceiling:
            self.outlier_count += 1
            return self.last_good if self.last_good is not None else 0.0

        if len(self.cluster) >= self.BOOTSTRAP_MIN:
            if abs(count - self._median_count()) > self.max_dev * self._mad_count():
                self.outlier_count += 1
                self.pending.append(count)
                if self._pending_is_new_level():
                    self._commit_pending()
                    return self.last_good
                if self.last_good is not None:
                    return self.last_good
                return self.from_count(int(math.trunc(self._median_count())))

        self.cluster.append(count)
        self.last_good_count = count
        self.last_good = self.from_count(count)
        self.pending.clear()
        self.stuck_flag = False
        return self.last_good


if __name__ == "__main__":
    import random
    import numpy as np

    f = SlidingWindowFilter(window_size=8, max_dev=3.0, value_ceiling=None)
    for v in [100.0, 101.0, 99.5, 100.5]:
        f.filter(v)

    med = f._median()
    mad = f._mad()
    r200 = f.filter(200.0)
    rnone = f.filter(None)
    cluster_before_nan = list(f.cluster)
    rnan = f.filter(np.float32("nan"))
    cluster_after_nan = list(f.cluster)

    f2 = SlidingWindowFilter(window_size=8, max_dev=3.0)
    shared = f.cluster is f2.cluster

    n = 10000

    def run_reject_and_step(scale):
        mu, sig, step_from, step_to, tol = 100.0 * scale, 1.0 * scale, 100.0 * scale, 120.0 * scale, 3.0 * scale
        ok = 0
        rates = []
        for seed in range(20):
            random.seed(seed)
            fg = SlidingWindowFilter()
            for _ in range(n):
                fg.filter(random.gauss(mu, sig))
            rej_pct = 100.0 * fg.outlier_count / n
            rates.append(rej_pct)
            if rej_pct < 2.0:
                ok += 1
        fs = SlidingWindowFilter()
        for _ in range(200):
            fs.filter(step_from)
        reached = None
        for i in range(1000):
            y = fs.filter(step_to)
            if reached is None and abs(y - step_to) <= tol:
                reached = i + 1
        return ok, (max(rates) if rates else None), reached

    seed_ok, max_r, reached = run_reject_and_step(1.0)
    ok_s, max_s, reached_s = run_reject_and_step(0.01)
    ok_l, max_l, reached_l = run_reject_and_step(50.0)

    ok_z = 0
    rates_z = []
    for seed in range(20):
        random.seed(seed)
        fz = SlidingWindowFilter()
        for _ in range(n):
            fz.filter(random.gauss(0.0, 1.0))
        pz = 100.0 * fz.outlier_count / n
        rates_z.append(pz)
        if pz < 2.0:
            ok_z += 1
    fz2 = SlidingWindowFilter()
    for _ in range(200):
        fz2.filter(0.0)
    reached_z = None
    for i in range(1000):
        y = fz2.filter(20.0)
        if reached_z is None and abs(y - 20.0) <= 3.0:
            reached_z = i + 1

    fk = SlidingWindowFilter()
    for _ in range(200):
        fk.filter(100.0)
    y_stuck = None
    for i in range(8):
        y_stuck = fk.filter(200.0)

    checks = [
        ("median", abs(med - 100.25) < 1e-12, med),
        ("mad", abs(mad - 0.741) < 0.01, mad),
        ("filter(200.0)", r200 == 100.5, r200),
        ("filter(None)", rnone == 100.5, rnone),
        ("instances isolated", not shared, not shared),
        ("np.float32 nan returns last_good", rnan == 100.5, rnan),
        ("np.float32 nan not in cluster", cluster_before_nan == cluster_after_nan, len(cluster_after_nan)),
        ("N(100,1) reject < 2% on 20/20 seeds", seed_ok == 20, (seed_ok, round(max_r, 3))),
        ("step 100->120 within 20 samples", reached is not None and reached <= 20, reached),
        ("scale x0.01 reject < 2% 20/20", ok_s == 20, (ok_s, round(max_s, 3))),
        ("scale x0.01 step within 20", reached_s is not None and reached_s <= 20, reached_s),
        ("scale x50 reject < 2% 20/20", ok_l == 20, (ok_l, round(max_l, 3))),
        ("scale x50 step within 20", reached_l is not None and reached_l <= 20, reached_l),
        ("N(0,1) reject < 2% 20/20", ok_z == 20, (ok_z, round(max(rates_z), 3))),
        ("step 0->20 within 20 samples", reached_z is not None and reached_z <= 20, reached_z),
        ("stuck 200 x8 promotes", y_stuck == 200.0, y_stuck),
        ("stuck 200 x8 sets stuck_flag", fk.stuck_flag is True, fk.stuck_flag),
    ]

    milli_miss = 0
    for i in range(1, 100000):
        x = i / 1000.0
        if SlidingWindowFilter._truncate_3(x) != x:
            milli_miss += 1
        xn = -x
        if SlidingWindowFilter._truncate_3(xn) != xn:
            milli_miss += 1
    checks.append(("truncate-3 milli grid 0.001..99.999", milli_miss == 0, milli_miss))
    for name, ok, val in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {val}")
