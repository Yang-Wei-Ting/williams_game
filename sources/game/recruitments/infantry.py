from game.recruitments.base import SoldierRecruitment
from game.soldiers.infantry import Infantry


class InfantryRecruitment(SoldierRecruitment):

    @property
    def target(self) -> type[Infantry]:
        return Infantry
