from typing import Any

from .base import BaseSchemaModel


class Attr(BaseSchemaModel):

    def __init__(self,
                 name: str,
                 type: str,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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
