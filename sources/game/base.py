import tkinter as tk
from abc import ABC, abstractmethod

from game.miscellaneous import get_pixels


class GameObject(ABC):

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, attach: bool = True) -> None:
        self._canvas = canvas
        self.x = x
        self.y = y
        self._create_widgets()
        self._register()
        if attach:
            self.attach_widgets_to_canvas()

    def detach_and_destroy_widgets(self) -> None:
        if hasattr(self, "_main_widget_id"):
            self.detach_widgets_from_canvas()
        self._unregister()
        self._destroy_widgets()

    @abstractmethod
    def _create_widgets(self) -> None:
        raise NotImplementedError

    def _destroy_widgets(self) -> None:
        self._main_widget.destroy()
        del self._main_widget

    @abstractmethod
    def _register(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _unregister(self) -> None:
        raise NotImplementedError

    def attach_widgets_to_canvas(self) -> None:
        self._main_widget_id = self._canvas.create_window(
            *get_pixels(self.x, self.y),
            window=self._main_widget,
        )

    def detach_widgets_from_canvas(self) -> None:
        self._canvas.delete(self._main_widget_id)
        del self._main_widget_id

    def get_distance_between(self, other) -> int:
        """
        Return the Manhattan distance between self and other.
        """
        if isinstance(other, tuple):
            return abs(other[0] - self.x) + abs(other[1] - self.y)

        return abs(other.x - self.x) + abs(other.y - self.y)
