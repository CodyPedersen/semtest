"""Benchmarks part 2 (mock temp change)"""
from typing import Generator
import semtest


def mock_llm_response_prompt_nested() -> Generator[str, None, None]:
    """Mocks a quality llm response"""
    yield from [
        "Buenas dias",
        "How are you?",
        "Welcome to Florida"
    ]


mock_llm_response_generator_prompt_nested = mock_llm_response_prompt_nested()

@semtest.benchmark(
    semantic_expectation="hello friend",
    iterations=3
)
def mock_temp_1() -> str:
    """A better prompt/temperature/config"""

    mocked_llm_response = next(mock_llm_response_generator_prompt_nested)

    # Forced error for 1/3 prompts
    assert mocked_llm_response != "How are you?", "testing exception function"

    return mocked_llm_response
