# MAP_TEMPLATE — georgia-latest.osm.pbf source record (2026-11-09, Research seat) [GEOMAP-2026-11-09]

Purpose (Timothy t782u/t783u): keep the source record, not the 357 MB file, so a fresh Geofabrik download can be checked and the streamlined output rebuilt. The pbf itself is not attached anywhere.

## 1. Source file

- Pi (deleted ~2026-11-09 5:00 PM EST for Tesseract 5.5.4): `~/work/maps/georgia-latest.osm.pbf`
- bytes: 357057388
- sha256: 2ac4c2ef929d4a04ff1280051c62b5791bf062f70eac16cfdabd27e9f9e4a1ce
- mtime: 2026-10-09T23:06:44Z (Oct 9 19:06 EDT)
- box copy: `/workspace/pi5-work-core-2026-11-09/extracted_r2/work/maps/georgia-latest.osm.pbf` (read-only; re-hashed MATCH vs INVENTORY)
- other copies: box zip member `work/maps/georgia-latest.osm.pbf` in `/workspace/pi5-work-core-2026-11-09/original/work_core_2026-11-09.zip`; Drive full zip 1l8vN9il7ng5JFCRA7TlUcAbvyZZoLqi6; Drive pieces wc_part02..wc_part06 (rejoin all 9, then unzip the member; see RETRIEVAL_MAP_2026-11-09 section 2)

## 2. PBF header (read with pure Python, scripts/pbf_header.py; no install)

- bbox (exact nanodegrees → degrees): left -85.606800000, right -80.743130000, top 35.003560000, bottom 30.353650000
- writing program: osmium/1.16.0
- osmosis replication timestamp: 1791577264 = 2026-10-09T20:21:04Z (2026-10-09 16:21:04 EDT)
- osmosis replication sequence number: 4937
- replication base url: https://download.geofabrik.de/north-america/us/georgia-updates
- required features: OsmSchema-V0.6, DenseNodes; optional: Sort.Type_then_ID
- first blob: OSMHeader, BlobHeader 14 bytes, datasize 183 bytes

## 3. Streamlined folder `~/work/maps/streamlined_20261010_101614/` (kept on the Pi; copy on box under extracted_r2/work/maps/)

Format per OSM_STREAMLINE_SPEC v1.6: pipe-separated, UTF-8, empty field = one blank, no header row; coordinates as hemisphere letter + fixed 7-decimal digits (no floats).

### addresses.txt
- bytes 40243482 · lines 499712 · sha256 6a5675d153615f10d482085c4c54be1b21d1d74a3530caa774392a6c2f05b9f6
- columns: `KIND|ID|HOUSE|STREET|CITY|STATE|ZIP|LAT|LON|POS`
- first 3 lines (each cut at 240 chars):
```
N|66493944|803|Kilkenny Road|Richmond Hill|GA|31324|N31.8066192|W81.2320722|NODE
N|66667081|10965|GA 56|Midville|GA|30441|N32.8419231|W82.2220682|NODE
N|68150985|3650|Ashford Dunwoody Road Northeast|Brookhaven|GA|30319|N33.8982580|W84.3308520|NODE
```
### road_nodes.txt
- bytes 334937440 · lines 9719197 · sha256 aed91bc734fa392e13963443d50076c0cda2eee5db4e1f1bb8683f78ae69708d
- columns: `NODEID|LAT|LON (every node a kept road uses, sorted by id)`
- first 3 lines (each cut at 240 chars):
```
1481302|N34.0852695|W84.2629160
51906004|N32.0293560|W85.0756430
51907721|N32.0247070|W85.0788760
```
### roads.txt
- bytes 159882942 · lines 1383997 · sha256 1687eebdb5e8410bb189dfa16a2452f63918390e3ebbf006ef6968ef6f9d4d45
- columns: `WAYID|CLASS|NAME|NREFS|REF REF REF...`
- first 3 lines (each cut at 240 chars):
```
6223052|residential| |32|51907721 51907722 51907724 51907726 51907727 51907728 51907731 51907732 51907734 51907735 51907737 51907738 51907740 51907741 51907744 51907745 51907747 51907749 51907751 51907752 51907754 51907757 51907759 51907760
6225312|residential| |4|51925803 51925804 14042249619 51925805
6225738|unclassified|Industrial Park Drive|16|51930979 51930982 10252722606 51930988 51930991 51930994 10252722604 12971322221 12971322214 51930996 51931000 51931004 51931008 51931011 51931016 51931021
```

## 4. Streamline tools (in the zip, work/Grok-Build-Core/mapbook/)

- `work/Grok-Build-Core/mapbook/OSM_STREAMLINE_SPEC_v1.md` · 4072 bytes · 5840e520c3d9650f
- `work/Grok-Build-Core/mapbook/osm_streamline.py` · 14533 bytes · c3a0db2bd38c0526
- `work/Grok-Build-Core/mapbook/osm_streamline.cpp` · 17012 bytes · af236c6684e61e04
- `work/Grok-Build-Core/mapbook/run_pi.sh` · 1539 bytes · 2536fb7a10338ac3
- `work/Grok-Build-Core/mapbook/make_osm_fixture.py` · 3656 bytes · 06795e6eab0a6267

## 5. Restore steps

1. Exact copy first (preferred): take the box copy, or rejoin the 9 Drive pieces and `unzip -p work_core_2026-11-09.zip work/maps/georgia-latest.osm.pbf > georgia-latest.osm.pbf`; check bytes 357057388 and sha256 2ac4c2ef929d4a04ff1280051c62b5791bf062f70eac16cfdabd27e9f9e4a1ce.
2. Fresh copy (if exact copies are gone): `wget https://download.geofabrik.de/north-america/us/georgia-latest.osm.pbf` (and the .md5 beside it). Expect a NEWER snapshot: sha256 and bytes will differ from this template. Compare instead: `python3 scripts/pbf_header.py georgia-latest.osm.pbf` → bbox should equal section 2; replication timestamp and sequence should be later than 2026-10-09T20:21:04Z / 4937; required features the same.
3. Rebuild: from `Grok-Build-Core/mapbook/`, `bash run_pi.sh ~/work/maps/georgia-latest.osm.pbf` (builds the C++ twin, self-tests both twins on the answer key, writes a new dated `streamlined_YYYYMMDD_HHMMSS/`; never overwrites). Python only: `python3 -I osm_streamline.py <pbf> <outdir>`.
4. Compare: the same pbf (sha above) is expected to give the section 3 sha256 values (box rebuild check with osm_streamline.py: result recorded in the retrieval map addendum, not here); a newer snapshot gives different counts. Record the new folder as a new pointer; keep this template as the sealed reference.
