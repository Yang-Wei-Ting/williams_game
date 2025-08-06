import tkinter as tk
from tkinter import ttk

from game.base import GameObject, GameObjectModel, GameObjectView
from game.miscellaneous import Configuration as C
from game.states import ControlState


class DisplayOutcomeControlModel(GameObjectModel):

    def __init__(self, text: str) -> None:
        if ControlState.display_outcome_control:
            ControlState.display_outcome_control.view.handle_click_event()

        x = C.HORIZONTAL_LAND_TILE_COUNT // 2
        y = C.VERTICAL_TILE_COUNT // 2
        super().__init__(x, y)

        self.text = text

        ControlState.display_outcome_control = self

    def destroy(self) -> None:
        ControlState.display_outcome_control = None


class DisplayOutcomeControlView(GameObjectView):

    def refresh(self) -> None:
        pass

    def _create_widgets(self) -> dict[str, ttk.Button]:
        widgets = {}
        widgets["main"] = ttk.Button(
            self._canvas,
            command=self.handle_click_event,
            cursor="hand2",
            style="BigText.Black_Burlywood4.TButton",
            takefocus=False,
            text=self._model.text,
        )
        return widgets

    def handle_click_event(self) -> None:
        model = self._model
        self.destroy()
        model.destroy()


class DisplayOutcomeControl(GameObject):
    pass
