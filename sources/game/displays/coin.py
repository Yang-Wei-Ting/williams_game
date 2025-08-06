from game.displays.base import Display, DisplayModel, DisplayView
from game.states import DisplayState, GameState


class CoinDisplayModel(DisplayModel):

    def __init__(self, x: int, y: int, starting_coin: int = 10) -> None:
        super().__init__(x, y, _coin=starting_coin)

    def get_data(self) -> dict:
        data = {
            **super().get_data(),
            "coin": self._coin,
        }
        return data


#####################################
class CoinDisplayView(DisplayView):

    def refresh_main_appearance(self, data: dict) -> None:
        self._widgets["main"].configure(text=f"Coin: {data["coin"]:3d}")


class CoinDisplay(Display):

    def _register(self) -> None:
        DisplayState.coin_display = self

    def _unregister(self) -> None:
        DisplayState.coin_display = None
