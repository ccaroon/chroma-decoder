from machine import Pin
from neopixel import NeoPixel

from chroma_decoder.color import Color


class Display:
    COLORS = (
        Color(255, 0, 0, 0.5).value,  # red
        Color(255, 2, 141, 0.5).value,  # pink
        Color(249, 115, 6, 0.5).value,  # orange
        Color(255, 255, 0, 0.5).value,  # yellow
        Color(0, 255, 0, 0.5).value,  # green
        Color(0, 190, 255, 0.5).value,  # cyan
        Color(0, 0, 255, 0.5).value,  # blue
        Color(64, 0, 255, 0.5).value,  # purple
    )
    COLOR_COUNT = len(COLORS)

    SUPPORT_COLORS = {  # noqa: RUF012 - annotate mutable class var
        "off": Color(0, 0, 0).value,
        "incorrect": Color(0, 0, 0).value,
        "correct_color": Color(255, 255, 255, 0.25).value,
        "correct": Color(73, 233, 72, 0.25).value,
    }

    def __init__(self, rows=1, cols=5, **kwargs):
        self.__pixel_pin = 7
        self.__row_count = rows
        self.__col_count = cols
        self.__swap_rc = kwargs.get("swap_rc", False)

        self.__pixel_count = self.__row_count * self.__col_count

        self.__pixels = NeoPixel(
            Pin(self.__pixel_pin, Pin.OUT),
            self.__pixel_count,
        )

        self.__active_row = 0
        self.__active_col = 0
        self.active_color = 0

        self.set(self.__active_row, self.__active_col, self.active_color)
        self.update()

    @property
    def active_pixel(self):
        """The Index of the Active Pixel"""
        return self.__rc_to_idx(self.__active_row, self.__active_col)

    def __rc_to_idx(self, row, col):
        """Convert a (row,col) to a linear index"""
        idx = None
        if self.__swap_rc:  # noqa: SIM108 - Use ternary
            idx = (col * self.__row_count) + row
        else:
            idx = (row * self.__col_count) + col

        return idx

    def activate_next_pixel(self):
        self.__active_col += 1
        if self.__active_col >= self.__col_count:
            self.__active_col = 0

    def activate_next_row(self):
        self.__active_row += 1
        # TODO: boundary checks
        if self.__active_row == self.__row_count - 1:
            pass

    def set(self, row, col, color_idx):
        idx = self.__rc_to_idx(row, col)
        self.__pixels[idx] = self.COLORS[color_idx]

    def is_active_pixel_off(self):
        return self.__pixels[self.active_pixel] == self.SUPPORT_COLORS["off"]

    def set_active_pixel(self, color_idx):
        """Set the Active Pixel's Color"""
        self.set(self.__active_row, self.__active_col, color_idx)

    def get_active_pixel(self):
        """Get the Active Pixel's Color"""
        return self.COLORS.index(self.__pixels[self.active_pixel])

    def blink_active_pixel(self):
        if self.__pixels[self.active_pixel] == self.SUPPORT_COLORS["off"]:
            color = self.COLORS[self.active_color]
        else:
            color = self.SUPPORT_COLORS["off"]

        self.__pixels[self.active_pixel] = color
        self.__pixels.write()

    def update(self):
        self.__pixels.write()
