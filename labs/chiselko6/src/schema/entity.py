from typing import Any, Dict
from uuid import uuid4

from .dim import Dimension
from .level import Level


class Entity:

    def __init__(self,
                 dim: Dimension,
                 level: Level,
                 attrs: Dict[str, Any]) -> None:
        self.id = uuid4()
        self.dim = dim
        self.level = level
        self.attrs = attrs

    def __getitem__(self, key: str) -> Any:
        attr_id = self.level.get_attr_by_name(key)
        return self.attrs[attr_id]

    def __contains__(self, key: str) -> bool:
        attr_id = self.level.get_attr_by_name(key)
        return attr_id in self.attrs
