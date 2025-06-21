"""Core comparator interfaces"""
from typing import Protocol, runtime_checkable
import numpy as np

@runtime_checkable
class ComparatorBase(Protocol):
    """Base comparator interface"""
    def __call__(self, response: str) -> np.float64: ...
