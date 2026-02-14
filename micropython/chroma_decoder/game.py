import time

from machine import Timer

from chroma_decoder.color_set import ColorSet
from chroma_decoder.controls import Controls
from chroma_decoder.display import Display
from chroma_decoder.level import Level


class Game:
    __BLINKER_PERIOD = 300

    def __init__(self):
        # Display
        self.__color_set = ColorSet("default")
        self.__display = Display(
            rows=5,
            cols=8,
            color_set=self.__color_set,
            rotated=True,
        )

        # Controls
        self.__controls = Controls(
            self.__color_set.count - 1,
            self.__button_handler,
        )

        # Cause the Active Pixel to blink every-so-often
        blinker = Timer(-1)
        blinker.init(
            mode=Timer.PERIODIC,
            period=self.__BLINKER_PERIOD,
            callback=self.__display.blink_active_pixel,
        )

        # Init the first level / secret code
        self.__level = self.__gen_level()

    def __gen_level(self):
        # reset display
        self.__display.reset()

        # gen new level
        # color / order / position
        new_level = Level(5, self.__color_set.count)
        print("Code: ", new_level.code)

        return new_level

    def __button_short_press(self):
        # incase it's off b/c of blinky, blinky
        self.__display.set_active_pixel(self.__display.active_color)

        self.__display.activate_next_pixel()

        if self.__display.is_active_pixel_off():
            self.__display.set_active_pixel(self.__display.active_color)
        else:
            color_idx = self.__display.get_active_pixel()
            # update the rotary so that the next turn will start
            # where the pixel left off
            self.__controls.dial.set(value=color_idx)

        self.__display.update()

    def __button_long_press(self):
        # Read the state of each pixel in the active row
        status = self.__display.active_row_status()
        # print(status)

        # TODO: if more than one pixel is set to the same color
        # ...dont activate next row
        # ...blank out all pixels of that color
        # ...????

        if -1 in status:
            # TODO: at least one pixel is not set
            # ...do ... something!?
            # first_off_idx = status.index(-1)
            # self.__display.active_pixel = first_off_idx
            # active first off pixel
            pass
        elif self.__level.code == status:
            #   - If yes, Check if it's the solution
            #   - If no, then can't advance
            # * Check solution & update indicators
            #   - if yes, celebrate
            #   - If no, advance to the next row
            self.__display.fill(self.__color_set.get_support("correct"))
            # TODO: how to leave this state & move to next level?
            # pass
        else:
            indicators = self.__level.check_code(status)
            self.__display.set_indicator_row(indicators)
            self.__display.activate_next_row()

    def __button_handler(self, btn):
        start_tick = 0
        end_tick = 0
        if btn.value() == 0:
            start_tick = time.ticks_ms()

            # tick while button is still pressed
            while btn.value() == 0:
                pass

            end_tick = time.ticks_ms()

            # Debounce
            time.sleep_ms(10)

            # print(f"S[{start_tick}] | E[{end_tick}] | Diff[{time.ticks_diff(end_tick, start_tick)}]")

            # Long Press
            if time.ticks_diff(end_tick, start_tick) >= Controls.BUTTON_LONG_PRESS_MS:
                # print("-> Button : Long Press")
                self.__button_long_press()
            # Short Press
            else:
                # print("-> Button : Short Press")
                self.__button_short_press()

    def run(self):
        while True:
            # Check Rotary Encoder
            color_idx = self.__controls.dial.value()
            if color_idx != self.__display.active_color:
                self.__display.active_color = color_idx
                self.__display.set_active_pixel(color_idx)
                self.__display.update()

            # Check Button
            # IRQ callback set on button Pin
            # See __button_handler() function

            # Blink Active Pixel
            # See the Timer in __init__()
            # self.__display.blink_active_pixel()
            # time.sleep_ms(50)
