from game.soldiers.base import Soldier


class Cavalry(Soldier):
    """
    Soldier with high mobility.
    Counter archers, countered by infantries.
    """

    attack_multipliers = {
        "Archer": 1.5,
        "Hero": 0.9,
        "Infantry": 0.9,
    }

    mobility = 3
