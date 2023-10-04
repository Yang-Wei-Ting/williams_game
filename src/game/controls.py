import subprocess
import sys
import tkinter as tk
from abc import abstractmethod
from random import choice

from game.bases import GameObject
from game.cores import Bowman, Horseman, King, Soldier, Swordsman
from game.miscs import Image


class Control(GameObject):
    """
    An abstract base class for all control button objects.
    """

    def _configure_widget(self) -> None:
        """
        Configure widget.
        """
        self.configure(
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

    instance = None

    def __init__(self, canvas: tk.Canvas, x: int, y: int) -> None:
        """
        """
        if Popup.instance:
            Popup.instance.handle_click_event()

        super().__init__(canvas, x, y)
        Popup.instance = self

    def handle_click_event(self) -> None:
        """
        Handle pop-up button's click events.
        """
        self.remove_canvas_window_object()
        Popup.instance = None


class EndTurn(Control):
    """
    A class that instantiates end turn buttons which upon clicked, end player's
    turn then execute computer's turn.
    """

    def __init__(self, canvas: tk.Canvas, x: int, y: int) -> None:
        """
        Create widget and canvas window object.
        """
        self._wave = self._create_enemies()
        super().__init__(canvas, x, y)

    def _configure_widget(self) -> None:
        """
        Configure widget.
        """
        super()._configure_widget()
        self.configure(image=Image.end_turn)

    def handle_click_event(self) -> None:
        """
        If an ally instance is chosen, unselect it first.
        If the targeted ally instance is out of an enemy instance's attack range,
        move the enemy instance toward the targeted ally instance.
        If any ally instance lies within the enemy instance's attack range, make
        the enemy instance attack the ally instance.
        If there's no enemy instance, heal all ally instances then create enemy instances.
        """
        if Soldier.chosen_ally:
            Soldier.chosen_ally.handle_click_event()

        for ally in Soldier.allies:
            ally.set_active()

        if not Soldier.enemies:
            try:
                next(self._wave)
            except StopIteration:
                if Popup.instance is None:
                    Popup(self._canvas, 0, 0).configure(image=Image.you_won)
                return

            for ally in Soldier.allies:
                ally.heal_itself(40)
        else:
            for enemy in Soldier.enemies:
                if Soldier.allies:
                    enemy.moved_this_turn = False
                    enemy.attacked_this_turn = False

                    enemy.attack_surrounding()
                    if enemy.attacked_this_turn:
                        enemy.promote()
                    else:
                        x, y = enemy.x, enemy.y
                        enemy.move_toward(Soldier.allies[0])
                        if enemy.x == x and enemy.y == y:
                            enemy.wobble()

                        enemy.attack_surrounding()
                        if enemy.attacked_this_turn:
                            enemy.promote()
                else:
                    if Popup.instance is None:
                        Popup(self._canvas, 0, 0).configure(image=Image.you_lost)
                    break

            for enemy in Soldier.enemies:
                enemy.set_active()

        for ally in Soldier.allies:
            ally.moved_this_turn = False
            ally.attacked_this_turn = False

    def _create_enemies(self):
        """
        Create enemy instances.
        """
        # Wave 1
        for x in range(-1, 2):
            Bowman(self._canvas, x, 6)
        yield

        # Wave 2
        for x in range(-2, 3):
            Horseman(self._canvas, x, 6)
        yield

        # Wave 3
        for x in range(-3, 4):
            Swordsman(self._canvas, x, 6)
        yield

        # Wave 4
        for x in range(-5, 6):
            choice([Bowman, Horseman, Swordsman])(self._canvas, x, 6).promote(4)
        yield

        # Wave 5
        for x in range(-5, 6):
            choice([Bowman, Horseman, Swordsman])(self._canvas, x, 6).promote(4)
        for x in range(-2, 3):
            choice([Bowman, Horseman, Swordsman])(self._canvas, x, 5).promote(4)
        yield

        # Wave 6
        for x in range(-3, 4):
            Bowman(self._canvas, x, 6)
            Swordsman(self._canvas, x, 5).promote(12)
        for x in (-5, -4, 4, 5):
            for y in (5, 6):
                Horseman(self._canvas, x, y).promote(12)
        yield

        # Wave 7
        for x in range(-3, 4):
            for y in (5, 6):
                Bowman(self._canvas, x, y)
        for x in (-5, -4, 4, 5):
            for y in range(4, 7):
                Horseman(self._canvas, x, y).promote(12)
        for x in (-3, -2, -1, 1, 2, 3):
            Swordsman(self._canvas, x, 4).promote(12)
        King(self._canvas, 0, 4).promote(60)
        yield


class Restart(Control):
    """
    A class that instantiates restart buttons which upon clicked, restart the game.
    """

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, window: tk.Tk) -> None:
        """
        Create widget and canvas window object.
        """
        self._window = window
        super().__init__(canvas, x, y)

    def _configure_widget(self) -> None:
        """
        Configure widget.
        """
        super()._configure_widget()
        self.configure(image=Image.restart)

    def handle_click_event(self) -> None:
        """
        Restart the game.
        """
        self._window.destroy()

        proc = subprocess.run([sys.executable, sys.argv[0]])
        sys.exit(proc.returncode)
