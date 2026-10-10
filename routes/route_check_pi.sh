#!/bin/bash
# route_check_pi.sh -- read every register source that refuses automated reads from the
# chat side (robots.txt, JavaScript-only pages). Runs on the Pi or the A15 on request; no daemon.
# Author: Timothy Norman (sole author). Claude = tool/validator. 2026-10-10.
# Usage:  bash route_check_pi.sh            -> ~/work/route_check_YYYYMMDD_HHMMSS.tsv
# Each row: register page id, source, HTTP code, bytes, first 120 printable characters.
# Not included on purpose: Stack Exchange (blocked for the assistant's fetch tool for legal
# reasons; open it yourself in a browser).
set -u
OUT="$HOME/work/route_check_$(date +%Y%m%d_%H%M%S).tsv"
mkdir -p "$HOME/work"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT
printf 'page_id\tsource\thttp\tbytes\tfirst_120\n' > "$OUT"
while IFS='|' read -r ID NAME URL; do
  [ -z "$ID" ] && continue
  case "$ID" in \#*) continue ;; esac
  RES=$(curl -sS -L -m 25 -A "Mozilla/5.0 (X11; Linux aarch64) route-check" -o "$TMP" -w '%{http_code}|%{size_download}' "$URL" 2>/dev/null || echo "000|0")
  CODE=${RES%%|*}; BYTES=${RES##*|}
  HEAD=$(head -c 400 "$TMP" 2>/dev/null | tr -d '\r' | tr '\n\t' '  ' | tr -cd '[:print:]' | cut -c1-120)
  printf '%s\t%s\t%s\t%s\t%s\n' "$ID" "$NAME" "$CODE" "$BYTES" "$HEAD" >> "$OUT"
  printf '%s  %s  %s bytes  %s\n' "$CODE" "$NAME" "$BYTES" "$URL"
done <<'LIST'
3eec86699c94810aaf73e1d3f3243203|Brazil IBGE data service|https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome
3eec86699c94816e82e4dd8338f50989|Openverse API|https://api.openverse.org/v1/images/?q=lighthouse
3eec86699c948177a840c5fdd3176607|Crystallography Open Database|https://www.crystallography.net/cod/1000000.cif
3eec86699c94813da1a1d3fb625c26e2|data.europa.eu search API|https://data.europa.eu/api/hub/search/search?q=lidar&limit=1
3eec86699c9481d7b143fe524f6b90fe|ECB data API|https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata
3eec86699c9481ffb4b6ea6500a27617|Gallica BnF SRU|https://gallica.bnf.fr/SRU?operation=searchRetrieve&version=1.2&query=gallica%20all%20%22euclide%22&maximumRecords=1
3eec86699c948157bdf0fe462189a746|iNaturalist API|https://api.inaturalist.org/v1/observations?per_page=1
3eec86699c94819fb10bd69c343958ef|Open Food Facts API|https://world.openfoodfacts.org/api/v2/product/737628064502.json
3eec86699c9481109d8ff3b4b2665069|MatWeb|https://www.matweb.com/
3eec86699c948110ad38d69c073ef876|OpenNeuro GraphQL|https://openneuro.org/crn/graphql?query=%7Bdatasets(first:1)%7BpageInfo%7Bcount%7D%7D%7D
3eec86699c948169a014f2e28a127ac7|DANDI API|https://api.dandiarchive.org/api/dandisets/?page_size=1
3eec86699c94818ca9e0f646fe4e0991|OSF API|https://api.osf.io/v2/nodes/?filter[title]=lidar
3eec86699c94813a8c83d0812dfa47c8|OSTI.gov API|https://www.osti.gov/api/v1/records?q=lidar&rows=1
3eec86699c94812c8540c7cc1cb9d9a6|PDG REST API|https://pdgapi.lbl.gov/summaries/S126M
3eec86699c94818c9fcffc2a7be0fd76|AlphaFold DB API|https://alphafold.ebi.ac.uk/api/prediction/P20273
3eec86699c9481eb918cf01b21438b39|PyPI JSON API|https://pypi.org/pypi/pcbasic/json
3eec86699c9481319a83e81fb9b57524|Statistics Canada WDS|https://www150.statcan.gc.ca/t1/wds/rest/getCodeSets
3eec86699c9481fabf35d9f020992bf2|Sefaria API|https://api.sefaria.org/api/v3/texts/Genesis.1.1
3e9c86699c9481d78beacca69c06026d|Chronicling America|https://chroniclingamerica.loc.gov/search/pages/results/?andtext=lidar&format=json&rows=1
3f5c86699c94814e82edd6ae4ae26054|code.gov|https://code.gov
3e9c86699c94811d81bee652d53984ca|Congress.gov API docs|https://api.congress.gov/
LIST
echo "DONE -> $OUT  ($(($(wc -l < "$OUT") - 1)) sources)"
