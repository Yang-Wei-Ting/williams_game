import tkinter as tk
from collections.abc import Iterator
from random import choice, sample

from game.base import GameObject
from game.controls.display_outcome import DisplayOutcomeControl
from game.miscellaneous import Configuration as C
from game.soldiers import Archer, Cavalry, Infantry
from game.states import BuildingState, ControlState, DisplayState, GameState, SoldierState


class EndTurnControl(GameObject):

    @property
    def _main_widget_configuration(self) -> dict:
        return {
            **super()._main_widget_configuration,
            "command": self.handle_click_event,
            "cursor": "hand2",
            "state": tk.NORMAL,
            "text": "End turn",
            "width": 8,
        }

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, attach: bool = True) -> None:
        self._day_generator_iterator = self._day_generator_function()
        self._wave_generator_iterator = self._wave_generator_function()
        super().__init__(canvas, x, y, attach=attach)

    def _register(self) -> None:
        ControlState.end_turn_control = self

    def _unregister(self) -> None:
        ControlState.end_turn_control = None

    def handle_click_event(self) -> None:
        for obj in GameState.selected_game_objects[::-1]:
            obj.handle_click_event()

        for ally in SoldierState.allied_soldiers:
            ally.attacked_this_turn = False
            ally.moved_this_turn = False
            ally.refresh_widgets()

        if SoldierState.enemy_soldiers:
            self._execute_computer_turn()

            for enemy in SoldierState.enemy_soldiers:
                enemy.attacked_this_turn = False
                enemy.moved_this_turn = False
                enemy.refresh_widgets()
        else:
            next(self._day_generator_iterator)

    def _execute_computer_turn(self) -> None:
        if not SoldierState.allied_soldiers and not BuildingState.critical_buildings:
            DisplayOutcomeControl(self._canvas, text="You have been defeated.")
            return

        for enemy in SoldierState.enemy_soldiers:
            enemy.hunt()

            if not SoldierState.allied_soldiers and not BuildingState.critical_buildings:
                DisplayOutcomeControl(self._canvas, text="You have been defeated.")
                break

    def _day_generator_function(self) -> Iterator[None]:
        while True:
            GameState.day += 1
            DisplayState.day_display.refresh_widgets()
            for ally in SoldierState.allied_soldiers:
                ally.restore_health_by(5)
            yield

            GameState.day += 1
            DisplayState.day_display.refresh_widgets()
            try:
                next(self._wave_generator_iterator)
                yield
            except StopIteration:
                while True:
                    DisplayOutcomeControl(self._canvas, text="Victory is yours!")
                    yield

            GameState.day += 1
            DisplayState.day_display.refresh_widgets()
            GameState.coin += GameState.wave * 5
            DisplayState.coin_display.refresh_widgets()
            for ally in SoldierState.allied_soldiers:
                ally.restore_health_by(5)
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

        def get_random_area():
            return choice([area_north_east, area_north_west, area_south_east, area_south_west])

        def get_random_common_soldier():
            return choice([Archer, Cavalry, Infantry])

        GameState.wave = 1
        Infantry(self._canvas, *choice(get_random_area()), color=C.RED)
        yield

        GameState.wave = 2
        Archer(self._canvas, *choice(get_random_area()), color=C.RED)
        yield

        GameState.wave = 3
        Cavalry(self._canvas, *choice(get_random_area()), color=C.RED)
        yield

        GameState.wave = 4
        for coordinate in sample(get_random_area(), 2):
            get_random_common_soldier()(self._canvas, *coordinate, color=C.RED)
        yield

        GameState.wave = 5
        for coordinate in sample(get_random_area(), 3):
            get_random_common_soldier()(self._canvas, *coordinate, color=C.RED)
        yield

        GameState.wave = 6
        for coordinate in sample(get_random_area(), 4):
            get_random_common_soldier()(self._canvas, *coordinate, color=C.RED)
        yield

        GameState.wave = 7
        for coordinate in sample(get_random_area(), 5):
            get_random_common_soldier()(self._canvas, *coordinate, color=C.RED)
        yield
