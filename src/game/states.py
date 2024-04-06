class GameState:
    """
    This class keeps tracks of program-level states.
    """

    occupied_coordinates = set()


class AttackRangeState:
    """
    This class keeps tracks of AttackRange class instance.
    """

    instance = None


class MovementState:
    """
    This class keeps tracks of Movement class instances.
    """

    instances = []


class SoldierState:
    """
    This class keeps tracks of Soldier class instances.
    """

    allies = []
    enemies = []
    chosen_ally = None


class PopUpControlState:

    instance = None
