#!/bin/bash
set -e

PWNY_PATH=$(find /home/pi/.pwn/lib -maxdepth 1 -type d -name "python3*" 2>/dev/null | sort -V | tail -1)

if [ -z "$PWNY_PATH" ]; then
    echo "ERROR: pwnagotchi not found"
    exit 1
fi

HW_PATH="$PWNY_PATH/site-packages/pwnagotchi/ui/hw"

echo "[1/5] Installing whisplay.py..."
cp hw/whisplay.py "$HW_PATH/whisplay.py"

echo "[2/5] Installing whisplaydriver..."
mkdir -p "$HW_PATH/libs/whisplay"
cp hw/libs/whisplay/whisplaydriver.py "$HW_PATH/libs/whisplay/whisplaydriver.py"
cp hw/libs/whisplay/__init__.py "$HW_PATH/libs/whisplay/__init__.py"

echo "[3/5] Installing plugin..."
mkdir -p /usr/local/share/pwnagotchi/custom-plugins
cp plugins/whisplay_led.py /usr/local/share/pwnagotchi/custom-plugins/whisplay_led.py

echo "[4/5] Patching __init__.py..."
HW_INIT="$HW_PATH/__init__.py"
if ! grep -q "whisplay" "$HW_INIT"; then
    echo "
    elif config['ui']['display']['type'] == 'whisplay':
        from pwnagotchi.ui.hw.whisplay import Whisplay
        return Whisplay(config)" >> "$HW_INIT"
fi

echo "[5/5] Patching utils.py..."
UTILS="$PWNY_PATH/site-packages/pwnagotchi/utils.py"
if ! grep -q "whisplay" "$UTILS"; then
    sed -i "s/elif config\['ui'\]\['display'\]\['type'\] in ('wavesharelcd1in47'/elif config['ui']['display']['type'] in ('whisplay',):\n        config['ui']['display']['type'] = 'whisplay'\n    elif config['ui']['display']['type'] in ('wavesharelcd1in47'/" "$UTILS"
fi

echo ""
echo "Done! Update /etc/pwnagotchi/config.toml:"
echo ""
echo "  [ui.display]"
echo "  type = \"whisplay\""
echo "  color = \"rgb\""
echo ""
echo "Then: sudo systemctl restart pwnagotchi"
