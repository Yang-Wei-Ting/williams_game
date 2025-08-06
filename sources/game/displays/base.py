from tkinter import ttk

from game.base import GameObject, GameObjectModel, GameObjectView


class DisplayModel(GameObjectModel):
    pass


class DisplayView(GameObjectView):

    def _create_widgets(self) -> None:
        self._widgets["main"] = ttk.Label(
            self.canvas,
            cursor="arrow",
            style="SmallText.Black_Burlywood4.TButton",
        )


class Display(GameObject):
    pass
