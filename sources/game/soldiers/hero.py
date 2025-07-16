import math

from game.soldiers.base import Soldier


class Hero(Soldier):

    attack = 40
    attack_multipliers = {
        "Archer": 1.5,
        "Cavalry": 1.5,
        "Hero": 1.5,
        "Infantry": 1.5,
    }

    health = 200

    mobility = 3

    cost = math.inf
