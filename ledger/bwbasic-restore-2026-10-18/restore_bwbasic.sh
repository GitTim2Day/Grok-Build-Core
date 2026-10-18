#!/usr/bin/env bash
# restore_bwbasic.sh  (bwbasic-boot-restore, 2026-10-18, America/New_York)
# Idempotent. Modes:
#   check   (default) verify; if anything is missing or wrong, restore it; then run BOOT.bas.
#   verify  read-only: report state and run BOOT.bas; repair nothing.
#   restore force reinstall/rebuild of every piece, then verify and run BOOT.bas.
# Exit 0 only when BOOT.bas prints 0.70710678 on bwbasic 2.20 (fail closed).
# Never edits BOOT.bas. Never touches /workspace/kbld9/protected/ or svct_v20*.
set -u
MODE="${1:-check}"
HERE="$(cd "$(dirname "$0")" && pwd)"
HYB="${BWB_HYBRID_SRC:-/workspace/bwbasic-hybrid-2026-10-18}"
S320="${BWB_320_SRC:-/workspace/bwbasic320-2026-10-18/src/x}"
REF220="$HYB/unified/ref220"
BOOT="/workspace/hybrid-boot/BOOT.bas"
EXPECT_BOOT_SHA=a8a21b610618f0cb9744cd2fa48da8b64432e178363279228411382469677901
EXPECT_SYS220=0334b1cc270b7e10e26135927a5c18d44f0291c4871903898c33b2bb535f9b8f   # /usr/bin/bwbasic, Debian 2.20pl2-14 amd64
EXPECT_320=85627c86a8ac51c44a67c403bd0c300dd8aa49cbfd0ed97006c1a8e37dbd5e9a       # /opt/bwbasic-3.20b/bwbasic320
EXPECT_UNI=2f7e6cd7579f219e786a1a0fc644ab38dcaf44914be887dfa551baa7a5327a27       # /opt/bwbasic-hybrid/bwbasic-unified
EXPECT_HYB=bcbac33583d4f26945a99356a3c5d833eb07fddda804acd4d70c676918c0753d       # /opt/bwbasic-hybrid/bwbasic-hybrid
EXPECT_BOOT_OUT=64830efbd41e819d2a620887c9da86026ddb448aed4bae95a9329d9d001e4551  # banner + 0.70710678 + prompt
LOGDIR="$HERE/logs"; mkdir -p "$LOGDIR"
LOG="$LOGDIR/restore-$(date +%Y%m%dT%H%M%S%z)-$MODE.log"
exec > >(tee -a "$LOG") 2>&1
exec 9>/tmp/restore_bwbasic.lock; flock -w 600 9 || { echo "FAIL lock"; exit 2; }
say(){ echo "[$(date '+%F %T %Z')] $*"; }
sha(){ [ -f "$1" ] && sha256sum "$1" | cut -d' ' -f1 || echo missing; }
SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo -n"
say "mode=$MODE host=$(hostname) gcc=$(command -v gcc || echo none)"

is220(){ # $1 = binary; banner check without a program file
  [ -x "$1" ] || return 1
  local d; d=$(mktemp -d /tmp/bwbchk-XXXX)   # clean cwd: no stray profile.bas
  ( cd "$d" && timeout 10 "$1" </dev/null 2>/dev/null ) | grep -q 'version 2.20'; }

verify_sources(){
  ( cd "$HYB" && grep -v ' /opt/' SHA256SUMS | sha256sum -c --quiet - ) || { say "FAIL hybrid source tree does not match its SHA256SUMS"; return 1; }
  ( cd "$S320" && sha256sum -c --quiet "$HERE/sources/S320_INPUTS.sha256" ) || { say "FAIL 3.20 source does not match S320_INPUTS.sha256"; return 1; }
  say "OK sources verified"; }

install_220(){
  say "installing bwbasic 2.20: trying apt (Debian main, free)"
  if $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y bwbasic && is220 /usr/bin/bwbasic; then
    say "apt bwbasic installed: $(dpkg-query -W -f='${Version}' bwbasic 2>/dev/null) sha=$(sha /usr/bin/bwbasic)"; return 0; fi
  say "apt failed; building 2.20pl2 from saved Debian source into /usr/local/bin/bwbasic"
  T=$(mktemp -d /tmp/bwb220-XXXX); tar xzf "$REF220/bwbasic_2.20pl2.orig.tar.gz" -C "$T" || return 1
  ( cd "$T/bwbasic-2.20pl2.orig" && for p in $(cat "$REF220/debian/patches/series"); do patch -p1 -s < "$REF220/debian/patches/$p" || exit 1; done &&
    gcc -ansi -O2 -w -DHAVE_RAISE=1 -DHAVE_STRING_H=1 -DHAVE_STDLIB_H=1 -DHAVE_SIGNAL=1 -o bwbasic \
      bwbasic.c bwb_int.c bwb_tbl.c bwb_cmd.c bwb_prn.c bwb_exp.c bwb_var.c bwb_inp.c bwb_fnc.c bwb_cnd.c \
      bwb_ops.c bwb_dio.c bwb_str.c bwb_elx.c bwb_mth.c bwb_stc.c bwb_par.c bwx_tty.c -lm ) || return 1
  $SUDO install -m 755 "$T/bwbasic-2.20pl2.orig/bwbasic" /usr/local/bin/bwbasic || return 1
  say "source-built 2.20 installed /usr/local/bin/bwbasic sha=$(sha /usr/local/bin/bwbasic) (no seal for source builds; BOOT output is the check)"; }

build_install(){ # $1 srcdir $2 cflags $3 expected $4 dest $5 sealed-fallback
  T=$(mktemp -d /tmp/bwbbuild-XXXX); cp "$1"/*.c "$1"/*.h "$T"/ || return 1
  ( cd "$T" && gcc $2 -o out bw*.c -lm 2>/dev/null ) || { say "FAIL build $4"; return 1; }
  h=$(sha "$T/out")
  if [ "$h" = "$3" ]; then say "rebuild $4 MATCH $h"; src="$T/out"
  elif [ "$(sha "$5")" = "$3" ]; then say "rebuild $4 MISMATCH $h; installing sealed saved copy $5"; src="$5"
  else say "rebuild $4 MISMATCH $h and no sealed copy; installing rebuild (flagged)"; src="$T/out"; fi
  $SUDO install -d -m 755 "$(dirname "$4")" && $SUDO install -m 755 "$src" "$4"; }

need=0
BW=$(command -v bwbasic || true)
if [ "$MODE" = restore ] || [ -z "$BW" ] || ! is220 "$BW"; then
  say "bwbasic 2.20 on PATH: ${BW:-none} -> NEEDS RESTORE"; need=1
else say "OK bwbasic 2.20 at $BW sha=$(sha "$BW") $( [ "$(sha "$BW")" = "$EXPECT_SYS220" ] && echo MATCH-seal || echo no-seal-match)"; fi
for pair in "/opt/bwbasic-3.20b/bwbasic320:$EXPECT_320" "/opt/bwbasic-hybrid/bwbasic-unified:$EXPECT_UNI" "/opt/bwbasic-hybrid/bwbasic-hybrid:$EXPECT_HYB"; do
  f=${pair%%:*}; e=${pair##*:}; h=$(sha "$f")
  if [ "$h" = "$e" ] && [ "$MODE" != restore ]; then say "OK $f MATCH"; else say "$f sha=$h expected=$e -> NEEDS RESTORE"; need=1; fi
done

if [ $need -eq 1 ]; then
  if [ "$MODE" = verify ]; then say "verify mode: not repairing"; else
    verify_sources || exit 3
    BW=$(command -v bwbasic || true)
    if [ -z "$BW" ] || ! is220 "$BW" || [ "$MODE" = restore ]; then install_220 || { say "FAIL 2.20 install"; exit 4; }; fi
    [ "$(sha /opt/bwbasic-3.20b/bwbasic320)" = "$EXPECT_320" ] && [ "$MODE" != restore ] || build_install "$S320" "-ansi -pedantic -Wall" "$EXPECT_320" /opt/bwbasic-3.20b/bwbasic320 "$S320/bwbasic320" || exit 5
    [ "$(sha /opt/bwbasic-hybrid/bwbasic-unified)" = "$EXPECT_UNI" ] && [ "$MODE" != restore ] || build_install "$HYB/unified/src" "-O2" "$EXPECT_UNI" /opt/bwbasic-hybrid/bwbasic-unified "$HYB/unified/bwbasic-unified" || exit 5
    if [ "$(sha /opt/bwbasic-hybrid/bwbasic-hybrid)" != "$EXPECT_HYB" ] || [ "$MODE" = restore ]; then
      [ "$(sha "$HYB/src/bwbasic-hybrid")" = "$EXPECT_HYB" ] || { say "FAIL dispatcher source hash"; exit 5; }
      $SUDO install -d -m 755 /opt/bwbasic-hybrid && $SUDO install -m 755 "$HYB/src/bwbasic-hybrid" /opt/bwbasic-hybrid/bwbasic-hybrid; say "dispatcher installed MATCH"; fi
  fi
fi

# ---- final hash report
for f in /usr/bin/bwbasic /usr/local/bin/bwbasic /opt/bwbasic-3.20b/bwbasic320 /opt/bwbasic-hybrid/bwbasic-unified /opt/bwbasic-hybrid/bwbasic-hybrid; do say "HASH $f $(sha "$f")"; done

# ---- boot (fail closed)
[ "$(sha "$BOOT")" = "$EXPECT_BOOT_SHA" ] || { say "FAIL BOOT.bas hash $(sha "$BOOT") != sealed; not running"; exit 6; }
BW=$(command -v bwbasic || true); is220 "${BW:-/nonexistent}" || { say "FAIL no bwbasic 2.20 on PATH"; exit 7; }
R=$(mktemp -d /tmp/bwboot-XXXX); ( cd "$R" && timeout 20 "$BW" "$BOOT" </dev/null > boot.out 2>&1 )
oh=$(sha "$R/boot.out"); cp "$R/boot.out" "$LOGDIR/boot-$(date +%Y%m%dT%H%M%S).out"
if tr -d '\r' < "$R/boot.out" | grep -qx '0.70710678'; then
  say "BOOT PASS: $BW printed 0.70710678 (output sha $oh $( [ "$oh" = "$EXPECT_BOOT_OUT" ] && echo MATCH || echo differs-from-2026-10-18-record))"; exit 0
else say "BOOT FAIL: 0.70710678 not printed"; tr -d '\r' < "$R/boot.out"; exit 8; fi
