import tkinter as tk
from unittest import TestCase, mock

from game.states import BuildingState, ControlState, GameState, HighlightState, SoldierState
from play import Program


class NonBlockingTk(tk.Tk):

    def mainloop(self, n=0):
        while self.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
            pass


class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        with mock.patch("play.tk.Tk", new=NonBlockingTk):
            Program._create_initial_allied_soldiers = lambda self: None
            Program._create_initial_buildings = lambda self: None
            cls.program = Program()

    def tearDown(self):
        for obj in GameState.selected_game_objects[::-1]:
            obj.handle_click_event()

        for obj in (
            SoldierState.allied_soldiers | SoldierState.enemy_soldiers |
            BuildingState.critical_buildings | BuildingState.noncritical_buildings
        ):
            try:
                obj.detach_widgets_from_canvas()
            except AttributeError:
                pass

            obj.destroy_widgets()

        self.assertEqual(GameState.occupied_coordinates, set())
        GameState.day = 1
        GameState.wave = 0
        GameState.coin = 0
        self.assertEqual(GameState.selected_game_objects, [])
        self.assertEqual(SoldierState.allied_soldiers, set())
        self.assertEqual(SoldierState.enemy_soldiers, set())
        self.assertEqual(BuildingState.critical_buildings, set())
        self.assertEqual(BuildingState.noncritical_buildings, set())
        self.assertIsNone(HighlightState.attack_range)
        self.assertEqual(HighlightState.movements, set())
        self.assertEqual(HighlightState.placements, set())
        self.assertEqual(ControlState.recruit_soldier_controls, set())
        if ControlState.pop_up_control:
            ControlState.pop_up_control.handle_click_event()

    @classmethod
    def tearDownClass(cls):
        cls.program._window.destroy()

    def process_events(self):
        while self.program._window.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
            pass
