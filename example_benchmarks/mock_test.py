"""Mock tests for framework mode to pick up."""
import json
from openai import OpenAI
import semtest


EXPECTATION = "Harold and Antonio are the likey administrators as they both have 'rwx' privileges"

TEST_DATASET = {
    "Harold": "rwx",
    "Antonio": "rwx",
    "John": "rw",
    "Liefeng": "r",
    "Lida": "r"
}

# First test picked up and executed by framework mode
@semtest.benchmark(
    semantic_expectation=EXPECTATION,
    iterations=2
)
def mock_prompt_1() -> str:
    """A better prompt/temperature/config"""

    client = OpenAI()
    llm_response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert at examining IT controls and answer questions in a succinct "
                    "fashion while answering with all required details"
                )
            },
            {
                "role": "user",
                "content": (
                    "Based on the following dataset of folder privileges, who are the most "
                    f"likely administrators\n```json\n{json.dumps(TEST_DATASET)}\n```"
                )
            }
        ]
    )

    response_text = llm_response.choices[0].message.content
    # additional post-processing

    return response_text


@semtest.benchmark(
    semantic_expectation=EXPECTATION,
    iterations=2
)
def mock_prompt_2() -> str:
    """A slightly worse prompt/temperature/config"""

    client = OpenAI()
    llm_response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert at examining IT controls and answer questions in a succinct "
                    "fashion while answering with all required details"
                )
            },
            {
                "role": "user",
                "content": (
                    "Below I'm supplying a list of privileges in json format, from this which are the "
                    f"most likely administrators\n```json\n{json.dumps(TEST_DATASET)}\n```"
                )
            }
        ]
    )

    response_text = llm_response.choices[0].message.content
    # additional post-processing

    return response_text
