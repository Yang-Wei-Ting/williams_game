import heapq
import math
import tkinter as tk
from tkinter import ttk

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

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, color: str, attach: bool = True) -> None:
        self.color = color

        match self.color:
            case C.BLUE:
                self._friends = SoldierState.allied_soldiers
                self._foes = SoldierState.enemy_soldiers
            case C.RED:
                self._friends = SoldierState.enemy_soldiers
                self._foes = SoldierState.allied_soldiers

        self.level = 1
        self.experience = 0
        self.attacked_this_turn = False
        self.moved_this_turn = False
        super().__init__(canvas, x, y, attach=attach)

    def _create_widgets(self) -> None:
        self._main_widget = ttk.Label(self._canvas)
        self.refresh_widgets()
        self.health_bar = ttk.Progressbar(
            self._canvas,
            length=C.HEALTH_BAR_LENGTH,
            maximum=self.health,
            mode="determinate",
            orient=tk.HORIZONTAL,
            style="Green_Red.Horizontal.TProgressbar",
            value=self.health,
        )

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
        is_exhausted = self.attacked_this_turn and self.moved_this_turn

        cursor = "arrow" if is_exhausted or self.color == C.RED else "hand2"
        color_name = C.COLOR_NAME_BY_HEX_TRIPLET[C.GRAY if is_exhausted else self.color]
        soldier_name = type(self).__name__.lower()

        self._main_widget.configure(
            cursor=cursor,
            image=getattr(Image, f"{color_name}_{soldier_name}_{self.level}"),
            style=f"Custom{color_name.capitalize()}.TButton",
        )

        if self.color == C.BLUE:
            if is_exhausted:
                self._main_widget.unbind("<ButtonPress-1>")
            else:
                self._main_widget.bind("<ButtonPress-1>", self._handle_ally_press_event)

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

    def _handle_ally_press_event(self, event: tk.Event) -> None:
        self._main_widget.bind("<Motion>", self._handle_ally_drag_event)
        self._canvas.bind_all("<ButtonRelease-1>", self._handle_ally_release_event)

        self._pressed_x = event.x
        self._pressed_y = event.y

        self._attack_target_by_id = {}
        if not self.attacked_this_turn:
            AttackRangeHighlight(self._canvas, self.x, self.y, half_diagonal=self.attack_range)

            covered_coordinates = set()
            for offset in range(self.attack_range + 1):
                for i in range(-offset, offset + 1):
                    j = offset - abs(i)
                    covered_coordinates.add((self.x + i, self.y + j))
                    if j != 0:
                        covered_coordinates.add((self.x + i, self.y - j))

            for soldier in self._foes:
                if (soldier.x, soldier.y) in covered_coordinates:
                    self._attack_target_by_id[soldier._main_widget_id] = soldier

        self._movement_target_by_id = {}
        if not self.moved_this_turn:
            frontier = set()
            frontier.add((self.x, self.y))
            cost_table = {(self.x, self.y): 0}

            while frontier:
                current = frontier.pop()

                if cost_table[current] == self.mobility:
                    continue

                for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
                    x, y = current[0] + dx, current[1] + dy
                    if (
                        0 < x < C.HORIZONTAL_LAND_TILE_COUNT - 1
                        and 0 < y < C.VERTICAL_TILE_COUNT - 1
                        and (x, y) not in GameState.occupied_coordinates
                        and (x, y) not in cost_table
                    ):
                        frontier.add((x, y))
                        cost_table[(x, y)] = cost_table[current] + 1

                        highlight = MovementHighlight(self._canvas, x, y)
                        self._movement_target_by_id[highlight._main_widget_id] = highlight

        self._main_widget.lift()
        self.health_bar.lift()
        if ControlState.display_outcome_control:
            ControlState.display_outcome_control._main_widget.lift()

        for obj in GameState.selected_game_objects[::-1]:
            obj.handle_click_event()

    def _handle_ally_drag_event(self, event: tk.Event) -> None:
        dx = event.x - self._pressed_x
        dy = event.y - self._pressed_y

        self._main_widget.place(
            x=self._main_widget.winfo_x() + dx,
            y=self._main_widget.winfo_y() + dy,
        )
        self.health_bar.place(
            x=self.health_bar.winfo_x() + dx,
            y=self.health_bar.winfo_y() + dy,
        )

    def _handle_ally_release_event(self, event: tk.Event) -> None:
        self._main_widget.unbind("<Motion>")
        self._canvas.unbind_all("<ButtonRelease-1>")

        x = self._main_widget.winfo_x()
        y = self._main_widget.winfo_y()
        overlapping_ids = set(self._canvas.find_overlapping(x, y, x + 40, y + 40))

        if target_ids := overlapping_ids & set(self._attack_target_by_id):
            assert len(target_ids) == 1
            target_id = target_ids.pop()
            soldier = self._attack_target_by_id[target_id]
            self.assault(soldier)
            self.promote()
        elif target_ids := overlapping_ids & set(self._movement_target_by_id):
            assert len(target_ids) == 1
            target_id = target_ids.pop()
            highlight = self._movement_target_by_id[target_id]
            self.move_to(highlight.x, highlight.y)

        self.detach_widgets_from_canvas()
        self.attach_widgets_to_canvas()

        if HighlightState.attack_range_highlight:
            HighlightState.attack_range_highlight.detach_and_destroy_widgets()

        for highlight in list(HighlightState.movement_highlights):
            highlight.detach_and_destroy_widgets()
