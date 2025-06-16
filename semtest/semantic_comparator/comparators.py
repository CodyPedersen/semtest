"""Embedding vector comparison algorithms"""
# pylint: disable=unnecessary-ellipsis
from typing import Protocol

import numpy as np

from sklearn.metrics.pairwise import cosine_similarity


"""
TODO: Decouple comparator from embedding implementation.
Generic comparator should support
- Schema comparison
- Data / Ground truth comparison (k/v structured)
- User-defined comparators (Callables), provided they follow the comparator protocol

Built-ins: Embedding Comparator/Cosine, Schema Comparator, Ground Truth comparator
"""

class ComparatorBase(Protocol):
    """Base comparator interface"""

    def calculate_distance(
        self, embedding_a: list[float], embedding_b: list[float]
    ) -> np.float64:
        """Abstract method for embedding vector distance calculation"""
        ...

    def __str__(self) -> str:
        """Return string representation of transform type"""
        ...


class CosineSimilarity:
    """Calculates cosine similarity between two vectors"""

    def calculate_distance(
        self, embedding_a: list[float], embedding_b: list[float]
    ) -> np.float64:
        """Calculate distance between two embedding vectors with cosine similarity"""

        embedding_a_matrix = np.array(embedding_a).reshape(1, -1)
        embedding_b_matrix = np.array(embedding_b).reshape(1, -1)
        similarity = cosine_similarity(embedding_a_matrix, embedding_b_matrix)
        similarity_metric = similarity.mean()

        if not isinstance(similarity_metric, np.floating):
            exc = f"Failed to generate a consistent similarity metric from {similarity_metric}"
            raise TypeError(exc)

        return similarity_metric

    def __str__(self) -> str:
        return "cosine_similarity"
