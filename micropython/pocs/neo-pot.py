from machine import ADC, Pin
from neopixel import NeoPixel

# ----------------------------------
# --- Wiring ---
# For KB2040
#
# * 3V      -> P+  // Pots +
# * GND     -> P-  // Pots -
# * D2/02   -> NiN // NeoPizel In
# * A0(26)  -> POT // Pots In
# ----------------------------------

COLOR_LIST = [
    (255, 0, 0),  # red
    # (255, 128, 0), # orange
    # (255, 255, 0), # yellow
    (0, 255, 0),  # green
    (0, 0, 255),  # blue
    (128, 0, 255),  # purple
]
NUM_COLORS = len(COLOR_LIST)

POTS_DIV = 65_535 / NUM_COLORS
POTS_BUFF_SIZE = 5

pin = Pin(2, Pin.OUT)
neo = NeoPixel(pin, 1)
pots = ADC(Pin(26))

pots_buffer = []


def average(values):
    avg = 0
    if values:
        avg = sum(values) / len(values)

    return avg


prev_clr_idx = None
while True:
    pots_buffer.append(pots.read_u16())
    if len(pots_buffer) > POTS_BUFF_SIZE:
        pots_buffer.pop(0)

    value = average(pots_buffer)
    clr_idx = int(value / POTS_DIV)
    # print(f"POTS -> {value} -> ClrIdx: {clr_idx}")

    if clr_idx != prev_clr_idx:
        neo[0] = COLOR_LIST[clr_idx]
        neo.write()
        prev_clr_idx = clr_idx

    # time.sleep(.5)
