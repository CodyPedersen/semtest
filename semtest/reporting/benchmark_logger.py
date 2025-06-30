"""Tools required to build a report from benchmark results"""
import logging
from collections.abc import Callable
from typing import Any, Sequence
import pandas as pd
import tabulate

from semtest.benchmarking.metrics import BenchmarkMetadata
from .models import BenchmarkReportRow


logger = logging.getLogger("semtest")

FMT_TOKEN = "="

def log_exceptions(benchmarks: Sequence[BenchmarkMetadata]) -> None:
    """Log exceptions from benchmarks"""
    logger.info(f"{FMT_TOKEN*30} Exceptions {FMT_TOKEN*30}\n")
    for benchmark in benchmarks:
        if benchmark.benchmarks.exceptions:
            logger.info(f"{FMT_TOKEN*15} Exceptions: {benchmark.func}  {FMT_TOKEN*15}\n")
            for e_ in benchmark.benchmarks.exceptions:
                logger.exception(f"{e_!s}")


def log_benchmark_init(func: Callable[..., Any], iterations: int) -> None:
    """Default benchmark init logging"""
    info = (
        f"{FMT_TOKEN*35} "
        f"{func.__name__} (n={iterations} iterations) "
        f"{FMT_TOKEN*35}\n"
    )
    logger.info(info)


def log_interim_benchmark(benchmark_md: BenchmarkMetadata) -> None:
    """Log interim benchmark results for realtime monitoring"""
    benchmark_dump = f"Benchmark results: {benchmark_md.model_dump_json(indent=2)}\n"
    logger.info(benchmark_dump)


def log_results_as_table(benchmarks: Sequence[BenchmarkReportRow]) -> None:
    """Log the formatted results table"""
    logger.info(f"{FMT_TOKEN*30} Benchmarking Results {FMT_TOKEN*30}\n")
    benchmark_dicts = [
        benchmark.model_dump()
        for benchmark in benchmarks
    ]
    report_df = pd.DataFrame(benchmark_dicts)
    print(tabulate.tabulate(report_df, headers='keys', tablefmt='fancy_grid'))
