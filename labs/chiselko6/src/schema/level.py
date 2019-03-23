from typing import Any, Dict, Iterable, Optional
from uuid import uuid4

from .attr import Attr


class Level:

    def __init__(self,
                 name: str,
                 attrs: Optional[Iterable[Attr]] = None) -> None:
        self.id = uuid4()
        self.name = name
        self.attrs = attrs or []
        self._attrs_name_map: Dict[str, Attr] = {
            v.name: v for v in attrs
        }

    def get_attr_by_name(self, attr_name: str) -> Attr:
        return self._attrs_name_map[attr_name]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Level):
            return self.name == other.name
        return False

    def __ne__(self, other: Any) -> bool:
        return NotImplemented
