import tkinter as tk
from unittest import TestCase, main, mock

from play import Program


class DoOneEventTk(tk.Tk):

    def mainloop(self):
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
        self.assertEqual(program._canvas.winfo_width(), 780)
        self.assertEqual(program._canvas.winfo_height(), 780)
        self.assertEqual(program._canvas["background"], "Black")
        self.assertEqual(program._canvas["highlightthickness"], "0")
        self.assertEqual(program._canvas.winfo_manager(), "pack")

        # breakpoint()


if __name__ == "__main__":
    main()
