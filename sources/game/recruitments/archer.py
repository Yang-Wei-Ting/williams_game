from game.recruitments.base import SoldierRecruitment
from game.soldiers.archer import Archer


class ArcherRecruitment(SoldierRecruitment):

    @property
    def target(self) -> type[Archer]:
        return Archer
