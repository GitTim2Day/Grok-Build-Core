#!/bin/sh
# build_bwbasic_3.20b_2026-10-08.sh -- rebuild the vetted Bywater BASIC 3.20b, pinned. Timothy Norman project.
# Record: knowledge/BWBASIC_VETTING_2026-10-08.md
# Fail closed: any hash or check that does not match stops the build. Nothing is installed system-wide.
# Usage: sh scripts/build_bwbasic_3.20b_2026-10-08.sh <empty-work-dir>
# Result: <work-dir>/bin/bwbasic  (put that folder first on PATH for the self-checks)
set -eu
REPO=https://github.com/kenmartin-unix/Bwbasic-3.20b
COMMIT=48ad357ea42ee15c7770e1ba9ed11238bfab2e78
TAR_SHA=b93b56e7931ceffdbc60ee1f8c8bae7f09a102504311babc057e323871c8a909
WD=${1:?give an empty work directory}
mkdir -p "$WD"; cd "$WD"
[ -z "$(ls -A .)" ] || { echo "REFUSED: work dir not empty"; exit 2; }

# 1 pin: clone, check out the exact commit
git clone -q "$REPO" src
git -C src checkout -q "$COMMIT"
[ "$(git -C src rev-parse HEAD)" = "$COMMIT" ] || { echo "REFUSED: commit mismatch"; exit 3; }

# 2 hash the tarball before opening it
GOT=$(sha256sum src/bwbasic-3.20b.tar | cut -d' ' -f1)
[ "$GOT" = "$TAR_SHA" ] || { echo "REFUSED: tar sha256 $GOT"; exit 4; }

# 3 tar guard: no links, devices, absolute paths or .. traversal
if tar -tvf src/bwbasic-3.20b.tar | grep -qE '^[lhcbp]'; then echo "REFUSED: link/device in tar"; exit 5; fi
if tar -tf src/bwbasic-3.20b.tar | grep -qE '^/|(^|/)\.\.(/|$)'; then echo "REFUSED: path traversal in tar"; exit 5; fi
mkdir x; tar -xf src/bwbasic-3.20b.tar -C x --no-same-owner --no-same-permissions

# 4 build: -std=gnu89 (NOT -ansi: -ansi hides rint() and CINT / integer division come out wrong)
mkdir build bin
cp x/bwbasic-3.20b/*.c x/bwbasic-3.20b/*.h build/
rm -f build/renum.c        # separate helper program, not part of the interpreter
( cd build && gcc -O2 -std=gnu89 -Wall -o ../bin/bwbasic bw*.c -lm )

# 5 smoke: the hybrid boot value and the line-1000 IF case that breaks 3.00
printf '5125 IF 1 THEN PRINT "OK": GOTO 5150\n5130 PRINT "FAIL"\n5150 END\n' > smoke.bas
[ "$(./bin/bwbasic smoke.bas </dev/null | tr -d '\r\n ')" = "OK" ] || { echo "FAIL: line-1000 IF smoke"; exit 6; }
printf 'PRINT CINT(3.5); 7 MOD 3\nSYSTEM\n' > smoke2.bas
[ "$(./bin/bwbasic smoke2.bas </dev/null | tr -s ' ' | tr -d '\r\n')" = " 4 1 " ] || { echo "FAIL: CINT/MOD smoke"; exit 6; }
echo "BUILT bin/bwbasic sha256 $(sha256sum bin/bwbasic | cut -d' ' -f1)"
echo "NOTE: binary hash depends on the gcc version; the tar hash above is the identity of the source."
