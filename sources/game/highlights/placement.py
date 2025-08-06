from collections.abc import Callable
from tkinter import ttk

from game.base import GameObject, GameObjectModel, GameObjectView
from game.miscellaneous import Configuration as C
from game.miscellaneous import Image, ImproperlyConfigured


class PlacementHighlightModel(GameObjectModel):
    pass


class PlacementHighlightView(GameObjectView):

    def _create_widgets(self) -> None:
        self._widgets["main"] = ttk.Button(
            self.canvas,
            cursor="hand2",
            style="Flat.Royalblue1.TButton",
            takefocus=False,
            image=Image.transparent_12x12,
        )

    def refresh(self, data: dict, event_handlers: dict[str, Callable]) -> None:
        self._widgets["main"].configure(command=event_handlers["click"])


class PlacementHighlight(GameObject):

    def _register(self) -> None:
        GameObject.unordered_collections["placement_highlight"].add(self)

    def _unregister(self) -> None:
        GameObject.unordered_collections["placement_highlight"].remove(self)

    @property
    def event_handlers(self) -> dict[str, Callable]:
        return {"click": self.handle_click_event}

    def handle_click_event(self) -> None:
        display = GameObject.singletons.get("coin_display")
        if not display:
            raise ImproperlyConfigured

        recruitment = GameObject.ordered_collections["selected_game_object"][-1]

        display.model.coin -= recruitment.target.get_model_class().cost
        display.refresh()

        for _recruitment in GameObject.unordered_collections["barrack_recruitment"]:
            _recruitment.refresh()

        soldier = recruitment.target.create(
            {
                "x": self.model.x,
                "y": self.model.y,
                "color": C.BLUE,
            },
            {
                "canvas": self.view.canvas,
                "attach": False,
            },
        )
        soldier.model.attacked_this_turn = True
        soldier.model.moved_this_turn = True
        soldier.refresh()
        data = soldier.model.get_data()
        soldier.view.attach_widgets(data)

        recruitment.handle_click_event()
