from collections.abc import Callable
import pytest


@pytest.fixture
def no_op_func() -> Callable[[], str]:
    def _no_op_inner() -> str:
        return "mock llm response"
    return _no_op_inner


@pytest.fixture
def raises_func() -> Callable[[], str]:
    def _raises_inner() -> str:
        raise ValueError("mock exception")
    return _raises_inner
