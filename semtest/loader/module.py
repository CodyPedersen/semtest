"""File & module interaction utilities"""
import os
import sys
from contextlib import contextmanager
from importlib import import_module
from pathlib import Path
from typing import Iterator
from types import ModuleType


@contextmanager
def inject_test_path(tests_directory: Path) -> Iterator[None]:
    """Inject test path into sys"""
    sys.path.insert(0, str(tests_directory))
    yield
    sys.path.pop(0)


def fetch_py_modules(directory: Path) -> list[ModuleType]:
    """Fetch python modules for a given directory"""
    with inject_test_path(directory):
        return [
            import_module(get_module_name(file, directory))
            for file in directory.rglob("*.py")
        ]


def get_module_name(filepath: Path, directory: Path) -> str:
    """From a filepath, get module name."""
    relative_path = filepath.relative_to(directory)

    return (
        str(relative_path)
        .replace('.py', "")
        .replace(os.sep, '.')
    )
