import tkinter as tk
from abc import abstractmethod
from collections.abc import Callable
from tkinter import ttk

from game.base import GameObject, GameObjectModel, GameObjectView
from game.miscellaneous import Configuration as C
from game.miscellaneous import Image, get_pixels


class BuildingModel(GameObjectModel):

    defense = 0.4
    health = 400.0

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self._register()

    def destroy(self) -> None:
        self._unregister()

    def _register(self) -> None:
        GameObjectModel.occupied_coordinates.add((self.x, self.y))

    def _unregister(self) -> None:
        GameObjectModel.occupied_coordinates.remove((self.x, self.y))

    def get_data(self) -> dict:
        data = {
            **super().get_data(),
            "defense": self.defense,
            "health": self.health,
            "max_health": type(self).health,
        }
        return data


class BuildingView(GameObjectView):

    def _create_widgets(self) -> None:
        self._widgets["main"] = ttk.Button(
            self.canvas,
            cursor="hand2",
            image=getattr(Image, type(self).__name__.removesuffix("View").lower()),
            style="CustomBlue.TButton",
            takefocus=False,
        )
        self._widgets["health_bar"] = ttk.Progressbar(
            self.canvas,
            length=C.HEALTH_BAR_LENGTH,
            mode="determinate",
            orient=tk.HORIZONTAL,
            style="Green_Red.Horizontal.TProgressbar",
        )

    def attach_widgets(self, data: dict) -> None:
        self._ids["main"] = self.canvas.create_window(
            *get_pixels(data["x"], data["y"], y_pixel_shift=5.0),
            window=self._widgets["main"],
        )
        self._ids["health_bar"] = self.canvas.create_window(
            *get_pixels(data["x"], data["y"], y_pixel_shift=-22.5),
            window=self._widgets["health_bar"],
        )

    def refresh(self, data: dict, event_handlers: dict[str, Callable]) -> None:
        self._widgets["main"].configure(
            command=event_handlers["click"],
        )
        self._widgets["health_bar"].configure(
            value=data["health"],
            maximum=data["max_health"],
        )


class Building(GameObject):

    @property
    def event_handlers(self) -> dict[str, Callable]:
        return {"click": self.handle_click_event}

    def handle_click_event(self) -> None:
        selected_game_objects = GameObject.ordered_collections["selected_game_object"]

        match selected_game_objects:
            case []:
                self._handle_selection()
                selected_game_objects.append(self)
            case [Building() as building]:
                if building is self:
                    selected_game_objects.pop()
                    self._handle_deselection()
                else:
                    building.handle_click_event()
                    self.handle_click_event()
            case [*_, last_selected]:
                last_selected.handle_click_event()
                self.handle_click_event()
            case [*rest]:
                raise NotImplementedError(rest)

    @abstractmethod
    def _handle_selection(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _handle_deselection(self) -> None:
        raise NotImplementedError
