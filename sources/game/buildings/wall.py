from game.base import GameObject
from game.buildings.base import Building, BuildingModel, BuildingView


class WallModel(BuildingModel):

    defense = 0.5
    health = 100.0


class WallView(BuildingView):
    pass


class Wall(Building):

    def _register(self) -> None:
        GameObject.unordered_collections["noncritical_building"].add(self)

    def _unregister(self) -> None:
        GameObject.unordered_collections["noncritical_building"].remove(self)

    def _handle_selection(self) -> None:
        pass

    def _handle_deselection(self) -> None:
        pass
