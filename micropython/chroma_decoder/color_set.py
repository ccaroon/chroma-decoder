from chroma_decoder.color import Color


class ColorSet:
    __NAMED_SETS = {  # noqa: RUF012 - annotate mutable class var
        "default": (
            Color(255, 0, 0, 0.5).value,  # red
            Color(255, 2, 141, 0.5).value,  # pink
            Color(249, 115, 6, 0.5).value,  # orange
            Color(255, 255, 0, 0.5).value,  # yellow
            Color(0, 255, 0, 0.5).value,  # green
            Color(0, 190, 255, 0.5).value,  # cyan
            Color(0, 0, 255, 0.5).value,  # blue
            Color(64, 0, 255, 0.5).value,  # purple
        ),
        "christmas": (
            Color(255, 0, 0, 0.5).value,  # red
            Color(0, 255, 0, 0.5).value,  # green
            Color(0, 0, 255, 0.5).value,  # blue
            Color(255, 255, 255, 0.5).value,  # white
            Color(255, 255, 0, 0.5).value,  # yellow
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
        "off": Color(0, 0, 0).value,
        "incorrect": Color(0, 0, 0).value,
        "correct_color": Color(255, 255, 255, 0.25).value,
        "correct": Color(73, 233, 72, 0.25).value,
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
        return self.__SUPPORT_COLORS.get(name)

    def index(self, color):
        return self.__colors.index(color)
