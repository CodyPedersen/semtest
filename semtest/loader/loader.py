"""Core loader functionality to ingest tests"""
import os
import sys

from typing import Callable
from importlib import import_module
from pathlib import Path

from semtest.benchmarking import BenchmarkMetadata
from semtest.parser import SemtestContext


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
        sys.path.insert(0, str(self.tests_directory))

        modules = []

        for file in self.tests_directory.rglob('*.py'):
            module = import_module(self._get_module_name(file))
            modules.append(module)

        benchmark_functions = []
        for module in modules:
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and hasattr(attr, '_benchmark'):
                    benchmark_functions.append(attr)

        sys.path.pop(0)

        return benchmark_functions

    def _get_module_name(self, filepath: Path) -> str:
        """From a filepath, get module name."""
        relative_path = filepath.relative_to(self.tests_directory)

        return (
            str(relative_path)
            .replace('.py', "")
            .replace(os.sep, '.')
        )
