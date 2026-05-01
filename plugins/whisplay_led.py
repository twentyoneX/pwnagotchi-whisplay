import pwnagotchi.plugins as plugins
import logging
import sys

class WhisplayLED(plugins.Plugin):
    __author__ = 'custom'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Controls Whisplay RGB LED'

    def __init__(self):
        self.board = None

    def on_loaded(self):
        try:
            sys.path.insert(0, '/home/pi/.pwn/lib/python3.13/site-packages')
            from pwnagotchi.ui.hw.libs.whisplay.whisplaydriver import WhisPlayBoard
            self.board = WhisPlayBoard()
            self.board.set_rgb(0, 0, 0)  # LED off
            logging.info('[WhisplayLED] LED turned off')
        except Exception as e:
            logging.error(f'[WhisplayLED] Error: {e}')

    def on_handshake(self, agent, filename, access_point, client_station):
        if self.board:
            self.board.set_rgb(0, 255, 0)  # Green flash
            import time
            time.sleep(2)
            self.board.set_rgb(0, 0, 0)  # Off again
