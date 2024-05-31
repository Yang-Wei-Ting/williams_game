import tkinter as tk
from tkinter import ttk

from game.base import GameObject
from game.miscellaneous import Configuration as C
from game.states import ControlState


class DisplayOutcomeControl(GameObject):

    def __init__(self, canvas: tk.Canvas, *, text: str, attach: bool = True) -> None:
        if ControlState.display_outcome_control:
            ControlState.display_outcome_control.handle_click_event()

        self._text = text
        x = C.HORIZONTAL_LAND_TILE_COUNT // 2
        y = C.VERTICAL_TILE_COUNT // 2
        super().__init__(canvas, x, y, attach=attach)

    def _create_widgets(self) -> None:
        self._main_widget = ttk.Button(
            self._canvas,
            command=self.handle_click_event,
            cursor="hand2",
            style="BigText.Black_Burlywood4.TButton",
            takefocus=False,
            text=self._text,
        )

    def _register(self) -> None:
        ControlState.display_outcome_control = self

    def _unregister(self) -> None:
        ControlState.display_outcome_control = None

    def handle_click_event(self) -> None:
        self.detach_and_destroy_widgets()
