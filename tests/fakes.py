from dataclasses import dataclass

import numpy as np


@dataclass
class NoOpSemanticComparator:
    semantic_expectation: str

    def __call__(self, response: str) -> np.float64:
        _ = response
        return np.float64(69.33)

    @property
    def baseline(self) -> str:
        return self.semantic_expectation

    def __str__(self) -> str:
        return "no_op_semantic_comparator"


class NoOpEmbeddingClient:
    def generate_embedding_vector(
        self, input_text: str, model: str | None = None
    ) -> list[float]:
        _, _ = input_text, model
        return [.1, .2, .3, .4, .5]
