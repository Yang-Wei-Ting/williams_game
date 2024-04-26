from game.soldiers.base import Soldier


class Archer(Soldier):
    """
    Soldier with high attack range but low attack and health.
    Counter infantries, countered by cavalries.
    """

    attack = 25
    attack_range = 3
    health = 50

    @property
    def counters(self) -> set:
        return {"Infantry"}
