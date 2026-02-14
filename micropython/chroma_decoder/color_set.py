from chroma_decoder.color import Color


class ColorSet:
    __NAMED_SETS = {  # noqa: RUF012 - annotate mutable class var
        "default": (
            Color(255, 0, 0, 0.5).value,  #   0 - red
            Color(255, 2, 141, 0.5).value,  # 1 - pink
            Color(249, 115, 6, 0.5).value,  # 2 - orange
            Color(255, 255, 0, 0.5).value,  # 3 - yellow
            Color(0, 255, 0, 0.5).value,  #   4 - green
            Color(0, 190, 255, 0.5).value,  # 5 - cyan
            Color(0, 0, 255, 0.5).value,  #   6 - blue
            Color(64, 0, 255, 0.5).value,  #  7 - purple
        ),
        "christmas": (
            Color(255, 0, 0, 0.5).value,  #     0 - red
            Color(0, 255, 0, 0.5).value,  #     1 - green
            Color(0, 0, 255, 0.5).value,  #     2 - blue
            Color(255, 255, 255, 0.5).value,  # 3 - white
            Color(255, 255, 0, 0.5).value,  #   4 - yellow
        ),
        # White -to- Red (shades of pink)
        "valentines": (
            Color(255, 255, 255, 0.5).value,
            Color(255, 154, 154, 0.5).value,
            Color(255, 103, 103, 0.5).value,
            Color(255, 52, 52, 0.5).value,
            Color(255, 0, 0, 0.5).value,
        ),
    }

    __SUPPORT_COLORS = {  # noqa: RUF012 - annotate mutable class var
        # OFF
        "OFF": Color(0, 0, 0).value,
        # color not used (spot does not matter)
        "UNUSED": Color(0, 0, 0).value,
        # color used, BUT not in correct spot (partially correct)
        "PARTIAL": Color(255, 255, 255, 0.25).value,
        # color used AND is in correct spot
        "CORRECT": Color(73, 233, 72, 0.25).value,
    }

    def __init__(self, name="default"):
        if name not in self.__NAMED_SETS:
            msg = f"Unknown ColorSet: '{name}'"
            raise ValueError(msg)

        self.__colors = self.__NAMED_SETS.get(name)
        self.__count = len(self.__colors)

    @property
    def count(self):
        return self.__count

    def get(self, idx):
        return self.__colors[idx]

    def get_support(self, name):
        return self.__SUPPORT_COLORS.get(name.upper())

    def index(self, color):
        return self.__colors.index(color)
