# Pwnagotchi + PiSugar Whisplay

Display driver and RGB LED plugin for running [jayofelony's Pwnagotchi](https://github.com/jayofelony/pwnagotchi) on the [PiSugar Whisplay HAT](https://docs.pisugar.com/).

---

## Hardware

| Component | Details |
|-----------|---------|
| Display | 1.69" IPS LCD, 240×280px, SPI (ST7789) |
| RGB LED | PWM controlled |
| Button | 1x programmable button |
| Interface | SPI + I2C |

### Pin Mapping (BOARD numbering)

| Signal | Physical Pin |
|--------|-------------|
| 5V | 2, 4 |
| GND | any GND |
| I2C SDA | 3 |
| I2C SCL | 5 |
| Backlight | 15 |
| SPI SCLK | 23 |
| SPI MOSI | 19 |
| SPI CS/CE0 | 24 |
| SPI D/C | 13 |
| SPI RST | 7 |
| RGB Red | 22 |
| RGB Green | 18 |
| RGB Blue | 16 |
| Button | 11 |

---

## Requirements

- Raspberry Pi Zero W or Zero 2W
- [jayofelony/pwnagotchi](https://github.com/jayofelony/pwnagotchi) v2.9.5.4+
- PiSugar Whisplay HAT

---

## Installation

### Step 1 — Flash pwnagotchi image

Download and flash the latest image from [jayofelony/pwnagotchi releases](https://github.com/jayofelony/pwnagotchi/releases).

### Step 2 — SSH into your Pwnagotchi

```bash
ssh pi@10.0.0.2
```

### Step 3 — Clone and run the installer

```bash
git clone https://github.com/twentyoneX/pwnagotchi-whisplay.git
cd pwnagotchi-whisplay
chmod +x install.sh
sudo ./install.sh
```

### Step 4 — Update config.toml

Edit `/etc/pwnagotchi/config.toml` and update the display section:

```toml
[ui.display]
enabled = true
type = "whisplay"
color = "rgb"
rotation = 0
xres = 240
yres = 280

[main.plugins.whisplay_led]
enabled = true

[main.plugins.memtemp]
enabled = true
scale = "celsius"
orientation = "horizontal"
position = "200, 185"
```

### Step 5 — Restart Pwnagotchi

```bash
sudo systemctl restart pwnagotchi
```

---

## RGB LED Behavior

The `whisplay_led` plugin controls the RGB LED on the Whisplay board:

| Color | Event |
|-------|-------|
| ⚪ White | Booting |
| 🔵 Blue | Ready / Idle |
| 🔵 Cyan | Scanning |
| 🟠 Orange | Associating with AP |
| 🟢 Green (3x flash) | Handshake captured! |
| 🟣 Purple | Friend nearby |
| 🔴 Red-orange (flash) | Deauthing client |
| ⚫ Off | Sleeping |

---

## File Structure

```
pwnagotchi-whisplay/
├── README.md
├── install.sh
├── hw/
│   ├── whisplay.py                   # Display driver
│   └── libs/
│       └── whisplay/
│           ├── __init__.py
│           └── whisplaydriver.py     # Hardware driver
└── plugins/
    └── whisplay_led.py               # RGB LED plugin
```

---

## Credits

- Hardware driver by [PiSugar](https://github.com/PiSugar/Whisplay)
- Pwnagotchi fork by [jayofelony](https://github.com/jayofelony/pwnagotchi)
- Integration by the Pwnagotchi community

---

## License

MIT
