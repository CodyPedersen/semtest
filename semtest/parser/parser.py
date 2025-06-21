"""Functionality to parse CLI arguments"""

import argparse
from pathlib import Path
from dataclasses import dataclass

from pydantic import BaseModel

from .paramspec import semtest_params
from .input_type import Verbosity


# TODO: Move to custom
class SemtestContext(BaseModel):
    """Listing of all permissible arguments"""
    directory: Path
    verbosity: Verbosity


@dataclass
class Parser:
    """Base CLI parsing class"""

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
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
