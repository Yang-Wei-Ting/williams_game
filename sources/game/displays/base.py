from abc import abstractmethod

from game.base import GameObject


class Display(GameObject):

    @property
    def _main_widget_configuration(self) -> dict:
        return {
            **super()._main_widget_configuration,
            "width": 8,
        }

    def _create_widgets(self) -> None:
        super()._create_widgets()
        self.refresh_widgets()

    @abstractmethod
    def refresh_widgets(self) -> None:
        raise NotImplementedError
