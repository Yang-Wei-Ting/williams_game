import tkinter as tk
from abc import abstractmethod
from tkinter.ttk import Progressbar

from game.base import GameObject
from game.miscellaneous import Configuration as C
from game.miscellaneous import Image, get_pixels
from game.states import GameState


class Building(GameObject):

    @property
    def _main_widget_configuration(self) -> dict:
        return {
            **super()._main_widget_configuration,
            "activebackground": C.BLUE,
            "background": C.BLUE,
            "command": self.handle_click_event,
            "cursor": "hand2",
            "image": getattr(Image, type(self).__name__.lower()),
            "state": tk.NORMAL,
        }

    @property
    def _health_bar_configuration(self) -> dict:
        return {
            "length": C.HEALTH_BAR_LENGTH,
            "maximum": self.health,
            "mode": "determinate",
            "orient": tk.HORIZONTAL,
            "style": "TProgressbar",
            "value": self.health,
        }

    def _create_widgets(self) -> None:
        super()._create_widgets()
        self.health_bar = Progressbar(self._canvas, **self._health_bar_configuration)

    def _destroy_widgets(self) -> None:
        self.health_bar.destroy()
        del self.health_bar
        super()._destroy_widgets()

    @abstractmethod
    def _register(self) -> None:
        GameState.occupied_coordinates.add((self.x, self.y))

    @abstractmethod
    def _unregister(self) -> None:
        GameState.occupied_coordinates.remove((self.x, self.y))

    def attach_widgets_to_canvas(self) -> None:
        self._main_widget_id = self._canvas.create_window(
            *get_pixels(self.x, self.y, y_pixel_shift=5.0),
            window=self._main_widget,
        )
        self._health_bar_id = self._canvas.create_window(
            *get_pixels(self.x, self.y, y_pixel_shift=-22.5),
            window=self.health_bar,
        )

    def detach_widgets_from_canvas(self) -> None:
        self._canvas.delete(self._health_bar_id)
        del self._health_bar_id
        super().detach_widgets_from_canvas()

    def handle_click_event(self) -> None:
        match GameState.selected_game_objects:
            case []:
                self._handle_selection()
                GameState.selected_game_objects.append(self)
            case [Building() as building]:
                if building is self:
                    GameState.selected_game_objects.pop()
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
