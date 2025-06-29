"""Tools required to build a report from benchmark results"""
import logging
from typing import Sequence
import pandas as pd
import tabulate

from semtest.benchmarking.metrics import BenchmarkMetadata
from .models import BenchmarkReportRow


logger = logging.getLogger("semtest")

def log_exceptions(benchmarks: Sequence[BenchmarkMetadata]) -> None:
    """Log exceptions from benchmarks"""
    logger.info(f"{'='*30} Exceptions {'='*30}\n")
    for benchmark in benchmarks:
        if benchmark.benchmarks.exceptions:
            logger.info(f"{'='*15} Exceptions: {benchmark.func}  {'='*15}\n")
            for e_ in benchmark.benchmarks.exceptions:
                logger.exception(f"{e_!s}")


def log_interim_benchmark(benchmark_md: BenchmarkMetadata) -> None:
    """Log interim benchmark results for realtime monitoring"""
    benchmark_dump = f"Benchmark results: {benchmark_md.model_dump_json(indent=2)}\n"
    logger.info(benchmark_dump)


def log_results_as_table(benchmarks: Sequence[BenchmarkReportRow]) -> None:
    """Log the formatted results table"""
    logger.info(f"{'='*30} Benchmarking Results {'='*30}\n")
    benchmark_dicts = [
        benchmark.model_dump()
        for benchmark in benchmarks
    ]
    report_df = pd.DataFrame(benchmark_dicts)
    print(tabulate.tabulate(report_df, headers='keys', tablefmt='fancy_grid'))
