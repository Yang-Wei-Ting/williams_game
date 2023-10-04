import tkinter as tk
from unittest import TestCase, mock

from game.states import BuildingState, ControlState, GameState, HighlightState, RecruitmentState, SoldierState
from play import Program


class NonBlockingTk(tk.Tk):

    def mainloop(self, n=0):
        while self.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
            pass


class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        with mock.patch("play.tk.Tk", new=NonBlockingTk):
            Program._create_initial_buildings = lambda self: None
            Program._create_initial_allied_soldiers = lambda self: None
            cls.program = Program()

    def tearDown(self):
        for obj in GameState.selected_game_objects[::-1]:
            obj.handle_click_event()

        for obj in (
            SoldierState.allied_soldiers | SoldierState.enemy_soldiers |
            BuildingState.critical_buildings | BuildingState.noncritical_buildings
        ):
            obj.detach_and_destroy_widgets()

        GameState.day = 1
        GameState.wave = 0
        GameState.coin = 0
        self.assertEqual(GameState.occupied_coordinates, set())
        self.assertEqual(GameState.selected_game_objects, [])

        self.assertEqual(BuildingState.critical_buildings, set())
        self.assertEqual(BuildingState.noncritical_buildings, set())

        if ControlState.display_outcome_control:
            ControlState.display_outcome_control.handle_click_event()

        self.assertIsNone(HighlightState.attack_range_highlight)
        self.assertEqual(HighlightState.movement_highlights, set())
        self.assertEqual(HighlightState.placement_highlights, set())

        self.assertEqual(RecruitmentState.barrack_recruitments, set())

        self.assertEqual(SoldierState.allied_soldiers, set())
        self.assertEqual(SoldierState.enemy_soldiers, set())

    @classmethod
    def tearDownClass(cls):
        cls.program._window.destroy()

    def process_events(self):
        while self.program._window.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
            pass
