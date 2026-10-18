#!/usr/bin/env bash
# timecap.sh - fresh-clock capture, bash implementation (feature id time-capture-auto-2026-10-18).
# Same stamp format, canonical hash and status lines as timecap.py; stamps are interchangeable.
#   fetch | status | open | close      [--stamp PATH]  (else $TIMECAP_STAMP, else default)
# The stamp time always comes from this script's own clock reads (date +%s%N = CLOCK_REALTIME,
# /proc/uptime = CLOCK_BOOTTIME, 10 ms resolution). No command takes a time argument.
# Exit: 0 fresh, 1 stale, 2 unverified (missing/corrupt/hash), 3 unverified (skew/future/boot/external).
# Test-only: TIMECAP_TEST_NOW="<wall_ns>:<mono_ns>" overrides "now" for 'status' only, and every
# line printed then ends with " [TEST CLOCK]".
set -u
TZ_NAME="America/New_York"
DEFAULT_STAMP="/workspace/time-capture/last_fetch.json"
FRESH_MAX_NS=60000000000
SKEW_MAX_NS=2000000000
EXT_SKEW_MAX_S=5
EXT_URL=${TIMECAP_EXT_URL:-https://www.google.com}  # override is for tests
LINE_NOFETCH="Time UNVERIFIED: no fetch available"
LINE_SKEW="Time UNVERIFIED: clock skew detected"
LINE_BOOT="Time UNVERIFIED: stamp is from a different boot (monotonic check impossible)"

boot_id() { cat /proc/sys/kernel/random/boot_id 2>/dev/null || echo unknown; }

mono_ns() {  # /proc/uptime first field "SSSS.CC" -> ns (truncated, never rounded)
  local up; read -r up _ < /proc/uptime || return 1
  local s=${up%.*} c=${up#*.}
  c=$(( 10#${c}0000000 )); c=${c:0:9}
  echo $(( 10#$s * 1000000000 + 10#$c ))
}

iso_local() { local s=$(( $1 / 1000000000 )) f=$(( $1 % 1000000000 ))
  printf '%s.%09d%s' "$(TZ=$TZ_NAME date -d "@$s" +%Y-%m-%dT%H:%M:%S)" "$f" "$(TZ=$TZ_NAME date -d "@$s" +%:z)"; }
iso_utc() { local s=$(( $1 / 1000000000 )) f=$(( $1 % 1000000000 ))
  printf '%s.%09dZ' "$(TZ=UTC date -d "@$s" +%Y-%m-%dT%H:%M:%S)" "$f"; }

canon_hash() {  # args: epoch iso_local iso_utc tz mono mono_clock host boot writer
  printf 'v1|%s|%s|%s|%s|%s|%s|%s|%s|%s' "$@" | sha256sum | cut -d' ' -f1; }

do_fetch() {
  local path=$1 wall mono
  wall=$(date +%s%N) || return 1
  mono=$(mono_ns) || return 1
  local il iu host bid h
  il=$(iso_local "$wall"); iu=$(iso_utc "$wall"); host=$(hostname); bid=$(boot_id)
  h=$(canon_hash "$wall" "$il" "$iu" "$TZ_NAME" "$mono" CLOCK_BOOTTIME "$host" "$bid" timecap.sh)
  mkdir -p "$(dirname "$path")" || return 1
  local tmp="$path.tmp.$$"
  jq -n --argjson e "$wall" --arg il "$il" --arg iu "$iu" --arg tz "$TZ_NAME" --argjson m "$mono" \
     --arg mc CLOCK_BOOTTIME --arg host "$host" --arg bid "$bid" --arg w timecap.sh --arg h "$h" \
     '{boot_id:$bid,fetch_epoch_ns:$e,host:$host,iso_local:$il,iso_utc:$iu,monotonic_clock:$mc,
       monotonic_ns:$m,sha256:$h,tz:$tz,writer:$w}' > "$tmp" || { rm -f "$tmp"; return 1; }
  mv -f "$tmp" "$path"   # atomic swap; the stamp is a runtime cache
  FETCHED_ISO=$il
}

# load PATH -> sets S_* vars; returns 1 if missing/corrupt/bad types/hash mismatch
load() {
  local path=$1 out
  [ -f "$path" ] || return 1
  out=$(jq -r '
    if type != "object" then error("notobj") else . end
    | [ (.fetch_epoch_ns|tojson), (.monotonic_ns|tojson) ] as $n
    | if ([.iso_local,.iso_utc,.tz,.monotonic_clock,.host,.boot_id,.writer,.sha256] | all(type=="string"))
         and ([.fetch_epoch_ns,.monotonic_ns] | all(type=="number"))
         and ($n | all(test("^-?[0-9]+$")))
      then [$n[0], .iso_local, .iso_utc, .tz, $n[1], .monotonic_clock, .host, .boot_id, .writer, .sha256]
           | map(gsub("[\n\t]";" ")) | join("\t")
      else error("types") end' "$path" 2>/dev/null) || return 1
  [ -n "$out" ] || return 1
  IFS=$'\t' read -r S_E S_IL S_IU S_TZ S_M S_MC S_HOST S_BID S_W S_H <<< "$out" || return 1
  [ "$S_TZ" = "$TZ_NAME" ] || return 1
  [ "$(canon_hash "$S_E" "$S_IL" "$S_IU" "$S_TZ" "$S_M" "$S_MC" "$S_HOST" "$S_BID" "$S_W")" = "$S_H" ] || return 1
  [ "$S_IL" = "$(iso_local "$S_E")" ] || return 1
  [ "$S_IU" = "$(iso_utc "$S_E")" ] || return 1
  return 0
}

do_status() {
  local path=$1 tag="" now_w now_m
  if [ -n "${TIMECAP_TEST_NOW:-}" ]; then
    now_w=${TIMECAP_TEST_NOW%%:*}; now_m=${TIMECAP_TEST_NOW#*:}; tag=" [TEST CLOCK]"
    [[ $now_w =~ ^[0-9]+$ && $now_m =~ ^[0-9]+$ ]] || { echo "$LINE_NOFETCH [BAD TEST CLOCK]"; return 2; }
  else
    now_w=$(date +%s%N); now_m=$(mono_ns)
  fi
  if ! load "$path"; then echo "$LINE_NOFETCH$tag"; return 2; fi
  if [ "$S_BID" != "$(boot_id)" ]; then echo "$LINE_BOOT$tag"; return 3; fi
  local wa=$(( now_w - S_E )) ma=$(( now_m - S_M )) d
  d=$(( wa - ma )); [ $d -lt 0 ] && d=$(( -d ))
  if [ $wa -lt 0 ] || [ $d -gt $SKEW_MAX_NS ]; then echo "$LINE_SKEW$tag"; return 3; fi
  local s=$(( S_E / 1000000000 )) t hms
  t=$(TZ=$TZ_NAME date -d "@$s" "+%-I:%M %p %Z"); hms=$(TZ=$TZ_NAME date -d "@$s" +%H:%M:%S)
  if [ $wa -le $FRESH_MAX_NS ]; then
    echo "Time (fresh fetch): $t, fetched $hms$tag"; return 0
  fi
  echo "Time: $t — STALE, fetched $(( wa / 1000000000 )) s ago$tag"; return 1
}

external_check() {  # sets EXT_STATE ok|skew|skipped, EXT_DELTA
  EXT_STATE=skipped; EXT_DELTA=""
  [ "${TIMECAP_NO_NET:-}" = "1" ] && return 0
  local hdr remote local_s
  hdr=$(curl -sI -m 3 "$EXT_URL" 2>/dev/null | tr -d '\r' | sed -n 's/^[Dd]ate: //p' | head -n1)
  local_s=$(date +%s)
  [ -n "$hdr" ] || return 0
  remote=$(date -d "$hdr" +%s 2>/dev/null) || return 0
  EXT_DELTA=$(( local_s - remote ))
  local a=$EXT_DELTA; [ $a -lt 0 ] && a=$(( -a ))
  if [ $a -gt $EXT_SKEW_MAX_S ]; then EXT_STATE=skew; else EXT_STATE=ok; fi
}

do_open_close() {
  local path=$1 rc
  do_fetch "$path" || { echo "$LINE_NOFETCH"; return 2; }
  external_check
  if [ "$EXT_STATE" = skew ]; then
    printf 'Time UNVERIFIED: external clock skew detected (%+d s vs %s Date header)\n' "$EXT_DELTA" "$EXT_URL"; return 3
  fi
  unset TIMECAP_TEST_NOW
  do_status "$path"; rc=$?
  if [ "$EXT_STATE" = ok ]; then
    printf 'External check: ok (%+d s vs %s Date header, limit %d s)\n' "$EXT_DELTA" "$EXT_URL" "$EXT_SKEW_MAX_S"
  else
    echo "External check: skipped (network unavailable or disabled)"
  fi
  return $rc
}

main() {
  local path=${TIMECAP_STAMP:-$DEFAULT_STAMP} args=()
  while [ $# -gt 0 ]; do
    if [ "$1" = "--stamp" ]; then path=${2:-}; shift 2 || { echo "usage" >&2; return 64; }
    else args+=("$1"); shift; fi
  done
  [ ${#args[@]} -eq 1 ] || { echo "usage: timecap.sh [--stamp PATH] fetch|status|open|close" >&2; return 64; }
  case ${args[0]} in
    fetch) do_fetch "$path" || { echo "$LINE_NOFETCH"; return 2; }; echo "fetched $FETCHED_ISO -> $path" ;;
    status) do_status "$path" ;;
    open|close) do_open_close "$path" ;;
    *) echo "usage: timecap.sh [--stamp PATH] fetch|status|open|close" >&2; return 64 ;;
  esac
}
main "$@"
