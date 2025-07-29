from game.soldiers.base import Soldier


class Hero(Soldier):

    attack = 40.0
    attack_multipliers = {
        "Archer": 1.5,
        "Cavalry": 1.5,
        "Hero": 1.5,
        "Infantry": 1.5,
    }

    health = 200.0

    mobility = 3

    cost = 65535
