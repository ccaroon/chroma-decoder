#!/usr/bin/env python
import argparse
import time

from led_matrix.color import Color
from led_matrix.program import Program


class ChromaDecoder(Program):
    """
    Single-Player Digital version of a Mastermind-like game
    """

    UPDATE_INTERVAL = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__colors = {
            "red": Color.make("red"),
            "pink": Color.make("#ff028d"),
            "orange": Color.make("#f97306"),
            "yellow": Color.make("yellow"),
            "green": Color.make("green"),
            "cyan": Color.make("cyan"),
            "blue": Color.make("blue"),
            "purple": Color.make("purple"),
            # --- support colors ---
            "off": Color.make("black"),
            "white": Color.make("white"),
            "ok_green": Color.make("#49e948"),
        }
        self.__color_list = list(self.__colors.values())

    def on_mouse_down(self, pos):
        # TODO: figure out a way to covert pos (x,y) to led position
        print(pos)

    def on_key_down(self, key_name, modifier):
        match key_name:
            case "left":
                print("left")
            case "right":
                print("right")
            case "space":
                pass
            case "q" | "Q":
                self.exit()
            case _:
                print(f"Key Pressed [{key_name}]")

    def loop(self):
        for x in range(5):
            for y in range(8):
                self.matrix.set_led(x, y, self.__color_list[y])

        self.matrix.set_led(2, 7, self.__colors["off"])
        self.matrix.set_led(3, 7, self.__colors["white"])
        self.matrix.set_led(4, 7, self.__colors["ok_green"])

        self.matrix.update()
        time.sleep(0.50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ChromaDecoder")
    parser.add_argument("--size", "-s", type=int, default=50, help="LED Size. Default: 50")
    args = parser.parse_args()

    print("Press 'Q' to exit!")
    program = ChromaDecoder(
        width=5,
        height=8,
        title="Chroma Decoder",
        noframe=False,
        led_size=args.size,
        led_shape="circle",
        led_spacing=5,
    )
    program.execute()
