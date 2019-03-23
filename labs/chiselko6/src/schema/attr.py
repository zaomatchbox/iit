from typing import Any
from uuid import uuid4


class Attr:

    def __init__(self,
                 name: str,
                 type: str) -> None:
        self.id = uuid4()
        self.name = name
        self.type = type
        self.level = None

    def assign_level(self, level: 'Level') -> 'Attr':
        self.level = level
        return self

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Attr):
            return self.id == other.id
        return False

    def __ne__(self, other: Any) -> bool:
        return NotImplemented
