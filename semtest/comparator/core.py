"""
Core comparator interfaces

TODO: Implementation of following comparators:
- Schema comparison
- Data / Ground truth comparison (k/v structured)
"""
from typing import Protocol, runtime_checkable
import numpy as np

@runtime_checkable
class ComparatorBase(Protocol):
    """Base comparator interface"""
    def __call__(self, response: str) -> np.float64: ...
