from game.soldiers.base import Soldier


class Infantry(Soldier):
    """
    Soldier with high attack.
    Counter cavalries, countered by archers.
    """

    attack = 40
    attack_multipliers = {
        "Archer": 0.9,
        "Cavalry": 1.5,
        "Hero": 0.9,
    }
