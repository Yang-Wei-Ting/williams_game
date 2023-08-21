import itertools
import math
import os
import sys
import tkinter as tk
from abc import ABC, abstractmethod
from glob import glob
from pathlib import PurePath
from random import choice
from subprocess import Popen
from tkinter.ttk import Progressbar


class Color:
    """
    A class that manages colors.
    """

    BLUE = "#043E6F"
    GRAY = "#3B3B3B"
    RED = "#801110"
    MAPPING = {BLUE: "blue", RED: "red"}


class Image:
    """
    A class that manages images.
    """

    @classmethod
    def initialize(cls) -> None:
        """
        Hook all images onto cls.
        """
        for path in glob("../images/*"):
            setattr(cls, PurePath(path).stem, tk.PhotoImage(file=path))


class GameObject(ABC):
    """
    An abstract base class for all game objects.
    """

    def __init__(self, canvas: tk.Canvas, x: int, y: int):
        """
        Create widget and canvas window object.
        """
        self._canvas = canvas
        self.x = x
        self.y = y
        self._create_widget()
        self._configure_widget()
        self._create_canvas_window_object()

    def _create_widget(self) -> None:
        """
        Create widget.
        """
        super(ABC, self).__init__(self._canvas)

    @abstractmethod
    def _configure_widget(self) -> None:
        """
        Configure widget.
        """
        self.configure()

    def _create_canvas_window_object(self) -> None:
        """
        Create canvas window object.
        """
        self._main_widget_id = self._canvas.create_window(
            self.x * 60 + 390,
            -self.y * 60 + 395,
            window=self,
        )

    def remove_canvas_window_object(self) -> None:
        """
        Remove canvas window object. Do nothing if no canvas window object exists.
        """
        if hasattr(self, "_main_widget_id"):
            self._canvas.delete(self._main_widget_id)
            delattr(self, "_main_widget_id")

    def move_to(self, x: int, y: int) -> None:
        """
        Move self to the new coordinate and update canvas window object's coordinate.
        """
        self.x = x
        self.y = y
        self._canvas.coords(self._main_widget_id, self.x * 60 + 390, -self.y * 60 + 395)

    def get_distance_between(self, other) -> float:
        """
        Return the distance between self and other.
        """
        return math.dist((self.x, self.y), (other.x, other.y))


class Control(GameObject, tk.Button):
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


class Popup(Control):
    """
    A class that instantiates popup button objects.
    Only one popup button object can exist at a given time.
    """

    instance = None

    def __init__(self, canvas: tk.Canvas, x: int, y: int):
        """
        """
        if Popup.instance:
            Popup.instance.handle_click_event()

        super().__init__(canvas, x, y)
        Popup.instance = self

    def handle_click_event(self) -> None:
        """
        Handle popup button's click events.
        """
        self.remove_canvas_window_object()
        Popup.instance = None


class EndTurn(Control):
    """
    A class that instantiates end turn buttons which upon clicked, end player's
    turn then execute computer's turn.
    """

    def __init__(self, canvas: tk.Canvas, x: int, y: int):
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

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, window: tk.Tk):
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

        with Popen([sys.executable, os.path.realpath(sys.argv[0])]) as proc:
            proc.communicate()

        sys.exit(0)


class Soldier(GameObject, tk.Button):
    """
    An abstract base class for all soldier game objects.
    This class keeps tracks of all its derived class instances and their coordinates.
    """

    allies = []
    enemies = []
    coordinates = set()
    chosen_ally = None

    attack = 30
    attack_range = 1
    defense = 15
    health = 70
    mobility = 2

    level = 1
    experience = 0
    PROMOTION_EXPERIENCE = {1: 4, 2: 8, 3: 16, 4: 32, 5: math.inf}

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, color: str = Color.RED):
        """
        Create widget and canvas window object.
        """
        self.color = color
        self.moved_this_turn = False
        self.attacked_this_turn = False
        super().__init__(canvas, x, y)

    def _configure_widget(self) -> None:
        """
        Configure widget.
        """
        name = f"{Color.MAPPING[self.color]}_{self.__class__.__name__.lower()}_{self.level}"
        self.configure(
            image=getattr(Image, name),
            background=self.color,
            activebackground=self.color,
            relief=tk.RAISED,
            borderwidth=5,
            highlightthickness=0,
            cursor="hand2",
            command=self.handle_click_event,
        )

    def _create_canvas_window_object(self) -> None:
        """
        Create canvas window object.
        Add self to 'Soldier.allies' or 'Soldier.enemies'.
        Add self's coordinate to 'Soldier.coordinates'.
        """
        super()._create_canvas_window_object()

        self.healthbar = Progressbar(
            self._canvas,
            length=self.health / 2,
            maximum=self.health,
            mode="determinate",
            orient=tk.HORIZONTAL,
            style="TProgressbar",
            value=self.health,
        )
        self._healthbar_id = self._canvas.create_window(
            self.x * 60 + 390,
            -self.y * 60 + 367.5,
            window=self.healthbar,
        )

        match self.color:
            case Color.BLUE:
                Soldier.allies.append(self)
            case Color.RED:
                Soldier.enemies.append(self)
        Soldier.coordinates.add((self.x, self.y))

    def remove_canvas_window_object(self) -> None:
        """
        Remove canvas window object.
        Remove self from 'Soldier.allies' or 'Soldier.enemies'.
        Remove self's coordinate from 'Soldier.coordinates'.
        """
        super().remove_canvas_window_object()

        if hasattr(self, "_healthbar_id"):
            self._canvas.delete(self._healthbar_id)
            delattr(self, "_healthbar_id")
            delattr(self, "healthbar")

        match self.color:
            case Color.BLUE:
                Soldier.allies.remove(self)
            case Color.RED:
                Soldier.enemies.remove(self)
        Soldier.coordinates.remove((self.x, self.y))

    def move_to(self, x: int, y: int) -> None:
        """
        Move self to the new coordinate and update canvas window object's coordinate.
        Update 'Soldier.coordinates' to reflect self's coordinate change.
        """
        Soldier.coordinates.remove((self.x, self.y))
        super().move_to(x, y)
        self._canvas.coords(self._healthbar_id, self.x * 60 + 390, -self.y * 60 + 365)
        Soldier.coordinates.add((self.x, self.y))

        self.moved_this_turn = True
        if self.attacked_this_turn:
            self.set_inactive()

    def move_toward(self, other) -> None:
        """
        Move self toward other.
        """
        distance = self.get_distance_between(other)
        if distance > self.attack_range:
            dx = int(self.mobility * (other.x - self.x) / distance)
            dy = int(self.mobility * (other.y - self.y) / distance)
            for x in range(self.x + dx * (dx > 0), self.x + dx * (dx < 0) - 1, -1):
                for y in range(self.y + dy * (dy > 0), self.y + dy * (dy < 0) - 1, -1):
                    if (x, y) not in Soldier.coordinates and -5 <= x <= 5 and -5 <= y <= 6:
                        self.move_to(x, y)
                        break

    def wobble(self) -> None:
        """
        Move self randomly.
        """
        if tiles := [
            (x, y)
            for x, y in itertools.product(
                range(self.x - 1, self.x + 2), range(self.y - 1, self.y + 2)
            )
            if (x, y) not in Soldier.coordinates and -5 <= x <= 5 and -5 <= y <= 5
        ]:
            self.move_to(*choice(tiles))

    def assault(self, other) -> None:
        """
        Make self attack other.
        """
        self.handle_click_event()

        match self.__class__.__name__[0], other.__class__.__name__[0]:
            case ("K", _) | ("B", "S") | ("H", "B") | ("S", "H"):
                multiplier = 2
            case _:
                multiplier = 1

        other.health -= max(self.attack * multiplier - other.defense, 0)
        self.experience += multiplier
        if other.health > 0:
            other.healthbar["value"] = other.health
        else:
            other.remove_canvas_window_object()
            self.experience += 1

        self.attacked_this_turn = True
        if self.moved_this_turn:
            self.set_inactive()

    def attack_surrounding(self) -> None:
        """
        If any rival instance lies within self's attack range, make self attack it.
        """
        match self.color:
            case Color.BLUE:
                others = Soldier.enemies
            case Color.RED:
                others = Soldier.allies

        for other in others:
            if self.get_distance_between(other) <= self.attack_range:
                self.assault(other)
                break

    def promote(self, experience: int = 0) -> None:
        """
        """
        self.experience += experience

        while self.experience >= self.PROMOTION_EXPERIENCE[self.level]:
            self.experience -= self.PROMOTION_EXPERIENCE[self.level]
            self.level += 1
            self.attack += 3
            self.defense += 2
            self.heal_itself(10)

        color = "gray" if self.moved_this_turn and self.attacked_this_turn else Color.MAPPING[self.color]
        name = f"{color}_{self.__class__.__name__.lower()}_{self.level}"
        self.config(image=getattr(Image, name))

    def heal_itself(self, amount: int) -> None:
        """
        Increase self's health point (cannot exceed the maximum value).
        """
        self.health = min(self.health + amount, self.__class__.health)
        self.healthbar["value"] = self.health

    def set_inactive(self) -> None:
        """
        Change widget's color into gray.
        """
        name = f"gray_{self.__class__.__name__.lower()}_{self.level}"
        self.config(
            image=getattr(Image, name),
            background=Color.GRAY,
            activebackground=Color.GRAY,
        )

    def set_active(self) -> None:
        """
        Reset widget's color.
        """
        name = f"{Color.MAPPING[self.color]}_{self.__class__.__name__.lower()}_{self.level}"
        self.config(
            image=getattr(Image, name),
            background=self.color,
            activebackground=self.color,
        )

    def handle_click_event(self) -> None:
        """
        Call '_handle_ally_click_event' or '_handle_enemy_click_event' based on self's color.
        """
        match self.color:
            case Color.BLUE:
                self._handle_ally_click_event()
            case Color.RED:
                self._handle_enemy_click_event()

    def _handle_ally_click_event(self) -> None:
        """
        Highlight or unhighlight all available movements of self as well as show
        or hide attack range indicator.
        If another ally instance is chosen, unselect it first.
        """
        if Soldier.chosen_ally:
            if Soldier.chosen_ally is self:
                Soldier.chosen_ally = None

                if AttackRange.instance:
                    AttackRange.instance.remove_canvas_window_object()

                for highlight in Movement.instances:
                    GameObject.remove_canvas_window_object(highlight)
                Movement.instances = []
            else:
                Soldier.chosen_ally.handle_click_event()
                self.handle_click_event()
        else:
            Soldier.chosen_ally = self

            if not self.attacked_this_turn:
                AttackRange(self._canvas, self.x, self.y, radius=self.attack_range)

            if not self.moved_this_turn:
                coordinates = itertools.product(
                    range(
                        max(self.x - self.mobility, -5),
                        min(self.x + self.mobility, 5) + 1,
                    ),
                    range(
                        max(self.y - self.mobility, -5),
                        min(self.y + self.mobility, 3) + 1,
                    ),
                )
                for coordinate in coordinates:
                    if (
                        coordinate not in Soldier.coordinates
                        and math.dist((self.x, self.y), coordinate) <= self.mobility
                    ):
                        Movement(self._canvas, *coordinate)

    def _handle_enemy_click_event(self) -> None:
        """
        Attack self with the chosen ally instance.
        """
        chosen_ally = Soldier.chosen_ally

        if (
            chosen_ally
            and not chosen_ally.attacked_this_turn
            and chosen_ally.get_distance_between(self) <= chosen_ally.attack_range
        ):
            chosen_ally.assault(self)
            chosen_ally.promote()


class King(Soldier):
    """
    Counter all soldiers.
    """

    defense = 20
    health = 150
    mobility = 3


class Bowman(Soldier):
    """
    Soldier with high attack range but low attak and low health.
    Counter swordsmen, countered by horsemen.
    """

    attack = 25
    attack_range = 3
    health = 50


class Horseman(Soldier):
    """
    Soldier with high mobility.
    Counter bowmen, countered by swordsmen.
    """

    mobility = 3


class Swordsman(Soldier):
    """
    Soldier with high defense.
    Counter horsemen, countered by bowmen.
    """

    defense = 20


class Movement(GameObject, tk.Button):
    """
    A class that instantiates movements.
    When a movement is clicked on, the chosen ally instance moves to its coordinate.
    """

    instances = []

    def _configure_widget(self) -> None:
        """
        Configure widget.
        """
        self.configure(
            image=Image.transparent_10x10,
            background="Royal Blue",
            activebackground="Royal Blue",
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            command=self.handle_click_event,
        )

    def _create_canvas_window_object(self) -> None:
        """
        Create canvas window object and append self to 'Movement.instances'.
        """
        super()._create_canvas_window_object()
        Movement.instances.append(self)

    def remove_canvas_window_object(self) -> None:
        """
        Remove canvas window object and remove self from 'Movement.instances'.
        """
        super().remove_canvas_window_object()
        Movement.instances.remove(self)

    def handle_click_event(self) -> None:
        """
        Move the chosen ally instance to the coordinate of the clicked movement.
        Unselect the ally instance then clear all highlights.
        """
        Soldier.chosen_ally.move_to(self.x, self.y)
        Soldier.chosen_ally.handle_click_event()


class AttackRange(GameObject):
    """
    A class that instantiates attack range indicators which indicate ally instances' attack range.
    Enemy instances can be attacked when they are covered by an attack range indicator.
    """

    instance = None

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, radius: int):
        """
        Create canvas window object.
        """
        self._radius = radius
        super().__init__(canvas, x, y)

    def _create_widget(self) -> None:
        """
        Override this method as there's no widget to create.
        """

    def _configure_widget(self) -> None:
        """
        Override this method as there's no widget to configure.
        """

    def _create_canvas_window_object(self) -> None:
        """
        Create canvas window object and set 'AttackRange.instance' to self.
        """
        self._main_widget_id = self._canvas.create_image(
            self.x * 60 + 390,
            -self.y * 60 + 395,
            image=getattr(Image, "red_circle_{0}x{0}".format(self._radius * 120)),
        )
        AttackRange.instance = self

    def remove_canvas_window_object(self) -> None:
        """
        Remove canvas window object and set 'AttackRange.instance' to None.
        """
        super().remove_canvas_window_object()
        AttackRange.instance = None
