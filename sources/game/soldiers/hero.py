from game.soldiers.base import Soldier


class Hero(Soldier):
    """
    Counter all soldiers.
    """

    defense = 20
    health = 150
    mobility = 3

    @property
    def counters(self) -> set:
        return {"Archer", "Cavalry", "Hero", "Infantry"}
