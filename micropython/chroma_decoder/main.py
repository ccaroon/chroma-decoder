import time

from chroma_decoder.controls import Controls
from chroma_decoder.display import Display


class Game:
    def __init__(self):
        self.__display = Display(1, 5)
        self.__controls = Controls(self.__display.COLOR_COUNT - 1, self.__button_handler)

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
            self.__display.blink_active_pixel()
            time.sleep_ms(50)

    def __button_handler(self, btn):
        start_tick = 0
        end_tick = 0
        if btn.value() == 0:
            start_tick = time.ticks_ms()

            # tick while button is still presses
            while btn.value() == 0:
                pass

            end_tick = time.ticks_ms()

            # Debounce
            time.sleep_ms(10)

            # print(f"S[{start_tick}] | E[{end_tick}] | Diff[{time.ticks_diff(end_tick, start_tick)}]")

            # Long Press
            if time.ticks_diff(end_tick, start_tick) >= Controls.BUTTON_LONG_PRESS_MS:
                # print("-> Button : Long Press")
                pass
            # Short (not-long) Press
            else:
                # print("-> Button : Short Press")
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


if __name__ == "__main__":
    game = Game()
    game.run()
