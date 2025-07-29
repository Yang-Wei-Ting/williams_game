from abc import abstractmethod
from tkinter import ttk

from game.base import GameObject


class Display(GameObject):

    def _create_widgets(self) -> None:
        self._main_widget = ttk.Label(
            self._canvas,
            cursor="arrow",
            style="SmallText.Black_Burlywood4.TButton",
        )
        self.refresh_widgets()

    @abstractmethod
    def refresh_widgets(self) -> None:
        raise NotImplementedError
