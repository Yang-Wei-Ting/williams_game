"""
© 2022 Wei-Ting Yang. All rights reserved.
"""


import tkinter as tk
from random import choices
from tkinter.ttk import Style

from game.controls import EndTurnControl, RestartControl
from game.miscs import Configuration as C
from game.miscs import Image, get_pixels
from game.soldiers import Archer, Cavalry, Infantry, King


class Program:
    """
    The main program.
    """

    def __init__(self) -> None:
        """
        Initialize the main program.
        """
        self._window = tk.Tk()
        self._window.title("Map")
        self._window.resizable(width=False, height=False)

        self._canvas = tk.Canvas(
            self._window,
            width=C.TILE_DIMENSION * C.HORIZONTAL_TILE_COUNT,
            height=C.TILE_DIMENSION * C.VERTICAL_TILE_COUNT,
            background="Black",
            highlightthickness=0,
        )
        self._canvas.pack()

        Image.initialize()

        self._end_turn_control = EndTurnControl(
            self._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
            C.VERTICAL_TILE_COUNT - 1,
        )
        self._restart_control = RestartControl(
            self._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
            0,
        )

        self._create_landscape()

        self._style = Style()
        self._style.theme_use("default")
        self._style.configure(
            "TProgressbar",
            troughcolor="Red",
            background="Green",
            darkcolor="Green",
            lightcolor="Green",
            bordercolor="Red",
            thickness=5,
        )
        self._create_initial_allies()

        self._window.mainloop()

    def _create_landscape(self) -> None:
        """
        Create landscape.
        """
        LANDS = [getattr(Image, f"land_{i}") for i in range(1, 11)]
        WEIGHTS = (30, 15, 14, 14, 7, 6, 5, 4, 3, 2)

        for y in range(C.VERTICAL_TILE_COUNT):
            for x in range(C.HORIZONTAL_LAND_TILE_COUNT):
                self._canvas.create_image(
                    *get_pixels(x, y),
                    image=choices(LANDS, weights=WEIGHTS)[0],
                )

            for _ in range(C.HORIZONTAL_SHORE_TILE_COUNT):
                x += 1
                self._canvas.create_image(*get_pixels(x, y), image=Image.shore)

            for _ in range(C.HORIZONTAL_OCEAN_TILE_COUNT):
                x += 1
                self._canvas.create_image(*get_pixels(x, y), image=Image.ocean)

    def _create_initial_allies(self) -> None:
        """
        Create initial ally instances.
        """
        King(self._canvas, 5, 10, color=C.BLUE)
        for coordinate in ((4, 9), (5, 9), (5, 8), (6, 9)):
            Infantry(self._canvas, *coordinate, color=C.BLUE)
        for coordinate in ((3, 10), (4, 10), (6, 10), (7, 10)):
            Archer(self._canvas, *coordinate, color=C.BLUE)
        for coordinate in ((2, 10), (2, 9), (8, 10), (8, 9)):
            Cavalry(self._canvas, *coordinate, color=C.BLUE)


if __name__ == "__main__":
    program = Program()
