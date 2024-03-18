import tkinter as tk
from abc import ABC, abstractmethod

from game.miscs import get_pixels


class GameObject(ABC):
    """
    An abstract base class for all game objects.
    """

    def __init__(self, canvas: tk.Canvas, x: int, y: int) -> None:
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
        self._main_widget = tk.Button(self._canvas)

    @abstractmethod
    def _configure_widget(self) -> None:
        """
        Configure widget.
        """
        raise NotImplementedError

    def _create_canvas_window_object(self) -> None:
        """
        Create canvas window object.
        """
        self._main_widget_id = self._canvas.create_window(
            *get_pixels(self.x, self.y),
            window=self._main_widget,
        )

    def remove_canvas_window_object(self) -> None:
        """
        Remove canvas window object.
        """
        self._canvas.delete(self._main_widget_id)
        del self._main_widget_id

    def get_distance_between(self, other) -> int:
        """
        Return the Manhattan distance between self and other.
        """
        if isinstance(other, tuple):
            return abs(other[0] - self.x) + abs(other[1] - self.y)

        return abs(other.x - self.x) + abs(other.y - self.y)
