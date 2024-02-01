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
