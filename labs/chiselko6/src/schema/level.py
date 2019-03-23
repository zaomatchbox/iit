from typing import Any, Dict, Iterable
from uuid import uuid4

from .attr import Attr


class Level:

    def __init__(self,
                 name: str) -> None:
        self.id = uuid4()
        self.name = name
        self.attrs = []
        self.dim = None
        self._attrs_name_map: Dict[str, Attr] = {}

    def add_attr(self, attr: Attr) -> 'Level':
        self.attrs.append(attr)
        attr.assign_level(self)
        self._attrs_name_map[attr.name] = attr
        return self

    def add_attrs(self, attrs: Iterable[Attr]) -> 'Level':
        self.attrs.extend(attrs)
        for attr in attrs:
            self._attrs_name_map[attr.name] = attr
            attr.assign_level(self)
        return self

    def assign_dim(self, dim: 'Dimension') -> 'Level':
        self.dim = dim
        return self

    def get_attr_by_name(self, attr_name: str) -> Attr:
        return self._attrs_name_map[attr_name]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Level):
            return self.name == other.name
        return False

    def __ne__(self, other: Any) -> bool:
        return NotImplemented
