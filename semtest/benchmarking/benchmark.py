"""Core benchmarking functionality"""
import json
import logging
from functools import wraps
from typing import Any, Callable

import numpy as np

from semtest.semantic_comparator import (
    ComparatorBase,
    CosineSimilarity,
)
from semtest.llm_client import EmbeddingClient


class Benchmark:
    """Core class to benchmark a single test"""

    def __init__(
        self,
        func: Callable[..., str],
        semantic_expectation: str,
        iterations: int,
        comparator: ComparatorBase,
        embedding_client: EmbeddingClient = EmbeddingClient(),
    ):
        self.func = func
        self.semantic_expectation = semantic_expectation
        self.iterations = iterations
        self.comparator = comparator
        self.embedding_client = embedding_client
        self.embedding_expectation = self._generate_embedding(semantic_expectation)

        # Benchmark metrics
        self.result_set: list[str] = []
        self.actual_embeddings: list[list[float]] = []
        self.semantic_distances: list[np.float64] = []

    @property
    def semantic_distance_mean(self) -> np.float64:
        """Calculate mean semantic distance from result expectations"""
        return np.mean(self.semantic_distances)

    @property
    def semantic_distance_median(self) -> np.float64:
        """Calculate median semantic distance from result expectation"""
        return np.median(self.semantic_distances)

    def _generate_embedding(self, input_data: str) -> list[float]:
        """Generate the base semantic embedding expectation"""

        return self.embedding_client.generate_embedding_vector(
            input_data
        )

    def _generate_result_embeddings(self) -> None:
        """From a set of LLM responses, generate result embeddings"""

        for result in self.result_set:
            self.actual_embeddings.append(
                self._generate_embedding(result)
            )

    def _calculate_semantic_distances(self) -> None:
        """For each result item, calculate distance"""

        for result_embedding in self.actual_embeddings:
            self.semantic_distances.append(
                self.comparator.calculate_distance(
                    embedding_a=self.embedding_expectation,
                    embedding_b=result_embedding
                )
            )

    def run(self, *args: Any, **kwargs: Any) -> "Benchmark":
        """Execute test and generate similarity metric"""

        info = f"Executing {self.func.__name__}, n={self.iterations} iterations"
        logging.info(info)

        for _ in range(self.iterations):
            # TODO: Implement failure catching for test cases
            res = self.func(*args, **kwargs)
            self.result_set.append(res)

        self._generate_result_embeddings()
        self._calculate_semantic_distances()

        return self

    def benchmarks(self) -> dict[str, Any]:
        """Dump LLM similarity metrics to dictionary"""

        return {
            "func": self.func.__name__,
            "iterations": self.iterations,
            "comparator": str(self.comparator),
            "expectation_str": self.semantic_expectation,
            "benchmarks": {
                "responses": self.result_set,
                "semantic_distances": self.semantic_distances,
                "mean_semantic_distance": self.semantic_distance_mean,
                "median_semantic_distance": self.semantic_distance_median
            }
        }

    def benchmarks_json(self, indent: int = 2) -> str:
        """Dump benchmarks to json format"""

        return json.dumps(self.benchmarks(), indent=indent)


def benchmark(
    semantic_expectation: str,
    iterations: int = 1,
    comparator: ComparatorBase = CosineSimilarity(),
    embedding_client: EmbeddingClient = EmbeddingClient()
) -> Callable[[Callable[..., Any]], Callable[..., Benchmark]]:
    """Generate and execute a benchmark client test"""

    def decorator(func: Callable[..., Any]) -> Callable[..., Benchmark]:

        benchmark_client = Benchmark(
            func=func,
            semantic_expectation=semantic_expectation,
            iterations=iterations,
            comparator=comparator,
            embedding_client=embedding_client
        )

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Benchmark:
            return benchmark_client.run(*args, **kwargs)

        return inner
    return decorator
