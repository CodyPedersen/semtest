"""Functionality for comparison of embedding vectors"""

from .semantic_comparator import SemanticComparator
from .comparators import ComparatorBase, CosineSimilarity

__all__ = ["ComparatorBase","CosineSimilarity", "SemanticComparator"]
