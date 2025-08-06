import tkinter as tk
from collections.abc import Iterator
from functools import wraps
from math import ceil
from random import choice, sample
from tkinter import ttk

from game.base import GameObject, GameObjectModel, GameObjectView
from game.controls.display_outcome import DisplayOutcomeControl, DisplayOutcomeControlModel, DisplayOutcomeControlView
from game.miscellaneous import Configuration as C
from game.miscellaneous import Environment as E
from game.miscellaneous import msleep
from game.soldiers import Archer, Cavalry, Infantry
from game.soldiers.base import Soldier
from game.states import BuildingState, ControlState, DisplayState, GameState, SoldierState


def block_user_input_during(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        overlay = tk.Toplevel(self._view._canvas.master)
        overlay.wm_geometry(f"{E.SCREEN_WIDTH}x{E.SCREEN_HEIGHT}+0+0")

        match E.WINDOWING_SYSTEM:
            case "win32":
                overlay.wm_attributes("-alpha", 0.01, "-disabled", 1, "-topmost", 1)
                overlay.wm_overrideredirect(True)
            case "x11":
                overlay.wm_overrideredirect(True)
                overlay.wait_visibility()
                overlay.wm_attributes("-alpha", 0.01, "-topmost", 1)

                # Wait until the overlay becomes transparent.
                msleep(self._view._canvas.master, 20)

        value = func(self, *args, **kwargs)

        overlay.destroy()

        return value
    return wrapper


class EndTurnControlModel(GameObjectModel):

    def __init__(self, x: int, y: int) -> None:
        self._day_generator_iterator = self._day_generator_function()
        self._wave_generator_iterator = self._wave_generator_function()
        super().__init__(x, y)

    def _day_generator_function(self) -> Iterator[None]:
        while True:
            GameState.day += 1
            if DisplayState.day_display:
                DisplayState.day_display._view.refresh_main_appearance()
            for ally in SoldierState.allied_soldiers:
                ally.restore_health_by(10.0)
            yield

            GameState.day += 1
            if DisplayState.day_display:
                DisplayState.day_display._view.refresh_main_appearance()
            try:
                next(self._wave_generator_iterator)
                yield
            except StopIteration:
                while True:
                    display_outcome_control_model = DisplayOutcomeControlModel(text="Victory is yours!")
                    display_outcome_control_view = DisplayOutcomeControlView(
                        model=display_outcome_control_model,
                        canvas=self._canvas,
                        attach=True,
                    )
                    DisplayOutcomeControl(
                        model=display_outcome_control_model,
                        view=display_outcome_control_view,
                    )
                    yield

            GameState.day += 1
            if DisplayState.day_display:
                DisplayState.day_display._view.refresh_main_appearance()
            GameState.coin += 8 + (GameState.wave * 2)
            if DisplayState.coin_display:
                DisplayState.coin_display._view.refresh_main_appearance()
            for ally in SoldierState.allied_soldiers:
                ally.restore_health_by(10.0)
            yield

    def _wave_generator_function(self) -> Iterator[None]:
        H = C.HORIZONTAL_LAND_TILE_COUNT
        V = C.VERTICAL_TILE_COUNT
        area_north_east = [
            *[(x, 0) for x in range(H - 3, H - 1)],     #     2
            *[(H - 1, y) for y in range(6)],            #     ▔▕ 6
        ]
        area_north_west = [
            *[(x, 0) for x in range(1, 3)],             #    2
            *[(0, y) for y in range(6)],                # 6▕ ▔
        ]
        area_south_east = [
            *[(H - 1, y) for y in range(V - 6, V)],     #     ▁▕ 6
            *[(x, V - 1) for x in range(H - 3, H - 1)], #     2
        ]
        area_south_west = [
            *[(0, y) for y in range(V - 6, V)],         # 6▕ ▁
            *[(x, V - 1) for x in range(1, 3)],         #    2
        ]

        def sample_n_coordinates_from_m_areas(n: int, m: int) -> list:
            coordinates = []
            for area in sample([area_north_east, area_north_west, area_south_east, area_south_west], m):
                coordinates.extend(area)
            return sample(coordinates, n)

        ######## TODO
        def sample_common_soldiers() -> Soldier:
            return choice([Archer, Cavalry, Infantry])

        common_soldiers = {Archer, Cavalry, Infantry}
        while common_soldiers:
            GameState.wave += 1
            [(x, y)] = sample_n_coordinates_from_m_areas(1, 1)
            common_soldiers.pop()(self._canvas, x, y, color=C.RED)
            yield

        for n in range(2, 18 + 1, 2):
            m = ceil(n / 6)
            GameState.wave += 1
            for x, y in sample_n_coordinates_from_m_areas(n, m):
                sample_common_soldiers()(self._canvas, x, y, color=C.RED)
            yield


class EndTurnControlView(GameObjectView):

    def _create_widgets(self) -> None:
        self._widgets["main"] = ttk.Button(
            self._canvas,
            cursor="hand2",
            style="SmallText.Black_Burlywood4.TButton",
            takefocus=False,
            text="End turn",
        )


class EndTurnControl(GameObject):

    def _bind_or_unbind_event_handlers(self) -> None:
        self._view._widgets["main"].configure(command=self.handle_click_event)

    def _register(self) -> None:
        ControlState.end_turn_control = self

    def _unregister(self) -> None:
        ControlState.end_turn_control = None

    @block_user_input_during
    def handle_click_event(self) -> None:
        for obj in GameState.selected_game_objects[::-1]:
            obj.handle_click_event()

        if SoldierState.enemy_soldiers:
            for enemy in SoldierState.enemy_soldiers:
                enemy._model.attacked_this_turn = False
                enemy._model.moved_this_turn = False
                enemy._view.refresh_main_appearance()

            self._execute_computer_turn()
        else:
            next(self._model._day_generator_iterator)

        for ally in SoldierState.allied_soldiers:
            ally._model.attacked_this_turn = False
            ally._model.moved_this_turn = False
            ally._view.refresh_main_appearance()

    def _execute_computer_turn(self) -> None:
        if not SoldierState.allied_soldiers and not BuildingState.critical_buildings:
            display_outcome_control_model = DisplayOutcomeControlModel(text="You have been defeated.")
            display_outcome_control_view = DisplayOutcomeControlView(
                model=display_outcome_control_model,
                canvas=self._canvas,
                attach=True,
            )
            DisplayOutcomeControl(
                model=display_outcome_control_model,
                view=display_outcome_control_view,
            )
            return

        for enemy in SoldierState.enemy_soldiers:
            enemy.hunt()

            if not SoldierState.allied_soldiers and not BuildingState.critical_buildings:
                display_outcome_control_model = DisplayOutcomeControlModel(text="You have been defeated.")
                display_outcome_control_view = DisplayOutcomeControlView(
                    model=display_outcome_control_model,
                    canvas=self._canvas,
                    attach=True,
                )
                DisplayOutcomeControl(
                    model=display_outcome_control_model,
                    view=display_outcome_control_view,
                )
                break
