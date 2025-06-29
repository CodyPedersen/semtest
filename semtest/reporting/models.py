"""Benchmark report metrics"""
from typing import Self
import numpy as np
from pydantic import BaseModel, ConfigDict

from semtest.benchmarking.metrics import BenchmarkMetadata


class BenchmarkReportRow(BaseModel):
    """Pydantic model for benchmark row data used in reporting"""
    benchmark: str
    iterations: int
    comparator: str
    mean_semantic_distance: np.float64
    median_semantic_distance: np.float64
    exceptions: list[str]
    exception_ct: int

    model_config = ConfigDict(arbitrary_types_allowed=True)  # numpy exception

    @classmethod
    def from_benchmark(cls, benchmark: BenchmarkMetadata) -> Self:
        """Create BenchmarkRowData from BenchmarkMetadata"""
        unique_exception_names = list({
            type(exc).__name__
            for exc in benchmark.benchmarks.exceptions
        })

        return cls(
            benchmark=benchmark.func,
            iterations=benchmark.iterations,
            comparator=benchmark.comparator,
            mean_semantic_distance=benchmark.benchmarks.mean_semantic_distance,
            median_semantic_distance=benchmark.benchmarks.median_semantic_distance,
            exceptions=unique_exception_names,
            exception_ct=len(benchmark.benchmarks.exceptions)
        )
