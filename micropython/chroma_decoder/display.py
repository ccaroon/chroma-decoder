from machine import Pin
from neopixel import NeoPixel


class Display:
    def __init__(self, rows=1, cols=5, **kwargs):
        self.__pixel_pin = 7
        self.__color_set = kwargs.get("color_set")

        self.__row_count = rows
        self.__col_count = cols
        self.__rotated = kwargs.get("rotated", False)
        if self.__rotated:
            self.__row_count = cols
            self.__col_count = rows

        self.__pixel_count = self.__row_count * self.__col_count

        self.__pixels = NeoPixel(
            Pin(self.__pixel_pin, Pin.OUT),
            self.__pixel_count,
        )

        self.__active_row = 0
        self.__active_col = 0
        self.__indicator_row = self.__row_count - 1
        self.active_color = 0

    @property
    def active_idx(self):
        """The Index of the Active Pixel"""
        return self.__rc_to_idx(self.__active_row, self.__active_col)

    # @property.setter
    # def active_idx(self, idx):
    #     # TODO: convert idx to r,c
    #     pass

    def __rc_to_idx(self, row, col):
        """Convert a (row,col) to a linear index"""
        idx = None

        if self.__rotated:
            adj_row = (self.__col_count - 1) - col
            adj_col = row
            idx = (adj_row * self.__row_count) + adj_col
        else:
            idx = (row * self.__col_count) + col

        return idx

    def activate_next_pixel(self):
        self.__active_col += 1
        if self.__active_col >= self.__col_count:
            self.__active_col = 0

    def active_row_status(self):
        """
        Get the status of each pixel in the active row indicated by a list of ints.

        -1  -> Pixel is OFF
        IDX -> Pixel is ON & set to color IDX
        """

        # set active pixel to active color b/c it's blinking and needs to be
        # stable to get a reading
        self.set_active_pixel(self.active_color)

        # assume all off
        status = [-1] * self.__col_count

        for col in range(self.__col_count):
            idx = self.__rc_to_idx(self.__active_row, col)
            if self.__pixels[idx] != self.__color_set.get_support("off"):
                status[col] = self.get(self.__active_row, col)

        return tuple(status)

    # def __active_row_complete(self):
    #     complete = True

    #     for col in range(self.__col_count):
    #         idx = self.__rc_to_idx(self.__active_row, col)
    #         if self.__pixels[idx] == self.SUPPORT_COLORS["off"]:
    #             complete = False
    #             break

    #     return complete

    def activate_next_row(self):
        next_row = self.__active_row + 1
        if next_row < self.__row_count - 1:
            self.__active_col = 0
            self.__active_row = next_row

    def set(self, row, col, color_idx):
        idx = self.__rc_to_idx(row, col)
        self.__pixels[idx] = self.__color_set.get(color_idx)

    def get(self, row, col):
        idx = self.__rc_to_idx(row, col)
        return self.__color_set.index(self.__pixels[idx])

    def is_active_pixel_off(self):
        return self.__pixels[self.active_idx] == self.__color_set.get_support("off")

    def set_active_pixel(self, color_idx):
        """Set the Active Pixel's Color"""
        self.set(self.__active_row, self.__active_col, color_idx)

    def get_active_pixel(self):
        """Get the Active Pixel's Color"""
        return self.__color_set.index(self.__pixels[self.active_idx])

    def set_indicator_row(self, statuses):
        for col in range(self.__col_count):
            idx = self.__rc_to_idx(self.__indicator_row, col)
            self.__pixels[idx] = self.__color_set.get_support(statuses[col])

        self.update()

    # Called by Timer
    def blink_active_pixel(self, _):
        """
        Args:
            _ (Timer): Unused
        """
        if self.__pixels[self.active_idx] == self.__color_set.get_support("off"):
            color = self.__color_set.get(self.active_color)
        else:
            color = self.__color_set.get_support("off")

        self.__pixels[self.active_idx] = color
        self.__pixels.write()

    def fill(self, color: tuple):
        self.__pixels.fill(color)
        self.update()

    def reset(self):
        self.__pixels.fill(self.__color_set.get_support("off"))
        self.set(self.__active_row, self.__active_col, self.active_color)
        self.update()

    def update(self):
        self.__pixels.write()
