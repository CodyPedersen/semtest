# semtest
Enables semantic testing of LLM responses and benchmarking against result expectations.


## Current functionality
semtest supports the semantic benchmarking process through the following:

1. Embedding vector generation against expected result set for a given input -> output expectation
2. Execution of inputs against a given model
3. Collection of llm responses for the given input
4. Analysis of embedding vector difference of the LLM response and the expectation


## Benchmarking in direct (non-framework) mode

Full example of this can be found in `examples/benchmarking_example.ipynb`.

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

## Benchmarking in framework mode
Framework mode allows you to execute a series of prepared tests from a directory, similar to other testing frameworks (pyest, etc). Framework mode follows the same rules as direct execution mode as above, but with a few modifications, as the engine executes your tests (you do not call the benchmarks directly)

Running in framework mode is done with the following command: `semtest <your_directory>`

Due to it's automated nature, outputs are currently standardize to CLI where a dataframe is generated and output to the CLI. Additional options for data retrieval will be added later.

Framework mode requires:
- A test directory with .py files containing your semtest.benchmark definitions
- Each benchmark should return the llm response string you want to gauge (or a modified version of it)

See `example_benchmarks` directory for an example on structuring your semantic benchmarks. Runnable with `semtest example_benchmarks`

Caveats: 
- Framework mode does not currenty support fixtures
- No relative imports within test directories due to treating every file as a top-level module

## Ongoing features
- Allow for parameterization of benchmarks with multiple I/O expectations
- Schema 
- Enable graceful test-case failures
- Implement LLM response schema validation via Pydantic (if applicable)
