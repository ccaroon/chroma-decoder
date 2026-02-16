import random


class Code:
    def __init__(self, slot_cnt, color_cnt, tries):
        # choose `slot_cnt` colors out of `color_cnt`
        # no duplicates
        code = []
        choices = list(range(color_cnt))
        for _ in range(slot_cnt):
            color_idx = random.choice(choices)  # noqa: S311 (random generators are not suitable for cryptographic purposes)
            code.append(color_idx)
            choices.remove(color_idx)

        self.__code = tuple(code)

        self.__max_tries = tries
        self.__tries = 0

    @property
    def value(self):
        return self.__code

    @property
    def tries(self):
        return self.__tries

    def out_of_tries(self):
        return self.__tries >= self.__max_tries

    def check(self, status):
        self.__tries += 1

        indicators = []
        for idx, color_idx in enumerate(status):
            if color_idx not in self.__code:
                indicators.append("UNUSED")
            elif color_idx != self.__code[idx]:
                indicators.append("PARTIAL")
            elif color_idx == self.__code[idx]:
                indicators.append("CORRECT")

        return indicators
