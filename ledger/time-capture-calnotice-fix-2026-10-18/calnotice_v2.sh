#!/usr/bin/env bash
# calnotice_v2.sh  (time-capture calendar notice builder, v2, 2026-10-18)
# Fix for D-2026-10-18-01: a calendar description carried a raw Unix timestamp
# (1792323736) that the calendar app auto-linked as a phone number.
#
# Usage: calnotice_v2.sh EPOCH "Title" ["Note"]
#   EPOCH : Unix seconds (10 digits) or nanoseconds (19 digits, truncated to s)
#   Title : short title; "GB: " is prefixed
#   Note  : optional first sentence of the description
# Prints two lines, TITLE: and DESCRIPTION:, for create_event summary/description.
# Rules:
#   - time shown human-readable in America/New_York, e.g. "Sun Oct 18 2026 7:42:16 AM EDT"
#   - the epoch itself NEVER appears in calendar text; it goes only to the local
#     log file named by $CALNOTICE_LOG (if set)
#   - fail closed: any run of 7+ digits in the final title/description -> exit 4, nothing printed
#   - seconds are truncated, never rounded
set -u
TZ_NAME=America/New_York
e=${1:-}; title=${2:-}; note=${3:-}
if [[ ! $e =~ ^[0-9]+$ ]]; then echo "calnotice_v2: EPOCH must be digits" >&2; exit 2; fi
case ${#e} in
  10) s=$e ;;
  19) s=${e:0:10} ;;
  *) echo "calnotice_v2: EPOCH must be 10 (s) or 19 (ns) digits" >&2; exit 2 ;;
esac
[ -n "$title" ] || { echo "calnotice_v2: Title required" >&2; exit 2; }
human=$(TZ=$TZ_NAME date -d "@$s" '+%a %b %-d %Y %-I:%M:%S %p %Z') || exit 2
t_line="GB: $title"
d_line="${note:+$note }Stamped $human."
if printf '%s\n%s\n' "$t_line" "$d_line" | grep -Eq '[0-9]{7,}'; then
  echo "calnotice_v2: REFUSED - title/note contains a run of 7+ digits (would render as a phone link); remove it" >&2
  exit 4
fi
if [ -n "${CALNOTICE_LOG:-}" ]; then
  printf '%s\tepoch=%s\thuman=%s\ttitle=%s\n' "$(TZ=$TZ_NAME date '+%Y-%m-%dT%H:%M:%S%:z')" "$s" "$human" "$t_line" >> "$CALNOTICE_LOG"
fi
printf 'TITLE: %s\nDESCRIPTION: %s\n' "$t_line" "$d_line"
