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
