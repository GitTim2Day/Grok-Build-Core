#!/bin/bash
# MAPBOOK — build + self-test + streamline the Georgia extract on the Pi.
# Usage (from the mapbook folder):  bash run_pi.sh ~/work/maps/georgia-latest.osm.pbf
# Stops at the first failure. Nothing is overwritten: output goes to a new dated folder.
set -u
SRC="${1:-$HOME/work/maps/georgia-latest.osm.pbf}"
OUT="$HOME/work/maps/streamlined_$(date +%Y%m%d_%H%M%S)"
echo "== 1/5 build C++ twin"
g++ -std=c++17 -O2 -Wall -Wextra osm_streamline.cpp -lz -o osm_streamline || { echo "BUILD FAILED (need: sudo apt install -y g++ zlib1g-dev)"; exit 1; }
echo "== 2/5 self-test both twins on the answer key"
mkdir -p faults
python3 -I make_osm_fixture.py osm_fixture_selftest.pbf >/dev/null || exit 1
for T in py cpp; do
  if [ "$T" = py ]; then python3 -I osm_streamline.py osm_fixture_selftest.pbf st_$T >/dev/null; else ./osm_streamline osm_fixture_selftest.pbf st_$T >/dev/null; fi
  for F in addresses roads road_nodes; do
    cmp -s st_$T/$F.txt osm_fixture_expected/$F.txt || { echo "SELF-TEST FAIL $T $F"; exit 1; }
  done
  echo "   $T: 3/3 outputs match the key"
done
echo "== 3/5 input check"
[ -s "$SRC" ] || { echo "MISSING INPUT $SRC"; exit 1; }
ls -l "$SRC"; sha256sum "$SRC"
mkdir -p "$OUT"
echo "== 4/5 streamline (C++), timed"
S=$(date +%s); ./osm_streamline "$SRC" "$OUT" || exit 1; E=$(date +%s)
echo "   seconds=$((E - S))"
echo "== 5/5 results"
ls -l "$OUT"; sha256sum "$OUT"/*.txt
head -3 "$OUT/addresses.txt"
echo "DONE -> $OUT   (optional Python cross-check: python3 -I osm_streamline.py \"$SRC\" ${OUT}_py)"
