import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk

from game.miscellaneous import get_pixels


class GameObjectModel:

    occupied_coordinates = set()

    def __init__(self, x: int, y: int, **kwargs) -> None:
        self.x = x
        self.y = y
        for key, value in kwargs.items():
            setattr(self, key, value)

        self._add_to_occupied_coordinates()

    def destroy(self) -> None:
        self._remove_from_occupied_coordinates()

    def _add_to_occupied_coordinates(self):
        GameObjectModel.occupied_coordinates.add((self.x, self.y))

    def _remove_from_occupied_coordinates(self):
        GameObjectModel.occupied_coordinates.remove((self.x, self.y))

    # GET
    def get_data(self) -> dict:
        return {"x": self.x, "y": self.y}

    def get_distance_to(self, other: "GameObjectModel | tuple") -> int:
        """
        Return the Manhattan distance between self and other.
        """
        if isinstance(other, GameObjectModel):
            x, y = other.x, other.y
        else:
            x, y = other

        return abs(x - self.x) + abs(y - self.y)

    # SET
    def move_to(self, x: int, y: int) -> None:
        """
        Move self to the new coordinate.
        """
        self._remove_from_occupied_coordinates()
        self.x = x
        self.y = y
        self._add_to_occupied_coordinates()


class GameObjectView(ABC):

    def __init__(self, model: GameObjectModel, canvas: tk.Canvas, attach: bool = True) -> None:
        self._canvas = canvas
        self._widgets: dict[str, ttk.Widget] = {}
        self._ids: dict[str, int] = {}

        data = model.get_data()
        self._create_widgets(data)
        if attach:
            self.attach_widgets(data)

    def destroy(self) -> None:
        self.detach_widgets()
        self._destroy_widgets()
        self._canvas = None

    @abstractmethod
    def _create_widgets(self, data: dict) -> None:
        raise NotImplementedError

    def _destroy_widgets(self) -> None:
        for widget in self._widgets.values():
            widget.destroy()
        self._widgets.clear()

    def attach_widgets(self, data: dict) -> None:
        self._ids["main"] = self._canvas.create_window(
            *get_pixels(data["x"], data["y"]), window=self._widgets["main"],
        )

    def detach_widgets(self) -> None:
        for id_ in self._ids.values():
            self._canvas.delete(id_)
        self._ids.clear()

    def bind_or_unbind_event_handlers(self, data: dict, event_handlers: dict) -> None:
        pass

    def refresh_main_appearance(self, data: dict) -> None:
        pass

    def refresh_main_position(self, data: dict) -> None:
        pass


class GameObject:

    def __init__(self, model: GameObjectModel, view: GameObjectView) -> None:
        self._model = model
        self._view = view
        self._view.bind_or_unbind_event_handlers(
            data=self._model.get_data(),
            event_handlers=self._get_event_handlers(),
        )

        self._register()

    def destroy(self) -> None:
        self._unregister()

        self._view = self._view.destroy()
        self._model = self._model.destroy()

    def _register(self) -> None:
        pass

    def _unregister(self) -> None:
        pass

    def _get_event_handlers(self) -> dict:
        return {}
