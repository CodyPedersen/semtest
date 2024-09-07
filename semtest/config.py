from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Core required attributes"""

    OPENAI_API_KEY: str = ""

    class Config:
        """Ingestion configurations"""
        env_file = '.env'
        env_file_encoding = 'utf-8'