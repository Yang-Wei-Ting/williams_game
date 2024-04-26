from game.recruitments.base import SoldierRecruitment
from game.soldiers.cavalry import Cavalry


class CavalryRecruitment(SoldierRecruitment):

    cost = 25

    @property
    def target(self) -> type[Cavalry]:
        return Cavalry
