from collections.abc import Callable

from game.base import GameObject
from game.displays.base import Display, DisplayModel, DisplayView


class DayDisplayModel(DisplayModel):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.day = 1

    def get_data(self) -> dict:
        data = {
            **super().get_data(),
            "day": self.day,
        }
        return data


class DayDisplayView(DisplayView):

    def refresh(self, data: dict, event_handlers: dict[str, Callable]) -> None:
        self._widgets["main"].configure(text=f"Day:  {data["day"]:3d}")


class DayDisplay(Display):

    def _register(self) -> None:
        GameObject.singletons["day_display"] = self

    def _unregister(self) -> None:
        del GameObject.singletons["day_display"]
