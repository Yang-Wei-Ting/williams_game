from game.soldiers.base import Soldier, SoldierModel, SoldierView


class CavalryModel(SoldierModel):

    attack_multipliers = {
        "ArcherModel": 1.5,
        "HeroModel": 0.7,
        "InfantryModel": 0.7,
    }

    mobility = 3


class CavalryView(SoldierView):
    pass


class Cavalry(Soldier):
    pass
