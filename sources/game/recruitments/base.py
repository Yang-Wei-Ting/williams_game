import sys
from collections.abc import Callable
from tkinter import ttk

from game.base import GameObject, GameObjectModel, GameObjectView
from game.highlights import PlacementHighlight
from game.miscellaneous import Configuration as C
from game.miscellaneous import Image, ImproperlyConfigured
from game.soldiers.base import Soldier


class SoldierRecruitmentModel(GameObjectModel):
    pass


class SoldierRecruitmentView(GameObjectView):

    def _create_widgets(self) -> None:
        self._widgets["main"] = ttk.Button(self.canvas, takefocus=False)

    def refresh(self, data: dict, event_handlers: dict[str, Callable]) -> None:
        if data["coin_reserve"] >= data["recruit_cost"]:
            color = C.BLUE
            command = event_handlers["click"]
        else:
            color = C.GRAY
            command = lambda: None

        color_name = C.COLOR_NAME_BY_HEX_TRIPLET[color]
        soldier_name = data["recruit_name"]

        self._widgets["main"].configure(
            cursor="hand2",
            command=command,
            image=getattr(Image, f"{color_name}_{soldier_name}_1"),
            style=f"Custom{color_name.capitalize()}.TButton",
        )


class SoldierRecruitment(GameObject):

    @property
    def target(self) -> type[Soldier]:
        module = sys.modules["game.soldiers"]
        return getattr(module, type(self).__name__.removesuffix("Recruitment"))

    def refresh(self) -> None:
        display = GameObject.singletons.get("coin_display")
        if not display:
            raise ImproperlyConfigured

        data = {
            "coin_reserve": display.model.coin,
            "recruit_name": self.target.__name__.lower(),
            "recruit_cost": self.target.get_model_class().cost,
        }
        self.view.refresh(data, self.event_handlers)

    def _register(self) -> None:
        GameObject.unordered_collections["barrack_recruitment"].add(self)

    def _unregister(self) -> None:
        GameObject.unordered_collections["barrack_recruitment"].remove(self)

    @property
    def event_handlers(self) -> dict[str, Callable]:
        return {"click": self.handle_click_event}

    def handle_click_event(self) -> None:
        selected_game_objects = GameObject.ordered_collections["selected_game_object"]

        match selected_game_objects:
            case [_]:
                self._handle_selection()
                selected_game_objects.append(self)
            case [_, SoldierRecruitment() as recruitment]:
                if recruitment is self:
                    selected_game_objects.pop()
                    self._handle_deselection()
                else:
                    recruitment.handle_click_event()
                    self.handle_click_event()
            case [*rest]:
                raise NotImplementedError(rest)

    def _handle_selection(self) -> None:
        [building] = GameObject.ordered_collections["selected_game_object"]
        for dx, dy in {
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1),
        }:
            x, y = building.model.x + dx, building.model.y + dy
            if (
                0 < x < C.HORIZONTAL_LAND_TILE_COUNT - 1
                and 0 < y < C.VERTICAL_TILE_COUNT - 1
                and (x, y) not in GameObjectModel.occupied_coordinates
            ):
                PlacementHighlight.create({"x": x, "y": y}, {"canvas": self.view.canvas})

        if control := GameObject.singletons.get("display_outcome_control"):
            control.view.lift_widgets()

    def _handle_deselection(self) -> None:
        for highlight in set(GameObject.unordered_collections["placement_highlight"]):
            highlight.destroy()
