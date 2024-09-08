# semtest
Enables semantic testing of LLM responses and benchmarking against result expectations.


## Current functionality
SemTest at maturity will contain a few necessary stages:

1. Embedding vector generation against expected result set for a given input -> output expectation
2. Execution of inputs against a given model
3. Collection of llm responses for the given input
4. Analysis of embedding vector difference of the LLM response and the expectation


## How to

semtest current supports benchmarking in non-framework mode. An example of this can be found in `examples/benchmarking_example.ipynb`.

To utilize this benchmarking, the `@semtest.benchmark` decorator can be used manually to execute a given function and obtain a series of results and distances from expected semantics.

Example
```python
import semtest

expected_semantics = "A dog is in the background of the photograph"

@semtest.benchmark(
    semantic_expectation=expected_semantics,
    iterations=3
)
def mock_prompt_benchmark():
    """Mock example of benchmarking functionality."""

    # intermediary logic ...

    mocked_llm_response = query_llm(...)  # example llm autocomplete response

    return mocked_llm_response  # return LLM string response for benchmarking

res: semtest.Benchmark = mock_prompt_benchmark()  # manually executed benchmark (non-framework mode)

print(res.benchmarks())
```

Output
```json
{
  "func": "mock_prompt_benchmark",
  "iterations": 3,
  "comparator": "cosine_similarity",
  "expectation_str": "A dog is in the background of the photograph",
  "benchmarks": {
    "responses": [
      "There's a dog in the background of the photo",
      "In the background of the photo is a dog",
      "There's an animal in the background of the photo and it's a dog."
    ],
    "semantic_distances": [
      0.8689512451809671,
      0.8314281742105534,
      0.7698003396849378
    ],
    "mean_semantic_distance": 0.8233932530254862,
    "median_semantic_distance": 0.8314281742105534
  }
}

```

## Ongoing features
- Implement framework mode (automatically execute all defined semtest.benchmark definitions and display results)
    - `semtest {directory}`
- Allow for parameterization of benchmarks with multiple I/O expectations
- Enable graceful test-case failures
- Implement LLM response schema validation via Pydantic (if applicable)
