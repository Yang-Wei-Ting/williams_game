import tkinter as tk
from collections.abc import Callable, Iterator
from functools import wraps
from math import ceil
from random import choice, sample
from tkinter import ttk

from game.base import GameObject, GameObjectModel, GameObjectView
from game.controls.display_outcome import DisplayOutcomeControl
from game.miscellaneous import Configuration as C
from game.miscellaneous import Environment as E
from game.miscellaneous import ImproperlyConfigured, msleep
from game.soldiers import Archer, Cavalry, Infantry
from game.soldiers.base import Soldier
from game.states import GameState


def block_user_input_during(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        overlay = tk.Toplevel(self.view.canvas.master)
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
                msleep(self.view.canvas.master, 20)

        value = func(self, *args, **kwargs)

        overlay.destroy()

        return value

    return wrapper


class EndTurnControlModel(GameObjectModel):
    pass


class EndTurnControlView(GameObjectView):

    def _create_widgets(self) -> None:
        self._widgets["main"] = ttk.Button(
            self.canvas,
            cursor="hand2",
            style="SmallText.Black_Burlywood4.TButton",
            takefocus=False,
            text="End turn",
        )

    def refresh(self, data: dict, event_handlers: dict[str, Callable]) -> None:
        self._widgets["main"].configure(command=event_handlers["click"])


class EndTurnControl(GameObject):

    def __init__(self, model: EndTurnControlModel, view: EndTurnControlView) -> None:
        self._day_generator_iterator = self._day_generator_function()
        self._wave_generator_iterator = self._wave_generator_function()
        super().__init__(model, view)

    def _register(self) -> None:
        GameObject.singletons["end_turn_control"] = self

    def _unregister(self) -> None:
        del GameObject.singletons["end_turn_control"]

    @property
    def event_handlers(self) -> dict[str, Callable]:
        return {"click": self.handle_click_event}

    @block_user_input_during
    def handle_click_event(self) -> None:
        for obj in GameObject.ordered_collections["selected_game_object"][::-1]:
            obj.handle_click_event()

        if GameObject.unordered_collections["enemy_soldier"]:
            for enemy in GameObject.unordered_collections["enemy_soldier"]:
                enemy.model.attacked_this_turn = False
                enemy.model.moved_this_turn = False
                enemy.refresh()

            self._execute_computer_turn()
        else:
            next(self._day_generator_iterator)

        for ally in GameObject.unordered_collections["allied_soldier"]:
            ally.model.attacked_this_turn = False
            ally.model.moved_this_turn = False
            ally.refresh()

    def _execute_computer_turn(self) -> None:
        allied_soldiers = GameObject.unordered_collections["allied_soldier"]
        enemy_soldiers = GameObject.unordered_collections["enemy_soldier"]
        critical_buildings = GameObject.unordered_collections["critical_building"]

        if not allied_soldiers and not critical_buildings:
            DisplayOutcomeControl.create(
                {"text": "You have been defeated."},
                {"canvas": self.view.canvas},
            )
            return

        for enemy in enemy_soldiers:
            enemy.hunt()

            if not allied_soldiers and not critical_buildings:
                DisplayOutcomeControl.create(
                    {"text": "You have been defeated."},
                    {"canvas": self.view.canvas},
                )
                break

    def _day_generator_function(self) -> Iterator[None]:
        day_display = GameObject.singletons.get("day_display")
        coin_display = GameObject.singletons.get("coin_display")
        if not day_display or not coin_display:
            raise ImproperlyConfigured

        allied_soldiers = GameObject.unordered_collections["allied_soldier"]

        while True:
            day_display.model.day += 1
            day_display.refresh()
            for ally in allied_soldiers:
                ally.restore_health_by(10.0)
            yield

            day_display.model.day += 1
            day_display.refresh()
            try:
                next(self._wave_generator_iterator)
                yield
            except StopIteration:
                while True:
                    DisplayOutcomeControl.create(
                        {"text": "Victory is yours!"},
                        {"canvas": self.view.canvas},
                    )
                    yield

            day_display.model.day += 1
            day_display.refresh()
            coin_display.model.coin += 8 + (GameState.wave * 2)
            coin_display.refresh()
            for ally in allied_soldiers:
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

        def sample_n_coordinates_from_m_areas(n: int, m: int) -> list[tuple[int, int]]:
            coordinates = []
            for area in sample(
                [area_north_east, area_north_west, area_south_east, area_south_west], m
            ):
                coordinates.extend(area)
            return sample(coordinates, n)

        def sample_common_soldiers() -> type[Soldier]:
            return choice([Archer, Cavalry, Infantry])

        common_soldiers = {Archer, Cavalry, Infantry}
        while common_soldiers:
            GameState.wave += 1
            [(x, y)] = sample_n_coordinates_from_m_areas(1, 1)
            common_soldiers.pop().create(
                {"x": x, "y": y, "color": C.RED},
                {"canvas": self.view.canvas},
            )
            yield

        for n in range(2, 18 + 1, 2):
            m = ceil(n / 6)
            GameState.wave += 1
            for x, y in sample_n_coordinates_from_m_areas(n, m):
                sample_common_soldiers().create(
                    {"x": x, "y": y, "color": C.RED},
                    {"canvas": self.view.canvas},
                )
            yield
