import tkinter as tk
from abc import ABC, abstractmethod

from game.miscs import get_pixels


class GameObject(ABC):
    """
    An abstract base class for all game objects.
    """

    def __init__(self, canvas: tk.Canvas, x: int, y: int) -> None:
        """
        Create widgets then attach them to canvas.
        """
        self._canvas = canvas
        self.x = x
        self.y = y
        self._create_widgets()
        self._configure_widgets()
        self._attach_widgets_to_canvas()

    @abstractmethod
    def _create_widgets(self) -> None:
        """
        Create widgets.
        """
        raise NotImplementedError

    @abstractmethod
    def _configure_widgets(self) -> None:
        """
        Configure widgets.
        """
        raise NotImplementedError

    def _attach_widgets_to_canvas(self) -> None:
        """
        Attach widgets to canvas.
        """
        self._main_widget_id = self._canvas.create_window(
            *get_pixels(self.x, self.y),
            window=self._main_widget,
        )

    def destroy_widgets(self) -> None:
        """
        Remove widgets from canvas then destroy them.
        """
        self._canvas.delete(self._main_widget_id)
        del self._main_widget_id
        self._main_widget.destroy()
        del self._main_widget

    def configure_main_widget(self, *args, **kwargs) -> None:
        """
        Configure main widget.
        """
        self._main_widget.configure(*args, **kwargs)

    def get_distance_between(self, other) -> int:
        """
        Return the Manhattan distance between self and other.
        """
        if isinstance(other, tuple):
            return abs(other[0] - self.x) + abs(other[1] - self.y)

        return abs(other.x - self.x) + abs(other.y - self.y)
