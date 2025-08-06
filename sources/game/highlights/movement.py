from tkinter import ttk

from game.base import GameObject, GameObjectModel, GameObjectView
from game.miscellaneous import Image
from game.states import HighlightState


class MovementHighlightModel(GameObjectModel):
    pass


class MovementHighlightView(GameObjectView):

    def _create_widgets(self) -> None:
        self._widgets["main"] = ttk.Label(
            self._canvas,
            cursor="arrow",
            style="Flat.Royalblue1.TButton",
            image=Image.transparent_12x12,
        )


class MovementHighlight(GameObject):

    def _register(self) -> None:
        HighlightState.movement_highlights.add(self)

    def _unregister(self) -> None:
        HighlightState.movement_highlights.remove(self)
