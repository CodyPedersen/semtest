"""Tools required to build a report from benchmark results"""
import logging
from typing import Any
import pandas as pd
import tabulate
from pydantic import Field
from pydantic.dataclasses import dataclass

from semtest.benchmarking.metrics import BenchmarkMetadata

logger = logging.getLogger("semtest")


@dataclass
class BenchmarkReport:
    """Convert a series of benchmarks into readable output"""
    # TODO: Buld out output option configurations

    benchmarks: list[BenchmarkMetadata] = Field(default_factory=list)

    def populate(self, benchmarks: list[BenchmarkMetadata]) -> None:
        """Populate reporter with data"""
        self.benchmarks += benchmarks

    def report(self) -> None:
        """Build BenchmarkMetadata objects into a standard report"""

        report_df = pd.DataFrame(self._build_row_dicts())

        fmt_token = "="
        report_header = f"{fmt_token*30} Benchmarking Results {fmt_token*30}\n"
        logger.info(report_header)

        print(tabulate.tabulate(report_df, headers='keys', tablefmt='fancy_grid'))


    def _build_row_dicts(self) -> list[dict[str, Any]]:
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
