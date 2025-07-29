from textwrap import dedent

from game.displays.base import Display
from game.states import DisplayState, GameState


class StatDisplay(Display):

    def _register(self) -> None:
        DisplayState.stat_display = self

    def _unregister(self) -> None:
        DisplayState.stat_display = None

    def refresh_widgets(self) -> None:
        if pressed := GameState.pressed_game_object:
            text = dedent(
                f"""\
                {type(pressed).__name__}

                LVL: {pressed.level:4d}
                EXP: {pressed.experience:4d}

                ATK: {int(pressed.attack):4d}
                RNG: {pressed.attack_range:4d}

                DEF: {int(pressed.defense * 100.0):4d}
                HP:  {int(pressed.health):4d}

                MOV: {pressed.mobility:4d}\
                """
            )
        else:
            text = "\n" * 11

        self._main_widget.configure(text=text)
