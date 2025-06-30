import numpy as np

from semtest.comparator.semantic_comparator import SemanticComparator, CosineSimilarity
from semtest.embeddings import EmbeddingClientBase


def test_semantic_generate_embeddings(
    mock_semantic_expectation: str,
    no_op_embedding_client: EmbeddingClientBase,
    expected_embeddings: tuple[np.ndarray[np.float64], np.ndarray[np.float64]]  # type: ignore
) -> None:
    semantic_comparator = SemanticComparator(
        semantic_expectation=mock_semantic_expectation,
        embedding_client=no_op_embedding_client
    )
    embeddings = semantic_comparator.generate_embeddings(
        response="mock llm response"
    )

    assert semantic_comparator.baseline == mock_semantic_expectation
    assert (
        embedding in expected_embeddings
        for embedding in embeddings
    )


def test_cosine_similarity(
    mock_semantic_expectation: str,
    no_op_embedding_client: EmbeddingClientBase,
) -> None:
    cosine_similarity_cmp = CosineSimilarity(
        semantic_expectation=mock_semantic_expectation,
        embedding_client=no_op_embedding_client
    )
    cos = cosine_similarity_cmp(response="mock llm response")

    assert np.isclose(cos, 1.0)  # due to nature of the fake, these are identical
