from components.base_component import BaseComponent


class Fightable(BaseComponent):
    """A Component capable of being fought because it has attributes such as hit points.
    """
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
