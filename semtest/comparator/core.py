"""
Core comparator interfaces

TODO: Implementation of following comparators:
- Schema Comparators 
- Data / Ground truth Comparators (k/v structured)
- Comparators should own the structure of their resulting metrics & aggregation
"""
from typing import Protocol, runtime_checkable
import numpy as np

@runtime_checkable
class ComparatorBase(Protocol):
    """Base comparator interface"""
    def __call__(self, response: str) -> np.float64: ...

    @property
    def baseline(self) -> str:
        """Response expectations for reporting"""
