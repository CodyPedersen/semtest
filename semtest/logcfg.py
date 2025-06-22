"""Logging configuration"""
import logging
import sys
from termcolor import colored

COLOR_CONFIG = {
        logging.DEBUG: 'white',
        logging.INFO: 'white',
        logging.WARNING: 'yellow',
        logging.ERROR: 'red',
        logging.CRITICAL: 'red',
    }


class TermcolorFormatter(logging.Formatter):
    """Custom formatter for logging"""

    def format(self, record: logging.LogRecord) -> str:
        """Format CLI logging colors"""

        color = COLOR_CONFIG.get(record.levelno, 'white')
        record.msg = colored(record.msg, color)  # type: ignore[arg-type]

        record.exc_text = (
            colored(self.formatException(record.exc_info), 'red')
            if record.exc_info
            else ""
        )
        return super().format(record)


def configure_cli_logging() -> None:
    """Configure CLI logging"""
    logger = logging.getLogger("semtest")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(TermcolorFormatter("%(message)s"))

    logger.addHandler(console_handler)
