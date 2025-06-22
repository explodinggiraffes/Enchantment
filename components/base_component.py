from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities import Entity


class BaseComponent:
    """A component that wraps its Entity."""
    entity: Entity

    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine
