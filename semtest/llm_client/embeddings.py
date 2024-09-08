"""Core OpenAI client for LLM interactions"""
import openai

from typing import Optional

from semtest.config import settings


class EmbeddingClient():
    """OpenAI embedded model client"""

    def __init__(
        self,
        model: str = settings.DEFAULT_EMBEDDING_MODEL,
        api_key: str = settings.OPENAI_API_KEY,
        base_url: str = settings.BASE_URL
    ):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def generate_embedding_vector(
        self, input_text: str, model: Optional[str] = None
    ) -> list[float]:
        """Generate embedding vector for a text chunk"""

        if not model:
            model = self.model

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
