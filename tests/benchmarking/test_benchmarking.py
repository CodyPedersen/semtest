from collections.abc import Callable

import numpy as np
import pytest

from semtest.benchmarking import benchmark
from semtest.comparator import ComparatorBase

# TODO: Pytests which validate numeric functionality


def test_benchmark_shape_without_exceptions(
    no_op_func: Callable[[], str],
    no_op_comparator: ComparatorBase,
) -> None:
    benchmark_fn = benchmark(
        comparator=no_op_comparator,
    )(no_op_func)

    benchmark_res = benchmark_fn()

    assert benchmark_res.func == no_op_func.__name__
    assert benchmark_res.comparator == "no_op_semantic_comparator"
    assert benchmark_res.benchmarks.mean_semantic_distance == 69.33
    assert benchmark_res.benchmarks.median_semantic_distance == 69.33
    assert not benchmark_res.benchmarks.exceptions


@pytest.mark.parametrize(
    "iterations", (1, 3, 5, 7, 9, 11, 13)
)
def test_multiple_iterations(
    no_op_func: Callable[[], str],
    no_op_comparator: ComparatorBase,
    iterations: int
) -> None:
    benchmark_fn = benchmark(
        comparator=no_op_comparator,
        iterations=iterations,
    )(no_op_func)

    benchmark_res = benchmark_fn()

    assert benchmark_res.iterations == iterations
    assert benchmark_res.benchmarks.responses == ["mock llm response"] * iterations
    assert np.isclose(benchmark_res.benchmarks.mean_semantic_distance, 69.33)
    assert np.isclose(benchmark_res.benchmarks.median_semantic_distance, 69.33)
    assert not benchmark_res.benchmarks.exceptions


def test_benchmark_with_exceptions(
    raises_func: Callable[[], str],
    no_op_comparator: ComparatorBase,
) -> None:
    benchmark_fn = benchmark(
        comparator=no_op_comparator,
    )(raises_func)

    benchmark_res = benchmark_fn()

    exception_ = benchmark_res.benchmarks.exceptions[0]

    assert benchmark_res.func == raises_func.__name__
    assert benchmark_res.comparator == "no_op_semantic_comparator"
    assert "mock exception" in str(exception_)
    assert isinstance(exception_, ValueError)
