"""Mock tests for framework mode to pick up."""
import semtest

from example_benchmarks.mock_helpers import mock_llm_response_prompt1, mock_llm_response_prompt2


mock_llm_response_generator_prompt_1 = mock_llm_response_prompt1()
mock_llm_response_generator_prompt_2 = mock_llm_response_prompt2()

EXPECTATION = "A dog is in the background of the photograph"

# First test picked up and executed by framework mode
@semtest.benchmark(
    semantic_expectation=EXPECTATION,
    iterations=3
)
def mock_prompt_1() -> str:
    """A better prompt/temperature/config"""

    mocked_llm_response = next(mock_llm_response_generator_prompt_1)

    return mocked_llm_response


# Second test picked up and executed by framework mode
@semtest.benchmark(
    semantic_expectation=EXPECTATION,
    iterations=3
)
def mock_prompt_2() -> str:
    """A slightly worse prompt/temperature/config"""

    mocked_llm_response = next(mock_llm_response_generator_prompt_2)  # mock llm response

    return mocked_llm_response
