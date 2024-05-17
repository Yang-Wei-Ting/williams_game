import heapq
import math
import tkinter as tk
from abc import abstractmethod
from tkinter.ttk import Progressbar

from game.base import GameObject
from game.highlights import AttackRangeHighlight, MovementHighlight
from game.miscellaneous import Configuration as C
from game.miscellaneous import Image, get_pixels
from game.states import BuildingState, ControlState, GameState, HighlightState, SoldierState


class Soldier(GameObject):

    attack = 30
    attack_multipliers = {}
    attack_range = 1

    defense = 0.15
    health = 100

    mobility = 2

    cost = 10

    @property
    def _health_bar_configuration(self) -> dict:
        return {
            "length": C.HEALTH_BAR_LENGTH,
            "maximum": self.health,
            "mode": "determinate",
            "orient": tk.HORIZONTAL,
            "style": "TProgressbar",
            "value": self.health,
        }

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, color: str, attach: bool = True) -> None:
        self.color = color

        match self.color:
            case C.BLUE:
                self._friends = SoldierState.allied_soldiers
                self._foes = SoldierState.enemy_soldiers
                self.handle_click_event = self._handle_ally_click_event
            case C.RED:
                self._friends = SoldierState.enemy_soldiers
                self._foes = SoldierState.allied_soldiers
                self.handle_click_event = self._handle_enemy_click_event

        self.level = 1
        self.experience = 0
        self.attacked_this_turn = False
        self.moved_this_turn = False
        super().__init__(canvas, x, y, attach=attach)

    def _create_widgets(self) -> None:
        super()._create_widgets()
        self.refresh_widgets()
        self.health_bar = Progressbar(self._canvas, **self._health_bar_configuration)

    def _destroy_widgets(self) -> None:
        self.health_bar.destroy()
        del self.health_bar
        super()._destroy_widgets()

    def _register(self) -> None:
        GameState.occupied_coordinates.add((self.x, self.y))
        self._friends.add(self)

    def _unregister(self) -> None:
        GameState.occupied_coordinates.remove((self.x, self.y))
        self._friends.remove(self)

    def attach_widgets_to_canvas(self) -> None:
        self._main_widget_id = self._canvas.create_window(
            *get_pixels(self.x, self.y, y_pixel_shift=5.0),
            window=self._main_widget,
        )
        self._health_bar_id = self._canvas.create_window(
            *get_pixels(self.x, self.y, y_pixel_shift=-22.5),
            window=self.health_bar,
        )

    def detach_widgets_from_canvas(self) -> None:
        self._canvas.delete(self._health_bar_id)
        del self._health_bar_id
        super().detach_widgets_from_canvas()

    def refresh_widgets(self) -> None:
        if self.attacked_this_turn and self.moved_this_turn:
            color = C.GRAY
        else:
            color = self.color

        color_name = C.COLOR_NAME_BY_HEX_TRIPLET[color]
        soldier_name = type(self).__name__.lower()

        self._main_widget.configure(
            activebackground=color,
            background=color,
            command=((lambda: None) if color == C.GRAY else self.handle_click_event),
            cursor="hand2",
            image=getattr(Image, f"{color_name}_{soldier_name}_{self.level}"),
            state=tk.NORMAL,
        )

    def move_to(self, x: int, y: int) -> None:
        """
        Move self to the new coordinate.
        """
        GameState.occupied_coordinates.remove((self.x, self.y))
        self.x = x
        self.y = y
        self._canvas.coords(self._main_widget_id, *get_pixels(self.x, self.y, y_pixel_shift=5.0))
        self._canvas.coords(self._health_bar_id, *get_pixels(self.x, self.y, y_pixel_shift=-22.5))
        GameState.occupied_coordinates.add((self.x, self.y))

        self.moved_this_turn = True
        self.refresh_widgets()

    def assault(self, other) -> None:
        """
        Make self attack other.
        """
        other.health -= self._get_damage_output_against(other)
        if other.health > 0:
            other.health_bar["value"] = other.health
        else:
            other.detach_and_destroy_widgets()
        self.experience += 1

        self.attacked_this_turn = True
        self.refresh_widgets()

    def promote(self) -> None:
        LEVEL_UP_EXPERIENCE_BY_LEVEL = {1: 4, 2: 8, 3: 16, 4: 32, 5: math.inf}
        while self.experience >= LEVEL_UP_EXPERIENCE_BY_LEVEL[self.level]:
            self.experience -= LEVEL_UP_EXPERIENCE_BY_LEVEL[self.level]
            self.level += 1
            self.attack *= 1.2
            self.defense += 0.05

        self.refresh_widgets()

    def restore_health_by(self, amount: int) -> None:
        """
        Restore self's health by amount (cannot exceed the maximum value).
        """
        self.health = min(self.health + amount, type(self).health)
        self.health_bar["value"] = self.health

    def hunt(self) -> None:
        """
        Identify the optimal rival soldier then move toward and potentially attack it.
        """
        MOVE_THEN_KILL = 1
        MOVE_THEN_HIT = 2
        MOVE = 3

        heap = []
        for i, other in enumerate(self._foes | BuildingState.critical_buildings):
            coordinate = self._get_coordinate_after_moving_toward(other)
            distance = other.get_distance_between(coordinate)
            damage = self._get_damage_output_against(other)

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
                while current:
                    path.append(current)
                    current = parent_table[current]
                return path[max(-len(path), -self.mobility - 1)]

            new_cost = cost_table[current] + 1
            for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
                x, y = current[0] + dx, current[1] + dy
                if (
                    0 <= x < C.HORIZONTAL_LAND_TILE_COUNT
                    and 0 <= y < C.VERTICAL_TILE_COUNT
                    and (x, y) not in GameState.occupied_coordinates
                    and ((x, y) not in cost_table or new_cost < cost_table[(x, y)])
                ):
                    heapq.heappush(frontier, (new_cost + other.get_distance_between((x, y)), (x, y)))
                    cost_table[(x, y)] = new_cost
                    parent_table[(x, y)] = current

        # TODO: When other is surrounded by obstacles, self should try to approach it.
        return start

    def _get_damage_output_against(self, other) -> float:
        return self.attack * self.attack_multipliers.get(type(other).__name__, 1.0) * (1.0 - other.defense)

    def _handle_ally_click_event(self) -> None:
        match GameState.selected_game_objects:
            case []:
                self._handle_ally_selection()
                GameState.selected_game_objects.append(self)
            case [obj] if obj is self:
                GameState.selected_game_objects.pop()
                self._handle_ally_deselection()
            case _:
                for obj in GameState.selected_game_objects[::-1]:
                    obj.handle_click_event()
                self.handle_click_event()

    def _handle_enemy_click_event(self) -> None:
        match GameState.selected_game_objects:
            case [Soldier() as soldier]:
                if (
                    not soldier.attacked_this_turn
                    and soldier.get_distance_between(self) <= soldier.attack_range
                ):
                    soldier.assault(self)
                    soldier.promote()
                    soldier.handle_click_event()

    def _handle_ally_selection(self) -> None:
        if not self.attacked_this_turn:
            AttackRangeHighlight(self._canvas, self.x, self.y, half_diagonal=self.attack_range)

        if not self.moved_this_turn:
            frontier = set()
            frontier.add((self.x, self.y))
            cost_table = {(self.x, self.y): 0}

            while frontier:
                current = frontier.pop()

                new_cost = cost_table[current] + 1
                for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
                    x, y = current[0] + dx, current[1] + dy
                    if (
                        0 < x < C.HORIZONTAL_LAND_TILE_COUNT - 1
                        and 0 < y < C.VERTICAL_TILE_COUNT - 1
                        and (x, y) not in GameState.occupied_coordinates
                        and (x, y) not in cost_table
                        and new_cost <= self.mobility
                    ):
                        frontier.add((x, y))
                        cost_table[(x, y)] = new_cost
                        MovementHighlight(self._canvas, x, y)

            if ControlState.display_outcome_control:
                ControlState.display_outcome_control._main_widget.lift()

    def _handle_ally_deselection(self) -> None:
        if HighlightState.attack_range_highlight:
            HighlightState.attack_range_highlight.detach_and_destroy_widgets()

        for highlight in list(HighlightState.movement_highlights):
            highlight.detach_and_destroy_widgets()
