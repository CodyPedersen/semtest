import pytest

from semtest.comparator import ComparatorBase
from semtest.embeddings import EmbeddingClientBase

from .fakes import NoOpSemanticComparator, NoOpEmbeddingClient


@pytest.fixture(scope="module")
def mock_semantic_expectation() -> str:
    return "mock llm response"


@pytest.fixture(scope="module")
def no_op_comparator(
    mock_semantic_expectation: str
) -> ComparatorBase:
    return NoOpSemanticComparator(
        semantic_expectation=mock_semantic_expectation
    )


@pytest.fixture(scope="module")
def no_op_embedding_client() -> EmbeddingClientBase:
    return NoOpEmbeddingClient()
