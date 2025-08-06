import tkinter as tk

from game.base import GameObject, GameObjectModel, GameObjectView
from game.miscellaneous import Image, get_pixels
from game.states import HighlightState


class AttackRangeHighlightModel(GameObjectModel):

    def __init__(self, x: int, y: int, half_diagonal: int) -> None:
        self._half_diagonal = half_diagonal
        super().__init__(x, y)


class AttackRangeHighlightView(GameObjectView):

    def _create_widgets(self) -> None:
        pass

    def _destroy_widgets(self) -> None:
        pass

    def attach_widgets(self) -> None:
        self._ids["main"] = self._canvas.create_image(
            *get_pixels(self._model.x, self._model.y),
            image=getattr(Image, "red_diamond_{0}x{0}".format(self._model._half_diagonal * 120)),
        )


class AttackRangeHighlight(GameObject):

    def _register(self) -> None:
        HighlightState.attack_range_highlight = self

    def _unregister(self) -> None:
        HighlightState.attack_range_highlight = None
