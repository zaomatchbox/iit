from typing import Any, Iterable, Optional
from uuid import uuid4

from .hier import Hierarchy
from .level import Level


class Dimension:

    def __init__(self,
                 name: str,
                 levels: Optional[Iterable[Level]] = None,
                 hiers: Optional[Iterable[Hierarchy]] = None) -> None:
        self.id = uuid4()
        self.name = name
        self.levels = levels or []
        self.hiers = hiers or []

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Dimension):
            return self.id == other.id
        return False

    def __ne__(self, other: Any) -> bool:
        return NotImplemented
