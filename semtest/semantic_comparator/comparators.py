"""Embedding vector comparison algorithms"""
from abc import ABC, abstractmethod

import numpy as np

from sklearn.metrics.pairwise import cosine_similarity


class ComparatorBase(ABC):
    """Base comparator interface"""

    @abstractmethod
    def calculate_distance(
        self, embedding_a: list[float], embedding_b: list[float]
    ) -> np.float64:
        """Abstract method for embedding vector distance calculation"""
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        """Return string representation of transform type"""
        raise NotImplementedError


class CosineSimilarity(ComparatorBase):
    """Calculates cosine similarity between two vectors"""

    def calculate_distance(
        self, embedding_a: list[float], embedding_b: list[float]
    ) -> np.float64:
        """Calculate distance between two embedding vectors with cosine similarity"""

        embedding_a_matrix = np.array(embedding_a).reshape(1, -1)
        embedding_b_matrix = np.array(embedding_b).reshape(1, -1)
        similarity = cosine_similarity(embedding_a_matrix, embedding_b_matrix)
        similarity_metric = similarity.mean()

        if not isinstance(similarity_metric, np.float64):
            exc = f"Failed to generate a consistent similarity metric from {similarity_metric}"
            raise TypeError(exc)

        return similarity_metric

    def __str__(self) -> str:
        """Return cosine similarity type"""
        return "cosine_similarity"
