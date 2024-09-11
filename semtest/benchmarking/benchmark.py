"""Core benchmarking functionality"""
import logging
from functools import cached_property, wraps
from typing import Any, Callable

import numpy as np

from semtest.semantic_comparator import (
    ComparatorBase,
    CosineSimilarity,
)
from semtest.llm_client import EmbeddingClient

from .metrics import BenchmarkMetadata, SemanticMetrics


class BenchmarkRunner:
    """
    Core class to execute a benchmarking run and track results.
    """

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

        self.embedding_expectation = (
            self.embedding_client.generate_embedding_vector(
                semantic_expectation
            )
        )

        self.result_set: list[str] = []
        self.result_embeddings: list[list[float]] = []

    def run(self, *args: Any, **kwargs: Any) -> "BenchmarkRunner":
        """Execute benchmark and generate response embeddings"""
        info = f"Executing {self.func.__name__}, n={self.iterations} iterations"
        logging.info(info)

        for _ in range(self.iterations):
            # TODO: Implement failure catching for test cases
            res = self.func(*args, **kwargs)
            self.result_set.append(res)

        self._generate_result_embeddings()

        return self

    @cached_property
    def metrics(self) -> BenchmarkMetadata:
        """Dump LLM similarity metrics as object"""

        return BenchmarkMetadata(
           func=self.func.__name__,
           iterations=self.iterations,
           comparator=str(self.comparator),
           expectation_input=self.semantic_expectation,
           benchmarks=SemanticMetrics(
               responses=self.result_set,
               semantic_distances=self._calculate_semantic_distances()
           )
        )

    @property
    def metrics_dict(self) -> dict[str, Any]:
        """Dump LLM similarity metrics to dictionary"""
        return self.metrics.model_dump()

    @property
    def metrics_json(self) -> str:
        """Dump LLM similarity benchmarks to json format"""
        return self.metrics.model_dump_json(indent=2)

    def _generate_result_embeddings(self) -> list[list[float]]:
        """From a set of LLM responses, generate result embeddings"""
        self.result_embeddings = [
            self.embedding_client.generate_embedding_vector(
                result
            )
            for result in self.result_set
        ]
        return self.result_embeddings

    def _calculate_semantic_distances(self) -> list[np.float64]:
        """For each result item, calculate distance"""
        return [
            self.comparator.calculate_distance(
                embedding_a=self.embedding_expectation,
                embedding_b=result_embedding
            )
            for result_embedding in self.result_embeddings
        ]


def benchmark(
    semantic_expectation: str,
    iterations: int = 1,
    comparator: ComparatorBase = CosineSimilarity(),
    embedding_client: EmbeddingClient = EmbeddingClient()
) -> Callable[[Callable[..., Any]], Callable[..., BenchmarkRunner]]:
    """Generate and execute a benchmark client test"""

    def decorator(func: Callable[..., Any]) -> Callable[..., BenchmarkRunner]:
        benchmark_runner = BenchmarkRunner(
            func=func,
            semantic_expectation=semantic_expectation,
            iterations=iterations,
            comparator=comparator,
            embedding_client=embedding_client
        )

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> BenchmarkRunner:
            return benchmark_runner.run(*args, **kwargs)

        return inner
    return decorator
