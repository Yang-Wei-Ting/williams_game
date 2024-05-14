import tkinter as tk
from abc import abstractmethod

from game.base import GameObject
from game.highlights import PlacementHighlight
from game.miscellaneous import Configuration as C
from game.miscellaneous import Image
from game.soldiers.base import Soldier
from game.states import ControlState, GameState, HighlightState, RecruitmentState


class SoldierRecruitment(GameObject):

    @property
    @abstractmethod
    def target(self) -> type[Soldier]:
        raise NotImplementedError

    def _create_widgets(self) -> None:
        super()._create_widgets()
        self.refresh_widgets()

    def _register(self) -> None:
        RecruitmentState.barrack_recruitments.add(self)

    def _unregister(self) -> None:
        RecruitmentState.barrack_recruitments.remove(self)

    def refresh_widgets(self) -> None:
        if GameState.coin >= self.cost:
            color = C.BLUE
        else:
            color = C.GRAY

        color_name = C.COLOR_NAME_BY_HEX_TRIPLET[color]
        soldier_name = self.target.__name__.lower()

        self._main_widget.configure(
            activebackground=color,
            background=color,
            command=(self.handle_click_event if color == C.BLUE else (lambda: None)),
            cursor="hand2",
            image=getattr(Image, f"{color_name}_{soldier_name}_1"),
            state=tk.NORMAL,
        )

    def handle_click_event(self) -> None:
        match GameState.selected_game_objects:
            case [_]:
                self._handle_selection()
                GameState.selected_game_objects.append(self)
            case [_, SoldierRecruitment() as recruitment]:
                if recruitment is self:
                    GameState.selected_game_objects.pop()
                    self._handle_deselection()
                else:
                    recruitment.handle_click_event()
                    self.handle_click_event()
            case [*rest]:
                raise NotImplementedError(rest)

    def _handle_selection(self) -> None:
        [building] = GameState.selected_game_objects
        for dx, dy in {
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1),
        }:
            x, y = building.x + dx, building.y + dy
            if (
                0 < x < C.HORIZONTAL_LAND_TILE_COUNT - 1
                and 0 < y < C.VERTICAL_TILE_COUNT - 1
                and (x, y) not in GameState.occupied_coordinates
            ):
                PlacementHighlight(self._canvas, x, y)

        if ControlState.display_outcome_control:
            ControlState.display_outcome_control._main_widget.lift()

    def _handle_deselection(self) -> None:
        for highlight in list(HighlightState.placement_highlights):
            highlight.detach_and_destroy_widgets()
