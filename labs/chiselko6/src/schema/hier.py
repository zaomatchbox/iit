from typing import Any, Iterable
from uuid import uuid4

from .level import Level


class Hierarchy:

    def __init__(self,
                 name: str,
                 levels: Iterable[Level]) -> None:
        self.id = uuid4()
        self.name = name
        self.levels = levels

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Hierarchy):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return NotImplemented
