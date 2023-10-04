import tkinter as tk
from unittest import TestCase, main

from game.miscs import Image


class ImageTest(TestCase):

    def test_image_hook(self):
        tk.Tk()
        Image.initialize()

        self.assertTrue(hasattr(Image, "blue_infantry_1"))
        self.assertIsInstance(Image.blue_infantry_1, tk.PhotoImage)


if __name__ == "__main__":
    main()
