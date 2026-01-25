import random
import time

from machine import Pin
from neopixel import NeoPixel

COLORS = {
    # "black":  (0,0,0),
    "red": (255, 0, 0),
    "orange": (255, 128, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "indigo": (75, 0, 255),
    "violet": (128, 0, 255),
}
COLOR_LIST = list(COLORS.values())

pin = Pin(2, Pin.OUT)
neo = NeoPixel(pin, 5)

while True:
    neo[0] = COLOR_LIST[random.randint(0, 5)]
    neo[1] = COLOR_LIST[random.randint(0, 5)]
    neo[2] = COLOR_LIST[random.randint(0, 5)]
    neo[3] = COLOR_LIST[random.randint(0, 5)]
    neo[4] = COLOR_LIST[random.randint(0, 5)]

    neo.write()
    time.sleep(2)
