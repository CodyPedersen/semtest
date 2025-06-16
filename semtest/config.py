"""Core configuration ingestion"""
import logging
import sys
from termcolor import colored
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Core required attributes. Values overridden by project .env file"""

    OPENAI_API_KEY: str
    BASE_URL: str = "https://api.openai.com/v1"
    DEFAULT_EMBEDDING_MODEL: str = "text-embedding-3-large"

    class Config:
        """Ingestion configurations"""
        env_file = '.env'
        env_file_encoding = 'utf-8'


class TermcolorFormatter(logging.Formatter):
    """Custom formatter for logging"""
    COLORS = {
        logging.DEBUG: 'white',
        logging.INFO: 'white',
        logging.WARNING: 'yellow',
        logging.ERROR: 'red',
        logging.CRITICAL: 'red',
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format CLI logging colors"""

        color = self.COLORS.get(record.levelno, 'white')
        record.msg = colored(record.msg, color)  # type: ignore[arg-type]

        # Color the exception traceback if present
        if record.exc_info:
            exc_text = self.formatException(record.exc_info)
            record.exc_text = colored(exc_text, 'red')
        else:
            record.exc_text = ""

        return super().format(record)

def configure_cli_logging() -> None:
    """Configure CLI logging"""
    logger = logging.getLogger("semtest")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(TermcolorFormatter("%(message)s"))

    logger.addHandler(console_handler)

settings = Settings()
