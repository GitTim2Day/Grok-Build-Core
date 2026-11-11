# SESSION_PATTERN_MAP_2026-11-10_BIINDEX_USGS_HARDEN

America/New_York: 2026-11-10 23:14 EST

## Pattern Match and Map

Hardened BiIndex incomplete-row handler applied to USGS GeoJSON FeatureCollection format.

File: biindex_usgs_harden.py
SHA-256: 5dc8a251ece9e8fc46806c00f1f53ad77a8f66a8c441a198656706a0e150a7ae
Size: 5944

Locked rules (no latitude):
- No type guess.
- Pillar only if already established by the row itself; otherwise blank.
- Missing / null fields stay blank (never invent values for felt, cdi, mmi, alert, tz, etc.).
- Log only established pillars or nothing for the incomplete aspect.
- Append-only. biindex_status = waiting.
- Original usgs_status preserved.
- Provenance: raw_sha256 of exact feature + processed_utc.

Demo on Puerto Rico M2.9 sample (id pr71539028) produced blank pillar, missing list, waiting status, no invented fields.

## Audit

Demo run clean. Status field collision fixed (usgs_status kept, biindex_status separate). Nulls remain None. No rewrite of source. No silent fill. Exit 0 on --demo.

## Pattern Match Again

Hardened for USGS summary feed shape. Incomplete-row contract holds. Ready for live feed slice or tremor CSV if source named. No external pillar established by the row itself.

Open: live feed or next named source only if directed.
