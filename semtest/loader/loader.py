"""Core loader functionality to ingest tests"""
from typing import Any, Callable
from pathlib import Path

from semtest.benchmarking import BenchmarkMetadata
from semtest.parser import SemtestContext

from .module import fetch_py_modules

class Loader:
    """Core loader class to ingest benchmarking modules (TLMs)"""

    def __init__(self, context: SemtestContext) -> None:
        self.tests_directory: Path = context.directory.resolve()

    def load(self) -> list[Callable[..., BenchmarkMetadata]]:
        """
        Recursively load all benchmark functions from specified directory. Imports
        all python files as a top-level module, and has some stipulations:
            1. No relative imports
            2. Files/modules must be uniquely named
        """
        modules = fetch_py_modules(self.tests_directory)

        benchmark_functions = []
        for module in modules:
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if self.is_benchmark(attr):
                    benchmark_functions.append(attr)

        return benchmark_functions

    @staticmethod
    def is_benchmark(attr: Any) -> bool:
        """Validation of benchmark attr signature"""
        return (callable(attr) and hasattr(attr, '_benchmark'))
