"""Core benchmarking functionality"""
# pylint: disable=broad-exception-caught
import logging
from functools import wraps
from typing import Any, Callable
from dataclasses import dataclass

from semtest.comparator import (
    ComparatorBase,
)
from .metrics import BenchmarkMetadata, SemanticMetrics

logger = logging.getLogger("semtest")


@dataclass
class BenchmarkRunner:
    """
    Core class to execute a benchmarking run and track results.
    """
    func: Callable[..., str]
    iterations: int
    comparator: ComparatorBase

    def run(self, *args: Any, **kwargs: Any) -> BenchmarkMetadata:
        """Execute benchmark and generate response embeddings"""
        fmt_token = '='
        info = (
            f"{fmt_token*35} "
            f"{self.func.__name__} (n={self.iterations} iterations) "
            f"{fmt_token*35}\n"
        )
        logger.info(info)

        results, exceptions = [], []
        for _ in range(self.iterations):
            try:
                res = self.func(*args, **kwargs)
                results.append(res)
            except Exception as e:
                logger.info("Exception captured\n")
                exception_msg = f"{e!r}\n"
                logger.exception(exception_msg)
                logger.info("\n")
                exceptions.append(e)

        return self.build_metrics(results, exceptions)

    def build_metrics(
        self,
        results: list[str],
        exceptions: list[Exception]
    ) -> BenchmarkMetadata:
        """Generate core benchmarking metrics"""
        expectation_input = getattr(
            self.comparator, "semantic_expectation", None
        )
        # To implement expectation schema

        return BenchmarkMetadata(
           func=self.func.__name__,
           iterations=self.iterations,
           comparator=str(self.comparator),
           expectation=expectation_input,
           benchmarks=SemanticMetrics(
                responses=results,
                exceptions=exceptions,
                semantic_distances=[
                    self.comparator(res) for res in results  # TODO: Move away from lazy evaluation
                ]
           )
        )


def benchmark(
    comparator: ComparatorBase,
    iterations: int = 1,
) -> Callable[[Callable[..., Any]], Callable[..., BenchmarkMetadata]]:
    """Generate and execute a benchmark client test"""

    def decorator(func: Callable[..., Any]) -> Callable[..., BenchmarkMetadata]:
        benchmark_runner = BenchmarkRunner(
            func=func,
            iterations=iterations,
            comparator=comparator,
        )

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> BenchmarkMetadata:
            return benchmark_runner.run(*args, **kwargs)

        setattr(inner, "_benchmark", True)  # Mark function as a benchmark

        return inner
    return decorator
