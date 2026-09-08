# Row 3C — Shepherd 10σ as probability claim (CLOSED)

**Failure:** Naming a deterministic floor as a probability claim.
**Pattern:** claiming done before verified — the floor was declared deterministic in code (sigma_free, EV2 + harmonic + shell snap) but still labeled "10-sigma," inviting a statistical reading it does not carry.
**Mitigation:** Rename to Shepherd 10-Sigma Equivalent or Better, with or without probabilities. MAD guard stays as an earned tool; sigma is no longer the identity.
**Pre-filter:** KBLD-9 (`GOSUB_MAD_Sigma_Guard`).
**Retest 1 — NAB machine temp (22,696 rows):** IQR 99.49% retained, max robust z 8.45, below 9 / 9.5 / 10. No probability invoked.
**Retest 2 — UCI Wine Quality (never-trained):** IQR 94.37% retained, max robust z 2.79, below all three thresholds. Floor held.
**Status:** CLOSED 2026-09-08. Both retests green.
