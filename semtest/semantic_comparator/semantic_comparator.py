"""Semantic comparison functionality"""

from typing import TypeVar

from .comparators import ComparatorBase

T = TypeVar("T", bound=ComparatorBase)


class SemanticComparator:
    """Core semantic comparison object"""

    def __init__(self, comparator: T):
        self.comparator = comparator

    def similarity(
        self, embedding_a: list[float], embedding_b: list[float]
    ) -> float:
        """Calculate similarity between two embeddings"""

        return self.comparator.calculate_distance(embedding_a, embedding_b)
