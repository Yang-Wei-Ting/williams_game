import tkinter as tk
from glob import glob
from pathlib import PurePath


class Configuration:
    """
    A class that manages colors.
    """

    BLUE = "#043E6F"
    GRAY = "#3B3B3B"
    RED = "#801110"
    COLOR_NAME_BY_HEX_TRIPLET = {
        BLUE: "blue",
        GRAY: "gray",
        RED: "red",
    }


class Image:
    """
    A class that manages images.
    """

    @classmethod
    def initialize(cls) -> None:
        """
        Hook all images onto cls.
        """
        for path in glob("images/*"):
            setattr(cls, PurePath(path).stem, tk.PhotoImage(file=path))


def get_pixels(x: int, y: int, *, x_pixel_shift: float = 0.0, y_pixel_shift: float = 0.0) -> tuple:
    """
    Compute pixels from coordinates and custom pixel shifts.
    """
    return (
        60 * (x + 1.5) + x_pixel_shift,
        60 * (y + 0.5) + y_pixel_shift,
    )
