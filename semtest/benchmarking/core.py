from collections.abc import Callable
from typing import Any, Protocol, runtime_checkable

from semtest.comparator import ComparatorBase
from .metrics import BenchmarkMetadata


@runtime_checkable
class BenchmarkRunnerBase(Protocol):
    """
    Protocol to execute a benchmarking run and track results.
    """
    def __init__(  # TODO: refactor to remove init requirements
        self,
        func: Callable[..., Any],
        iterations: int,
        comparator: ComparatorBase
    ) -> None:
        """Initialize the benchmark runner"""

    def run(self, *args: Any, **kwargs: Any) -> BenchmarkMetadata:
        """Execute benchmark and generate response embeddings"""
