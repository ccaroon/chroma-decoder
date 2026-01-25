import random
import time

from machine import Pin
from neopixel import NeoPixel

COLORS = {
    "red": (255, 0, 0),
    "pink": (255,2,141),
    "orange": (249,115,6),
    "yellow": (255,255,0),
    "green": (0, 255, 0),
    "cyan": (0,190,255),
    "blue": (0, 0, 255),
    "purple": (64,0,255),
    # --- support colors ---
    "off": (0,0,0),
    "white": (255,255,255),
    "ok_green": (73,233,72)
}
COLOR_LIST = list(COLORS.values())
COLOR_CNT = len(COLOR_LIST)

pin = Pin(2, Pin.OUT)
neo = NeoPixel(pin, 40)

SHOW_COLORS = [
    COLORS["red"],
    COLORS["pink"],
    COLORS["orange"],
    COLORS["yellow"],
    COLORS["green"],
    COLORS["cyan"],
    COLORS["blue"],
    COLORS["purple"],
]

while True:
    for idx in range(0,40):
        neo[idx] = SHOW_COLORS[idx % 8]

        neo.write()
        time.sleep(.25)
