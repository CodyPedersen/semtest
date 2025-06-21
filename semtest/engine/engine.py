"""Engine specification - see Engine class"""
import logging
from dataclasses import dataclass

from semtest.benchmarking import BenchmarkMetadata
from semtest.reporting import BenchmarkReport
from semtest.loader import Loader
from semtest.parser import SemtestContext

logger = logging.getLogger("semtest")

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
        begin_load_log = "\nLoading semtest benchmarks...\n"
        logger.info(begin_load_log)

        benchmark_fns = self.loader.load()

        begin_benchmark_log = "Initializing semtest benchmarks...\n"
        logger.info(begin_benchmark_log)

        results: list[BenchmarkMetadata] = []
        for benchmark_func in benchmark_fns:
            benchmark_metadata = benchmark_func()
            results.append(benchmark_metadata)
            benchmark_dump = f"benchmark results: {benchmark_metadata.model_dump_json(indent=2)}\n"
            logger.info(benchmark_dump)

        self.reporter.populate(results)
        self.reporter.report()

        return results
