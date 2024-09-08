"""Semantic comparison functionality"""

from typing import TypeVar

import numpy as np

from .comparators import ComparatorBase

T = TypeVar("T", bound=ComparatorBase)


class SemanticComparator:
    """Core semantic comparison object"""

    def __init__(self, comparator: T):
        self.comparator = comparator

    def similarity(
        self, embedding_a: list[float], embedding_b: list[float]
    ) -> np.float64:
        """Calculate similarity between two embeddings"""

        return self.comparator.calculate_distance(embedding_a, embedding_b)
