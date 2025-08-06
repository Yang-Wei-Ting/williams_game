from textwrap import dedent

from game.displays.base import Display, DisplayModel, DisplayView
from game.states import DisplayState, GameState


class StatDisplayModel(DisplayModel):
    pass


class StatDisplayView(DisplayView):

    def refresh_main_appearance(self, data: dict) -> None:
        if pressed := GameState.pressed_game_object:
            text = dedent(
                f"""\
                {type(pressed).__name__}

                LVL: {pressed._model.level:4d}
                EXP: {pressed._model.experience:4d}

                ATK: {int(pressed._model.attack):4d}
                RNG: {pressed._model.attack_range:4d}

                DEF: {int(pressed._model.defense * 100.0):4d}
                HP:  {int(pressed._model.health):4d}

                MOV: {pressed._model.mobility:4d}\
                """
            )
        else:
            text = "\n" * 11

        self._widgets["main"].configure(text=text)


class StatDisplay(Display):

    def _register(self) -> None:
        DisplayState.stat_display = self

    def _unregister(self) -> None:
        DisplayState.stat_display = None
