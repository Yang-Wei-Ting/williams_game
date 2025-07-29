"""
© 2022-2025 Wei-Ting Yang. All rights reserved.
"""


import sys
import tkinter as tk
from random import choices

from game.buildings import Barrack
from game.controls import EndTurnControl
from game.displays import CoinDisplay, DayDisplay
from game.miscellaneous import Configuration as C
from game.miscellaneous import Environment as E
from game.miscellaneous import Image, Style, get_pixels
from game.soldiers import Hero


class Program:

    def __init__(self) -> None:
        self._window = tk.Tk()
        self._detect_environment()
        self._check_requirements()
        self._window.title("TkTactics")
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
        Style.initialize()

        self._create_landscape()
        self._create_displays()
        self._create_controls()

        self._create_initial_buildings()
        self._create_initial_allied_soldiers()

        self._window.mainloop()

    def _detect_environment(self) -> None:
        E.SCREEN_HEIGHT = self._window.winfo_screenheight()
        E.SCREEN_WIDTH = self._window.winfo_screenwidth()
        E.TCL_TK_VERSION = self._window.call("info", "patchlevel")
        E.WINDOWING_SYSTEM = self._window.call("tk", "windowingsystem")

    def _check_requirements(self) -> None:
        if E.WINDOWING_SYSTEM == "aqua":
            sys.exit("Aqua windowing system is currently not supported.")

    def _create_landscape(self) -> None:
        LANDS = [getattr(Image, f"land_{i}") for i in range(1, 11)]
        WEIGHTS = (30, 15, 14, 14, 7, 6, 5, 4, 3, 2)

        # TODO: Track canvas image object ID.
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

    def _create_displays(self) -> None:
        DayDisplay(
            self._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
            0,
        )
        CoinDisplay(
            self._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
            1,
        )

    def _create_controls(self) -> None:
        EndTurnControl(
            self._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
            C.VERTICAL_TILE_COUNT - 1,
        )

    def _create_initial_buildings(self) -> None:
        Barrack(
            self._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT // 2,
            C.VERTICAL_TILE_COUNT // 2,
        )

    def _create_initial_allied_soldiers(self) -> None:
        Hero(
            self._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT // 2,
            C.VERTICAL_TILE_COUNT // 2 + 1,
            color=C.BLUE,
        )


if __name__ == "__main__":
    program = Program()
