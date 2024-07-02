from tkinter import ttk

from game.base import GameObject
from game.miscellaneous import Image
from game.states import HighlightState


class MovementHighlight(GameObject):

    def _create_widgets(self) -> None:
        self._main_widget = ttk.Label(
            self._canvas,
            cursor="arrow",
            style="Flat.Royalblue1.TButton",
            image=Image.transparent_12x12,
        )

    def _register(self) -> None:
        HighlightState.movement_highlights.add(self)

    def _unregister(self) -> None:
        HighlightState.movement_highlights.remove(self)
