from game.soldiers.base import Soldier


class Cavalry(Soldier):
    """
    Soldier with high mobility.
    Counter archers, countered by infantries.
    """

    mobility = 3

    @property
    def counters(self) -> set:
        return {"Archer"}
