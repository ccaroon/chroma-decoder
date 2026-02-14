# (
#     0,0,0,0,0,
#     0,0,0,0,0,
#     0,0,0,0,0,
#     0,0,0,0,0,
#     0,0,0,0,0,
#     0,0,0,0,0,
#     0,0,0,0,0,
#     0,0,0,0,0,
# )

# TODO: re-work this class / code


class Glyph:
    CHECK_MARK = (
        (0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0),
        (0, 0, 0, 0, 1),
        (0, 0, 0, 1, 0),
        (1, 0, 1, 0, 0),
        (0, 1, 0, 0, 0),
        (0, 0, 0, 0, 0),
    )

    WRONG_X = (
        (0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0),
        (1, 0, 0, 0, 1),
        (0, 1, 0, 1, 0),
        (0, 0, 1, 0, 0),
        (0, 1, 0, 1, 0),
        (1, 0, 0, 0, 1),
        (0, 0, 0, 0, 0),
    )

    @classmethod
    def get(cls, name):
        glpyh = None

        if name == "check-mark":
            glpyh = cls.CHECK_MARK
        elif name == "wrong_x":
            glpyh = cls.WRONG_X
        else:
            glpyh = None

        return glpyh
