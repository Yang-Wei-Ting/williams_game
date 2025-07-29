from game.buildings.base import Building
from game.miscellaneous import Configuration as C
from game.recruitments import ArcherRecruitment, CavalryRecruitment, InfantryRecruitment
from game.states import BuildingState, RecruitmentState


class Barrack(Building):

    defense = 0.4
    health = 400

    def _register(self) -> None:
        super()._register()
        BuildingState.critical_buildings.add(self)

    def _unregister(self) -> None:
        super()._unregister()
        BuildingState.critical_buildings.remove(self)

    def _handle_selection(self) -> None:
        InfantryRecruitment(
            self._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
            2,
        )
        ArcherRecruitment(
            self._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
            3,
        )
        CavalryRecruitment(
            self._canvas,
            C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
            4,
        )

    def _handle_deselection(self) -> None:
        for recruitment in set(RecruitmentState.barrack_recruitments):
            recruitment.detach_and_destroy_widgets()
