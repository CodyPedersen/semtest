"""Functionality for comparison of embedding vectors"""

from .core import ComparatorBase
from .semantic_comparator import CosineSimilarity

__all__ = ["ComparatorBase","CosineSimilarity"]
