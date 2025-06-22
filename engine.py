from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

from event_handlers import MainGameEventHandler
from procgen import generate_dungeon

if TYPE_CHECKING:
    from entities import Actor
    from event_handlers import EventHandler
    from game_map import GameMap

MAP_WIDTH = 80
MAP_HEIGHT = 45

ROOM_SIZE_MAX = 10
ROOM_SIZE_MIN = 6
ROOMS_MAX = 30

MONSTERS_PER_ROOM_MAX = 2


class Engine:
    """Handles:
    - Creating and rendering the game map.
    - AI for all Actors controlled by the game.
    """
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player
        self.game_map = generate_dungeon(
            max_rooms=ROOMS_MAX,
            room_min_size=ROOM_SIZE_MIN,
            room_max_size=ROOM_SIZE_MAX,
            map_width=MAP_WIDTH,
            map_height=MAP_HEIGHT,
            monsters_per_room=MONSTERS_PER_ROOM_MAX,
            engine=self
        )

    def handle_enemy_turns(self) -> None:
        """Handle AI for all Actors controlled by the game."""
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )

        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        """Render the game map and HUD."""
        self.game_map.render(console)

        console.print(
            x=1,
            y=47,
            string=f"HP: {self.player.fighter.hp}/{self.player.fighter.max_hp}",
        )

        context.present(console)
        console.clear()
