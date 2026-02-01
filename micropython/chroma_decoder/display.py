from machine import Pin
from neopixel import NeoPixel


class Display:
    COLORS = (
        (255, 0, 0),  # red
        (255, 2, 141),  # pink
        (249, 115, 6),  # orange
        (255, 255, 0),  # yellow
        (0, 255, 0),  # green
        (0, 190, 255),  # cyan
        (0, 0, 255),  # blue
        (64, 0, 255),  # purple
    )
    COLOR_COUNT = len(COLORS)

    SUPPORT_COLORS = {  # noqa: RUF012
        "off": (0, 0, 0),
        "incorrect": (0, 0, 0),
        "correct_color": (255, 255, 255),
        "correct": (73, 233, 72),
    }

    def __init__(self, rows=8, cols=5):
        self.__pixel_pin = 7
        self.__row_count = rows
        self.__col_count = cols

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
        return (row * self.__col_count) + col

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
