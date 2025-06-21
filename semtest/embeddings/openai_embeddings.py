"""Core OpenAI client for LLM interactions"""
from dataclasses import dataclass
from functools import cached_property

import openai

from semtest.config import settings


@dataclass
class OpenAIEmbeddingClient:
    """OpenAI embedded model client"""

    model: str = settings.DEFAULT_EMBEDDING_MODEL
    api_key: str = settings.OPENAI_API_KEY
    base_url: str = settings.BASE_URL

    @cached_property
    def client(self) -> openai.OpenAI:
        """Inner embedding client"""
        return openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def generate_embedding_vector(
        self, input_text: str, model: str | None = None
    ) -> list[float]:
        """Generate embedding vector for a text chunk"""
        model = model or self.model

        response = self.client.embeddings.create(
            input=input_text,
            model=model
        )

        if not response:
            exc = (
                f"Failed to generate embeddings vector. input: {input_text} "
                f"metadata: (model={model}, base_url={self.base_url}, )"
            )
            raise ValueError(exc)

        try:
            embedding = response.data[0].embedding
        except KeyError as e:
            exc = f"Failed to parse embedding response: {response}"
            raise ValueError(exc) from e

        return embedding
