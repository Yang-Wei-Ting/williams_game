from game.soldiers.base import Soldier


class Archer(Soldier):

    attack_multipliers = {
        "Cavalry": 0.7,
        "Hero": 0.7,
        "Infantry": 1.5,
    }
    attack_range = 3
