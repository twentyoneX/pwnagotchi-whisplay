import logging
import numpy as np

import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.hw.base import DisplayImpl


class Whisplay(DisplayImpl):
    def __init__(self, config):
        super(Whisplay, self).__init__(config, 'whisplay')
        self._display = None

    def layout(self):
        fonts.setup(10, 9, 10, 35, 25, 9)
        self._layout['width'] = 280
        self._layout['height'] = 240
        self._layout['face'] = (0, 50)
        self._layout['name'] = (20, 2)
        self._layout['channel'] = (20, 16)
        self._layout['aps'] = (55, 16)
        self._layout['uptime'] = (190, 16)
        self._layout['line1'] = [0, 30, 280, 30]
        self._layout['line2'] = [0, 218, 280, 218]
        self._layout['friend_face'] = (0, 140)
        self._layout['friend_name'] = (40, 142)
        self._layout['shakes'] = (20, 220)
        self._layout['mode'] = (220, 220)
        self._layout['status'] = {
            'pos': (160, 80),
            'font': fonts.status_font(fonts.Small),
            'max': 18
        }
        return self._layout

    def initialize(self):
        logging.info("Initializing Whisplay with PiSugar WhisPlayBoard driver")
        from pwnagotchi.ui.hw.libs.whisplay.whisplaydriver import WhisPlayBoard
        self._display = WhisPlayBoard()
        self._display.set_rgb(0, 0, 0)
        self._display.set_backlight(50)

    def render(self, canvas):
        logging.info(f"Canvas size: {canvas.size} mode: {canvas.mode}")
        img = canvas.convert('RGB').resize((280, 240))
        img = img.rotate(90, expand=True)
        pixel_data = []
        for y in range(280):
            for x in range(240):
                r, g, b = img.getpixel((x, y))
                rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
                pixel_data.extend([(rgb565 >> 8) & 0xFF, rgb565 & 0xFF])
        self._display.draw_image(0, 0, 240, 280, pixel_data)

    def clear(self):
        self._display.fill_screen(0)
