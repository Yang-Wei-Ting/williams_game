import heapq
import math
import tkinter as tk
from abc import abstractmethod
from queue import Queue
from tkinter.ttk import Progressbar

from game.bases import GameObject
from game.highlights import AttackRange, Movement
from game.miscs import Configuration as C
from game.miscs import Image, get_pixels
from game.states import AttackRangeState, GameState, MovementState, SoldierState


class Soldier(GameObject):
    """
    An abstract base class for all soldier game objects.
    """

    attack = 30
    attack_range = 1
    defense = 15
    health = 70
    mobility = 2

    @property
    @abstractmethod
    def counters(self):
        raise NotImplementedError

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, color: str = C.RED) -> None:
        """
        Create widgets then attach them to canvas.
        """
        self.color = color
        self.level = 1
        self.experience = 0
        self.moved_this_turn = False
        self.attacked_this_turn = False
        super().__init__(canvas, x, y)

    def _create_widgets(self) -> None:
        """
        Create widgets.
        """
        super()._create_widgets()
        self.healthbar = Progressbar(
            self._canvas,
            length=self.health / 2,
            maximum=self.health,
            mode="determinate",
            orient=tk.HORIZONTAL,
            style="TProgressbar",
            value=self.health,
        )

    def _configure_widgets(self) -> None:
        """
        Configure widgets.
        """
        self.configure_main_widget(
            relief=tk.RAISED,
            borderwidth=5,
            highlightthickness=0,
            cursor="hand2",
            command=self.handle_click_event,
        )
        self.refresh_image()

    def _attach_widgets_to_canvas(self) -> None:
        """
        Attach widgets to canvas.
        Add self to 'SoldierState.allies' or 'SoldierState.enemies'.
        Add self's coordinate to 'GameState.occupied_coordinates'.
        """
        self._main_widget_id = self._canvas.create_window(
            *get_pixels(self.x, self.y, y_pixel_shift=5.0),
            window=self._main_widget,
        )
        self._healthbar_id = self._canvas.create_window(
            *get_pixels(self.x, self.y, y_pixel_shift=-22.5),
            window=self.healthbar,
        )

        self._get_friends().append(self)
        GameState.occupied_coordinates.add((self.x, self.y))

    def detach_widgets(self) -> None:
        """
        Remove widgets from canvas.
        Remove self from 'SoldierState.allies' or 'SoldierState.enemies'.
        Remove self's coordinate from 'GameState.occupied_coordinates'.
        """
        GameState.occupied_coordinates.remove((self.x, self.y))
        self._get_friends().remove(self)

        self._canvas.delete(self._healthbar_id)
        del self._healthbar_id
        del self.healthbar
        super().detach_widgets()

    def move_to(self, x: int, y: int) -> None:
        """
        Move self to the new coordinate and update canvas window object's coordinate.
        Update 'GameState.occupied_coordinates' to reflect self's coordinate change.
        """
        GameState.occupied_coordinates.remove((self.x, self.y))
        self.x = x
        self.y = y
        self._canvas.coords(self._main_widget_id, *get_pixels(self.x, self.y, y_pixel_shift=5.0))
        self._canvas.coords(self._healthbar_id, *get_pixels(self.x, self.y, y_pixel_shift=-22.5))
        GameState.occupied_coordinates.add((self.x, self.y))

        self.moved_this_turn = True
        self.refresh_image()

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
            other.detach_widgets()
            self.experience += 1

        self.attacked_this_turn = True
        self.refresh_image()

    def promote(self, experience: int = 0) -> None:
        """
        """
        self.experience += experience

        LEVEL_UP_EXPERIENCE_BY_LEVEL = {1: 4, 2: 8, 3: 16, 4: 32, 5: math.inf}
        while self.experience >= LEVEL_UP_EXPERIENCE_BY_LEVEL[self.level]:
            self.experience -= LEVEL_UP_EXPERIENCE_BY_LEVEL[self.level]
            self.level += 1
            self.attack += 3
            self.defense += 2
            self.heal_itself(10)

        self.refresh_image()

    def _get_coordinate_after_moving_toward(self, other) -> tuple:
        """
        Use the A* pathfinding algorithm to compute the shortest path for self
        to move toward other until other is within self's attack range.
        Deduce the new coordinate that self can reach this turn by following
        the aforementioned shortest path.
        """
        start = (self.x, self.y)

        frontier = []
        heapq.heappush(frontier, (0, start))
        cost_table = {start: 0}
        parent_table = {start: None}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if other.get_distance_between(current) <= self.attack_range:
                path = []
                while current != start:
                    path.append(current)
                    current = parent_table[current]
                path.append(start)
                return path[max(-len(path), -self.mobility - 1)]

            new_cost = cost_table[current] + 1
            for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
                x, y = current[0] + dx, current[1] + dy
                if (
                    0 <= x <= 10 and
                    0 <= y <= 11 and
                    (x, y) not in GameState.occupied_coordinates and
                    ((x, y) not in cost_table or new_cost < cost_table[(x, y)])
                ):
                    heapq.heappush(frontier, (new_cost + other.get_distance_between((x, y)), (x, y)))
                    cost_table[(x, y)] = new_cost
                    parent_table[(x, y)] = current

        # TODO: When other is surrounded by obstacles, self should try to approach it.
        return start

    def hunt(self) -> None:
        """
        Identify the optimal rival instance then move toward and potentially attack it.
        """
        MOVE_THEN_KILL = 1
        MOVE_THEN_HIT = 2
        MOVE = 3

        heap = []
        for i, other in enumerate(self._get_foes()):
            coordinate = self._get_coordinate_after_moving_toward(other)
            distance = other.get_distance_between(coordinate)
            damage = min(self.attack * (1 + (type(other) in self.counters)) - other.defense, other.health)

            if distance > self.attack_range:
                action = MOVE
                order_by = [distance, -damage, other.health]
            elif damage < other.health:
                action = MOVE_THEN_HIT
                order_by = [-damage, other.health, distance]
            else:
                action = MOVE_THEN_KILL
                order_by = [-damage, distance]

            heapq.heappush(heap, (action, *order_by, i, coordinate, other))

        action, *_, coordinate, other = heapq.heappop(heap)

        self.move_to(*coordinate)
        if action in {MOVE_THEN_HIT, MOVE_THEN_KILL}:
            self.assault(other)
            self.promote()

    def heal_itself(self, amount: int) -> None:
        """
        Increase self's health point (cannot exceed the maximum value).
        """
        self.health = min(self.health + amount, self.__class__.health)
        self.healthbar["value"] = self.health

    def refresh_image(self) -> None:
        """
        Update image, background, and activebackground values based on self.moved_this_turn,
        self.attacked_this_turn, self.color, type of self, and self.level.
        """
        if self.moved_this_turn and self.attacked_this_turn:
            color = C.GRAY
        else:
            color = self.color

        color_name = C.COLOR_NAME_BY_HEX_TRIPLET[color]
        soldier_type = type(self).__name__.lower()

        self.configure_main_widget(
            image=getattr(Image, f"{color_name}_{soldier_type}_{self.level}"),
            background=color,
            activebackground=color,
        )

    def _get_friends(self) -> list:
        """
        Retrieve friendly Soldier instances based on self.color.
        """
        FRIENDS_BY_COLOR = {
            C.BLUE: SoldierState.allies,
            C.RED: SoldierState.enemies,
        }
        return FRIENDS_BY_COLOR[self.color]

    def _get_foes(self) -> list:
        """
        Retrieve hostile Soldier instances based on self.color.
        """
        FOES_BY_COLOR = {
            C.BLUE: SoldierState.enemies,
            C.RED: SoldierState.allies,
        }
        return FOES_BY_COLOR[self.color]

    def handle_click_event(self) -> None:
        """
        Call '_handle_ally_click_event' or '_handle_enemy_click_event' based on self's color.
        """
        EVENT_HANDLER_BY_COLOR = {
            C.BLUE: self._handle_ally_click_event,
            C.RED: self._handle_enemy_click_event,
        }
        EVENT_HANDLER_BY_COLOR[self.color]()

    def _handle_ally_click_event(self) -> None:
        """
        Highlight or unhighlight all available movements of self as well as show
        or hide attack range indicator.
        If another ally instance is chosen, unselect it first.
        """
        if SoldierState.chosen_ally:
            if SoldierState.chosen_ally is self:
                SoldierState.chosen_ally = None

                if AttackRangeState.instance:
                    AttackRangeState.instance.detach_widgets()

                for highlight in MovementState.instances:
                    GameObject.detach_widgets(highlight)
                MovementState.instances = []
            else:
                SoldierState.chosen_ally.handle_click_event()
                self.handle_click_event()
        else:
            SoldierState.chosen_ally = self

            if not self.attacked_this_turn:
                AttackRange(self._canvas, self.x, self.y, half_diagonal=self.attack_range)

            if not self.moved_this_turn:
                frontier = Queue()
                frontier.put((self.x, self.y))
                cost_table = {(self.x, self.y): 0}

                while not frontier.empty():
                    current = frontier.get()

                    new_cost = cost_table[current] + 1
                    for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
                        x, y = current[0] + dx, current[1] + dy
                        if (
                            0 <= x <= 10 and
                            3 <= y <= 11 and
                            (x, y) not in GameState.occupied_coordinates and
                            (x, y) not in cost_table and
                            new_cost <= self.mobility
                        ):
                            frontier.put((x, y))
                            Movement(self._canvas, x, y)
                            cost_table[(x, y)] = new_cost

    def _handle_enemy_click_event(self) -> None:
        """
        Attack self with the chosen ally instance.
        """
        chosen_ally = SoldierState.chosen_ally

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
        return {King, Archer, Cavalry, Infantry}


class Archer(Soldier):
    """
    Soldier with high attack range but low attack and low health.
    Counter infantries, countered by cavalries.
    """

    attack = 25
    attack_range = 3
    health = 50

    @property
    def counters(self):
        return {Infantry}


class Cavalry(Soldier):
    """
    Soldier with high mobility.
    Counter archers, countered by infantries.
    """

    mobility = 3

    @property
    def counters(self):
        return {Archer}


class Infantry(Soldier):
    """
    Soldier with high defense.
    Counter cavalries, countered by archers.
    """

    defense = 20

    @property
    def counters(self):
        return {Cavalry}
