"""LLM client module"""

from .core import EmbeddingClientBase
from .openai_embeddings import OpenAIEmbeddingClient

__all__ = ["EmbeddingClientBase", "OpenAIEmbeddingClient"]
