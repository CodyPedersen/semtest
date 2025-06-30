"""Mock tests for framework mode to pick up."""
import json
from openai import OpenAI

import semtest

from example_benchmarks.external_prompt import (
    TEST_SYSTEM_PROMPT,
    TEST_USER_PROMPT,
)


EXPECTATION = "Harold and Antonio are the likey administrators as they both have 'rwx' privileges"

TEST_DATASET = {
    "Harold": "rwx",
    "Antonio": "rwx",
    "John": "rw",
    "Liefeng": "r",
    "Lida": "r"
}


cosine_similarity = semtest.CosineSimilarity(
    semantic_expectation=EXPECTATION
)

# First test picked up and executed by framework mode
@semtest.benchmark(
    comparator=cosine_similarity,
    iterations=2
)
def mock_prompt_1() -> str | None:
    """A better prompt/temperature/config"""

    client = OpenAI()
    llm_response = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": TEST_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": TEST_USER_PROMPT.format(sample_data=json.dumps(TEST_DATASET))
            }
        ]
    )

    response_text = llm_response.choices[0].message.content
    # additional post-processing

    return response_text


@semtest.benchmark(
    comparator=cosine_similarity,
    iterations=2
)
def mock_prompt_2() -> str | None:
    """A slightly worse prompt/temperature/config"""

    client = OpenAI()
    llm_response = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0.99,
        messages=[
            {
                "role": "system",
                "content": TEST_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": TEST_USER_PROMPT.format(sample_data=json.dumps(TEST_DATASET))
            }
        ]
    )

    response_text = llm_response.choices[0].message.content
    # additional post-processing

    return response_text


@semtest.benchmark(
    comparator=cosine_similarity,
    iterations=2
)
def raises_() -> str:
    """Intentionally raises"""

    raise ValueError("Example ValueError thrown")
