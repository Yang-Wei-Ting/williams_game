import math
import tkinter as tk
from abc import ABC, abstractmethod
from glob import glob
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
        for path in glob("images/*"):
            setattr(cls, PurePath(path).stem, tk.PhotoImage(file=path))


class GameObject(ABC):
    """
    An abstract base class for all game objects.
    """

    def __init__(self, canvas: tk.Canvas, x: int, y: int):
        """
        Create widget and canvas window object.
        """
        self._canvas = canvas
        self.x = x
        self.y = y
        self._create_widget()
        self._configure_widget()
        self._create_canvas_window_object()

    def _create_widget(self) -> None:
        """
        Create widget.
        """
        super(ABC, self).__init__(self._canvas)

    @abstractmethod
    def _configure_widget(self) -> None:
        """
        Configure widget.
        """
        self.configure()

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
