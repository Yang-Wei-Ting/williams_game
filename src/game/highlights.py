import tkinter as tk

from game.bases import GameObject
from game.miscs import Image, get_pixels
from game.states import AttackRangeState, MovementState, SoldierState


class AttackRange(GameObject):
    """
    A class that instantiates attack range indicators which indicate ally instances' attack range.
    Enemy instances can be attacked when they are covered by an attack range indicator.
    """

    def __init__(self, canvas: tk.Canvas, x: int, y: int, *, half_diagonal: int) -> None:
        """
        Create canvas window object.
        """
        self._half_diagonal = half_diagonal
        super().__init__(canvas, x, y)

    def _create_widget(self) -> None:
        """
        Override this method as there's no widget to create.
        """

    def _configure_widget(self) -> None:
        """
        Override this method as there's no widget to configure.
        """

    def _create_canvas_window_object(self) -> None:
        """
        Create canvas window object and set 'AttackRangeState.instance' to self.
        """
        self._main_widget_id = self._canvas.create_image(
            *get_pixels(self.x, self.y),
            image=getattr(Image, "red_diamond_{0}x{0}".format(self._half_diagonal * 120)),
        )
        AttackRangeState.instance = self

    def remove_canvas_window_object(self) -> None:
        """
        Remove canvas window object and set 'AttackRangeState.instance' to None.
        """
        super().remove_canvas_window_object()
        AttackRangeState.instance = None


class Movement(GameObject):
    """
    A class that instantiates movements.
    When a movement is clicked on, the chosen ally instance moves to its coordinate.
    """

    def _configure_widget(self) -> None:
        """
        Configure widget.
        """
        self.configure_main_widget(
            image=Image.transparent_12x12,
            background="Royal Blue",
            activebackground="Royal Blue",
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            command=self.handle_click_event,
        )

    def _create_canvas_window_object(self) -> None:
        """
        Create canvas window object and append self to 'MovementState.instances'.
        """
        super()._create_canvas_window_object()
        MovementState.instances.append(self)

    def remove_canvas_window_object(self) -> None:
        """
        Remove canvas window object and remove self from 'MovementState.instances'.
        """
        super().remove_canvas_window_object()
        MovementState.instances.remove(self)

    def handle_click_event(self) -> None:
        """
        Move the chosen ally instance to the coordinate of the clicked movement.
        Unselect the ally instance then clear all highlights.
        """
        SoldierState.chosen_ally.move_to(self.x, self.y)
        SoldierState.chosen_ally.handle_click_event()
