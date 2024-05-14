import tkinter as tk

from game.base import GameObject
from game.miscellaneous import Configuration as C
from game.states import ControlState


class DisplayOutcomeControl(GameObject):

    @property
    def _main_widget_configuration(self) -> dict:
        return {
            **super()._main_widget_configuration,
            "command": self.handle_click_event,
            "cursor": "hand2",
            "font": ("Times New Roman", 36, "bold italic"),
            "state": tk.NORMAL,
            "text": self._text,
        }

    def __init__(self, canvas: tk.Canvas, *, text: str, attach: bool = True) -> None:
        if ControlState.display_outcome_control:
            ControlState.display_outcome_control.handle_click_event()

        self._text = text
        x = C.HORIZONTAL_LAND_TILE_COUNT // 2
        y = C.VERTICAL_TILE_COUNT // 2
        super().__init__(canvas, x, y, attach=attach)

    def _register(self) -> None:
        ControlState.display_outcome_control = self

    def _unregister(self) -> None:
        ControlState.display_outcome_control = None

    def handle_click_event(self) -> None:
        self.detach_and_destroy_widgets()
