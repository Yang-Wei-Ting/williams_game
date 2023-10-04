from unittest import main, mock, skip

from game.miscellaneous import Configuration as C
from game.soldiers import Archer, Cavalry, Hero, Infantry
from game.states import GameState, HighlightState, SoldierState
from game.test_bases import BaseTest


class SoldierMatchupTest(BaseTest):

    def fight(self, attacker_cls, defender_cls):
        attacker = attacker_cls(
            self.program._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT // 2,
            C.VERTICAL_TILE_COUNT // 2 + 2,
            color=C.BLUE,
        )
        defender = defender_cls(
            self.program._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT // 2,
            C.VERTICAL_TILE_COUNT // 2 - 2,
            color=C.RED,
        )
        self.process_events()

        while True:
            if attacker.health <= 0:
                return "defender won"

            attacker.hunt()
            self.process_events()

            if defender.health <= 0:
                return "attacker won"

            defender.hunt()
            self.process_events()

    def test_archer_vs_cavalry(self):
        self.assertEqual(self.fight(Archer, Cavalry), "defender won")

    def test_archer_vs_hero(self):
        self.assertEqual(self.fight(Archer, Hero), "defender won")

    def test_archer_vs_infantry(self):
        self.assertEqual(self.fight(Archer, Infantry), "attacker won")

    def test_cavalry_vs_archer(self):
        self.assertEqual(self.fight(Cavalry, Archer), "attacker won")

    def test_cavalry_vs_hero(self):
        self.assertEqual(self.fight(Cavalry, Hero), "defender won")

    def test_cavalry_vs_infantry(self):
        self.assertEqual(self.fight(Cavalry, Infantry), "defender won")

    def test_hero_vs_archer(self):
        self.assertEqual(self.fight(Hero, Archer), "attacker won")

    def test_hero_vs_cavalry(self):
        self.assertEqual(self.fight(Hero, Cavalry), "attacker won")

    def test_hero_vs_infantry(self):
        self.assertEqual(self.fight(Hero, Infantry), "attacker won")

    def test_infantry_vs_archer(self):
        self.assertEqual(self.fight(Infantry, Archer), "defender won")

    def test_infantry_vs_cavalry(self):
        self.assertEqual(self.fight(Infantry, Cavalry), "attacker won")

    def test_infantry_vs_hero(self):
        self.assertEqual(self.fight(Infantry, Hero), "defender won")


class SoldierControlTest(BaseTest):

    @skip("")
    def test_press_an_ally(self):
        ally = Infantry(
            self.program._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT // 2,
            C.VERTICAL_TILE_COUNT // 2,
            color=C.BLUE,
        )
        mock_event = mock.Mock(x=C.HORIZONTAL_LAND_TILE_COUNT // 2, y=C.VERTICAL_TILE_COUNT // 2)
        ally._handle_ally_press_event(mock_event)
        self.process_events()

        self.assertEqual(ally._main_widget["background"], C.BLUE)
        self.assertEqual(GameState.selected_game_objects, [ally])
        self.assertEqual(GameState.occupied_coordinates, {ally_coordinate})
        self.assertEqual(SoldierState.allied_soldiers, {ally})
        self.assertEqual(SoldierState.enemy_soldiers, set())
        self.assertIsNotNone(HighlightState.attack_range_highlight)
        self.assertEqual(
            (HighlightState.attack_range_highlight.x, HighlightState.attack_range_highlight.y),
            ally_coordinate,
        )
        self.assertNotEqual(HighlightState.movement_highlights, set())

        ally._handle_ally_release_event(mock_event)
        self.process_events()

    def test_press_an_enemy(self):
        pass

    def test_drag_an_ally_onto_one_of_its_available_movements(self):
        pass

    def test_drag_an_ally_onto_an_enemy_within_its_attack_range(self):
        pass

    def test_drag_an_ally_onto_an_enemy_outside_its_attack_range(self):
        pass

    def test_move_an_ally_then_order_it_to_attack(self):
        pass

    def test_order_an_ally_to_attack_then_move_it(self):
        pass


@skip("")
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
        enemy.mobility = 9
        ally = Infantry(self.program._canvas, 8, 3, color=C.BLUE)

        coordinate = enemy._get_approaching_path(ally)[-1]
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
        enemy = Cavalry(self.program._canvas, 2, 9, color=C.RED)
        enemy.mobility = 9
        ally = Infantry(self.program._canvas, 8, 3, color=C.BLUE)

        coordinate = enemy._get_approaching_path(ally)[-1]
        self.process_events()

        self.assertEqual(coordinate, (4, 2))


@skip("")
@mock.patch("game.soldiers.base.Soldier.promote")
@mock.patch("game.soldiers.base.Soldier.assault")
@mock.patch("game.soldiers.base.Soldier.move_to")
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
        killable_ally = Infantry(self.program._canvas, 4, 6, color=C.BLUE)
        killable_ally.health = 1
        hittable_ally = Infantry(self.program._canvas, 5, 7, color=C.BLUE)
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
        hittable_ally = Infantry(self.program._canvas, 2, 4, color=C.BLUE)
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
        ally_with_higher_health = Infantry(self.program._canvas, 2, 4, color=C.BLUE)
        ally_with_higher_health.health = 2
        ally_with_lower_health = Infantry(self.program._canvas, 6, 9, color=C.BLUE)
        ally_with_lower_health.health = 1

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
        closer_ally = Infantry(self.program._canvas, 2, 5, color=C.BLUE)
        closer_ally.health = 1
        farther_ally = Infantry(self.program._canvas, 7, 9, color=C.BLUE)
        farther_ally.health = 1

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
