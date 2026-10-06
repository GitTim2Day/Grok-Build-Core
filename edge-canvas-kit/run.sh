#!/bin/sh
# run.sh -- start the edge-canvas-kit (Pi 5 / Linux / macOS). Needs only python3 + a browser.
#   ./run.sh              this device only  -> http://127.0.0.1:8765
#   ./run.sh --lan        home network (prints a token URL for the phone)
#   ./run.sh --kiosk      this device + Chromium full-screen kiosk (if chromium is installed)
#   ./run.sh --check      run the self-tests (python3 selfcheck.py --quick)
cd "$(dirname "$0")" || exit 1
PY=python3
command -v "$PY" >/dev/null 2>&1 || { echo "python3 not found (Raspberry Pi OS ships it)"; exit 1; }
case "$1" in
  --check) exec "$PY" selfcheck.py --quick ;;
  --kiosk)
    shift
    "$PY" server.py "$@" &
    SRV=$!
    sleep 2
    for B in chromium chromium-browser google-chrome; do
      if command -v "$B" >/dev/null 2>&1; then
        "$B" --kiosk --noerrdialogs --disable-infobars --no-first-run --disable-background-networking \
             --disable-component-update "http://127.0.0.1:8765/"
        break
      fi
    done
    echo "browser closed; stopping server"; kill "$SRV" 2>/dev/null; exit 0 ;;
  *) exec "$PY" server.py "$@" ;;
esac
