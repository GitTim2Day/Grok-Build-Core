# Row 3C — KBLD-9 pre-filter + NAB retest

**Date:** 2026-09-08
**Pattern:** Shepherd 10σ named as a probability claim; MAD/10-sigma guard treated as identity.
**Mitigation:** Rename to Shepherd 10 Sigma equivalent or better, with or without probabilities. KBLD-9 pre-filter: IQR noise floor, golden-ratio damping (~1.618), SHA-256 audit chain. 10×MAD stays earned, never the identity.
**Data source:** Numenta Anomaly Benchmark — realKnownCause/machine_temperature_system_failure.csv
https://raw.githubusercontent.com/numenta/NAB/master/data/realKnownCause/machine_temperature_system_failure.csv
22,696 rows, 5-min intervals, Dec 2013–Feb 2014, labeled anomalies (planned shutdown + catastrophic failure).
**Retest result:** IQR retained 99.49%; golden-ratio damping kept all corrections inside the 10×MAD floor; max robust z = 8.45 (below 9 / 9.5 / 10). No residual recurrence.
**Closed:** yes. Open follow-up: re-run on UCI Wine Quality (never-trained distribution).
