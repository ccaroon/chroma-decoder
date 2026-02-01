from machine import Pin
from rotary_irq_rp2 import RotaryIRQ


class Controls:
    __BUTTON_PIN = 2
    __ROTARY_PIN1 = 4
    __ROTARy_PIN2 = 5

    def __init__(self, dial_pos_count, button_handler):
        button = Pin(self.__BUTTON_PIN, Pin.IN, Pin.PULL_UP)
        button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

        # The Rotary Encoder
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

    # def __handle_button(self, btn):
    #     global active_pixel
    #     global active_color

    #     if btn.value() == 0:
    #         # incase it's off b/c of blinky, blinky
    #         neo[active_pixel] = SHOW_COLORS[active_color]

    #         active_pixel += 1
    #         if active_pixel >= PIXEL_COUNT:
    #             active_pixel = 0

    #         if neo[active_pixel] == COLORS["off"]:
    #             neo[active_pixel] = SHOW_COLORS[active_color]
    #         else:
    #             active_color = SHOW_COLORS.index(neo[active_pixel])
    #             # update the rotary so that the next turn will start
    #             # where the pixel left off
    #             self.__dial.set(value=active_color)

    #         neo.write()

    #         # Debounce
    #         while btn.value() == 0:
    #             pass
    #         time.sleep_ms(10)
