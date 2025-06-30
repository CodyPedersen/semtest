import numpy as np
import pytest


@pytest.fixture
def expected_embeddings() -> tuple[np.ndarray[np.float64], np.ndarray[np.float64]]:   # type: ignore
    # TODO: Standardize embedding results under one fixture
    return (
        np.array([[0.1, 0.2, 0.3, 0.4, 0.5]]),
        np.array([[0.1, 0.2, 0.3, 0.4, 0.5]]),
    )
