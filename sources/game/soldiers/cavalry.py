from game.soldiers.base import Soldier


class Cavalry(Soldier):

    attack_multipliers = {
        "Archer": 1.5,
        "Hero": 0.7,
        "Infantry": 0.7,
    }

    mobility = 3
