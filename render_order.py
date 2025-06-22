from enum import auto, Enum


class RenderOrder(Enum):
    """Determines the order in which something within a tile is rendered.
    For example, an Actor is rendered instead of an item or corpse if both occupy the same location."""
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
