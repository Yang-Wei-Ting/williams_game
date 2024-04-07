class GameState:
    """
    This class keeps tracks of program-level states.
    """

    occupied_coordinates = set()


class SoldierState:
    """
    This class keeps tracks of Soldier class instances.
    """

    allies = []
    enemies = []
    chosen_ally = None


class MovementState:
    """
    This class keeps tracks of Movement class instances.
    """

    instances = []


class AttackRangeState:
    """
    This class keeps tracks of AttackRange class instance.
    """

    instance = None


class PopUpControlState:

    instance = None
