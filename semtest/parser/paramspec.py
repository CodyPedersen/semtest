"""Core arguments for semtest"""
from typing import Any, Callable
from pydantic import BaseModel

from .input_type import Verbosity, directory, verbosity


class SemtestParamSpec(BaseModel):
    """Core defined argument options"""
    flag: str
    type: type | Callable[..., Any]
    help: str
    default: str | None = None
    required: bool | None = None


semtest_params = [
    SemtestParamSpec(
        flag="directory",
        type=directory,
        default=".",
        help="Input directory of semtests to execute against."
    ),
    SemtestParamSpec(
        flag="--verbosity",
        type=verbosity,
        default="warn",
        help=f"Verbosity level: {Verbosity.__members__.values()}"
    )
]
