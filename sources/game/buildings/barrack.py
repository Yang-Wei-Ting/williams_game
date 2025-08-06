from game.base import GameObject
from game.buildings.base import Building, BuildingModel, BuildingView
from game.miscellaneous import Configuration as C
from game.recruitments import ArcherRecruitment, CavalryRecruitment, InfantryRecruitment


class BarrackModel(BuildingModel):
    pass


class BarrackView(BuildingView):
    pass


class Barrack(Building):

    def _register(self) -> None:
        GameObject.unordered_collections["critical_building"].add(self)

    def _unregister(self) -> None:
        GameObject.unordered_collections["critical_building"].remove(self)

    def _handle_selection(self) -> None:
        InfantryRecruitment.create(
            {
                "x": C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
                "y": 4,
            },
            {
                "canvas": self.view.canvas,
            },
        )
        ArcherRecruitment.create(
            {
                "x": C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
                "y": 5,
            },
            {
                "canvas": self.view.canvas,
            },
        )
        CavalryRecruitment.create(
            {
                "x": C.HORIZONTAL_LAND_TILE_COUNT + C.HORIZONTAL_SHORE_TILE_COUNT,
                "y": 6,
            },
            {
                "canvas": self.view.canvas,
            },
        )

    def _handle_deselection(self) -> None:
        for recruitment in set(GameObject.unordered_collections["barrack_recruitment"]):
            recruitment.destroy()
