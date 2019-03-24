from collections import defaultdict
from typing import Dict, Iterable, List, Set, Tuple

from .constants import MAX_DISTANCE
from .models import Document


class Indexer:

    def __init__(self) -> None:
        self._docs: List[Document] = []
        self._visited: Set[Document] = set()
        self._doc_index: Dict[str, Document] = {}
        self._last_searched = -1
        self._content_dict: Dict[str, Iterable[Document]] = defaultdict(list)
        self._distances: Dict[Tuple[Document, Document],
                              int] = defaultdict(lambda: MAX_DISTANCE)

    def add(self, doc: Document) -> None:
        self._docs.append(doc)
        self._doc_index[doc.gate] = doc

    def index(self) -> bool:
        if self._last_searched == len(self._docs) - 1:
            return False
        for i in range(self._last_searched + 1, len(self._docs)):
            doc = self._docs[i]
            if doc not in self._visited:
                self._index(doc)
        self._last_searched = len(self._docs) - 1
        self._recalc_distances()
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

    def _recalc_distances(self) -> None:
        self._distances = defaultdict(lambda: MAX_DISTANCE)
        doc_count = len(self._docs)
        for doc in self._docs:
            self._distances[(doc, doc)] = 0
            for link in doc.links:
                linked_doc = self._doc_index[link]
                self._distances[(doc, linked_doc)] = 1
        for k in range(doc_count):
            mid_doc = self._docs[k]
            for i in range(doc_count):
                from_doc = self._docs[i]
                for j in range(doc_count):
                    to_doc = self._docs[j]
                    self._distances[(from_doc, to_doc)] = min(
                            self._distances[(from_doc, mid_doc)]
                            + self._distances[(mid_doc, to_doc)],
                            self._distances[(from_doc, to_doc)]
                            )

    def get_distance(self, src_link: str, dest_link: str) -> int:
        src_doc = self._doc_index[src_link]
        dest_doc = self._doc_index[dest_link]
        return self._distances[(src_doc, dest_doc)]
