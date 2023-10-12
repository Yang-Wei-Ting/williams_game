import itertools
import math
import tkinter as tk
from abc import abstractmethod
from tkinter.ttk import Progressbar

from game.bases import GameObject
from game.miscs import Color, Image


class Soldier(GameObject):
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

    @property
    @abstractmethod
    def counters(self):
        raise NotImplementedError

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, color: str = Color.RED) -> None:
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
        mx = int(self.mobility * (other.x - self.x) / distance)
        my = int(self.mobility * (other.y - self.y) / distance)
        tiles = (
            (x, y)
            for x, y in itertools.product(
                range(self.x + mx * (mx > 0), self.x + mx * (mx < 0) - 1, -1),
                range(self.y + my * (my > 0), self.y + my * (my < 0) - 1, -1),
            )
            if (x, y) not in Soldier.coordinates and -5 <= x <= 5 and -5 <= y <= 6
        )
        if tile := next(tiles, None):
            self.move_to(*tile)

    def assault(self, other) -> None:
        """
        Make self attack other.
        """
        multiplier = 1 + (type(other) in self.counters)
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
                AttackRange(self._canvas, self.x, self.y, half_diagonal=self.attack_range)

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
                        and self.get_distance_between(coordinate) <= self.mobility
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
            chosen_ally.handle_click_event()
            chosen_ally.assault(self)
            chosen_ally.promote()


class King(Soldier):
    """
    Counter all soldiers.
    """

    defense = 20
    health = 150
    mobility = 3

    @property
    def counters(self):
        return {King, Bowman, Horseman, Swordsman}


class Bowman(Soldier):
    """
    Soldier with high attack range but low attack and low health.
    Counter swordsmen, countered by horsemen.
    """

    attack = 25
    attack_range = 3
    health = 50

    @property
    def counters(self):
        return {Swordsman}


class Horseman(Soldier):
    """
    Soldier with high mobility.
    Counter bowmen, countered by swordsmen.
    """

    mobility = 3

    @property
    def counters(self):
        return {Bowman}


class Swordsman(Soldier):
    """
    Soldier with high defense.
    Counter horsemen, countered by bowmen.
    """

    defense = 20

    @property
    def counters(self):
        return {Horseman}


class Movement(GameObject):
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
            image=Image.transparent_12x12,
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

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, half_diagonal: int) -> None:
        """
        Create canvas window object.
        """
        self._half_diagonal = half_diagonal
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
            image=getattr(Image, "red_diamond_{0}x{0}".format(self._half_diagonal * 120)),
        )
        AttackRange.instance = self

    def remove_canvas_window_object(self) -> None:
        """
        Remove canvas window object and set 'AttackRange.instance' to None.
        """
        super().remove_canvas_window_object()
        AttackRange.instance = None
