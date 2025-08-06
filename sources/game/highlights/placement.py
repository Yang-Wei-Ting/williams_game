from tkinter import ttk

from game.base import GameObject, GameObjectModel, GameObjectView
from game.miscellaneous import Configuration as C
from game.miscellaneous import Image
from game.states import DisplayState, GameState, HighlightState, RecruitmentState


class PlacementHighlightModel(GameObjectModel):
    pass


class PlacementHighlightView(GameObjectView):

    def _create_widgets(self) -> None:
        self._widget["main"] = ttk.Button(
            self._canvas,
            command=self.handle_click_event,
            cursor="hand2",
            style="Flat.Royalblue1.TButton",
            takefocus=False,
            image=Image.transparent_12x12,
        )


class PlacementHighlight(GameObject):

    def _bind_or_unbind_event_handlers(self) -> None:
        self._view._widget["main"].configure(command=self.handle_click_event)

    def _register(self) -> None:
        HighlightState.placement_highlights.add(self)

    def _unregister(self) -> None:
        HighlightState.placement_highlights.remove(self)

    # TODO
    def handle_click_event(self) -> None:
        recruitment = GameState.selected_game_objects[-1]

        GameState.coin -= recruitment.target.cost
        if DisplayState.coin_display:
            DisplayState.coin_display._view.refresh_main_appearance()
        for _recruitment in RecruitmentState.barrack_recruitments:
            _recruitment._view.refresh_main_appearance()

        soldier = recruitment.target(self._canvas, self.x, self.y, attach=False, color=C.BLUE)
        soldier.attacked_this_turn = True
        soldier.moved_this_turn = True
        soldier.refresh_widgets()
        soldier.attach_widgets_to_canvas()

        recruitment.handle_click_event()
