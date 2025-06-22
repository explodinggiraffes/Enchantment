from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from event_handlers import GameOverEventHandler
from render_order import RenderOrder

if TYPE_CHECKING:
    from entities import Actor


# Note: The tcod tutorial has named this class "Fighter". But we want to reserve that name for Dungeons & Dragons style
# character classes.
class CombatComponent(BaseComponent):
    entity: Actor

    """A Component capable of being fought because it has attributes such as hit points."""
    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense  # TODO: Is this basicaly armor class? defense is how much taken damage will be reduced
        self.power = power      # TODO: Is this basically level? power is the entity’s raw attack power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.entity.ai:
            self.die()

    def die(self) -> None:
        if self.engine.player is self.entity:
            death_message = "You died!"
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"{self.entity.name} is dead!"

        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"remains of {self.entity.name}"
        self.entity.render_order = RenderOrder.CORPSE

        print(death_message)
