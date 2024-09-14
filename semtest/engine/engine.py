"""Engine specification - see Engine class"""
import logging

from semtest.benchmarking import BenchmarkMetadata
from semtest.reporting import BenchmarkReport
from semtest.loader import Loader
from semtest.parser import SemtestContext

logger = logging.getLogger("semtest")
class Engine:
    """
    Core engine for semtest framework mode. Using a settings
    context object and loader, the engine orchestrates the 
    process of loading tests, executing tests, and building 
    the final output object for the user.
    """

    def __init__(
        self,
        context: SemtestContext,
        loader: Loader,
        reporter: BenchmarkReport
    ) -> None:
        self.context = context
        self.loader = loader
        self.reporter = reporter

    def execute(self) -> list[BenchmarkMetadata]:
        """Load all tests, execute them and provide results"""

        benchmark_fns = self.loader.load()

        results: list[BenchmarkMetadata] = []
        for benchmark_func in benchmark_fns:
            benchmark_metadata = benchmark_func()
            results.append(benchmark_metadata)
            benchmark_dump = f"benchmark_metadata: {benchmark_metadata.model_dump()}\n"
            logger.info(benchmark_dump)

        self.reporter.populate(results)
        self.reporter.report()

        return results
