import sys
import tkinter as tk
from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Callable
from tkinter import ttk

from game.miscellaneous import get_pixels


class GameObjectModel:

    occupied_coordinates: set[tuple[int, int]] = set()

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def destroy(self) -> None:
        pass

    def get_data(self) -> dict:
        return {"x": self.x, "y": self.y}

    def get_distance_to(self, other: "GameObjectModel | tuple[int, int]") -> int:
        """
        Return the Manhattan distance between self and other.
        """
        if isinstance(other, GameObjectModel):
            x, y = other.x, other.y
        else:
            x, y = other

        return abs(x - self.x) + abs(y - self.y)


class GameObjectView(ABC):

    def __init__(self, model: GameObjectModel, canvas: tk.Canvas, attach: bool = True) -> None:
        self.canvas = canvas
        self._widgets: dict[str, ttk.Widget] = {}
        self._ids: dict[str, int] = {}

        self._create_widgets()
        if attach:
            self.attach_widgets(model.get_data())

    def destroy(self) -> None:
        self.detach_widgets()
        self._destroy_widgets()

        self.canvas = None

    @abstractmethod
    def _create_widgets(self) -> None:
        raise NotImplementedError

    def _destroy_widgets(self) -> None:
        for widget in self._widgets.values():
            widget.destroy()
        self._widgets.clear()

    def attach_widgets(self, data: dict) -> None:
        self._ids["main"] = self.canvas.create_window(
            *get_pixels(data["x"], data["y"]),
            window=self._widgets["main"],
        )

    def detach_widgets(self) -> None:
        for id_ in self._ids.values():
            self.canvas.delete(id_)
        self._ids.clear()

    def lift_widgets(self) -> None:
        for widget in self._widgets.values():
            widget.lift()

    def refresh(self, data: dict, event_handlers: dict[str, Callable]) -> None:
        pass


class GameObject:

    singletons: dict[str, "GameObject"] = {}
    ordered_collections: defaultdict[str, list["GameObject"]] = defaultdict(list)
    unordered_collections: defaultdict[str, set["GameObject"]] = defaultdict(set)

    @classmethod
    def create(cls, model_config: dict, view_config: dict) -> "GameObject":
        model = cls.get_model_class()(**model_config)
        view = cls.get_view_class()(model, **view_config)
        return cls(model, view)

    @classmethod
    def get_model_class(cls) -> type[GameObjectModel]:
        module = sys.modules[cls.__module__]
        return getattr(module, cls.__name__ + "Model")

    @classmethod
    def get_view_class(cls) -> type[GameObjectView]:
        module = sys.modules[cls.__module__]
        return getattr(module, cls.__name__ + "View")

    def __init__(self, model: GameObjectModel, view: GameObjectView) -> None:
        self.model = model
        self.view = view
        self.refresh()
        self._register()

    def destroy(self) -> None:
        self._unregister()
        self.view.destroy()
        self.view = None
        self.model.destroy()
        self.model = None

    def refresh(self) -> None:
        self.view.refresh(self.model.get_data(), self.event_handlers)

    @abstractmethod
    def _register(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _unregister(self) -> None:
        raise NotImplementedError

    @property
    def event_handlers(self) -> dict[str, Callable]:
        return {}
