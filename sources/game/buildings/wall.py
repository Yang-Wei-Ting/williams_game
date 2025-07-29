from game.buildings.base import Building
from game.states import BuildingState


class Wall(Building):

    defense = 0.5
    health = 100.0

    def _register(self) -> None:
        super()._register()
        BuildingState.noncritical_buildings.add(self)

    def _unregister(self) -> None:
        super()._unregister()
        BuildingState.noncritical_buildings.remove(self)

    def _handle_selection(self) -> None:
        pass

    def _handle_deselection(self) -> None:
        pass
