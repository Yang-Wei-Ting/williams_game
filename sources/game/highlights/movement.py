from tkinter import ttk

from game.base import GameObject, GameObjectModel, GameObjectView
from game.miscellaneous import Image


class MovementHighlightModel(GameObjectModel):
    pass


class MovementHighlightView(GameObjectView):

    def _create_widgets(self) -> None:
        self._widgets["main"] = ttk.Label(
            self.canvas,
            cursor="arrow",
            style="Flat.Royalblue1.TButton",
            image=Image.transparent_12x12,
        )


class MovementHighlight(GameObject):

    def _register(self) -> None:
        GameObject.unordered_collections["movement_highlight"].add(self)

    def _unregister(self) -> None:
        GameObject.unordered_collections["movement_highlight"].remove(self)
