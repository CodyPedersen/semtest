"""Functionality to parse CLI arguments"""

import argparse
from pathlib import Path
from pydantic import BaseModel

from .paramspec import semtest_params


class SemtestContext(BaseModel):
    """Listing of all permissible arguments"""
    directory: Path


class Parser:
    """Base CLI parsing class"""

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="semtest: the semantic llm testbench"
        )

    def parse_arguments(self) -> SemtestContext:
        """Parse CLI arguments and return the resulting object"""

        for param in semtest_params:
            self.parser.add_argument(
                param.flag,
                **param.model_dump(exclude_none=True, exclude=["flag"])  # type: ignore[arg-type]
            )

        args = self.parser.parse_args()
        arg_dict = vars(args)

        return SemtestContext(**arg_dict)
