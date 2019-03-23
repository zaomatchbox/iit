from typing import Any, Iterable

from .base import BaseSchemaModel
from .hier import Hierarchy
from .level import Level


class Dimension(BaseSchemaModel):

    def __init__(self,
                 name: str,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = name
        self.levels = []
        self.hiers = []

    def add_levels(self, levels: Iterable[Level]) -> 'Dimension':
        self.levels.extend(levels)
        for level in levels:
            level.assign_dim(self)
        return self

    def add_level(self, level: Level) -> 'Dimension':
        self.levels.append(level)
        level.assign_dim(self)
        return self

    def add_hiers(self, hiers: Iterable[Hierarchy]) -> 'Dimension':
        self.hiers.extend(hiers)
        for hier in hiers:
            hier.assign_dim(self)
        return self

    def add_hier(self, hier: Hierarchy) -> 'Dimension':
        self.hiers.append(hier)
        hier.assign_dim(self)
        return self

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Dimension):
            return self.id == other.id
        return False

    def __ne__(self, other: Any) -> bool:
        return NotImplemented
