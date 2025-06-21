"""Core embedding client interfaces"""
from typing import Protocol, runtime_checkable

@runtime_checkable
class EmbeddingClientBase(Protocol):
    """Base protocol for all compatible embedding clients"""
    def generate_embedding_vector(
        self, input_text: str, model: str | None = None
    ) -> list[float]:
        """Required method for generation of embedding vectors against ref."""
