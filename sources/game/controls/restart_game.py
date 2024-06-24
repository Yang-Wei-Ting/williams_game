import subprocess
import sys
from tkinter import ttk

from game.base import GameObject
from game.states import ControlState


class RestartGameControl(GameObject):

    def _create_widgets(self) -> None:
        self._main_widget = ttk.Button(
            self._canvas,
            command=self.handle_click_event,
            cursor="hand2",
            style="SmallText.Black_Burlywood4.TButton",
            takefocus=False,
            text="Restart",
        )

    def _register(self) -> None:
        ControlState.restart_game_control = self

    def _unregister(self) -> None:
        ControlState.restart_game_control = None

    def handle_click_event(self) -> None:
        self._canvas.master.destroy()

        proc = subprocess.run([sys.executable, sys.argv[0]])
        sys.exit(proc.returncode)
