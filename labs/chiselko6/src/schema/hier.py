from typing import Any, Iterable

from .base import BaseSchemaModel
from .level import Level


class Hierarchy(BaseSchemaModel):

    def __init__(self,
                 name: str,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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
