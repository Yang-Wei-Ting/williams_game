"""
© 2022-2024 Wei-Ting Yang. All rights reserved.
"""


import tkinter as tk
from random import choices

from game.buildings import Barrack
from game.controls import EndTurnControl, RestartGameControl
from game.displays import CoinDisplay, DayDisplay
from game.miscellaneous import Configuration as C
from game.miscellaneous import Image, Style, get_pixels
from game.soldiers import Hero


class Program:

    def __init__(self) -> None:
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
        Style.initialize()

        self._create_landscape()
        self._create_displays()
        self._create_controls()

        self._create_initial_buildings()
        self._create_initial_allied_soldiers()

        self._window.mainloop()

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
            1,
        )
        CoinDisplay(
            self._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
            2,
        )

    def _create_controls(self) -> None:
        RestartGameControl(
            self._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
            0,
        )
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
