#!/usr/bin/env python3

import copy

import tcod

import entity_factories
from engine import Engine
from procgen import generate_dungeon

WINDOW_WIDTH = 80
WINDOW_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 45

ROOM_SIZE_MAX = 10
ROOM_SIZE_MIN = 6
ROOMS_MAX = 30

MONSTERS_PER_ROOM_MAX=2


def main() -> None:
    # Load the font, a 32 by 8 tile font with libtcod's old character layout.
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # Create the main console.
    console = tcod.console.Console(WINDOW_WIDTH, WINDOW_HEIGHT, order="F")

    # Create the player.
    # Note: We can’t use player.spawn here, because spawn requires the GameMap, which isn’t created until after we
    # create the player. <-FIXME?
    player = copy.deepcopy(entity_factories.player)

    # TODO: Comment + create player outside of main() if possible.
    engine = Engine(player=player)

    # TODO
    engine.game_map = generate_dungeon(
        max_rooms=ROOMS_MAX,
        room_min_size=ROOM_SIZE_MIN,
        room_max_size=ROOM_SIZE_MAX,
        map_width=MAP_WIDTH,
        map_height=MAP_HEIGHT,
        monsters_per_room=MONSTERS_PER_ROOM_MAX,
        engine=engine
    )
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
