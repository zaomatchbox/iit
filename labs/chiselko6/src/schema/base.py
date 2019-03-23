from typing import Optional
from uuid import uuid4


class BaseSchemaModel:

    def __init__(self, info: Optional[str] = None, *args, **kwargs) -> None:
        self.id = uuid4()
        self._info = info or ''

    @property
    def info(self) -> str:
        return self._info

    @info.setter
    def info(self, info: str) -> None:
        self._info = info
