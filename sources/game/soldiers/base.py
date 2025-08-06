import heapq
import tkinter as tk
from tkinter import ttk
from typing import Optional

from game.base import GameObject, GameObjectModel, GameObjectView
from game.highlights import AttackRangeHighlight, AttackRangeHighlightModel, AttackRangeHighlightView, MovementHighlight, MovementHighlightModel, MovementHighlightView
from game.miscellaneous import Configuration as C
from game.miscellaneous import Environment as E
from game.miscellaneous import Image, get_pixels, msleep
from game.states import BuildingState, ControlState, DisplayState, GameState, HighlightState, SoldierState


class SoldierModel(GameObjectModel):

    _attack = 30.0
    _attack_multipliers = {}
    _attack_range = 1

    _defense = 0.15
    _health = 100.0

    _mobility = 2

    _cost = 10

    def __init__(self, x: int, y: int, color: str, level: int = 1) -> None:
        kwargs = {
            "_color": color,
            "_level": level,
            "_experience": 0,
            "_moved_this_turn": False,
            "_attacked_this_turn": False,
        }
        super().__init__(x, y, **kwargs)

    # GET
    def get_data(self) -> dict:
        data = {
            **super().get_data(),
            "color": self._color,
            "level": self._level,
            "experience": self._experience,
            "attack": self._attack,
            "attack_multipliers": self._attack_multipliers,
            "attack_range": self._attack_range,
            "defense": self._defense,
            "health": self._health,
            "mobility": self._mobility,
            "cost": self._cost,
            "moved_this_turn": self._moved_this_turn,
            "attacked_this_turn": self._attacked_this_turn,
        }
        return data

    ################################################
    def is_alive(self) -> bool:
        return self._health > 0.0

    def get_approaching_path(self, other: "SoldierModel | BuildingModel") -> tuple:
        """
        Use the A* pathfinding algorithm to compute the shortest path for self
        to move toward other until other is within self's attack range.
        Trim the path so that it ends at the furthest coordinate self can reach
        this turn and return it.
        """
        start = (self.x, self.y)

        frontier = []
        heapq.heappush(frontier, (0, start))
        cost_table = {start: 0}
        parent_table = {start: None}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if other.get_distance_to(current) <= self._attack_range:
                path = []
                while current:
                    path.append(current)
                    current = parent_table[current]
                path.reverse()
                return tuple(path[:self._mobility + 1])

            new_cost = cost_table[current] + 1
            for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
                x, y = current[0] + dx, current[1] + dy
                if (
                    0 <= x < C.HORIZONTAL_LAND_TILE_COUNT
                    and 0 <= y < C.VERTICAL_TILE_COUNT
                    and (x, y) not in GameObjectModel.occupied_coordinates
                    and ((x, y) not in cost_table or new_cost < cost_table[(x, y)])
                ):
                    heapq.heappush(frontier, (new_cost + other.get_distance_to((x, y)), (x, y)))
                    cost_table[(x, y)] = new_cost
                    parent_table[(x, y)] = current

        # TODO: When other is surrounded by obstacles, self should try to approach it.
        return (start,)

    #### other type hint
    def get_damage_output_against(self, other) -> float:
        multiplier = self._attack_multipliers.get(type(other).__name__, 1.0)
        return self._attack * multiplier * (1.0 - other._defense)

    # SET
    def move_to(self, x: int, y: int) -> None:
        super().move_to(x, y)
        self._moved_this_turn = True

    def restore_health_by(self, amount: float) -> None:
        """
        Restore self's health by amount (cannot exceed the maximum value).
        """
        self._health = min(self._health + amount, type(self)._health)

    def _learn(self, experience: int = 1) -> None:
        self._experience += experience

        LEVEL_UP_EXPERIENCE_BY_LEVEL = {1: 4, 2: 8, 3: 16, 4: 32, 5: 65535}
        while self._experience >= LEVEL_UP_EXPERIENCE_BY_LEVEL[self._level]:
            self._experience -= LEVEL_UP_EXPERIENCE_BY_LEVEL[self._level]
            self._level += 1
            self._attack *= 1.2
            self._defense += 0.05

    ### other type hint
    def assault(self, other) -> None:
        """
        Make self attack other.
        """
        other._health -= self.get_damage_output_against(other)
        self._learn()
        self._attacked_this_turn = True


class SoldierView(GameObjectView):

    def _create_widgets(self, data: dict) -> None:
        self._widgets["main"] = ttk.Label(self._canvas)
        self.refresh_main_appearance()
        self._widgets["health_bar"] = ttk.Progressbar(
            self._canvas,
            length=C.HEALTH_BAR_LENGTH,
            maximum=data["health"],
            mode="determinate",
            orient=tk.HORIZONTAL,
            style="Green_Red.Horizontal.TProgressbar",
            value=data["health"],
        )

    def attach_widgets(self, data: dict) -> None:
        self._ids["main"] = self._canvas.create_window(
            *get_pixels(data["x"], data["y"], y_pixel_shift=5.0),
            window=self._widgets["main"],
        )
        self._ids["health_bar"] = self._canvas.create_window(
            *get_pixels(data["x"], data["y"], y_pixel_shift=-22.5),
            window=self._widgets["health_bar"],
        )

    def refresh_main_appearance(self, data: dict) -> None:
        if data["color"] == C.BLUE and data["moved_this_turn"] and data["attacked_this_turn"]:
            cursor = "arrow"
            hex_triplet = C.GRAY
        else:
            cursor = "hand2"
            hex_triplet = data["color"]

        color_name = C.COLOR_NAME_BY_HEX_TRIPLET[hex_triplet]
        soldier_name = type(self).__name__.removesuffix("View").lower()

        self._widgets["main"].configure(
            cursor=cursor,
            image=getattr(Image, f"{color_name}_{soldier_name}_{data["level"]}"),
            style=f"Custom{color_name.capitalize()}.TButton",
        )

    def refresh_health_bar_appearance(self, data: dict) -> None:
        self._widgets["health_bar"]["value"] = data["health"]

    def refresh_position(self, data: dict) -> None:
        self._canvas.coords(
            self._ids["main"],
            *get_pixels(data["x"], data["y"], y_pixel_shift=5.0),
        )
        self._canvas.coords(
            self._ids["health_bar"],
            *get_pixels(data["x"], data["y"], y_pixel_shift=-22.5),
        )

    def bind_or_unbind_event_handlers(self, data: dict) -> None:
        if data["color"] == C.BLUE:
            if data["moved_this_turn"] and data["attacked_this_turn"]:
                self._widgets["main"].unbind("<ButtonPress-1>")
            else:
                self._widgets["main"].bind("<ButtonPress-1>", self._controller._handle_ally_press_event)
        else:
            self._widgets["main"].bind("<ButtonPress-1>", self._controller._handle_enemy_press_event)


class Soldier(GameObject):

    def _register(self) -> None:
        data = self.get_data_from_model()

        match data["color"]:
            case C.BLUE:
                self._friends = SoldierState.allied_soldiers
                self._foes = SoldierState.enemy_soldiers
            case C.RED:
                self._friends = SoldierState.enemy_soldiers
                self._foes = SoldierState.allied_soldiers

        self._friends.add(self)

    def _unregister(self) -> None:
        self._friends.remove(self)

    def move_to(self, x: int, y: int) -> None:
        self._model.move_to(x, y)
        data = self.get_data_from_model()
        self._view.refresh_position(data)
        self._view.refresh_main_appearance(data)
        self._view.bind_or_unbind_event_handlers(data)

    ### other type hint
    def assault(self, other) -> None:
        self._model.assault(other._model)
        data = self.get_data_from_model()
        self._view.refresh_main_appearance(data)
        self._view.bind_or_unbind_event_handlers(data)

        if other._model.is_alive():
            other._view.refresh_health_bar_appearance()
        else:
            other.destroy()

    def restore_health_by(self, amount: float) -> None:
        self._model.restore_health_by(amount)
        self._view.refresh_health_bar_appearance()

    def hunt(self) -> None:
        """
        Identify the optimal rival soldier then move toward and potentially attack it.
        """
        MOVE_THEN_KILL = 1
        MOVE_THEN_HIT = 2
        MOVE = 3

        heap = []
        for i, other in enumerate(self._foes | BuildingState.critical_buildings):
            path = self._model.get_approaching_path(other._model)
            distance = other._model.get_distance_to(path[-1])
            damage = self._model.get_damage_output_against(other._model)

            self_data = self.get_data_from_model()
            other_data = other.get_data_from_model()

            if distance > self_data["attack_range"]:
                action = MOVE
                order_by = [distance, -damage, other_data["health"]]
            elif damage < other_data["health"]:
                action = MOVE_THEN_HIT
                order_by = [-damage, other_data["health"], distance]
            else:
                action = MOVE_THEN_KILL
                order_by = [-damage, distance]

            heapq.heappush(heap, (action, *order_by, i, path, other))

        action, *_, path, other = heapq.heappop(heap)

        self.move_to(*path[-1])
        if action in {MOVE_THEN_HIT, MOVE_THEN_KILL}:
            self.assault(other)

        # Display trails
        highlights = []
        for coordinate in path[:-1]:
            model = MovementHighlightModel(*coordinate)
            view = MovementHighlightView(model=model, canvas=self._view._canvas)
            controller = MovementHighlight(model=model, view=view)
            highlights.append(controller)

        msleep(self._view._canvas.master, 200)

        for highlight in highlights:
            highlight.destroy()

        msleep(self._view._canvas.master, 200)

    def _handle_ally_press_event(self, event: tk.Event) -> None:
        self._view._widgets["main"].grab_set()
        self._view._widgets["main"].bind("<Motion>", self._handle_ally_drag_event)
        self._view._widgets["main"].bind("<ButtonRelease-1>", self._handle_ally_release_event)

        self._pressed_x = event.x
        self._pressed_y = event.y

        # On X11, clean up highlights in case the mouse button was released outside the window.
        if E.WINDOWING_SYSTEM == "x11":
            if HighlightState.attack_range_highlight:
                HighlightState.attack_range_highlight.destroy()

            for highlight in list(HighlightState.movement_highlights):
                highlight.destroy()

            GameState.pressed_game_object = None
            if DisplayState.stat_display:
                DisplayState.stat_display._view.refresh_main_appearance()

        data = self.get_data_from_model()

        self._attack_target_by_id = {}
        if not data["attacked_this_turn"]:
            model = AttackRangeHighlightModel(
                x=data["x"],
                y=data["y"],
                half_diagonal=data["attack_range"],
            )
            view = AttackRangeHighlightView(model=model, canvas=self._view._canvas)
            AttackRangeHighlight(model=model, view=view)

            covered_coordinates = set()
            for offset in range(data["attack_range"] + 1):
                for i in range(-offset, offset + 1):
                    j = offset - abs(i)
                    covered_coordinates.add((data["x"] + i, data["y"] + j))
                    if j != 0:
                        covered_coordinates.add((data["x"] + i, data["y"] - j))

            for soldier in self._foes:
                if (soldier._model.x, soldier._model.y) in covered_coordinates:
                    self._attack_target_by_id[soldier.view._ids["main"]] = soldier

        self._movement_target_by_id = {}
        if not data["moved_this_turn"]:
            frontier = set()
            frontier.add((data["x"], data["y"]))
            cost_table = {(data["x"], data["y"]): 0}

            while frontier:
                current = frontier.pop()

                if cost_table[current] == data["mobility"]:
                    continue

                for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
                    x, y = current[0] + dx, current[1] + dy
                    if (
                        0 < x < C.HORIZONTAL_LAND_TILE_COUNT - 1
                        and 0 < y < C.VERTICAL_TILE_COUNT - 1
                        and (x, y) not in GameObjectModel.occupied_coordinates
                        and (x, y) not in cost_table
                    ):
                        frontier.add((x, y))
                        cost_table[(x, y)] = cost_table[current] + 1

                        model = MovementHighlightModel(x=x, y=y)
                        view = MovementHighlightView(model=model, canvas=self._view._canvas)
                        controller = MovementHighlight(model=model, view=view)
                        self._movement_target_by_id[controller._view._ids["main"]] = controller

        self._view._widgets["main"].lift()
        self._view._widgets["health_bar"].lift()
        if ControlState.display_outcome_control:
            ControlState.display_outcome_control._view._widgets["main"].lift()

        GameState.pressed_game_object = self
        if DisplayState.stat_display:
            DisplayState.stat_display._view.refresh_main_appearance()

        for obj in GameState.selected_game_objects[::-1]:
            obj.handle_click_event()

    def _handle_ally_drag_event(self, event: tk.Event) -> None:
        dx = event.x - self._pressed_x
        dy = event.y - self._pressed_y

        self._view._widgets["main"].place(
            x=self._view._widgets["main"].winfo_x() + dx,
            y=self._view._widgets["main"].winfo_y() + dy,
        )
        self._view._widgets["health_bar"].place(
            x=self._view._widgets["health_bar"].winfo_x() + dx,
            y=self._view._widgets["health_bar"].winfo_y() + dy,
        )

    def _handle_ally_release_event(self, event: tk.Event) -> None:
        self._view._widgets["main"].grab_release()
        self._view._widgets["main"].unbind("<Motion>")
        self._view._widgets["main"].unbind("<ButtonRelease-1>")

        x = self._view._widgets["main"].winfo_x()
        y = self._view._widgets["main"].winfo_y()
        overlapping_ids = set(self._view._canvas.find_overlapping(x, y, x + 40, y + 40))

        if target_ids := overlapping_ids & set(self._attack_target_by_id):
            if len(target_ids) == 1:
                target_id = target_ids.pop()
                soldier = self._attack_target_by_id[target_id]
                self.assault(soldier)
                self.promote()
        elif target_ids := overlapping_ids & set(self._movement_target_by_id):
            if len(target_ids) == 1:
                target_id = target_ids.pop()
                highlight = self._movement_target_by_id[target_id]
                self.move_to(highlight._model.x, highlight._model.y)

        self._view.detach_widgets()
        self._view.attach_widgets()

        if HighlightState.attack_range_highlight:
            HighlightState.attack_range_highlight.destroy()

        for highlight in list(HighlightState.movement_highlights):
            highlight.destroy()

        GameState.pressed_game_object = None
        if DisplayState.stat_display:
            DisplayState.stat_display._view.refresh_main_appearance()

    def _handle_enemy_press_event(self, event: tk.Event) -> None:
        self._view._widgets["main"].grab_set()
        self._view._widgets["main"].bind("<ButtonRelease-1>", self._handle_enemy_release_event)

        attack_range_highlight_model = AttackRangeHighlightModel(
            x=self._model.x,
            y=self._model.y,
            half_diagonal=self._model.attack_range,
        )
        attack_range_highlight_view = AttackRangeHighlightView(
            model=attack_range_highlight_model,
            canvas=self._view._canvas,
            attach=True,
        )

        frontier = set()
        frontier.add((self._model.x, self._model.y))
        cost_table = {(self._model.x, self._model.y): 0}

        while frontier:
            current = frontier.pop()

            if cost_table[current] == self._model.mobility:
                continue

            for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
                x, y = current[0] + dx, current[1] + dy
                if (
                    0 <= x < C.HORIZONTAL_LAND_TILE_COUNT
                    and 0 <= y < C.VERTICAL_TILE_COUNT
                    and (x, y) not in GameState.occupied_coordinates
                    and (x, y) not in cost_table
                ):
                    frontier.add((x, y))
                    cost_table[(x, y)] = cost_table[current] + 1

                    movement_highlight_model = MovementHighlightModel(x=x, y=y)
                    movement_highlight_view = MovementHighlightView(canvas=self._view._canvas, attach=True)
                    MovementHighlight(model=movement_highlight_model, view=movement_highlight_view)

        self._view._widgets["main"].lift()
        self._view._widgets["health_bar"].lift()
        if ControlState.display_outcome_control:
            ControlState.display_outcome_control._view._widgets["main"].lift()

        GameState.pressed_game_object = self
        if DisplayState.stat_display:
            DisplayState.stat_display._view.refresh_main_appearance()

        for obj in GameState.selected_game_objects[::-1]:
            obj.handle_click_event()

    def _handle_enemy_release_event(self, event: tk.Event) -> None:
        self._view._widgets["main"].grab_release()
        self._view._widgets["main"].unbind("<ButtonRelease-1>")

        if HighlightState.attack_range_highlight:
            HighlightState.attack_range_highlight.destroy()

        for highlight in list(HighlightState.movement_highlights):
            highlight.destroy()

        GameState.pressed_game_object = None
        if DisplayState.stat_display:
            DisplayState.stat_display._view.refresh_main_appearance()
