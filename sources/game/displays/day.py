from game.displays.base import Display
from game.states import DisplayState, GameState


class DayDisplay(Display):

    def _register(self) -> None:
        DisplayState.day_display = self

    def _unregister(self) -> None:
        DisplayState.day_display = None

    def refresh_widgets(self) -> None:
        self._main_widget.configure(text=f"Day:  {GameState.day:>3}")
