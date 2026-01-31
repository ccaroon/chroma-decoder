import time

from machine import Pin
from rotary_irq_rp2 import RotaryIRQ
from neopixel import NeoPixel

# NeoPixels
COLORS = {
    "red": (255, 0, 0),
    "pink": (255, 2, 141),
    "orange": (249, 115, 6),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "cyan": (0, 190, 255),
    "blue": (0, 0, 255),
    "purple": (64, 0, 255),
    # --- support colors ---
    "off": (0, 0, 0),
    "white": (255, 255, 255),
    "ok_green": (73, 233, 72),
}
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
COLOR_COUNT = len(SHOW_COLORS)

PIXEL_COUNT = 5
pin = Pin(7, Pin.OUT)
neo = NeoPixel(pin, PIXEL_COUNT)


def blink_active_pixel():
    global active_pixel
    global active_color

    color = SHOW_COLORS[active_color] if neo[active_pixel] == COLORS["off"] else COLORS["off"]

    neo[active_pixel] = color
    neo.write()


# The Button
button = Pin(2, Pin.IN, Pin.PULL_UP)

def check_button(btn):
    global active_pixel
    global active_color

    if btn.value() == 0:
        # incase it's off b/c of blinky, blinky
        neo[active_pixel] = SHOW_COLORS[active_color]

        active_pixel += 1
        if active_pixel >= PIXEL_COUNT:
            active_pixel = 0

        if neo[active_pixel] == COLORS["off"]:
            neo[active_pixel] = SHOW_COLORS[active_color]
        else:
            # neo[active_pixel] =
            active_color = neo[active_pixel]

        neo.write()


# button.irq(trigger=Pin.IRQ_FALLING, handler=check_button)


# The Rotary Encoder
rotary = RotaryIRQ(
    Pin(4, Pin.IN, Pin.PULL_UP),
    Pin(5, Pin.IN, Pin.PULL_UP),
    min_val=0,
    max_val=7,
    incr=1,
    reverse=False,
    range_mode=RotaryIRQ.RANGE_WRAP,
    pull_up=True,
    half_step=False,
    invert=False,
)


# Main Loop
active_pixel = 0
active_color = 0
neo[active_pixel] = SHOW_COLORS[active_color]
neo.write()
while True:
    # Check Rotary Encoder
    enc_val = rotary.value()
    if enc_val != active_color:
        active_color = enc_val
        neo[active_pixel] = SHOW_COLORS[active_color]
        neo.write()

    # Check Button
    check_button(button)

    blink_active_pixel()

    time.sleep_ms(50)


#
