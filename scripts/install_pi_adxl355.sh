#!/bin/sh
# Run ON the Pi 5 after Wi-Fi is up.
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/GitTim2Day/Grok-Build-Core/main/scripts/install_pi_adxl355.sh | sh
set -eu
DEST="${HOME}/pi_adxl355_link.py"
URL="https://raw.githubusercontent.com/GitTim2Day/Grok-Build-Core/main/scripts/pi_adxl355_link.py"

sudo apt-get update
sudo apt-get install -y python3-smbus2 i2c-tools

curl -fsSL "$URL" -o "$DEST"
chmod +x "$DEST"

echo "Wrote $DEST"
echo "Probe the bus:  i2cdetect -y 1"
echo "Expect 1d or 53 before any claim."
echo "Then:  python3 $DEST"
