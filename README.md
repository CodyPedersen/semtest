# semtest
Enables semantic testing of LLM responses and benchmarking against result expectations.


## Future functionality
SemTest at maturity will contain a few necessary stages:

1. Embedding vector generation against expected result set for a given input -> output expectation
2. Execution of inputs against a given model
3. Collection of llm responses for the given input
4. Analysis of embedding vector difference of the LLM response and the expectation
5. [Optional] schema validation of response via Pydantic
6. [Optional] exact match response verification


## Proposed Test Case Schema
@semtest.benchmark
    - expected inputs/outputs
    - iterations
    - validation_types [semantic distance, exact, schema]
    - schema validation [optional]
