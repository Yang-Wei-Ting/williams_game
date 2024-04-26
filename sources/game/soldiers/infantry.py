from game.soldiers.base import Soldier


class Infantry(Soldier):
    """
    Soldier with high defense.
    Counter cavalries, countered by archers.
    """

    defense = 20

    @property
    def counters(self) -> set:
        return {"Cavalry"}
