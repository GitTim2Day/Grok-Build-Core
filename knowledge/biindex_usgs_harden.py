#!/usr/bin/env python3
"""biindex_usgs_harden.py — hardened BiIndex incomplete-row handler for USGS GeoJSON.

Locked rules (no latitude):
- No type guess.
- Pillar only if already established by the row itself; otherwise blank.
- Missing / null fields stay blank (never invent).
- Log only established pillars or nothing for the incomplete aspect.
- Append-only. Status = waiting.
- Provenance: SHA-256 of raw feature + timestamp.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OPTIONAL_NULLABLE = {
    "felt", "cdi", "mmi", "alert", "tz", "sig", "nst", "dmin", "rms", "gap",
    "magType", "types", "ids", "sources", "detail"
}

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def now_ny() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def flatten_feature(feat: dict[str, Any]) -> dict[str, Any]:
    props = feat.get("properties") or {}
    geom = feat.get("geometry") or {}
    coords = geom.get("coordinates") or [None, None, None]
    row = {
        "id": feat.get("id"),
        "mag": props.get("mag"),
        "place": props.get("place"),
        "time_ms": props.get("time"),
        "updated_ms": props.get("updated"),
        "tz": props.get("tz"),
        "url": props.get("url"),
        "detail": props.get("detail"),
        "felt": props.get("felt"),
        "cdi": props.get("cdi"),
        "mmi": props.get("mmi"),
        "alert": props.get("alert"),
        "usgs_status": props.get("status"),
        "tsunami": props.get("tsunami"),
        "sig": props.get("sig"),
        "net": props.get("net"),
        "code": props.get("code"),
        "magType": props.get("magType"),
        "type": props.get("type"),
        "title": props.get("title"),
        "lon": coords[0] if len(coords) > 0 else None,
        "lat": coords[1] if len(coords) > 1 else None,
        "depth_km": coords[2] if len(coords) > 2 else None,
    }
    return row

def incomplete_columns(row: dict[str, Any]) -> list[str]:
    return [k for k, v in row.items() if v is None or (isinstance(v, str) and not v.strip())]

def process_featurecollection(fc: dict[str, Any], log_path: Path | None = None) -> list[dict[str, Any]]:
    if fc.get("type") != "FeatureCollection":
        raise ValueError("not a FeatureCollection")
    features = fc.get("features") or []
    out: list[dict[str, Any]] = []
    log_lines: list[str] = []
    stamp = now_ny()

    for feat in features:
        raw = json.dumps(feat, separators=(",", ":"), sort_keys=True)
        row = flatten_feature(feat)
        missing = incomplete_columns(row)
        pillar = None
        hardened = {
            **row,
            "pillar": pillar,
            "missing": ",".join(missing) if missing else "",
            "biindex_status": "waiting",
            "raw_sha256": sha256_text(raw),
            "processed_utc": stamp,
        }
        out.append(hardened)
        log_lines.append(
            f"{stamp} id={row.get('id')} missing={len(missing)} pillar=blank biindex_status=waiting sha={hardened['raw_sha256'][:16]}"
        )

    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as f:
            for line in log_lines:
                f.write(line + "\n")

    return out

def demo_from_sample():
    sample = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "id": "pr71539028",
            "properties": {
                "mag": 2.87,
                "place": "47 km NNW of San Antonio, Puerto Rico",
                "time": 1794364823300,
                "updated": 1794366719650,
                "tz": None,
                "url": "https://earthquake.usgs.gov/earthquakes/eventpage/pr71539028",
                "detail": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/pr71539028.geojson",
                "felt": None,
                "cdi": None,
                "mmi": None,
                "alert": None,
                "status": "reviewed",
                "tsunami": 0,
                "sig": 127,
                "net": "pr",
                "code": "71539028",
                "magType": "md",
                "type": "earthquake",
                "title": "M 2.9 - 47 km NNW of San Antonio, Puerto Rico"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-67.2981666666667, 18.8773333333333, 8.48]
            }
        }]
    }
    rows = process_featurecollection(sample)
    print(json.dumps(rows[0], indent=2, default=str))
    print("---")
    print("missing fields left blank, pillar blank, status=waiting, no invented type")
    return rows

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_from_sample()
    else:
        print("usage: biindex_usgs_harden.py --demo")
        print("or import process_featurecollection")
