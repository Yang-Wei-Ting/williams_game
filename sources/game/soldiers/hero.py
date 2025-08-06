from game.soldiers.base import Soldier, SoldierModel, SoldierView


class HeroModel(SoldierModel):

    attack = 40.0
    attack_multipliers = {
        "ArcherModel": 1.5,
        "CavalryModel": 1.5,
        "HeroModel": 1.5,
        "InfantryModel": 1.5,
    }

    health = 200.0

    mobility = 3

    cost = 65535


class HeroView(SoldierView):
    pass


class Hero(Soldier):
    pass
