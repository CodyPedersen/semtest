"""Benchmarks part 2 (mock temp change)"""
import json
from openai import OpenAI
import semtest

EXPECTATION = json.dumps({
    "Liefeng": 5,
    "Bob": 5,
    "John": 2,
    "Frank": 3,
    "Jeff": 5
})

TEST_DATASET = """
Round 1
    Bob,1
    Liefeng, 2
    John,2,
    Liefeng,3
Round 2
    Frank,3
    Bob, 4
    Jeff, 5
"""


def chat_completion_variable_temp(temp: float, test_dataset: str) -> str:
    """Generate a chat completion"""
    client = OpenAI()
    llm_response = client.chat.completions.create(
        model="gpt-4o",
        temperature=temp,
        messages=[
            {
                "role": "system",
                "content": "You are an expert at summarizing data"
            },
            {
                "role": "user",
                "content": f'''
                    Please convert the following set of scores per round into json
                    format summing up all scores per round in the following format

                    ```json
                    {{
                        "user_one": 5,
                        "user_two": 8,
                        "user_three": 9,
                        ...
                    }}
                    ```

                    Dataset:
                    ```
                    {test_dataset}
                    ```
                '''
            }
        ]
    )

    response_text = llm_response.choices[0].message.content

    start = "```json"
    li = str.find(response_text, start) + len(start)
    ri = str.rfind(response_text, "```")

    return response_text[li:ri].strip()


@semtest.benchmark(
    semantic_expectation=EXPECTATION,
    iterations=2
)
def mock_test_json_temp_1() -> str:
    """A better prompt/temperature/config"""
    return chat_completion_variable_temp(temp=.7, test_dataset=TEST_DATASET)


@semtest.benchmark(
    semantic_expectation=EXPECTATION,
    iterations=2
)
def mock_test_json_temp_2() -> str:
    """A better prompt/temperature/config"""
    return chat_completion_variable_temp(temp=0.0, test_dataset=TEST_DATASET)
