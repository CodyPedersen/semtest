"""Tools required to build a report from benchmark results"""
from typing import Sequence

from semtest.benchmarking.metrics import BenchmarkMetadata

from .benchmark_logger import (
    log_exceptions,
    log_results_as_table,
)
from .models import BenchmarkReportRow


class BenchmarkReport:
    """Convert a series of benchmarks into readable output"""
    # TODO: Buld out output option configurations

    # self-use to allow for future variable reporting requirements
    def report(self, benchmarks: Sequence[BenchmarkMetadata]) -> None:
        """Build BenchmarkMetadata objects into a standard report"""
        log_exceptions(benchmarks)

        benchmark_rows = [
            BenchmarkReportRow.from_benchmark(benchmark)
            for benchmark in benchmarks
        ]
        log_results_as_table(benchmark_rows)
