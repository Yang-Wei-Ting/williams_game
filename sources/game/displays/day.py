from game.displays.base import Display, DisplayModel, DisplayView
from game.states import DisplayState, GameState


class DayDisplayModel(DisplayModel):
    pass


class DayDisplayView(DisplayView):

    def refresh_main_appearance(self) -> None:
        self._widgets["main"].configure(text=f"Day:  {GameState.day:3d}")


class DayDisplay(Display):

    def _register(self) -> None:
        DisplayState.day_display = self

    def _unregister(self) -> None:
        DisplayState.day_display = None
