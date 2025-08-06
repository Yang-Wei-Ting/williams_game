from game.soldiers.base import Soldier, SoldierModel, SoldierView


class ArcherModel(SoldierModel):

    attack_multipliers = {
        "CavalryModel": 0.7,
        "HeroModel": 0.7,
        "InfantryModel": 1.5,
    }
    attack_range = 3


class ArcherView(SoldierView):
    pass


class Archer(Soldier):
    pass
