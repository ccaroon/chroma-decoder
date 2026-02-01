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
            # enc_val = rotary.value()
            # if enc_val != active_color:
            #     active_color = enc_val
            #     neo[active_pixel] = SHOW_COLORS[active_color]
            #     neo.write()

            # Check Button
            # check_button(button)
            # --or--
            # IRQ callback set on button Pin (above)

            # blink_active_pixel()
            self.__display.blink_active_pixel()
            time.sleep_ms(50)

    def __button_handler(self, btn):
        if btn.value() == 0:
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

            # Debounce
            while btn.value() == 0:
                pass
            time.sleep_ms(10)


if __name__ == "__main__":
    game = Game()
    game.run()
