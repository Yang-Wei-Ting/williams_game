from game.soldiers.base import Soldier


class Cavalry(Soldier):
    """
    Soldier with high mobility.
    Counter archers, countered by infantries.
    """

    attack_multipliers = {
        "Archer": 1.5,
        "Hero": 0.7,
        "Infantry": 0.7,
    }

    mobility = 3
