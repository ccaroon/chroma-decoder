import time

from machine import Timer

from chroma_decoder.code import Code
from chroma_decoder.color_set import ColorSet
from chroma_decoder.controls import Controls
from chroma_decoder.display import Display


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

        # Init the first secret code
        self.__code = None
        self.__code_solved = False
        self.__gen_code()

    def __gen_code(self):
        # reset display
        self.__display.reset()
        self.__controls.dial.set(value=self.__display.active_color)

        self.__code_solved = False

        # size[0] = rows | size[1] = cols
        size = self.__display.size
        self.__code = Code(size[1], self.__color_set.count, size[0] - 1)
        print("Code: ", self.__code.value, size[0] - 1)

    def __is_row_valid(self, status):
        count = status.count(self.__display.active_color)
        return count <= 1

    def __remove_dups(self, status):
        new_colors = []
        for color_idx in status:
            if color_idx in (self.__display.active_color, -1):
                new_colors.append(self.__color_set.get_support("off"))
            else:
                new_colors.append(color_idx)

        self.__display.set_active_row(new_colors)
        # Set the active pixel to the active color b/c the above
        # set_active_row() call turned it off
        self.__display.set_active_pixel(self.__display.active_color)

    def __button_short_press(self):
        # incase it's off b/c of blinky, blinky
        self.__display.set_active_pixel(self.__display.active_color)

        # Check for duplicate instances of the active_color in the active row
        status = self.__display.active_row_status()
        if not self.__is_row_valid(status):
            self.__remove_dups(status)

        # Move to next pixel
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
        if self.__code_solved:
            self.__gen_code()
        else:
            # Read the state of each pixel in the active row
            status = self.__display.active_row_status()

            if not self.__is_row_valid(status):
                self.__remove_dups(status)
                self.__display.update()
            # If -1 in status, then not all pixels/cols in the row
            # have been set yet.
            elif -1 not in status:
                if self.__code.value == status:
                    self.__display.disable_blinker()
                    self.__display.glyph("check-mark", "correct")
                    self.__code_solved = True
                else:
                    indicators = self.__code.check(status)
                    self.__display.set_indicator_row(indicators)
                    self.__display.activate_next_row()

                if self.__code.out_of_tries():
                    self.__display.disable_blinker()
                    self.__display.glyph("wrong-x", "wrong")
                    self.__code_solved = True

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
