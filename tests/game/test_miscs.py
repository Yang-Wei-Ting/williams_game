import tkinter as tk
from unittest import TestCase, main

from game.miscs import Image


class ImageTest(TestCase):

    def test_image_hook(self):
        tk.Tk()
        Image.initialize()

        self.assertTrue(hasattr(Image, "restart"))
        self.assertIsInstance(Image.restart, tk.PhotoImage)


if __name__ == "__main__":
    main()
