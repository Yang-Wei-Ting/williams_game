class GameState:

    day = 1
    wave = 0
    coin = 10
    cost_by_coordinate = {}
    occupied_coordinates = set()
    pressed_game_object = None
    selected_game_objects = []


class BuildingState:

    critical_buildings = set()
    noncritical_buildings = set()


class ControlState:

    display_outcome_control = None
    end_turn_control = None


class DisplayState:

    coin_display = None
    day_display = None
    stat_display = None


class HighlightState:

    attack_range_highlight = None
    movement_highlights = set()
    placement_highlights = set()


class RecruitmentState:

    barrack_recruitments = set()


class SoldierState:

    allied_soldiers = set()
    enemy_soldiers = set()
