import tkinter as tk
from tkinter.ttk import Progressbar, Style
from unittest import TestCase, main

from game.cores import AttackRange, Bowman, Horseman, King, Movement, Soldier, Swordsman
from game.miscs import Color, Image


class SoldierTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.window = tk.Tk()
        cls.canvas = tk.Canvas(cls.window, width=780, height=780)
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
        Soldier.allies = []
        Soldier.enemies = []
        Soldier.coordinates = set()
        Soldier.chosen_ally = None

        AttackRange.instance = None
        Movement.instances = []

    @classmethod
    def tearDownClass(cls):
        cls.window.destroy()

    def process_events(self):
        while self.window.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
            pass

    """
    def test_unit_creation__blue_king(self):
        ally = King(self.canvas, 0, 0, color=Color.BLUE)
        self.process_events()

        self.assertEqual(ally.color, Color.BLUE)
        self.assertFalse(ally.moved_this_turn)
        self.assertFalse(ally.attacked_this_turn)
        self.assertIs(ally._canvas, self.canvas)
        self.assertEqual(ally.x, 0)
        self.assertEqual(ally.y, 0)
        self.assertIsInstance(ally, tk.Button)
        self.assertIs(ally.master, self.canvas)
        # ally["image"]
        self.assertEqual(ally["background"], Color.BLUE)
        self.assertEqual(ally["activebackground"], Color.BLUE)
        self.assertEqual(ally["relief"], tk.RAISED)
        self.assertEqual(ally["borderwidth"], 5)
        self.assertEqual(ally["highlightthickness"], 0)
        self.assertEqual(ally["cursor"], "hand2")
        self.assertIsInstance(ally.healthbar, Progressbar)
        self.assertIs(ally.healthbar.master, self.canvas)
        self.assertEqual(ally.healthbar["length"], 75)
        self.assertEqual(ally.healthbar["maximum"], 150)
        self.assertEqual(str(ally.healthbar["mode"]), "determinate")
        self.assertEqual(str(ally.healthbar["orient"]), tk.HORIZONTAL)
        self.assertEqual(ally.healthbar["style"], "TProgressbar")
        self.assertEqual(ally.healthbar["value"], 150)
        # ally._healthbar_id
        self.assertEqual(ally.attack, 30)
        self.assertEqual(ally.attack_range, 1)
        self.assertEqual(ally.defense, 20)
        self.assertEqual(ally.health, 150)
        self.assertEqual(ally.mobility, 3)
        self.assertEqual(ally.level, 1)
        self.assertEqual(ally.experience, 0)
        self.assertEqual(Soldier.allies, [ally])
        self.assertEqual(Soldier.enemies, [])
        self.assertEqual(Soldier.coordinates, {(0, 0)})
        self.assertIsNone(Soldier.chosen_ally)
    """


class SoldierClickTest(SoldierTest):

    def test_click_on_an_ally(self):
        ally = Swordsman(self.canvas, 0, 0, color=Color.BLUE)
        ally.handle_click_event()
        self.process_events()

        # The ally should be selected
        self.assertIs(Soldier.chosen_ally, ally)
        # The ally's attack range should be displayed
        self.assertIsNotNone(AttackRange.instance)
        # The ally's available movements should be displayed
        self.assertNotEqual(Movement.instances, [])
        # The ally should be active
        self.assertEqual(ally["background"], Color.BLUE)

    def test_click_on_an_ally_twice(self):
        ally = Swordsman(self.canvas, 0, 0, color=Color.BLUE)
        ally.handle_click_event()
        ally.handle_click_event()
        self.process_events()

        # The ally should not be selected
        self.assertIsNone(Soldier.chosen_ally)
        # The ally's attack range should not be displayed
        self.assertIsNone(AttackRange.instance)
        # The ally's available movements should not be displayed
        self.assertEqual(Movement.instances, [])
        # The ally should be active
        self.assertEqual(ally["background"], Color.BLUE)

    def test_click_on_an_ally_then_click_on_another_ally(self):
        ally1 = Swordsman(self.canvas, 0, 0, color=Color.BLUE)
        ally2 = Swordsman(self.canvas, 0, 1, color=Color.BLUE)
        ally1.handle_click_event()
        ally2.handle_click_event()
        self.process_events()

        # The second ally should be selected
        self.assertIs(Soldier.chosen_ally, ally2)
        # Attack range should be displayed
        self.assertIsNotNone(AttackRange.instance)
        # Available movements should be displayed
        self.assertNotEqual(Movement.instances, [])
        # Both allies should be active
        self.assertEqual(ally1["background"], Color.BLUE)
        self.assertEqual(ally2["background"], Color.BLUE)

    def test_click_on_an_enemy(self):
        ally = Swordsman(self.canvas, 0, 0, color=Color.BLUE)
        enemy = Swordsman(self.canvas, 0, 1, color=Color.RED)
        enemy.handle_click_event()
        self.process_events()

        # No ally should be selected
        self.assertIsNone(Soldier.chosen_ally)
        # No attack range should be displayed
        self.assertIsNone(AttackRange.instance)
        # No available movements should be displayed
        self.assertEqual(Movement.instances, [])
        # The enemy should be active
        self.assertEqual(enemy["background"], Color.RED)

    def test_click_on_an_ally_then_click_on_one_of_its_available_movements(self):
        ally = Swordsman(self.canvas, 0, 0, color=Color.BLUE)
        ally.handle_click_event()
        movement = Movement.instances[0]
        movement.handle_click_event()
        self.process_events()

        # The coordinate of the clicked movement should become the ally's new coordinate
        self.assertEqual((ally.x, ally.y), (movement.x, movement.y))
        # The ally should be unselected
        self.assertIsNone(Soldier.chosen_ally)
        # The ally's attack range should not be displayed
        self.assertIsNone(AttackRange.instance)
        # The ally's available movements should not be displayed
        self.assertEqual(Movement.instances, [])
        # The ally should be active
        self.assertEqual(ally["background"], Color.BLUE)

    def test_click_on_an_ally_then_click_on_an_enemy_within_its_attack_range(self):
        ally = Swordsman(self.canvas, 0, 0, color=Color.BLUE)
        enemy = Swordsman(self.canvas, 0, 1, color=Color.RED)
        ally.handle_click_event()
        enemy.handle_click_event()
        self.process_events()

        # The ally should be unselected
        self.assertIsNone(Soldier.chosen_ally)
        # The ally's attack range should not be displayed
        self.assertIsNone(AttackRange.instance)
        # The ally's available movements should not be displayed
        self.assertEqual(Movement.instances, [])
        # The ally should be active
        self.assertEqual(ally["background"], Color.BLUE)

    def test_click_on_an_ally_then_click_on_an_enemy_outside_its_attack_range(self):
        ally = Swordsman(self.canvas, 0, 0, color=Color.BLUE)
        enemy = Swordsman(self.canvas, 5, 5, color=Color.RED)
        ally.handle_click_event()
        enemy.handle_click_event()
        self.process_events()

        # The ally should be selected
        self.assertIs(Soldier.chosen_ally, ally)
        # The ally's attack range should be displayed
        self.assertIsNotNone(AttackRange.instance)
        # The ally's available movements should be displayed
        self.assertNotEqual(Movement.instances, [])
        # The ally should be active
        self.assertEqual(ally["background"], Color.BLUE)
        # The enemy should not be attacked
        self.assertEqual(enemy.health, enemy.__class__.health)

    def test_move_an_ally_then_order_it_to_attack(self):
        ally = Swordsman(self.canvas, 0, 0, color=Color.BLUE)
        enemy = Swordsman(self.canvas, 0, 2, color=Color.RED)
        ally.handle_click_event()
        next(m for m in Movement.instances if (m.x, m.y) == (0, 1)).handle_click_event()
        ally.handle_click_event()
        enemy.handle_click_event()
        self.process_events()

        # The ally should be unselected
        self.assertIsNone(Soldier.chosen_ally)
        # The ally's attack range should not be displayed
        self.assertIsNone(AttackRange.instance)
        # The ally's available movements should not be displayed
        self.assertEqual(Movement.instances, [])
        # The ally should be inactive
        self.assertEqual(ally["background"], Color.GRAY)

    def test_order_an_ally_to_attack_then_move_it(self):
        ally = Swordsman(self.canvas, 0, 0, color=Color.BLUE)
        enemy = Swordsman(self.canvas, 0, 1, color=Color.RED)
        ally.handle_click_event()
        enemy.handle_click_event()
        ally.handle_click_event()
        next(m for m in Movement.instances if (m.x, m.y) == (0, -1)).handle_click_event()
        self.process_events()

        # The ally should be unselected
        self.assertIsNone(Soldier.chosen_ally)
        # The ally's attack range should not be displayed
        self.assertIsNone(AttackRange.instance)
        # The ally's available movements should not be displayed
        self.assertEqual(Movement.instances, [])
        # The ally should be inactive
        self.assertEqual(ally["background"], Color.GRAY)


class SoldierStatsTest(SoldierTest):

    def test_king_stats(self):
        ally = King(self.canvas, 0, 0, color=Color.BLUE)
        enemy = King(self.canvas, 0, 1, color=Color.RED)
        self.process_events()

        # Should have superior defense, health, and mobility
        self.assertTrue(ally.attack == enemy.attack == Soldier.attack)
        self.assertTrue(ally.attack_range == enemy.attack_range == Soldier.attack_range)
        self.assertTrue(ally.defense == enemy.defense > Soldier.defense)
        self.assertTrue(ally.health == enemy.health > Soldier.health)
        self.assertTrue(ally.mobility == enemy.mobility > Soldier.mobility)

    def test_bowman_stats(self):
        ally = Bowman(self.canvas, 0, 0, color=Color.BLUE)
        enemy = Bowman(self.canvas, 0, 1, color=Color.RED)
        self.process_events()

        # Should have superior attack_range but inferior attack and health
        self.assertTrue(ally.attack == enemy.attack < Soldier.attack)
        self.assertTrue(ally.attack_range == enemy.attack_range > Soldier.attack_range)
        self.assertTrue(ally.defense == enemy.defense == Soldier.defense)
        self.assertTrue(ally.health == enemy.health < Soldier.health)
        self.assertTrue(ally.mobility == enemy.mobility == Soldier.mobility)

    def test_horseman_stats(self):
        ally = Horseman(self.canvas, 0, 0, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 1, color=Color.RED)
        self.process_events()

        # Should have superior mobility
        self.assertTrue(ally.attack == enemy.attack == Soldier.attack)
        self.assertTrue(ally.attack_range == enemy.attack_range == Soldier.attack_range)
        self.assertTrue(ally.defense == enemy.defense == Soldier.defense)
        self.assertTrue(ally.health == enemy.health == Soldier.health)
        self.assertTrue(ally.mobility == enemy.mobility > Soldier.mobility)

    def test_swordsman_stats(self):
        ally = Swordsman(self.canvas, 0, 0, color=Color.BLUE)
        enemy = Swordsman(self.canvas, 0, 1, color=Color.RED)
        self.process_events()

        # Should have superior defense
        self.assertTrue(ally.attack == enemy.attack == Soldier.attack)
        self.assertTrue(ally.attack_range == enemy.attack_range == Soldier.attack_range)
        self.assertTrue(ally.defense == enemy.defense > Soldier.defense)
        self.assertTrue(ally.health == enemy.health == Soldier.health)
        self.assertTrue(ally.mobility == enemy.mobility == Soldier.mobility)


class SoldierCounterTest(SoldierTest):

    def test_king_counters(self):
        ally = King(self.canvas, 0, 0, color=Color.BLUE)
        enemy = King(self.canvas, 0, 1, color=Color.RED)
        self.process_events()

        self.assertTrue(ally.counters == enemy.counters == {King, Bowman, Horseman, Swordsman})

    def test_bowman_counters(self):
        ally = Bowman(self.canvas, 0, 0, color=Color.BLUE)
        enemy = Bowman(self.canvas, 0, 1, color=Color.RED)
        self.process_events()

        self.assertTrue(ally.counters == enemy.counters == {Swordsman})

    def test_horseman_counters(self):
        ally = Horseman(self.canvas, 0, 0, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 1, color=Color.RED)
        self.process_events()

        self.assertTrue(ally.counters == enemy.counters == {Bowman})

    def test_swordsman_counters(self):
        ally = Swordsman(self.canvas, 0, 0, color=Color.BLUE)
        enemy = Swordsman(self.canvas, 0, 1, color=Color.RED)
        self.process_events()

        self.assertTrue(ally.counters == enemy.counters == {Horseman})


class SoldierGetCoordinateAfterMovingTowardTest(SoldierTest):

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_north(self):
        ally = Bowman(self.canvas, 0, 5, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 0, color=Color.RED)
        coordinate = enemy.get_coordinate_after_moving_toward(ally)
        self.process_events()

        self.assertEqual(coordinate, (0, enemy.mobility))

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_south(self):
        ally = Bowman(self.canvas, 0, -5, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 0, color=Color.RED)
        coordinate = enemy.get_coordinate_after_moving_toward(ally)
        self.process_events()

        self.assertEqual(coordinate, (0, -enemy.mobility))

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_east(self):
        ally = Bowman(self.canvas, 5, 0, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 0, color=Color.RED)
        coordinate = enemy.get_coordinate_after_moving_toward(ally)
        self.process_events()

        self.assertEqual(coordinate, (enemy.mobility, 0))

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_west(self):
        ally = Bowman(self.canvas, -5, 0, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 0, color=Color.RED)
        coordinate = enemy.get_coordinate_after_moving_toward(ally)
        self.process_events()

        self.assertEqual(coordinate, (-enemy.mobility, 0))

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_northeast(self):
        ally = Bowman(self.canvas, 5, 5, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 0, color=Color.RED)
        coordinate = enemy.get_coordinate_after_moving_toward(ally)
        self.process_events()

        mx = my = int(enemy.mobility / 2)
        self.assertIn(coordinate, {(mx + 1, my), (mx, my + 1)})

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_northwest(self):
        ally = Bowman(self.canvas, -5, 5, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 0, color=Color.RED)
        coordinate = enemy.get_coordinate_after_moving_toward(ally)
        self.process_events()

        mx = my = int(enemy.mobility / 2)
        self.assertIn(coordinate, {(-mx - 1, my), (-mx, my + 1)})

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_southeast(self):
        ally = Bowman(self.canvas, 5, -5, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 0, color=Color.RED)
        coordinate = enemy.get_coordinate_after_moving_toward(ally)
        self.process_events()

        mx = my = int(enemy.mobility / 2)
        self.assertIn(coordinate, {(mx + 1, -my), (mx, -my - 1)})

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_southwest(self):
        ally = Bowman(self.canvas, -5, -5, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 0, color=Color.RED)
        coordinate = enemy.get_coordinate_after_moving_toward(ally)
        self.process_events()

        mx = my = int(enemy.mobility / 2)
        self.assertIn(coordinate, {(-mx - 1, -my), (-mx, -my - 1)})

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_north_northeast(self):
        ally = Bowman(self.canvas, 3, 4, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 0, color=Color.RED)
        coordinate = enemy.get_coordinate_after_moving_toward(ally)
        self.process_events()

        mx = int(enemy.mobility * 3 / 7)
        my = int(enemy.mobility * 4 / 7)
        self.assertEqual(coordinate, (mx, my + 1))

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_east_northeast(self):
        ally = Bowman(self.canvas, 4, 3, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 0, color=Color.RED)
        coordinate = enemy.get_coordinate_after_moving_toward(ally)
        self.process_events()

        mx = int(enemy.mobility * 4 / 7)
        my = int(enemy.mobility * 3 / 7)
        self.assertEqual(coordinate, (mx + 1, my))

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_north_northwest(self):
        ally = Bowman(self.canvas, -3, 4, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 0, color=Color.RED)
        coordinate = enemy.get_coordinate_after_moving_toward(ally)
        self.process_events()

        mx = int(enemy.mobility * 3 / 7)
        my = int(enemy.mobility * 4 / 7)
        self.assertEqual(coordinate, (-mx, my + 1))

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_west_northwest(self):
        ally = Bowman(self.canvas, -4, 3, color=Color.BLUE)
        enemy = Horseman(self.canvas, 0, 0, color=Color.RED)
        coordinate = enemy.get_coordinate_after_moving_toward(ally)
        self.process_events()

        mx = int(enemy.mobility * 4 / 7)
        my = int(enemy.mobility * 3 / 7)
        self.assertEqual(coordinate, (-mx - 1, my))

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_south_southeast(self):
        pass

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_east_southeast(self):
        pass

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_south_southwest(self):
        pass

    def test_get_coordinate_after_moving_an_enemy_toward_an_ally_positioned_in_the_west_southwest(self):
        pass


if __name__ == "__main__":
    main()
