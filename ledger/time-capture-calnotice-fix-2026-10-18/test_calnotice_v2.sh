#!/usr/bin/env bash
# test_calnotice_v2.sh: fails if any generated calendar notice contains /[0-9]{7,}/
set -u
cd "$(dirname "$0")"
pass=0; fail=0
ok(){ echo "PASS $1"; pass=$((pass+1)); }
ko(){ echo "FAIL $1"; fail=$((fail+1)); }
nodigits(){ ! printf '%s' "$1" | grep -Eq '[0-9]{7,}'; }
LOG=$(mktemp); export CALNOTICE_LOG=$LOG

# T1 the defect fixture: epoch 1792323736
out=$(./calnotice_v2.sh 1792323736 "SVCT timestamp" "Grok Build work block (abbreviated summary slot)."); rc=$?
echo "  notice: $(printf '%s' "$out" | tr '\n' '|')"
[ $rc -eq 0 ] && nodigits "$out" && ok "T1 fixture notice has no 7+ digit run" || ko "T1"
want=$(TZ=America/New_York date -d @1792323736 '+%a %b %-d %Y %-I:%M:%S %p %Z')
printf '%s' "$out" | grep -qF "Stamped $want." && ok "T2 human time = date -d @1792323736 ($want)" || ko "T2"
# T3 nanosecond input, truncated not rounded
out=$(./calnotice_v2.sh 1792323736999999999 "ns test"); rc=$?
[ $rc -eq 0 ] && nodigits "$out" && printf '%s' "$out" | grep -qF "$want" && ok "T3 ns input truncated to same second, no digit run" || ko "T3"
# T4 current time
now=$(date +%s); out=$(./calnotice_v2.sh "$now" "now test"); rc=$?
[ $rc -eq 0 ] && nodigits "$out" && ok "T4 current-time notice has no 7+ digit run" || ko "T4"
# T5 fail closed: note carrying a raw epoch is refused, nothing printed
out=$(./calnotice_v2.sh 1792323736 "SVCT" "Timestamp 1792323736" 2>/dev/null); rc=$?
[ $rc -eq 4 ] && [ -z "$out" ] && ok "T5 note with raw epoch refused (exit 4, no output)" || ko "T5 rc=$rc"
# T6 fail closed: title with a phone-like run refused
out=$(./calnotice_v2.sh 1792323736 "call 8005551234" 2>/dev/null); rc=$?
[ $rc -eq 4 ] && [ -z "$out" ] && ok "T6 title with 10-digit run refused" || ko "T6 rc=$rc"
# T7 negative control: the v1 description text from the defective event trips the grep
v1="Grok Build work block (abbreviated summary slot). Timestamp 1792323736, actually stamped 7:42:16 AM ET."
nodigits "$v1" && ko "T7 control did not trip" || ok "T7 negative control: v1 text is caught by /[0-9]{7,}/"
# T8 epoch kept for machines in the local log only
grep -q 'epoch=1792323736' "$LOG" && ok "T8 epoch recorded in local log only" || ko "T8"
# T9 bad input
./calnotice_v2.sh 12345 "x" >/dev/null 2>&1; [ $? -eq 2 ] && ok "T9 malformed epoch rejected (exit 2)" || ko "T9"
rm -f "$LOG"
echo "RESULT: $pass passed, $fail failed"
[ $fail -eq 0 ]
