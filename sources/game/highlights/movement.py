import tkinter as tk

from game.base import GameObject
from game.miscellaneous import Image
from game.states import GameState, HighlightState


class MovementHighlight(GameObject):

    @property
    def _main_widget_configuration(self) -> dict:
        return {
            **super()._main_widget_configuration,
            "activebackground": "Royal Blue",
            "background": "Royal Blue",
            "borderwidth": 0,
            "command": self.handle_click_event,
            "cursor": "hand2",
            "image": Image.transparent_12x12,
            "relief": tk.FLAT,
            "state": tk.NORMAL,
        }

    def _register(self) -> None:
        HighlightState.movement_highlights.add(self)

    def _unregister(self) -> None:
        HighlightState.movement_highlights.remove(self)

    def handle_click_event(self) -> None:
        soldier = GameState.selected_game_objects[-1]
        soldier.move_to(self.x, self.y)
        soldier.handle_click_event()
