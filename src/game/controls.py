import subprocess
import sys
import tkinter as tk
from abc import abstractmethod
from random import choice, sample

from game.bases import GameObject
from game.miscs import Configuration as C
from game.miscs import Image
from game.soldiers import Archer, Cavalry, Infantry, King
from game.states import PopupState, SoldierState


class Control(GameObject):
    """
    An abstract base class for all control button objects.
    """

    def _create_widgets(self) -> None:
        self._main_widget = tk.Button(self._canvas)

    def _configure_widgets(self) -> None:
        """
        Configure widgets.
        """
        self.configure_main_widget(
            background="Burlywood4",
            activebackground="Burlywood4",
            relief=tk.RAISED,
            borderwidth=5,
            highlightthickness=0,
            cursor="hand2",
            command=self.handle_click_event,
        )

    @abstractmethod
    def handle_click_event(self) -> None:
        """
        Handle control button's click events.
        """
        raise NotImplementedError


class Popup(Control):
    """
    A class that instantiates pop-up button objects.
    Only one pop-up button object can exist at a given time.
    """

    def __init__(self, canvas: tk.Canvas, x: int, y: int) -> None:
        """
        """
        if PopupState.instance:
            PopupState.instance.handle_click_event()

        super().__init__(canvas, x, y)
        PopupState.instance = self

    def handle_click_event(self) -> None:
        """
        Handle pop-up button's click events.
        """
        PopupState.instance = None
        self.destroy_widgets()


class EndTurn(Control):
    """
    A class that instantiates end turn buttons which upon clicked, end player's
    turn then execute computer's turn.
    """

    def __init__(self, canvas: tk.Canvas, x: int, y: int) -> None:
        """
        Create widgets then attach them to canvas.
        """
        self._enemy_wave_generator_iterator = self._enemy_wave_generator_function()
        super().__init__(canvas, x, y)

    def _configure_widgets(self) -> None:
        """
        Configure widgets.
        """
        super()._configure_widgets()
        self.configure_main_widget(image=Image.end_turn)

    def handle_click_event(self) -> None:
        """
        If an ally instance is chosen, unselect it first.
        Activate all ally instances.
        If there's any enemy instance left, execute computer's turn then activate
        all enemy instances. Otherwise, summon next enemy wave.
        """
        if SoldierState.chosen_ally:
            SoldierState.chosen_ally.handle_click_event()

        for ally in SoldierState.allies:
            ally.moved_this_turn = False
            ally.attacked_this_turn = False
            ally.refresh_image()

        if SoldierState.enemies:
            self._execute_computer_turn()

            for enemy in SoldierState.enemies:
                enemy.moved_this_turn = False
                enemy.attacked_this_turn = False
                enemy.refresh_image()
        else:
            self._summon_next_wave()

    def _execute_computer_turn(self) -> None:
        """
        Execute each enemy's turn.
        If there is no ally instance, display defeat pop-up.
        """
        if not SoldierState.allies:
            self._display_popup("defeat")
            return

        for enemy in sample(SoldierState.enemies, len(SoldierState.enemies)):
            enemy.hunt()

            if not SoldierState.allies:
                self._display_popup("defeat")
                break

    def _summon_next_wave(self) -> None:
        """
        Summon next enemy wave and heal all ally instances.
        If there is no more enemy wave, display victory pop-up.
        """
        try:
            next(self._enemy_wave_generator_iterator)
        except StopIteration:
            self._display_popup("victory")
        else:
            for ally in SoldierState.allies:
                ally.heal_itself(40)

    def _display_popup(self, image_name: str) -> None:
        """
        Display pop-up image.
        """
        if PopupState.instance is None:
            x, y = C.HORIZONTAL_LAND_TILE_COUNT // 2, C.VERTICAL_TILE_COUNT // 2
            Popup(self._canvas, x, y).configure_main_widget(image=getattr(Image, image_name))

    def _enemy_wave_generator_function(self):
        """
        Lazily create enemy waves.
        """
        # Wave 1
        for x in range(4, 7):
            Archer(self._canvas, x, 0)
        yield

        # Wave 2
        for x in range(3, 8):
            Cavalry(self._canvas, x, 0)
        yield

        # Wave 3
        for x in range(2, 9):
            Infantry(self._canvas, x, 0)
        yield

        # Wave 4
        for x in range(0, 11):
            choice([Archer, Cavalry, Infantry])(self._canvas, x, 0).promote(4)
        yield

        # Wave 5
        for x in range(0, 11):
            choice([Archer, Cavalry, Infantry])(self._canvas, x, 0).promote(4)
        for x in range(3, 8):
            choice([Archer, Cavalry, Infantry])(self._canvas, x, 1).promote(4)
        yield

        # Wave 6
        for x in range(2, 9):
            Archer(self._canvas, x, 0)
            Infantry(self._canvas, x, 1).promote(12)
        for x in (0, 1, 9, 10):
            for y in (0, 1):
                Cavalry(self._canvas, x, y).promote(12)
        yield

        # Wave 7
        for x in range(2, 9):
            for y in (0, 1):
                Archer(self._canvas, x, y)
        for x in (0, 1, 9, 10):
            for y in range(0, 3):
                Cavalry(self._canvas, x, y).promote(12)
        for x in (2, 3, 4, 6, 7, 8):
            Infantry(self._canvas, x, 2).promote(12)
        King(self._canvas, 5, 2).promote(60)
        yield


class Restart(Control):
    """
    A class that instantiates restart buttons which upon clicked, restart the game.
    """

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, window: tk.Tk) -> None:
        """
        Create widgets then attach them to canvas.
        """
        self._window = window
        super().__init__(canvas, x, y)

    def _configure_widgets(self) -> None:
        """
        Configure widgets.
        """
        super()._configure_widgets()
        self.configure_main_widget(image=Image.restart)

    def handle_click_event(self) -> None:
        """
        Restart the game.
        """
        self._window.destroy()

        proc = subprocess.run([sys.executable, sys.argv[0]])
        sys.exit(proc.returncode)
