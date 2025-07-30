import tkinter as tk
from glob import glob
from pathlib import PurePath
from tkinter import ttk


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

    # In pixels
    TILE_DIMENSION = 60
    HEALTH_BAR_LENGTH = 45

    HORIZONTAL_LAND_TILE_COUNT = 21
    HORIZONTAL_SHORE_TILE_COUNT = 1
    HORIZONTAL_OCEAN_TILE_COUNT = 2
    HORIZONTAL_TILE_COUNT = (
        HORIZONTAL_LAND_TILE_COUNT + HORIZONTAL_SHORE_TILE_COUNT + HORIZONTAL_OCEAN_TILE_COUNT
    )
    VERTICAL_TILE_COUNT = 13


class Environment:

    SCREEN_HEIGHT = None
    SCREEN_WIDTH = None
    TCL_TK_VERSION = None
    WINDOWING_SYSTEM = None


class Image:

    @classmethod
    def initialize(cls) -> None:
        """
        Hook all images onto cls.
        """
        for path in glob("images/*"):
            setattr(cls, PurePath(path).stem, tk.PhotoImage(file=path))


class Style:

    @classmethod
    def initialize(cls) -> None:
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "TButton",
            anchor=tk.CENTER,
            borderwidth=3,
            focusthickness=0,
            padding=0,
            relief=tk.RAISED,
            width=-1,
        )
        style.map(
            "Black_Burlywood4.TButton",
            background=[("Burlywood4",)],
            foreground=[("Black",)],
        )
        style.map(
            "CustomBlue.TButton",
            background=[(Configuration.BLUE,)],
        )
        style.map(
            "CustomGray.TButton",
            background=[(Configuration.GRAY,)],
        )
        style.map(
            "CustomRed.TButton",
            background=[(Configuration.RED,)],
        )
        style.map(
            "Royalblue1.TButton",
            background=[("Royalblue1",)],
        )
        style.configure(
            "BigText.Black_Burlywood4.TButton",
            font=("Courier", 36, "bold italic"),
            padding=9,
        )
        style.configure(
            "SmallText.Black_Burlywood4.TButton",
            anchor=tk.W,
            font=("Courier", 18, "bold"),
            padding=3,
            width=9,
        )
        style.configure(
            "Flat.Royalblue1.TButton",
            borderwidth=0,
            relief=tk.FLAT,
        )

        style.configure(
            "Green_Red.Horizontal.TProgressbar",
            background="Green",
            borderwidth=0,
            thickness=5,
            troughcolor="Red",
        )


def get_pixels(x: int, y: int, *, x_pixel_shift: float = 0.0, y_pixel_shift: float = 0.0) -> tuple:
    """
    Compute pixels from coordinates and custom pixel shifts.
    """
    return (
        Configuration.TILE_DIMENSION * (x + 0.5) + x_pixel_shift,
        Configuration.TILE_DIMENSION * (y + 0.5) + y_pixel_shift,
    )


def msleep(widget: tk.Misc, time: int) -> None:
    """
    Sleep for time milliseconds.
    """
    flag = tk.BooleanVar()
    widget.after(time, flag.set, True)
    widget.wait_variable(flag)
