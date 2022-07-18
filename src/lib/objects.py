import glob
import math
import tkinter as tk
from abc import ABC, abstractmethod
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


class GameObject(ABC):
    """
    An abstract base class for all game objects.
    """

    def __init__(
        self,
        canvas: tk.Canvas,
        x: int,
        y: int,
    ):
        """
        Create widget and canvas window object.
        """
        self._canvas = canvas
        self.x = x
        self.y = y
        self._set_widget_config()
        self._create_widget()
        self._create_canvas_window_object()

    @abstractmethod
    def _set_widget_config(self) -> None:
        """
        Configure widget.
        """
        self._widget_config = {}

    def _create_widget(self) -> None:
        """
        Create widget.
        """
        super(ABC, self).__init__(self._canvas, **self._widget_config)

    def _create_canvas_window_object(self) -> None:
        """
        Create canvas window object.
        """
        self._main_widget_id = self._canvas.create_window(
            self.x * 60 + 390,
            -self.y * 60 + 395,
            window=self,
        )

    def remove_canvas_window_object(self) -> None:
        """
        Remove canvas window object. Do nothing if no canvas window object exists.
        """
        if hasattr(self, "_main_widget_id"):
            self._canvas.delete(self._main_widget_id)
            delattr(self, "_main_widget_id")

    def move_to(self, x: int, y: int) -> None:
        """
        Move self to the new coordinate and update canvas window object's coordinate.
        """
        self.x = x
        self.y = y
        self._canvas.coords(self._main_widget_id, self.x * 60 + 390, -self.y * 60 + 395)

    def get_distance_between(self, other) -> float:
        """
        Return the distance between self and other.
        """
        return math.dist((self.x, self.y), (other.x, other.y))
