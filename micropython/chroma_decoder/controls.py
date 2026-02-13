from machine import Pin
from rotary_irq_rp2 import RotaryIRQ


class Controls:
    BUTTON_LONG_PRESS_MS = 500

    __BUTTON_PIN = 2
    __ROTARY_PIN1 = 4
    __ROTARy_PIN2 = 5

    def __init__(self, dial_pos_count, button_handler):
        # The Rotary Encoder - Button
        button = Pin(self.__BUTTON_PIN, Pin.IN, Pin.PULL_UP)
        button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

        # The Rotary Encoder - Dial
        self.__dial = RotaryIRQ(
            Pin(self.__ROTARY_PIN1, Pin.IN, Pin.PULL_UP),
            Pin(self.__ROTARy_PIN2, Pin.IN, Pin.PULL_UP),
            min_val=0,
            max_val=dial_pos_count,
            incr=1,
            reverse=False,
            range_mode=RotaryIRQ.RANGE_WRAP,
            pull_up=True,
            half_step=False,
            invert=False,
        )

    @property
    def dial(self):
        return self.__dial
