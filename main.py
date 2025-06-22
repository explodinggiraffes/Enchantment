#!/usr/bin/env python3

import tcod

from entity_factories import create_player
from engine import Engine

WINDOW_WIDTH = 80
WINDOW_HEIGHT = 50


def main() -> None:
    # Load the font, a 32 by 8 tile font with libtcod's old character layout.
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # Create the main console.
    console = tcod.console.Console(WINDOW_WIDTH, WINDOW_HEIGHT, order="F")

    # Create the player.
    player = create_player()

    # Create the game engine.
    engine = Engine(player=player)
    engine.update_fov()

    # Create a window based on this console and tileset.
    # Then start the event loop, which runs until SystemExit is raised.
    with tcod.context.new(
        columns=console.width, rows=console.height, tileset=tileset, title="Enchantment", vsync=True
    ) as context:
        while True:
            engine.render(console=console, context=context)

            # For a non-blocking event loop replace `tcod.event.wait` with `tcod.event.get`.
            #events = tcod.event.wait()

            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()
