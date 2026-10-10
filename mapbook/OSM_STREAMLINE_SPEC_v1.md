# OSM streamline — spec v1.6 (2026-10-10, supersedes v1.5)

Author: Timothy Norman (sole author). Claude = tool/validator.
Purpose: one read of a Geofabrik `.osm.pbf` extract (Georgia, 340 MB) keeping only
addresses (offline geocoder) and roads (routing feed). Everything else is dropped.
No outside libraries: zlib + a hand-written protobuf reader. Integer coordinates only.

## Limits (variables)
- MH = 65536      max BlobHeader bytes (larger: REFUSE file)
- MB = 33554432   max Blob bytes, compressed or raw (larger: REFUSE file)
- Supported required features: OsmSchema-V0.6, DenseNodes. Any other: REFUSE file.
- Blob kinds: raw (1) and zlib (3) only. Any other: REFUSE file.
- The first block must be OSMHeader. An empty file, or data before the header: REFUSE
  (defect S1, v1 accepted an empty file as a zero-count success).
- Text bytes (tags, names, messages) pass through exactly as stored: no decoding,
  no repair of invalid UTF-8 (defect S2, twins disagreed on a corrupted name).
- zlib: inflate at most MB+1 bytes. Stream error or incomplete stream: REFUSE "zlib error".
  More than MB bytes: REFUSE "blob size out of range". Bytes after the stream end are
  ignored. Then output length must equal raw_size, else REFUSE "raw_size mismatch"
  (defect S3: Python crashed on corrupt data and had no output cap).
- Check order (defect S4, twins refused corrupt files for different first reasons):
  header length -> header bytes present ("truncated header") -> parse all header
  fields -> blob size -> blob bytes present -> parse ALL blob fields (unsupported
  compression refuses during this scan) -> then inflate -> raw_size check.
- Wire types: a known field number with an unexpected wire type is IGNORED, as if
  absent (ids, coordinates and lists alike).
- Every field, fixed-width ones too, must fit inside its buffer, else REFUSE
  "truncated field" (defect S5: Python skipped the bounds check on 4/8-byte fields).
- Text is written by byte length, never stopped at a zero byte (defect S6: C++ cut
  messages and names at NUL).

## Coordinates (no floats)
nano = lat_offset + granularity * stored  (nanodegrees, integer).
Text form: hemisphere letter + absolute value, 7 decimals, by TEXT CHOP of the
9-digit fraction (drop last 2 digits; truncation toward zero, never rounding).
Latitude N/S, longitude E/W. If the chopped text is all zeros the letter is N
(latitude) or E (longitude) whatever the sign was — no negative zero.

## Pass 1 (FOR each block: READ -> RECORD -> CLEAR)
```
FOR each block
  READ header, blob; decompress; IF OSMHeader THEN GOSUB CHECK_FEATURES
  FOR each primitive group
    FOR each node (plain or dense)
      IF tags have addr:housenumber THEN GOSUB KEEP_ADDR_NODE (coords known now)
    NEXT
    FOR each way
      IF tags have addr:housenumber THEN GOSUB KEEP_ADDR_WAY (needs first ref)
      IF tags have highway in ROADSET THEN GOSUB KEEP_ROAD (needs all refs)
    NEXT
    relations: skip (counted)
  NEXT
  CLEAR block, string table, scratch
NEXT
```
## Pass 2
FOR each block, FOR each node: IF id in NEED (refs of kept roads + first ref of
address ways) THEN record coordinates. CLEAR. After pass 2 every needed id must
be found; missing ids are counted and their rows marked MISSINGREF (no guessing).

## ROADSET
motorway trunk primary secondary tertiary unclassified residential service
motorway_link trunk_link primary_link secondary_link tertiary_link living_street road

## Outputs (pipe-separated, UTF-8, empty field = one blank)
- addresses.txt: `KIND|ID|HOUSE|STREET|CITY|STATE|ZIP|LAT|LON|POS`
  KIND N (node) or W (way). POS = NODE (exact point) or FIRSTREF (first node of the
  way) or MISSINGREF.
- roads.txt: `WAYID|CLASS|NAME|NREFS|REF REF REF...`
- road_nodes.txt: `NODEID|LAT|LON` for every node a kept road uses (sorted by id).
- summary.txt: input bytes + SHA-256, blocks, nodes, ways, relations seen, kept
  counts, missing refs, output bytes.

## Answer key
`osm_fixture.pbf` is built by `make_osm_fixture.py` byte by byte; expected outputs
are written by hand in `osm_fixture_expected/`.
