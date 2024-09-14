"""Definitions of types/validations and input conversion"""
import argparse
import os
from enum import Enum
from pathlib import Path


class Verbosity(str, Enum):
    """Valid verbosity settings"""
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    EXCEPTION = "exception"


class InputType:
    """Bucket for input validation/conversion"""

    @staticmethod
    def directory(value: str) -> Path:
        """Validate input directory"""
        if not os.path.isdir(value):
            exc = f"{value} is not a valid directory"
            raise argparse.ArgumentTypeError(exc)

        return Path(value)

    @staticmethod
    def verbosity(value: str) -> Verbosity:
        """Verbosity validaiton"""
        verbosity_options = Verbosity.__members__.values()
        if value.lower() not in verbosity_options:
            exc = f"{value} not a valid verbosity level. Valid values: {verbosity_options}"
            raise argparse.ArgumentTypeError(exc)

        return Verbosity(value)
