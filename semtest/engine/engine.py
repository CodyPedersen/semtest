"""Engine specification - see Engine class"""
from dataclasses import dataclass

from semtest.benchmarking import BenchmarkMetadata
from semtest.reporting import BenchmarkReport, log_interim_benchmark
from semtest.loader import Loader
from semtest.parser import SemtestContext


@dataclass
class Engine:
    """
    Core engine for semtest framework mode. Using a settings
    context object and loader, the engine orchestrates the 
    process of loading tests, executing tests, and building 
    the final output object for the user.
    """

    context: SemtestContext
    loader: Loader
    reporter: BenchmarkReport

    def execute(self) -> list[BenchmarkMetadata]:
        """Load all tests, execute them and provide results"""
        benchmark_funcs = self.loader.load()

        benchmarks = []
        for benchmark_func in benchmark_funcs:
            benchmark = benchmark_func()
            log_interim_benchmark(benchmark)
            benchmarks.append(benchmark)

        self.reporter.report(benchmarks)

        return benchmarks
