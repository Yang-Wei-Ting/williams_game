import tkinter as tk
from tkinter.ttk import Progressbar
from unittest import main, mock

from game.miscs import Configuration as C
from game.miscs import Image, get_pixels
from game.soldiers import Archer, Cavalry, Infantry, King, Soldier
from game.states import GameState, HighlightState, SoldierState
from game.test_bases import BaseTest


class SoldierStatsTest(BaseTest):

    def test_king_stats(self):
        ally = King(self.program._canvas, 5, 6, color=C.BLUE)
        enemy = King(self.program._canvas, 5, 5, color=C.RED)
        self.process_events()

        # Should have superior defense, health, and mobility
        self.assertTrue(ally.attack == enemy.attack == Soldier.attack)
        self.assertTrue(ally.attack_range == enemy.attack_range == Soldier.attack_range)
        self.assertTrue(ally.defense == enemy.defense > Soldier.defense)
        self.assertTrue(ally.health == enemy.health > Soldier.health)
        self.assertTrue(ally.mobility == enemy.mobility > Soldier.mobility)

    def test_archer_stats(self):
        ally = Archer(self.program._canvas, 5, 6, color=C.BLUE)
        enemy = Archer(self.program._canvas, 5, 5, color=C.RED)
        self.process_events()

        # Should have superior attack_range but inferior attack and health
        self.assertTrue(ally.attack == enemy.attack < Soldier.attack)
        self.assertTrue(ally.attack_range == enemy.attack_range > Soldier.attack_range)
        self.assertTrue(ally.defense == enemy.defense == Soldier.defense)
        self.assertTrue(ally.health == enemy.health < Soldier.health)
        self.assertTrue(ally.mobility == enemy.mobility == Soldier.mobility)

    def test_cavalry_stats(self):
        ally = Cavalry(self.program._canvas, 5, 6, color=C.BLUE)
        enemy = Cavalry(self.program._canvas, 5, 5, color=C.RED)
        self.process_events()

        # Should have superior mobility
        self.assertTrue(ally.attack == enemy.attack == Soldier.attack)
        self.assertTrue(ally.attack_range == enemy.attack_range == Soldier.attack_range)
        self.assertTrue(ally.defense == enemy.defense == Soldier.defense)
        self.assertTrue(ally.health == enemy.health == Soldier.health)
        self.assertTrue(ally.mobility == enemy.mobility > Soldier.mobility)

    def test_infantry_stats(self):
        ally = Infantry(self.program._canvas, 5, 6, color=C.BLUE)
        enemy = Infantry(self.program._canvas, 5, 5, color=C.RED)
        self.process_events()

        # Should have superior defense
        self.assertTrue(ally.attack == enemy.attack == Soldier.attack)
        self.assertTrue(ally.attack_range == enemy.attack_range == Soldier.attack_range)
        self.assertTrue(ally.defense == enemy.defense > Soldier.defense)
        self.assertTrue(ally.health == enemy.health == Soldier.health)
        self.assertTrue(ally.mobility == enemy.mobility == Soldier.mobility)


class SoldierCountersTest(BaseTest):

    def test_king_counters(self):
        ally = King(self.program._canvas, 5, 6, color=C.BLUE)
        enemy = King(self.program._canvas, 5, 5, color=C.RED)
        self.process_events()

        self.assertTrue(ally.counters == enemy.counters == {King, Archer, Cavalry, Infantry})

    def test_archer_counters(self):
        ally = Archer(self.program._canvas, 5, 6, color=C.BLUE)
        enemy = Archer(self.program._canvas, 5, 5, color=C.RED)
        self.process_events()

        self.assertTrue(ally.counters == enemy.counters == {Infantry})

    def test_cavalry_counters(self):
        ally = Cavalry(self.program._canvas, 5, 6, color=C.BLUE)
        enemy = Cavalry(self.program._canvas, 5, 5, color=C.RED)
        self.process_events()

        self.assertTrue(ally.counters == enemy.counters == {Archer})

    def test_infantry_counters(self):
        ally = Infantry(self.program._canvas, 5, 6, color=C.BLUE)
        enemy = Infantry(self.program._canvas, 5, 5, color=C.RED)
        self.process_events()

        self.assertTrue(ally.counters == enemy.counters == {Cavalry})


class SoldierCreationTest(BaseTest):

    def setUp(self):
        super().setUp()
        self.real_create_window = self.program._canvas.create_window
        self.mock_create_window = mock.Mock()
        self.program._canvas.create_window = self.mock_create_window

    def tearDown(self):
        super().tearDown()
        self.program._canvas.create_window = self.real_create_window

    def test_ally_creation_with_attachment(self):
        ally_coordinate = (5, 6)
        ally = Infantry(self.program._canvas, *ally_coordinate, color=C.BLUE)
        self.process_events()

        self.assertEqual(ally.color, C.BLUE)
        self.assertEqual(ally.level, 1)
        self.assertEqual(ally.experience, 0)
        self.assertFalse(ally.attacked_this_turn)
        self.assertFalse(ally.moved_this_turn)
        self.assertIs(ally._canvas, self.program._canvas)
        self.assertEqual((ally.x, ally.y), ally_coordinate)

        self.assertIsInstance(ally._main_widget, tk.Button)
        self.assertIs(ally._main_widget.master, ally._canvas)
        self.assertEqual(ally._main_widget["activebackground"], C.BLUE)
        self.assertEqual(ally._main_widget["background"], C.BLUE)
        self.assertEqual(ally._main_widget["borderwidth"], 5)
        self.assertIn("handle_click_event", ally._main_widget["command"])
        self.assertEqual(ally._main_widget["cursor"], "hand2")
        self.assertEqual(ally._main_widget["highlightthickness"], 0)
        self.assertEqual(ally._main_widget["image"], str(Image.blue_infantry_1))
        self.assertEqual(ally._main_widget["padx"], 0)
        self.assertEqual(ally._main_widget["pady"], 0)
        self.assertEqual(ally._main_widget["relief"], tk.RAISED)
        self.assertEqual(ally._main_widget["state"], tk.NORMAL)

        self.assertIsInstance(ally.healthbar, Progressbar)
        self.assertIs(ally.healthbar.master, ally._canvas)
        self.assertEqual(ally.healthbar["length"], C.HEALTH_BAR_LENGTH)
        self.assertEqual(ally.healthbar["maximum"], ally.health)
        self.assertEqual(ally.healthbar["mode"].string, "determinate")
        self.assertEqual(ally.healthbar["orient"].string, tk.HORIZONTAL)
        self.assertEqual(ally.healthbar["style"], "TProgressbar")
        self.assertEqual(ally.healthbar["value"], ally.health)

        self.assertEqual(GameState.occupied_coordinates, {ally_coordinate})
        self.assertEqual(SoldierState.allied_soldiers, {ally})
        self.assertEqual(SoldierState.enemy_soldiers, set())

        self.assertEqual(self.mock_create_window.call_count, 2)
        self.mock_create_window.assert_any_call(
            *get_pixels(ally.x, ally.y, y_pixel_shift=5.0),
            window=ally._main_widget,
        )
        self.mock_create_window.assert_any_call(
            *get_pixels(ally.x, ally.y, y_pixel_shift=-22.5),
            window=ally.healthbar,
        )

    def test_ally_creation_without_attachment(self):
        ally_coordinate = (5, 6)
        Infantry(self.program._canvas, *ally_coordinate, attach=False, color=C.BLUE)
        self.process_events()

        self.mock_create_window.assert_not_called()

    def test_enemy_creation_with_attachment(self):
        enemy_coordinate = (5, 6)
        enemy = Infantry(self.program._canvas, *enemy_coordinate, color=C.RED)
        self.process_events()

        self.assertEqual(enemy.color, C.RED)
        self.assertEqual(enemy.level, 1)
        self.assertEqual(enemy.experience, 0)
        self.assertFalse(enemy.attacked_this_turn)
        self.assertFalse(enemy.moved_this_turn)
        self.assertIs(enemy._canvas, self.program._canvas)
        self.assertEqual((enemy.x, enemy.y), enemy_coordinate)

        self.assertIsInstance(enemy._main_widget, tk.Button)
        self.assertIs(enemy._main_widget.master, enemy._canvas)
        self.assertEqual(enemy._main_widget["activebackground"], C.RED)
        self.assertEqual(enemy._main_widget["background"], C.RED)
        self.assertEqual(enemy._main_widget["borderwidth"], 5)
        self.assertIn("handle_click_event", enemy._main_widget["command"])
        self.assertEqual(enemy._main_widget["cursor"], "hand2")
        self.assertEqual(enemy._main_widget["highlightthickness"], 0)
        self.assertEqual(enemy._main_widget["image"], str(Image.red_infantry_1))
        self.assertEqual(enemy._main_widget["padx"], 0)
        self.assertEqual(enemy._main_widget["pady"], 0)
        self.assertEqual(enemy._main_widget["relief"], tk.RAISED)
        self.assertEqual(enemy._main_widget["state"], tk.NORMAL)

        self.assertIsInstance(enemy.healthbar, Progressbar)
        self.assertIs(enemy.healthbar.master, enemy._canvas)
        self.assertEqual(enemy.healthbar["length"], C.HEALTH_BAR_LENGTH)
        self.assertEqual(enemy.healthbar["maximum"], enemy.health)
        self.assertEqual(enemy.healthbar["mode"].string, "determinate")
        self.assertEqual(enemy.healthbar["orient"].string, tk.HORIZONTAL)
        self.assertEqual(enemy.healthbar["style"], "TProgressbar")
        self.assertEqual(enemy.healthbar["value"], enemy.health)

        self.assertEqual(GameState.occupied_coordinates, {enemy_coordinate})
        self.assertEqual(SoldierState.allied_soldiers, set())
        self.assertEqual(SoldierState.enemy_soldiers, {enemy})

        self.assertEqual(self.mock_create_window.call_count, 2)
        self.mock_create_window.assert_any_call(
            *get_pixels(enemy.x, enemy.y, y_pixel_shift=5.0),
            window=enemy._main_widget,
        )
        self.mock_create_window.assert_any_call(
            *get_pixels(enemy.x, enemy.y, y_pixel_shift=-22.5),
            window=enemy.healthbar,
        )

    def test_enemy_creation_without_attachment(self):
        enemy_coordinate = (5, 6)
        Infantry(self.program._canvas, *enemy_coordinate, attach=False, color=C.RED)
        self.process_events()

        self.mock_create_window.assert_not_called()


class SoldierClickTest(BaseTest):

    def test_click_on_an_ally(self):
        ally_coordinate = (5, 6)
        ally = Infantry(self.program._canvas, *ally_coordinate, color=C.BLUE)
        ally.handle_click_event()
        self.process_events()

        self.assertEqual(ally._main_widget["background"], C.BLUE)
        self.assertEqual(GameState.selected_game_objects, [ally])
        self.assertEqual(GameState.occupied_coordinates, {ally_coordinate})
        self.assertEqual(SoldierState.allied_soldiers, {ally})
        self.assertEqual(SoldierState.enemy_soldiers, set())
        self.assertIsNotNone(HighlightState.attack_range)
        self.assertEqual(
            (HighlightState.attack_range.x, HighlightState.attack_range.y),
            ally_coordinate,
        )
        self.assertNotEqual(HighlightState.movements, set())

    def test_click_on_an_ally_twice(self):
        ally_coordinate = (5, 6)
        ally = Infantry(self.program._canvas, *ally_coordinate, color=C.BLUE)
        ally.handle_click_event()
        ally.handle_click_event()
        self.process_events()

        self.assertEqual(ally._main_widget["background"], C.BLUE)
        self.assertEqual(GameState.selected_game_objects, [])
        self.assertEqual(GameState.occupied_coordinates, {ally_coordinate})
        self.assertEqual(SoldierState.allied_soldiers, {ally})
        self.assertEqual(SoldierState.enemy_soldiers, set())
        self.assertIsNone(HighlightState.attack_range)
        self.assertEqual(HighlightState.movements, set())

    def test_click_on_an_ally_then_click_on_another_ally(self):
        ally1_coordinate = (5, 6)
        ally2_coordinate = (5, 5)
        ally1 = Infantry(self.program._canvas, *ally1_coordinate, color=C.BLUE)
        ally2 = Infantry(self.program._canvas, *ally2_coordinate, color=C.BLUE)
        ally1.handle_click_event()
        ally2.handle_click_event()
        self.process_events()

        self.assertEqual(ally1._main_widget["background"], C.BLUE)
        self.assertEqual(ally2._main_widget["background"], C.BLUE)
        self.assertEqual(GameState.selected_game_objects, [ally2])
        self.assertEqual(GameState.occupied_coordinates, {ally1_coordinate, ally2_coordinate})
        self.assertEqual(SoldierState.allied_soldiers, {ally1, ally2})
        self.assertEqual(SoldierState.enemy_soldiers, set())
        self.assertIsNotNone(HighlightState.attack_range)
        self.assertEqual(
            (HighlightState.attack_range.x, HighlightState.attack_range.y),
            ally2_coordinate,
        )
        self.assertNotEqual(HighlightState.movements, set())

    def test_click_on_an_enemy(self):
        enemy_coordinate = (5, 6)
        enemy = Infantry(self.program._canvas, *enemy_coordinate, color=C.RED)
        enemy.handle_click_event()
        self.process_events()

        self.assertEqual(enemy._main_widget["background"], C.RED)
        self.assertEqual(GameState.selected_game_objects, [])
        self.assertEqual(GameState.occupied_coordinates, {enemy_coordinate})
        self.assertEqual(SoldierState.allied_soldiers, set())
        self.assertEqual(SoldierState.enemy_soldiers, {enemy})
        self.assertIsNone(HighlightState.attack_range)
        self.assertEqual(HighlightState.movements, set())

    def test_click_on_an_ally_then_click_on_one_of_its_available_movements(self):
        ally_coordinate = (5, 6)
        ally = Infantry(self.program._canvas, *ally_coordinate, color=C.BLUE)
        ally.handle_click_event()
        movement = HighlightState.movements.pop()
        movement.handle_click_event()
        self.process_events()

        self.assertEqual(ally._main_widget["background"], C.BLUE)
        self.assertEqual((ally.x, ally.y), (movement.x, movement.y))
        self.assertEqual(GameState.selected_game_objects, [])
        self.assertEqual(GameState.occupied_coordinates, {(movement.x, movement.y)})
        self.assertEqual(SoldierState.allied_soldiers, {ally})
        self.assertEqual(SoldierState.enemy_soldiers, set())
        self.assertIsNone(HighlightState.attack_range)
        self.assertEqual(HighlightState.movements, set())

    def test_click_on_an_ally_then_click_on_an_enemy_within_its_attack_range(self):
        ally_coordinate = (5, 6)
        enemy_coordinate = (5, 5)
        ally = Infantry(self.program._canvas, *ally_coordinate, color=C.BLUE)
        enemy = Infantry(self.program._canvas, *enemy_coordinate, color=C.RED)
        ally.handle_click_event()
        enemy.handle_click_event()
        self.process_events()

        self.assertEqual(ally._main_widget["background"], C.BLUE)
        self.assertEqual(GameState.selected_game_objects, [])
        self.assertIsNone(HighlightState.attack_range)
        self.assertEqual(HighlightState.movements, set())

    def test_click_on_an_ally_then_click_on_an_enemy_outside_its_attack_range(self):
        ally = Infantry(self.program._canvas, 5, 6, color=C.BLUE)
        enemy = Infantry(self.program._canvas, 10, 1, color=C.RED)
        ally.handle_click_event()
        enemy.handle_click_event()
        self.process_events()

        # The ally should be selected
        self.assertEqual(len(GameState.selected_game_objects), 1)
        self.assertIs(GameState.selected_game_objects[0], ally)
        # The ally's attack range should be displayed
        self.assertIsNotNone(HighlightState.attack_range)
        # The ally's available movements should be displayed
        self.assertNotEqual(HighlightState.movements, set())
        # The ally should be active
        self.assertEqual(ally._main_widget["background"], C.BLUE)
        # The enemy should not be attacked
        self.assertEqual(enemy.health, type(enemy).health)

    def test_move_an_ally_then_order_it_to_attack(self):
        ally = Infantry(self.program._canvas, 5, 6, color=C.BLUE)
        enemy = Infantry(self.program._canvas, 5, 4, color=C.RED)
        ally.handle_click_event()
        next(m for m in HighlightState.movements if (m.x, m.y) == (5, 5)).handle_click_event()
        ally.handle_click_event()
        enemy.handle_click_event()
        self.process_events()

        # The ally should be unselected
        self.assertEqual(GameState.selected_game_objects, [])
        # The ally's attack range should not be displayed
        self.assertIsNone(HighlightState.attack_range)
        # The ally's available movements should not be displayed
        self.assertEqual(HighlightState.movements, set())
        # The ally should be inactive
        self.assertEqual(ally._main_widget["background"], C.GRAY)

    def test_order_an_ally_to_attack_then_move_it(self):
        ally = Infantry(self.program._canvas, 5, 6, color=C.BLUE)
        enemy = Infantry(self.program._canvas, 5, 5, color=C.RED)
        ally.handle_click_event()
        enemy.handle_click_event()
        ally.handle_click_event()
        next(m for m in HighlightState.movements if (m.x, m.y) == (5, 7)).handle_click_event()
        self.process_events()

        # The ally should be unselected
        self.assertEqual(GameState.selected_game_objects, [])
        # The ally's attack range should not be displayed
        self.assertIsNone(HighlightState.attack_range)
        # The ally's available movements should not be displayed
        self.assertEqual(HighlightState.movements, set())
        # The ally should be inactive
        self.assertEqual(ally._main_widget["background"], C.GRAY)


class SoldierComputerPathfindingTest(BaseTest):

    def test_pathfinding_for_enemy_with_attack_range_greater_than_one(self):
        """
        • · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · e e · A · ·
        · · · · · · · e · · ·
        · · · · · · · e · · ·
        · · · · · · · · e · ·
        · · · · · · · · e · ·
        · · · · · · · · e · ·
        · · E · · · · e · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        """
        for c in {(5, 3), (6, 3), (7, 4), (7, 5), (8, 6), (8, 7), (8, 8), (7, 9)}:
            Infantry(self.program._canvas, *c, color=C.RED)
        enemy = Archer(self.program._canvas, 2, 9, color=C.RED)
        enemy.attack_range = 3
        enemy.mobility = 9
        ally = Infantry(self.program._canvas, 8, 3, color=C.BLUE)

        coordinate = enemy._get_coordinate_after_moving_toward(ally)
        self.process_events()

        self.assertEqual(coordinate, (6, 4))

    def test_pathfinding_for_enemy_with_attack_range_equal_to_one(self):
        """
        • · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · e e · A · ·
        · · · · · · · e · · ·
        · · · · · · · e · · ·
        · · · · · · · · e · ·
        · · · · · · · · e · ·
        · · · · · · · · e · ·
        · · E · · · · e · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        """
        for c in {(5, 3), (6, 3), (7, 4), (7, 5), (8, 6), (8, 7), (8, 8), (7, 9)}:
            Infantry(self.program._canvas, *c, color=C.RED)
        enemy = Infantry(self.program._canvas, 2, 9, color=C.RED)
        enemy.attack_range = 1
        enemy.mobility = 9
        ally = Infantry(self.program._canvas, 8, 3, color=C.BLUE)

        coordinate = enemy._get_coordinate_after_moving_toward(ally)
        self.process_events()

        self.assertEqual(coordinate, (4, 2))


@mock.patch("game.soldiers.Soldier.promote")
@mock.patch("game.soldiers.Soldier.assault")
@mock.patch("game.soldiers.Soldier.move_to")
class SoldierComputerTargetSelectionTest(BaseTest):

    def test_killable_target_should_be_preferred_over_hittable_or_untouchable_targets(
        self, mock_move_to, mock_assault, mock_promote,
    ):
        """
        • · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · A A · · · · ·
        · · · · · A · · · · ·
        · · · e · · · · · · ·
        · · E e · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        """
        for c in {(3, 8), (3, 9)}:
            Infantry(self.program._canvas, *c, color=C.RED)
        enemy = Archer(self.program._canvas, 2, 9, color=C.RED)
        enemy.attack = 25
        enemy.attack_range = 3
        enemy.mobility = 2
        killable_ally = Infantry(self.program._canvas, 4, 6, color=C.BLUE)
        killable_ally.defense = 20
        killable_ally.health = 30
        hittable_ally = Infantry(self.program._canvas, 5, 7, color=C.BLUE)
        hittable_ally.defense = 20
        hittable_ally.health = 70
        untouchable_ally = Infantry(self.program._canvas, 5, 6, color=C.BLUE)

        enemy.hunt()
        self.process_events()

        self.assertEqual(mock_move_to.call_args, mock.call(2, 7))
        self.assertEqual(mock_assault.call_args, mock.call(killable_ally))
        mock_promote.assert_called_once()

    def test_hittable_target_should_be_preferred_over_untouchable_target(
        self, mock_move_to, mock_assault, mock_promote,
    ):
        """
        • · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · A · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · E · · · · · A · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        """
        enemy = Archer(self.program._canvas, 2, 9, color=C.RED)
        enemy.attack = 25
        enemy.attack_range = 3
        enemy.mobility = 2
        hittable_ally = Infantry(self.program._canvas, 2, 4, color=C.BLUE)
        hittable_ally.defense = 20
        hittable_ally.health = 70
        untouchable_ally = Infantry(self.program._canvas, 8, 9, color=C.BLUE)

        enemy.hunt()
        self.process_events()

        self.assertEqual(mock_move_to.call_args, mock.call(2, 7))
        self.assertEqual(mock_assault.call_args, mock.call(hittable_ally))
        mock_promote.assert_called_once()

    def test_when_multiple_targets_are_killable_then_the_one_with_the_highiest_health_should_be_preferred(
        self, mock_move_to, mock_assault, mock_promote,
    ):
        """
        • · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · A · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · E · · · A · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        """
        enemy = Archer(self.program._canvas, 2, 9, color=C.RED)
        enemy.attack = 25
        enemy.attack_range = 3
        enemy.mobility = 2
        ally_with_higher_health = Infantry(self.program._canvas, 2, 4, color=C.BLUE)
        ally_with_higher_health.defense = 20
        ally_with_higher_health.health = 30
        ally_with_lower_health = Infantry(self.program._canvas, 6, 9, color=C.BLUE)
        ally_with_lower_health.defense = 20
        ally_with_lower_health.health = 10

        enemy.hunt()
        self.process_events()

        self.assertEqual(mock_move_to.call_args, mock.call(2, 7))
        self.assertEqual(mock_assault.call_args, mock.call(ally_with_higher_health))
        mock_promote.assert_called_once()

    def test_when_multiple_targets_are_killable_and_have_the_same_health_then_the_closer_one_should_be_preferred(
        self, mock_move_to, mock_assault, mock_promote,
    ):
        """
        • · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · A · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · E · · · · A · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        """
        enemy = Archer(self.program._canvas, 2, 9, color=C.RED)
        enemy.attack = 25
        enemy.attack_range = 3
        enemy.mobility = 2
        closer_ally = Infantry(self.program._canvas, 2, 5, color=C.BLUE)
        closer_ally.defense = 20
        closer_ally.health = 30
        farther_ally = Infantry(self.program._canvas, 7, 9, color=C.BLUE)
        farther_ally.defense = 20
        farther_ally.health = 30

        enemy.hunt()
        self.process_events()

        self.assertEqual(mock_move_to.call_args, mock.call(2, 8))
        self.assertEqual(mock_assault.call_args, mock.call(closer_ally))
        mock_promote.assert_called_once()

    def test_when_multiple_targets_are_hittable_then_the_one_that_can_be_dealt_the_highest_damage_should_be_preferred(
        self, mock_move_to, mock_assault, mock_promote,
    ):
        pass

    def test_when_multiple_targets_are_hittable_and_can_be_dealt_the_same_ammount_of_damage_then_the_one_with_the_least_amount_of_health_should_be_preferred(
        self, mock_move_to, mock_assault, mock_promote,
    ):
        pass

    def test_when_multiple_targets_are_hittable_and_can_be_dealt_the_same_ammount_of_damage_and_have_the_same_amount_of_health_then_the_closer_one_should_be_preferred(
        self, mock_move_to, mock_assault, mock_promote,
    ):
        pass

    def test_when_multiple_targets_are_untouchable_then_the_closer_one_should_be_preferred(
        self, mock_move_to, mock_assault, mock_promote,
    ):
        pass

    def test_when_multiple_targets_are_untouchable_and_are_equally_far_away_then_the_one_that_can_be_dealt_the_highest_damage_should_be_preferred(
        self, mock_move_to, mock_assault, mock_promote,
    ):
        pass

    def test_when_multiple_targets_are_untouchable_and_are_equally_far_away_and_can_be_dealt_the_same_ammount_of_damage_then_the_one_with_the_least_amount_of_health_should_be_preferred(
        self, mock_move_to, mock_assault, mock_promote,
    ):
        pass


if __name__ == "__main__":
    main()
