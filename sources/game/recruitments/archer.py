from game.recruitments.base import SoldierRecruitment
from game.soldiers.archer import Archer


class ArcherRecruitment(SoldierRecruitment):

    cost = 20

    @property
    def target(self) -> type[Archer]:
        return Archer
