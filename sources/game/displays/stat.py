from collections.abc import Callable
from textwrap import dedent

from game.base import GameObject
from game.displays.base import Display, DisplayModel, DisplayView


class StatDisplayModel(DisplayModel):
    pass


class StatDisplayView(DisplayView):

    def refresh(self, data: dict, event_handlers: dict[str, Callable]) -> None:
        if data:
            text = dedent(
                f"""\
                {data["name"]}

                LVL: {data["level"]:4d}
                EXP: {data["experience"]:4d}

                ATK: {int(data["attack"]):4d}
                RNG: {data["attack_range"]:4d}

                DEF: {int(data["defense"] * 100.0):4d}
                HP:  {int(data["health"]):4d}

                MOV: {data["mobility"]:4d}\
                """
            )
        else:
            text = "\n" * 11

        self._widgets["main"].configure(text=text)


class StatDisplay(Display):

    def refresh(self) -> None:
        if obj := GameObject.singletons.get("pressed_game_object"):
            data = obj.model.get_data()
        else:
            data = {}

        self.view.refresh(data, self.event_handlers)

    def _register(self) -> None:
        GameObject.singletons["stat_display"] = self

    def _unregister(self) -> None:
        del GameObject.singletons["stat_display"]
