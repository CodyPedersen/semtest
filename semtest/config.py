"""Core runtime settings """
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Core required attributes. Values overridden by project .env file"""

    OPENAI_API_KEY: str
    BASE_URL: str = "https://api.openai.com/v1"
    DEFAULT_EMBEDDING_MODEL: str = "text-embedding-3-large"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        secrets_dir="secrets"
    )


settings = Settings()
