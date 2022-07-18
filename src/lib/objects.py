import glob
import tkinter as tk
from pathlib import PurePath


class Image:
    """
    A class that manages images.
    """

    @classmethod
    def initialize(cls) -> None:
        """
        Hook all images onto cls.
        """
        for path in glob.glob("images/*"):
            setattr(cls, PurePath(path).stem, tk.PhotoImage(file=path))
