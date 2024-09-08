"""Functionality for comparison of embedding vectors"""

from .semantic_comparator import SemanticComparator
from .comparators import CosineSimilarity

__all__ = ["CosineSimilarity", "SemanticComparator"]
