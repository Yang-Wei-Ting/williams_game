from abc import abstractmethod
from tkinter import ttk

from game.base import GameObject, GameObjectModel, GameObjectView


class DisplayModel(GameObjectModel):
    pass


class DisplayView(GameObjectView):

    def _create_widgets(self, data: dict) -> None:
        self._widgets["main"] = ttk.Label(
            self._canvas,
            cursor="arrow",
            style="SmallText.Black_Burlywood4.TButton",
        )
        self.refresh_main_appearance(data)


class Display(GameObject):
    pass
