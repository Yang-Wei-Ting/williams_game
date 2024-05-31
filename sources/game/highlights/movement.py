from tkinter import ttk

from game.base import GameObject
from game.miscellaneous import Image
from game.states import GameState, HighlightState


class MovementHighlight(GameObject):

    def _create_widgets(self) -> None:
        self._main_widget = ttk.Button(
            self._canvas,
            command=self.handle_click_event,
            cursor="hand2",
            style="Flat.Royalblue1.TButton",
            takefocus=False,
            image=Image.transparent_12x12,
        )

    def _register(self) -> None:
        HighlightState.movement_highlights.add(self)

    def _unregister(self) -> None:
        HighlightState.movement_highlights.remove(self)

    def handle_click_event(self) -> None:
        soldier = GameState.selected_game_objects[-1]
        soldier.move_to(self.x, self.y)
        soldier.handle_click_event()
