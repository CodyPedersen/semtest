"""Definitions of types/validations and input conversion"""
import argparse
import os
from pathlib import Path


class InputType:
    """Bucket for input validation/conversion"""

    @staticmethod
    def directory(value: str) -> Path:
        """Validate input directory"""

        if not os.path.isdir(value):
            raise argparse.ArgumentTypeError(f"{value} is not a valid directory")

        return Path(value)
