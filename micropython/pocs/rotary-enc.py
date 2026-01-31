import time

from machine import Pin
from rotary_irq_rp2 import RotaryIRQ
# ------------------------------------------------------------------------------
# https://learn.adafruit.com/bluetooth-le-hid-volume-knob-with-circuitpython/build-the-ble-volume-knob
# https://learn.adafruit.com/pro-trinket-rotary-encoder/example-rotary-encoder-volume-control
# https://github.com/TTitanUA/micropython_rotary_encoder
# https://github.com/miketeachman/micropython-rotary
# ------------------------------------------------------------------------------

# ------------ WIRING --------------
# Orient with the 2 Pins at the Top
# ----------------------------------
# 2 Pins -> Button
# * Left: Input (A|D)
# * Right: GND
#
# 3 Pins -> Rotary
# * Left: Input1
# * Center: GND
# * Right: Input2
# ----------------------------------
# * ESP32 has an Encoder class: `from machine import Encoder`
# ----------------------------------

# The Button
count = 0
button = Pin(2, Pin.IN, Pin.PULL_UP)


def button_handler(pin):
    global count
    count += 1
    print(f"Button Press #{count}")
    time.sleep_ms(25)


button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# The Rotary Encoder
rot_r = Pin(4, Pin.IN, Pin.PULL_UP)
rot_l = Pin(5, Pin.IN, Pin.PULL_UP)

## CCaroon
# def rotate_right(pin):
#     print("-> Right ->")
#     time.sleep_ms(5)

# rot_r.irq(trigger=Pin.IRQ_FALLING, handler=rotate_right)

# def rotate_left(pin):
#     print("<- Left <-")
#     time.sleep_ms(5)

# rot_l.irq(trigger=Pin.IRQ_FALLING, handler=rotate_left)

## Mike Teachman
rotary = RotaryIRQ(
    rot_r,
    rot_l,
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
old_enc_val = rotary.value()
while True:
    # Main program can do other tasks
    # print("...nothing happening...")

    enc_val = rotary.value()
    if enc_val != old_enc_val:
        print(f"Encoder Value [{enc_val}]")
        old_enc_val = enc_val

    time.sleep_ms(50)





#
