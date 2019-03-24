from typing import Any, Iterable


class Document:

    def __init__(self, name: str, content: str, gate: str,
                 links: Iterable[str]) -> None:
        self._name = name
        self._content = content
        self._links = links
        self._gate = gate

    @property
    def content(self):
        return self._content

    @property
    def name(self):
        return self._name

    @property
    def gate(self):
        return self._gate

    @property
    def links(self):
        return self._links

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Document):
            return self.gate == other.gate
        return False

    def __ne__(self, other: Any) -> bool:
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.gate)
