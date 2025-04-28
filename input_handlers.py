# pylint: skip-file

from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]):
    """Handles events by converting them to a game Action.
    Note: As of tcod 18.0, EventDispatch is considered deprecated:
    "Event dispatch should be handled via a single custom method in a Protocol instead of this class.
    Note that events can and should be handled using Python's `match` statement."
    """

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        """Called when the termination of the program is requested."""
        return EscapeAction()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """Called when a keyboard key is pressed or repeated."""
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        return action
