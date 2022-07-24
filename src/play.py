"""
© 2022 Wei-Ting Yang. All rights reserved.
"""


import tkinter as tk
from random import choice, choices
from tkinter.ttk import Style

from lib.objects import Bowman, Color, Horseman, Image, King, Swordsman


class Program:
    """
    The main program.
    """

    def __init__(self):
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

        # Create mountains
        create(choice(range(210, 391, 60)), choice([210, 270]), image=Image.mountain_1)
        create(choice(range(210, 391, 60)), choice(range(450, 571, 60)), image=Image.mountain_2)
        create(570, choice(range(210, 571, 60)), image=Image.mountain_3)

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
        King(self._canvas, 0, -5, color=Color.BLUE)
        for coordinate in ((-1, -4), (0, -4), (1, -4)):
            Bowman(self._canvas, *coordinate, color=Color.BLUE)
        for coordinate in ((-3, -3), (-2, -3), (2, -3), (3, -3)):
            Horseman(self._canvas, *coordinate, color=Color.BLUE)
        for coordinate in ((-1, -3), (0, -3), (1, -3)):
            Swordsman(self._canvas, *coordinate, color=Color.BLUE)


if __name__ == "__main__":
    program = Program()
