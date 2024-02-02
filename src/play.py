"""
© 2022 Wei-Ting Yang. All rights reserved.
"""


import tkinter as tk
from random import choices
from tkinter.ttk import Style

from game.controls import EndTurn, Restart
from game.cores import Archer, Cavalry, Infantry, King
from game.miscs import Configuration as C
from game.miscs import Image


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
            width=780,
            height=780,
            background="Black",
            highlightthickness=0,
        )
        self._canvas.pack()

        Image.initialize()

        self._end_turn_button = EndTurn(self._canvas, 9.75, 11.9)
        self._restart_button = Restart(self._canvas, 0.25, 11.9, window=self._window)

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
        create = self._canvas.create_image

        # Create lands
        LANDS = [getattr(Image, f"land_{i}") for i in range(1, 15)]
        WEIGHTS = (2, 2, 3, 3, 4, 4, 5, 4, 4, 3, 3, 2, 2, 3)
        for x in range(90, 691, 60):
            for y in range(30, 691, 60):
                create(x, y, image=choices(LANDS, weights=WEIGHTS)[0])

        # Create water
        for i in range(90, 691, 60):
            create(i, 750, image=Image.water_s)
            create(30, i, image=Image.water_w)
            create(750, i, image=Image.water_e)
        create(30, 30, image=Image.water_w)
        create(750, 30, image=Image.water_e)
        create(30, 750, image=Image.water_sw)
        create(750, 750, image=Image.water_se)

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
