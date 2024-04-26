import tkinter as tk

from game.base import GameObject
from game.miscellaneous import Configuration as C
from game.miscellaneous import Image
from game.states import DisplayState, GameState, HighlightState, RecruitmentState


class PlacementHighlight(GameObject):

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
        HighlightState.placement_highlights.add(self)

    def _unregister(self) -> None:
        HighlightState.placement_highlights.remove(self)

    def handle_click_event(self) -> None:
        recruitment = GameState.selected_game_objects[-1]

        GameState.coin -= recruitment.cost
        DisplayState.coin_display.refresh_widgets()
        for _recruitment in RecruitmentState.barrack_recruitments:
            _recruitment.refresh_widgets()

        soldier = recruitment.target(self._canvas, self.x, self.y, attach=False, color=C.BLUE)
        soldier.attacked_this_turn = True
        soldier.moved_this_turn = True
        soldier.refresh_widgets()
        soldier.attach_widgets_to_canvas()

        recruitment.handle_click_event()
