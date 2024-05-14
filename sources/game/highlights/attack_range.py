import tkinter as tk

from game.base import GameObject
from game.miscellaneous import Image, get_pixels
from game.states import HighlightState


class AttackRangeHighlight(GameObject):

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, half_diagonal: int, attach: bool = True) -> None:
        self._half_diagonal = half_diagonal
        super().__init__(canvas, x, y, attach=attach)

    def _create_widgets(self) -> None:
        pass

    def _destroy_widgets(self) -> None:
        pass

    def _register(self) -> None:
        HighlightState.attack_range_highlight = self

    def _unregister(self) -> None:
        HighlightState.attack_range_highlight = None

    def attach_widgets_to_canvas(self) -> None:
        self._main_widget_id = self._canvas.create_image(
            *get_pixels(self.x, self.y),
            image=getattr(Image, "red_diamond_{0}x{0}".format(self._half_diagonal * 120)),
        )
