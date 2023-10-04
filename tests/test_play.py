import tkinter as tk
from unittest import TestCase, main, mock

from game.miscs import Configuration as C
from play import Program


class DoOneEventTk(tk.Tk):

    def mainloop(self, n=0):
        while self.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
            pass


class ProgramTest(TestCase):

    @mock.patch("play.tk.Tk", new=DoOneEventTk)
    def test_program_initialization(self):
        program = Program()

        self.assertIsInstance(program._window, DoOneEventTk)
        self.assertEqual(program._window.title(), "Map")
        self.assertEqual(program._window.resizable(), (False, False))
        self.assertIsInstance(program._canvas, tk.Canvas)
        self.assertIs(program._canvas.master, program._window)
        self.assertEqual(program._canvas.winfo_width(), C.TILE_DIMENSION * C.HORIZONTAL_TILE_COUNT)
        self.assertEqual(program._canvas.winfo_height(), C.TILE_DIMENSION * C.VERTICAL_TILE_COUNT)
        self.assertEqual(program._canvas["background"], "Black")
        self.assertEqual(program._canvas["highlightthickness"], "0")
        self.assertEqual(program._canvas.winfo_manager(), "pack")

        program._window.destroy()


if __name__ == "__main__":
    main()
