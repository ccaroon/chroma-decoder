class Color:
    def __init__(self, r, g, b, brightness=1.0):
        self.__red = int(r * brightness)
        self.__green = int(g * brightness)
        self.__blue = int(b * brightness)

        self.__brightness = brightness

    @property
    def value(self):
        return (self.__red, self.__green, self.__blue)
