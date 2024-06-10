from game.soldiers.base import Soldier


class Infantry(Soldier):
    """
    Soldier with high defense.
    Counter cavalries, countered by archers.
    """

    attack_multipliers = {
        "Archer": 0.7,
        "Cavalry": 1.5,
        "Hero": 0.7,
    }

    defense = 0.25
