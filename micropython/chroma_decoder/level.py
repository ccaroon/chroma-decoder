import random


class Level:
    def __init__(self, slot_cnt, color_cnt):
        # choose `slot_cnt` colors out of `color_cnt`
        # no duplicates
        code = []
        choices = list(range(color_cnt))
        for _ in range(slot_cnt):
            color_idx = random.choice(choices)  # noqa: S311 (random generators are not suitable for cryptographic purposes)
            code.append(color_idx)
            choices.remove(color_idx)

        self.__code = tuple(code)

    @property
    def code(self):
        return self.__code

    def check_code(self, status):
        indicators = []
        for idx, color_idx in enumerate(status):
            if color_idx not in self.__code:
                indicators.append("UNUSED")
            elif color_idx != self.__code[idx]:
                indicators.append("PARTIAL")
            elif color_idx == self.__code[idx]:
                indicators.append("CORRECT")

        return indicators
