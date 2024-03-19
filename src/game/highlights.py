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
        Attach widgets to canvas.
        """
        self._half_diagonal = half_diagonal
        super().__init__(canvas, x, y)

    def _create_widgets(self) -> None:
        """
        Override this method as the main widget, tk.PhotoImage, already exists.
        """

    def _configure_widgets(self) -> None:
        """
        Override this method as the main widget, tk.PhotoImage, is already configured.
        """

    def _attach_widgets_to_canvas(self) -> None:
        """
        Attach widgets to canvas and set 'AttackRangeState.instance' to self.
        """
        self._main_widget_id = self._canvas.create_image(
            *get_pixels(self.x, self.y),
            image=getattr(Image, "red_diamond_{0}x{0}".format(self._half_diagonal * 120)),
        )
        AttackRangeState.instance = self

    def destroy_widgets(self) -> None:
        """
        Remove widgets from canvas and set 'AttackRangeState.instance' to None.
        """
        self._canvas.delete(self._main_widget_id)
        del self._main_widget_id
        AttackRangeState.instance = None


class Movement(GameObject):
    """
    A class that instantiates movements.
    When a movement is clicked on, the chosen ally instance moves to its coordinate.
    """

    def _configure_widgets(self) -> None:
        """
        Configure widgets.
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

    def _attach_widgets_to_canvas(self) -> None:
        """
        Attach widgets to canvas and append self to 'MovementState.instances'.
        """
        super()._attach_widgets_to_canvas()
        MovementState.instances.append(self)

    def destroy_widgets(self) -> None:
        """
        Remove widgets from canvas then destroy them and remove self from 'MovementState.instances'.
        """
        super().destroy_widgets()
        MovementState.instances.remove(self)

    def handle_click_event(self) -> None:
        """
        Move the chosen ally instance to the coordinate of the clicked movement.
        Unselect the ally instance then clear all highlights.
        """
        SoldierState.chosen_ally.move_to(self.x, self.y)
        SoldierState.chosen_ally.handle_click_event()
