"""Core arguments for semtest"""
from typing import Any, Optional, Callable
from pydantic import BaseModel

from .input_type import InputType, Verbosity


class SemtestParamSpec(BaseModel):
    """Core defined argument options"""
    flag: str
    type: type | Callable[..., Any]
    help: str
    default: Optional[str] = None
    required: Optional[bool] = None


semtest_params = [
    SemtestParamSpec(
        flag="directory",
        type=InputType.directory,
        default=".",
        help="Input directory of semtests to execute against."
    ),
    SemtestParamSpec(
        flag="--verbosity",
        type=InputType.verbosity,
        default="warn",
        help=f"Verbosity level: {Verbosity.__members__.values()}"
    )
]
