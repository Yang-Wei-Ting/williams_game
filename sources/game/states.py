from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from game.buildings.base import Building
    from game.controls import DisplayOutcomeControl, EndTurnControl
    from game.displays import CoinDisplay, DayDisplay, StatDisplay
    from game.highlights import AttackRangeHighlight, MovementHighlight, PlacementHighlight
    from game.recruitments.base import SoldierRecruitment
    from game.soldiers.base import Soldier


class GameState:

    day: int = 1
    wave: int = 0
    coin: int = 10
    cost_by_coordinate: dict[tuple[int, int], int] = {}
    occupied_coordinates: set[tuple[int, int]] = set()
    pressed_game_object: Optional["Soldier"] = None
    selected_game_objects: list["SoldierRecruitment | Building"] = []


class BuildingState:

    critical_buildings: set["Building"] = set()
    noncritical_buildings: set["Building"] = set()


class ControlState:

    display_outcome_control: Optional["DisplayOutcomeControl"] = None
    end_turn_control: Optional["EndTurnControl"] = None


class DisplayState:

    coin_display: Optional["CoinDisplay"] = None
    day_display: Optional["DayDisplay"] = None
    stat_display: Optional["StatDisplay"] = None


class HighlightState:

    attack_range_highlight: Optional["AttackRangeHighlight"] = None
    movement_highlights: set["MovementHighlight"] = set()
    placement_highlights: set["PlacementHighlight"] = set()


class RecruitmentState:

    barrack_recruitments: set["SoldierRecruitment"] = set()


class SoldierState:

    allied_soldiers: set["Soldier"] = set()
    enemy_soldiers: set["Soldier"] = set()
