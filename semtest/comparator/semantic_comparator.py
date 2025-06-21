"""Embedding vector comparison algorithms"""
# pylint: disable=unnecessary-ellipsis
from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from semtest.embeddings.core import EmbeddingClientBase
from semtest.embeddings import OpenAIEmbeddingClient


@dataclass
class SemanticComparator(ABC):
    """Base class for semantic comparators"""
    semantic_expectation: str
    embedding_client: EmbeddingClientBase = field(default_factory=OpenAIEmbeddingClient)

    def generate_embeddings(
        self,
        response: str
    ) -> tuple[np.ndarray[np.float64], np.ndarray[np.float64]]:  # type: ignore
        """Generate embeddings between base semantic reference and response"""
        embedding_a = self.embedding_client.generate_embedding_vector(self.semantic_expectation)
        embedding_b = self.embedding_client.generate_embedding_vector(response)
        return np.array(embedding_a).reshape(1, -1), np.array(embedding_b).reshape(1, -1)


@dataclass
class GenericSemanticComparator(SemanticComparator):
    """Generic semantic comparator - accepts callable with 2 embedding vectors"""
    comparator: Callable[..., np.float64] | None = None

    def __call__(self, response: str) -> np.float64:
        if not self.comparator: # fix me
            raise ValueError("Please supply a comparator")

        embedding_a_matrix, embedding_b_matrix = self.generate_embeddings(response)
        similarity = self.comparator(embedding_a_matrix, embedding_b_matrix)

        if not similarity:
            raise ValueError("Unable to generate mean similarity")
        return similarity


@dataclass
class CosineSimilarity(SemanticComparator):
    """Calculates cosine similarity between two vectors"""

    def __call__(self, response: str) -> np.float64:
        """Calculate distance between two embedding vectors with cosine similarity"""
        embedding_a_matrix, embedding_b_matrix = self.generate_embeddings(response)
        similarity = cosine_similarity(embedding_a_matrix, embedding_b_matrix)
        similarity_metric = similarity.mean()

        if not isinstance(similarity_metric, np.floating):
            exc = f"Failed to generate a consistent similarity metric from {similarity_metric}"
            raise TypeError(exc)

        return similarity_metric

    def __str__(self) -> str:
        return "cosine_similarity"
