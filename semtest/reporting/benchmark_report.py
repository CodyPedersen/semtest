"""Tools required to build a report from benchmark results"""
from typing import Any, Optional
import pandas as pd
import tabulate

from semtest.benchmarking.metrics import BenchmarkMetadata


class BenchmarkReport:
    """Convert a series of benchmarks into readable output"""
    # TODO: Buld out output option configurations

    def __init__(
        self,
        benchmarks: Optional[list[BenchmarkMetadata]] = None
    ) -> None:
        self.benchmarks: list[BenchmarkMetadata] = benchmarks or []

    def populate(self, benchmarks: list[BenchmarkMetadata]) -> None:
        """Populate reporter with data"""
        self.benchmarks += benchmarks

    def report(self) -> None:
        """Build BenchmarkMetadata objects into a standard report"""

        report_df = pd.DataFrame(self._build_row_dicts())
        print(tabulate.tabulate(report_df, headers='keys', tablefmt='fancy_grid'))


    def _build_row_dicts(self) -> list[dict[str,Any]]:
        """Generate row dicts from benchmark metadata"""
        row_dicts = []

        for benchmark in self.benchmarks:
            row_dicts.append({  # TODO: define pydantic schema and adapter
                "benchmark": benchmark.func,
                "iterations": benchmark.iterations,
                "comparator": benchmark.comparator,
                "mean_semantic_distance": benchmark.benchmarks.mean_semantic_distance,
                "median_semantic_distance": benchmark.benchmarks.median_semantic_distance,
                "exceptions": list({type(exc).__name__ for exc in benchmark.benchmarks.exceptions}),
                "exception_ct": len(benchmark.benchmarks.exceptions)
            })
        return row_dicts
