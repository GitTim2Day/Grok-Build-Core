# Archive / boo-boo log — 2026-09-28 SlidingWindowFilter
Standing: do not trash. Retrieve only.
Owner: Timothy H. Norman

## Kept on shelf (do not delete)
- knowledge/sealed_truncate.py
- knowledge/sealed_truncate_2026-09-28.py (dated, has __main__ sweep)
- knowledge/sliding_window_filter.py (8163, wired cut + live suite)
- knowledge/sliding_window_filter_2026-09-28.py (earlier dated body)
- knowledge/FAILURE_PATTERN_2026-09-28_HALF_SHELF_DROP_SELFTEST.md
- knowledge/SESSION_PATTERN_MAP_2026-09-28_SEALED_TRUNCATE.md

## Boo-boo 1 — half-shelf-drop-selftest
Commit 06026a7 shipped class only (~4k). Disk still had __main__.
Mitigation: GET back after hop; require if __name__.

## Boo-boo 2 — dead first 20-seed loop (332 bytes)
Disk 8495 vs shelf 8163. Loop ran N(100,1) then was overwritten by
run_reject_and_step(1.0). Not a missing test. Retrieved below.

```python
    seed_ok = 0
    seed_rates = []
    n = 10000
    for seed in range(20):
        random.seed(seed)
        fg = SlidingWindowFilter()
        for _ in range(n):
            fg.filter(random.gauss(100.0, 1.0))
        rej_pct = 100.0 * fg.outlier_count / n
        seed_rates.append(rej_pct)
        if rej_pct < 2.0:
            seed_ok += 1
```

Live suite still covers that case inside run_reject_and_step(1.0).
This block is archive only. Do not put it back unless named.

## Boo-boo 3 — 1e-9 nudge (superseded, not trashed)
Filter first used math.trunc(x*1000 + copysign(1e-9, x)).
Sealed face forbids the nudge. Wired to sealed_truncate.to_count.
Old dated file on the repo still shows the nudge path.

Trash count this project: 0 this sitting.
