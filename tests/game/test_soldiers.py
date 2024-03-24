import tkinter as tk
from tkinter.ttk import Style
from unittest import TestCase, main, mock

from game.miscs import Configuration as C
from game.miscs import Image
from game.soldiers import Archer, Cavalry, Infantry, King, Soldier
from game.states import AttackRangeState, MovementState, SoldierState


class SoldierTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.window = tk.Tk()
        cls.canvas = tk.Canvas(
            cls.window,
            width=C.TILE_DIMENSION * C.HORIZONTAL_TILE_COUNT,
            height=C.TILE_DIMENSION * C.VERTICAL_TILE_COUNT,
        )
        cls.canvas.pack()
        Image.initialize()
        cls.style = Style()
        cls.style.theme_use("default")
        cls.style.configure(
            "TProgressbar",
            troughcolor="Red",
            background="Green",
            darkcolor="Green",
            lightcolor="Green",
            bordercolor="Red",
            thickness=5,
        )

    def tearDown(self):
        if SoldierState.chosen_ally:
            SoldierState.chosen_ally.handle_click_event()
        for ally in SoldierState.allies[:]:
            ally.destroy_widgets()
        for enemy in SoldierState.enemies[:]:
            enemy.destroy_widgets()

    @classmethod
    def tearDownClass(cls):
        cls.window.destroy()

    def process_events(self):
        while self.window.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
            pass


class SoldierClickTest(SoldierTest):

    def test_click_on_an_ally(self):
        ally = Infantry(self.canvas, 5, 6, color=C.BLUE)
        ally.handle_click_event()
        self.process_events()

        # The ally should be selected
        self.assertIs(SoldierState.chosen_ally, ally)
        # The ally's attack range should be displayed
        self.assertIsNotNone(AttackRangeState.instance)
        # The ally's available movements should be displayed
        self.assertNotEqual(MovementState.instances, [])
        # The ally should be active
        self.assertEqual(ally._main_widget["background"], C.BLUE)

    def test_click_on_an_ally_twice(self):
        ally = Infantry(self.canvas, 5, 6, color=C.BLUE)
        ally.handle_click_event()
        ally.handle_click_event()
        self.process_events()

        # The ally should not be selected
        self.assertIsNone(SoldierState.chosen_ally)
        # The ally's attack range should not be displayed
        self.assertIsNone(AttackRangeState.instance)
        # The ally's available movements should not be displayed
        self.assertEqual(MovementState.instances, [])
        # The ally should be active
        self.assertEqual(ally._main_widget["background"], C.BLUE)

    def test_click_on_an_ally_then_click_on_another_ally(self):
        ally1 = Infantry(self.canvas, 5, 6, color=C.BLUE)
        ally2 = Infantry(self.canvas, 5, 5, color=C.BLUE)
        ally1.handle_click_event()
        ally2.handle_click_event()
        self.process_events()

        # The second ally should be selected
        self.assertIs(SoldierState.chosen_ally, ally2)
        # Attack range should be displayed
        self.assertIsNotNone(AttackRangeState.instance)
        # Available movements should be displayed
        self.assertNotEqual(MovementState.instances, [])
        # Both allies should be active
        self.assertEqual(ally1._main_widget["background"], C.BLUE)
        self.assertEqual(ally2._main_widget["background"], C.BLUE)

    def test_click_on_an_enemy(self):
        ally = Infantry(self.canvas, 5, 6, color=C.BLUE)
        enemy = Infantry(self.canvas, 5, 5, color=C.RED)
        enemy.handle_click_event()
        self.process_events()

        # No ally should be selected
        self.assertIsNone(SoldierState.chosen_ally)
        # No attack range should be displayed
        self.assertIsNone(AttackRangeState.instance)
        # No available movements should be displayed
        self.assertEqual(MovementState.instances, [])
        # The enemy should be active
        self.assertEqual(enemy._main_widget["background"], C.RED)

    def test_click_on_an_ally_then_click_on_one_of_its_available_movements(self):
        ally = Infantry(self.canvas, 5, 6, color=C.BLUE)
        ally.handle_click_event()
        movement = MovementState.instances[0]
        movement.handle_click_event()
        self.process_events()

        # The coordinate of the clicked movement should become the ally's new coordinate
        self.assertEqual((ally.x, ally.y), (movement.x, movement.y))
        # The ally should be unselected
        self.assertIsNone(SoldierState.chosen_ally)
        # The ally's attack range should not be displayed
        self.assertIsNone(AttackRangeState.instance)
        # The ally's available movements should not be displayed
        self.assertEqual(MovementState.instances, [])
        # The ally should be active
        self.assertEqual(ally._main_widget["background"], C.BLUE)

    def test_click_on_an_ally_then_click_on_an_enemy_within_its_attack_range(self):
        ally = Infantry(self.canvas, 5, 6, color=C.BLUE)
        enemy = Infantry(self.canvas, 5, 5, color=C.RED)
        ally.handle_click_event()
        enemy.handle_click_event()
        self.process_events()

        # The ally should be unselected
        self.assertIsNone(SoldierState.chosen_ally)
        # The ally's attack range should not be displayed
        self.assertIsNone(AttackRangeState.instance)
        # The ally's available movements should not be displayed
        self.assertEqual(MovementState.instances, [])
        # The ally should be active
        self.assertEqual(ally._main_widget["background"], C.BLUE)

    def test_click_on_an_ally_then_click_on_an_enemy_outside_its_attack_range(self):
        ally = Infantry(self.canvas, 5, 6, color=C.BLUE)
        enemy = Infantry(self.canvas, 10, 1, color=C.RED)
        ally.handle_click_event()
        enemy.handle_click_event()
        self.process_events()

        # The ally should be selected
        self.assertIs(SoldierState.chosen_ally, ally)
        # The ally's attack range should be displayed
        self.assertIsNotNone(AttackRangeState.instance)
        # The ally's available movements should be displayed
        self.assertNotEqual(MovementState.instances, [])
        # The ally should be active
        self.assertEqual(ally._main_widget["background"], C.BLUE)
        # The enemy should not be attacked
        self.assertEqual(enemy.health, enemy.__class__.health)

    def test_move_an_ally_then_order_it_to_attack(self):
        ally = Infantry(self.canvas, 5, 6, color=C.BLUE)
        enemy = Infantry(self.canvas, 5, 4, color=C.RED)
        ally.handle_click_event()
        next(m for m in MovementState.instances if (m.x, m.y) == (5, 5)).handle_click_event()
        ally.handle_click_event()
        enemy.handle_click_event()
        self.process_events()

        # The ally should be unselected
        self.assertIsNone(SoldierState.chosen_ally)
        # The ally's attack range should not be displayed
        self.assertIsNone(AttackRangeState.instance)
        # The ally's available movements should not be displayed
        self.assertEqual(MovementState.instances, [])
        # The ally should be inactive
        self.assertEqual(ally._main_widget["background"], C.GRAY)

    def test_order_an_ally_to_attack_then_move_it(self):
        ally = Infantry(self.canvas, 5, 6, color=C.BLUE)
        enemy = Infantry(self.canvas, 5, 5, color=C.RED)
        ally.handle_click_event()
        enemy.handle_click_event()
        ally.handle_click_event()
        next(m for m in MovementState.instances if (m.x, m.y) == (5, 7)).handle_click_event()
        self.process_events()

        # The ally should be unselected
        self.assertIsNone(SoldierState.chosen_ally)
        # The ally's attack range should not be displayed
        self.assertIsNone(AttackRangeState.instance)
        # The ally's available movements should not be displayed
        self.assertEqual(MovementState.instances, [])
        # The ally should be inactive
        self.assertEqual(ally._main_widget["background"], C.GRAY)


class SoldierStatsTest(SoldierTest):

    def test_king_stats(self):
        ally = King(self.canvas, 5, 6, color=C.BLUE)
        enemy = King(self.canvas, 5, 5, color=C.RED)
        self.process_events()

        # Should have superior defense, health, and mobility
        self.assertTrue(ally.attack == enemy.attack == Soldier.attack)
        self.assertTrue(ally.attack_range == enemy.attack_range == Soldier.attack_range)
        self.assertTrue(ally.defense == enemy.defense > Soldier.defense)
        self.assertTrue(ally.health == enemy.health > Soldier.health)
        self.assertTrue(ally.mobility == enemy.mobility > Soldier.mobility)

    def test_archer_stats(self):
        ally = Archer(self.canvas, 5, 6, color=C.BLUE)
        enemy = Archer(self.canvas, 5, 5, color=C.RED)
        self.process_events()

        # Should have superior attack_range but inferior attack and health
        self.assertTrue(ally.attack == enemy.attack < Soldier.attack)
        self.assertTrue(ally.attack_range == enemy.attack_range > Soldier.attack_range)
        self.assertTrue(ally.defense == enemy.defense == Soldier.defense)
        self.assertTrue(ally.health == enemy.health < Soldier.health)
        self.assertTrue(ally.mobility == enemy.mobility == Soldier.mobility)

    def test_cavalry_stats(self):
        ally = Cavalry(self.canvas, 5, 6, color=C.BLUE)
        enemy = Cavalry(self.canvas, 5, 5, color=C.RED)
        self.process_events()

        # Should have superior mobility
        self.assertTrue(ally.attack == enemy.attack == Soldier.attack)
        self.assertTrue(ally.attack_range == enemy.attack_range == Soldier.attack_range)
        self.assertTrue(ally.defense == enemy.defense == Soldier.defense)
        self.assertTrue(ally.health == enemy.health == Soldier.health)
        self.assertTrue(ally.mobility == enemy.mobility > Soldier.mobility)

    def test_infantry_stats(self):
        ally = Infantry(self.canvas, 5, 6, color=C.BLUE)
        enemy = Infantry(self.canvas, 5, 5, color=C.RED)
        self.process_events()

        # Should have superior defense
        self.assertTrue(ally.attack == enemy.attack == Soldier.attack)
        self.assertTrue(ally.attack_range == enemy.attack_range == Soldier.attack_range)
        self.assertTrue(ally.defense == enemy.defense > Soldier.defense)
        self.assertTrue(ally.health == enemy.health == Soldier.health)
        self.assertTrue(ally.mobility == enemy.mobility == Soldier.mobility)


class SoldierCounterTest(SoldierTest):

    def test_king_counters(self):
        ally = King(self.canvas, 5, 6, color=C.BLUE)
        enemy = King(self.canvas, 5, 5, color=C.RED)
        self.process_events()

        self.assertTrue(ally.counters == enemy.counters == {King, Archer, Cavalry, Infantry})

    def test_archer_counters(self):
        ally = Archer(self.canvas, 5, 6, color=C.BLUE)
        enemy = Archer(self.canvas, 5, 5, color=C.RED)
        self.process_events()

        self.assertTrue(ally.counters == enemy.counters == {Infantry})

    def test_cavalry_counters(self):
        ally = Cavalry(self.canvas, 5, 6, color=C.BLUE)
        enemy = Cavalry(self.canvas, 5, 5, color=C.RED)
        self.process_events()

        self.assertTrue(ally.counters == enemy.counters == {Archer})

    def test_infantry_counters(self):
        ally = Infantry(self.canvas, 5, 6, color=C.BLUE)
        enemy = Infantry(self.canvas, 5, 5, color=C.RED)
        self.process_events()

        self.assertTrue(ally.counters == enemy.counters == {Cavalry})


class SoldierComputerPathfindingTest(SoldierTest):

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
            Infantry(self.canvas, *c, color=C.RED)
        enemy = Archer(self.canvas, 2, 9, color=C.RED)
        enemy.attack_range = 3
        enemy.mobility = 9
        ally = Infantry(self.canvas, 8, 3, color=C.BLUE)

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
            Infantry(self.canvas, *c, color=C.RED)
        enemy = Infantry(self.canvas, 2, 9, color=C.RED)
        enemy.attack_range = 1
        enemy.mobility = 9
        ally = Infantry(self.canvas, 8, 3, color=C.BLUE)

        coordinate = enemy._get_coordinate_after_moving_toward(ally)
        self.process_events()

        self.assertEqual(coordinate, (4, 2))


@mock.patch("game.soldiers.Soldier.promote")
@mock.patch("game.soldiers.Soldier.assault")
@mock.patch("game.soldiers.Soldier.move_to")
class SoldierComputerTargetSelectionTest(SoldierTest):

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
            Infantry(self.canvas, *c, color=C.RED)
        enemy = Archer(self.canvas, 2, 9, color=C.RED)
        enemy.attack = 25
        enemy.attack_range = 3
        enemy.mobility = 2
        killable_ally = Infantry(self.canvas, 4, 6, color=C.BLUE)
        killable_ally.defense = 20
        killable_ally.health = 30
        hittable_ally = Infantry(self.canvas, 5, 7, color=C.BLUE)
        hittable_ally.defense = 20
        hittable_ally.health = 70
        untouchable_ally = Infantry(self.canvas, 5, 6, color=C.BLUE)

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
        enemy = Archer(self.canvas, 2, 9, color=C.RED)
        enemy.attack = 25
        enemy.attack_range = 3
        enemy.mobility = 2
        hittable_ally = Infantry(self.canvas, 2, 4, color=C.BLUE)
        hittable_ally.defense = 20
        hittable_ally.health = 70
        untouchable_ally = Infantry(self.canvas, 8, 9, color=C.BLUE)

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
        enemy = Archer(self.canvas, 2, 9, color=C.RED)
        enemy.attack = 25
        enemy.attack_range = 3
        enemy.mobility = 2
        ally_with_higher_health = Infantry(self.canvas, 2, 4, color=C.BLUE)
        ally_with_higher_health.defense = 20
        ally_with_higher_health.health = 30
        ally_with_lower_health = Infantry(self.canvas, 6, 9, color=C.BLUE)
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
        enemy = Archer(self.canvas, 2, 9, color=C.RED)
        enemy.attack = 25
        enemy.attack_range = 3
        enemy.mobility = 2
        closer_ally = Infantry(self.canvas, 2, 5, color=C.BLUE)
        closer_ally.defense = 20
        closer_ally.health = 30
        farther_ally = Infantry(self.canvas, 7, 9, color=C.BLUE)
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
