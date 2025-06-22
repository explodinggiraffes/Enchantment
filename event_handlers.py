# pylint: skip-file

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, BumpAction, GameExitAction, WaitAction

if TYPE_CHECKING:
    from engine import Engine

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    tcod.event.KeySym.HOME: (-1, -1),
    tcod.event.KeySym.END: (-1, 1),
    tcod.event.KeySym.PAGEUP: (1, -1),
    tcod.event.KeySym.PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_3: (1, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_9: (1, -1),
    # Vi keys.
    tcod.event.KeySym.h: (-1, 0),
    tcod.event.KeySym.j: (0, 1),
    tcod.event.KeySym.k: (0, -1),
    tcod.event.KeySym.l: (1, 0),
    tcod.event.KeySym.y: (-1, -1),
    tcod.event.KeySym.u: (1, -1),
    tcod.event.KeySym.b: (-1, 1),
    tcod.event.KeySym.n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}


# Note: As of tcod 18.0, EventDispatch is considered deprecated:
# "Event dispatch should be handled via a single custom method in a Protocol instead of this class.
# Note that events can and should be handled using Python's `match` statement."

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        """Called when the termination of the program is requested."""
        return GameExitAction()


class MainGameEventHandler(EventHandler):
    """Handles events by converting them to a game Action."""
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()  # Update the FOV before the players next action.

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """Called when a keyboard key is pressed or repeated."""
        action: Optional[Action] = None

        key = event.sym
        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(self.engine.player, dx, dy)
        elif key in WAIT_KEYS:
            action = WaitAction(self.engine.player)
        elif key == tcod.event.KeySym.ESCAPE:
            action = GameExitAction(self.engine.player)

        return action

class GameOverEventHandler(EventHandler):
    """Handles the event generated when the game ends, such as when the player dies."""
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """Called when a keyboard key is pressed or repeated."""
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_ESCAPE:
            action = GameExitAction(self.engine.player)

        return action
