import tkinter as tk
from abc import abstractmethod

from game.bases import GameObject
from game.states import CoinDisplayState, GameState


class Display(GameObject):

    def _create_widgets(self) -> None:
        """
        Create widgets.
        """
        self._main_widget = tk.Label(self._canvas)

    @abstractmethod
    def refresh(self) -> None:
        """
        """
        raise NotImplementedError


class CoinDisplay(Display):

    def _configure_widgets(self) -> None:
        """
        Configure widgets.
        """
        self.configure_main_widget(
            background="Burlywood4",
            activebackground="Burlywood4",
            relief=tk.RAISED,
            borderwidth=5,
            highlightthickness=0,
        )
        self.refresh()

    def _attach_widgets_to_canvas(self) -> None:
        """
        """
        super()._attach_widgets_to_canvas()
        CoinDisplayState.instance = self

    def destroy_widgets(self) -> None:
        """
        """
        CoinDisplayState.instance = None
        super().destroy_widgets()

    def refresh(self) -> None:
        """
        Update label text.
        """
        self.configure_main_widget(text=str(GameState.coin))
