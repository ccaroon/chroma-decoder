# BASIC
# from machine import Pin
# import time

# # Wiring
# #
# # * Button/leg1 -> Pin2
# # * Button/leg2 -> GND


# count = 0
# button = Pin(2, Pin.IN, Pin.PULL_UP)

# print("Press the button...")

# while True:
#     if button.value() == 0:
#         count += 1
#         print(f"Button Press #{count}")

#     # Debounce delay
#     time.sleep(0.1)

# -----------------------------------------------------------

# IRQ Based
from machine import Pin
import time

count = 0
button = Pin(2, Pin.IN, Pin.PULL_UP)


def button_handler(pin):
    global count
    count += 1
    print(f"Button Press #{count}")


button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

while True:
    # Main program can do other tasks
    print("...nothing happening...")
    time.sleep(1)
