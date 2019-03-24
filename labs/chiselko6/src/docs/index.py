from collections import defaultdict
from typing import Dict, Iterable, List, Set

from .models import Document


class Indexer:

    def __init__(self) -> None:
        self._links: List[Document] = []
        self._visited: Set[Document] = set()
        self._doc_index: Dict[str, Document] = {}
        self._last_searched = -1
        self._content_dict: Dict[str, Iterable[Document]] = defaultdict(list)

    def add(self, doc: Document) -> None:
        self._links.append(doc)
        self._doc_index[doc.gate] = doc

    def index(self) -> bool:
        if self._last_searched == len(self._links) - 1:
            return False
        for i in range(self._last_searched + 1, len(self._links)):
            doc = self._links[i]
            if doc not in self._visited:
                self._index(doc)
        self._last_searched = len(self._links) - 1
        return True

    def _index(self, doc: Document) -> None:
        for kw in doc.content.split():
            self._content_dict[kw.lower()].append(doc)
        for kw in doc.name.split():
            self._content_dict[kw.lower()].append(doc)

        self._visited.add(doc)
        for link in doc.links:
            if self._doc_index[link] not in self._visited:
                self._index(self._doc_index[link])

    def search(self, query: str) -> List[Document]:
        result: Set[str] = set()
        for kw in query.split():
            result.update(self._content_dict[kw.lower()])
        return list(result)
