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
    comparator=cosine_similarity,
    iterations=2
)
def mock_prompt_2() -> str | None:
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
                    "Below I'm supplying a list of privileges in json "
                    "format, from this which are the most likely "
                    f"administrators\n```json\n{json.dumps(TEST_DATASET)}\n```"
                )
            }
        ]
    )

    response_text = llm_response.choices[0].message.content
    # additional post-processing

    return response_text
