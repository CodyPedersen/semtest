"""Core benchmarking functionality"""
# pylint: disable=broad-exception-caught
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

logger = logging.getLogger("semtest")


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
        self.exceptions: list[Exception] = []

    def run(self, *args: Any, **kwargs: Any) -> BenchmarkMetadata:
        """Execute benchmark and generate response embeddings"""
        fmt_token = '='
        info = (
            f"{fmt_token*35} "
            f"{self.func.__name__} (n={self.iterations} iterations) "
            f"{fmt_token*35}\n"
        )
        logger.info(info)

        for _ in range(self.iterations):
            try:
                res = self.func(*args, **kwargs)
                self.result_set.append(res)
            except Exception as e:
                logger.info("Exception captured\n")
                exception_msg = f"{e!r}\n"
                logger.exception(exception_msg)
                logger.info("\n")
                self.exceptions.append(e)

        self._generate_result_embeddings()

        return self.metrics

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
               exceptions=self.exceptions,
               result_embeddings=self.result_embeddings,
               semantic_distances=self._calculate_semantic_distances()
           )
        )

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
) -> Callable[[Callable[..., Any]], Callable[..., BenchmarkMetadata]]:
    """Generate and execute a benchmark client test"""

    def decorator(func: Callable[..., Any]) -> Callable[..., BenchmarkMetadata]:
        benchmark_runner = BenchmarkRunner(
            func=func,
            semantic_expectation=semantic_expectation,
            iterations=iterations,
            comparator=comparator,
            embedding_client=embedding_client
        )

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> BenchmarkMetadata:
            return benchmark_runner.run(*args, **kwargs)

        setattr(inner, "_benchmark", True)  # Mark function as a benchmark

        return inner
    return decorator
