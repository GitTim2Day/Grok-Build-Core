#!/bin/bash
# x_post_connecter.sh — shell wrapper for X-post ConnectEr
# OAuth 1.0a. Token from $X_POST_TOKEN_PATH (four-part: key,secret,token,token_secret)
# Fail-closed. One attempt. No auto-retry.
# Six-pillar row on success. MISS log on failure.

set -euo pipefail

TOKEN_PATH="${X_POST_TOKEN_PATH:-}"
if [[ -z "$TOKEN_PATH" || ! -f "$TOKEN_PATH" ]]; then
  echo "MISS: token file missing at \$X_POST_TOKEN_PATH" >&2
  echo "MISS,$(date -u +%Y-%m-%dT%H:%M:%SZ),token-missing," >> miss_log.csv
  exit 1
fi

# Read four-part token (one per line or colon-separated — adjust to sealed format)
mapfile -t TOKEN_PARTS < "$TOKEN_PATH"
CONSUMER_KEY="${TOKEN_PARTS[0]}"
CONSUMER_SECRET="${TOKEN_PARTS[1]}"
ACCESS_TOKEN="${TOKEN_PARTS[2]}"
ACCESS_SECRET="${TOKEN_PARTS[3]}"

POST_TEXT="${1:-}"
if [[ -z "$POST_TEXT" ]]; then
  echo "MISS: empty post text" >&2
  echo "MISS,$(date -u +%Y-%m-%dT%H:%M:%SZ),empty-text," >> miss_log.csv
  exit 1
fi

# Do-No-Harm length check (BASIC gate is primary; this is belt)
if [[ ${#POST_TEXT} -gt 280 ]]; then
  echo "MISS: length > 280" >&2
  echo "MISS,$(date -u +%Y-%m-%dT%H:%M:%SZ),length," >> miss_log.csv
  exit 1
fi

# OAuth 1.0a signature via Python (stdlib only)
SIGNATURE=$(python3 - <<'PY'
import hmac, hashlib, base64, urllib.parse, time, os, sys
text = sys.argv[1]
ck, cs, at, ase = sys.argv[2:6]
method = "POST"
url = "https://api.x.com/2/tweets"
params = {
    "oauth_consumer_key": ck,
    "oauth_nonce": str(int(time.time()*1000)),
    "oauth_signature_method": "HMAC-SHA1",
    "oauth_timestamp": str(int(time.time())),
    "oauth_token": at,
    "oauth_version": "1.0"
}
param_str = "&".join(f"{k}={urllib.parse.quote(v, safe='')}" for k,v in sorted(params.items()))
base = f"{method}&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(param_str, safe='')}"
key = f"{urllib.parse.quote(cs, safe='')}&{urllib.parse.quote(ase, safe='')}"
sig = base64.b64encode(hmac.new(key.encode(), base.encode(), hashlib.sha1).digest()).decode()
print(sig)
PY
"$POST_TEXT" "$CONSUMER_KEY" "$CONSUMER_SECRET" "$ACCESS_TOKEN" "$ACCESS_SECRET")

# Build Authorization header (simplified; full header construction left for text-session refinement)
AUTH_HEADER="OAuth oauth_consumer_key=\"$CONSUMER_KEY\", oauth_nonce=\"...\", oauth_signature=\"$SIGNATURE\", oauth_signature_method=\"HMAC-SHA1\", oauth_timestamp=\"...\", oauth_token=\"$ACCESS_TOKEN\", oauth_version=\"1.0\""

RESPONSE=$(curl -s -X POST "https://api.x.com/2/tweets" \
  -H "Authorization: $AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -d "{\"text\": $(printf '%s' "$POST_TEXT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}")

POST_ID=$(echo "$RESPONSE" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("data",{}).get("id",""))' 2>/dev/null || true)

if [[ -n "$POST_ID" ]]; then
  STAMP=$(TZ=America/New_York date '+%Y-%m-%dT%H:%M:%S%z')
  SHA=$(printf '%s' "$POST_TEXT" | sha256sum | awk '{print $1}')
  echo "HIT,$STAMP,$SHA,$POST_ID" >> local_manifest.csv
  echo "$POST_ID"
  exit 0
else
  echo "MISS,$(date -u +%Y-%m-%dT%H:%M:%SZ),api-fail,$RESPONSE" >> miss_log.csv
  echo "MISS" >&2
  exit 1
fi