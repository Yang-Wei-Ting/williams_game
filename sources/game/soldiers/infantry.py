from game.soldiers.base import Soldier


class Infantry(Soldier):

    attack_multipliers = {
        "Archer": 0.7,
        "Cavalry": 1.5,
        "Hero": 0.7,
    }
    attack_range = 2

    defense = 0.25
