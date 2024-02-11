import tkinter as tk
from glob import glob
from pathlib import PurePath


class Configuration:
    """
    A class that manages colors and dimensional settings.
    """

    BLUE = "#043E6F"
    GRAY = "#3B3B3B"
    RED = "#801110"
    COLOR_NAME_BY_HEX_TRIPLET = {
        BLUE: "blue",
        GRAY: "gray",
        RED: "red",
    }

    TILE_DIMENSION = 60  # pixels
    HORIZONTAL_LAND_TILE_COUNT = 11
    HORIZONTAL_SHORE_TILE_COUNT = 1
    HORIZONTAL_OCEAN_TILE_COUNT = 2
    HORIZONTAL_TILE_COUNT = (
        HORIZONTAL_LAND_TILE_COUNT + HORIZONTAL_SHORE_TILE_COUNT + HORIZONTAL_OCEAN_TILE_COUNT
    )
    VERTICAL_TILE_COUNT = 12


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
        Configuration.TILE_DIMENSION * (x + 0.5) + x_pixel_shift,
        Configuration.TILE_DIMENSION * (y + 0.5) + y_pixel_shift,
    )
