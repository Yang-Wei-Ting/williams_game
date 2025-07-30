from game.displays.base import Display
from game.states import DisplayState, GameState


class CoinDisplay(Display):

    def _register(self) -> None:
        DisplayState.coin_display = self

    def _unregister(self) -> None:
        DisplayState.coin_display = None

    def refresh_widgets(self) -> None:
        self._main_widget.configure(text=f"Coin: {GameState.coin:>3}")
