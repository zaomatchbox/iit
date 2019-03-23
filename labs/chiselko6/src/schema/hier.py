from typing import Any, Iterable
from uuid import uuid4

from .level import Level


class Hierarchy:

    def __init__(self,
                 name: str) -> None:
        self.id = uuid4()
        self.name = name
        self.levels = []
        self.dim = None

    def add_level(self, level: Level) -> 'Hierarchy':
        self.levels.append(level)
        return self

    def add_levels(self, levels: Iterable[Level]) -> 'Hierarchy':
        self.levels.extend(levels)
        return self

    def assign_dim(self, dim: 'Dimension') -> 'Hierarchy':
        self.dim = dim
        return self

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Hierarchy):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return NotImplemented
