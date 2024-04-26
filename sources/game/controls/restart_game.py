import subprocess
import sys
import tkinter as tk

from game.base import GameObject
from game.states import ControlState


class RestartGameControl(GameObject):

    @property
    def _main_widget_configuration(self) -> dict:
        return {
            **super()._main_widget_configuration,
            "command": self.handle_click_event,
            "cursor": "hand2",
            "state": tk.NORMAL,
            "text": "Restart",
            "width": 8,
        }

    def _register(self) -> None:
        ControlState.restart_game_control = self

    def _unregister(self) -> None:
        ControlState.restart_game_control = None

    def handle_click_event(self) -> None:
        self._canvas.master.destroy()

        proc = subprocess.run([sys.executable, sys.argv[0]])
        sys.exit(proc.returncode)
